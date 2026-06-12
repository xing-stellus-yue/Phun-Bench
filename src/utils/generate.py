from collections import defaultdict
import asyncio
from asyncio import Semaphore
import os
import time
import traceback

from openai import AsyncOpenAI, RateLimitError

from configs import _optional_bool, get_semaphore_num, get_parameter
from utils.llm_cache_sqlite import get_cache_key, load_cache_entry, save_cache_entry

CNT = defaultdict(int)

async def get_qwen_stream_output(stream):   
    output=""
    is_thinking=False
    thinking_tag="<think>"
    thinking_tag_end="</think>"
    async for chunk in stream:
        delta=chunk.choices[0].delta
        # print(chunk)
        # print(delta)
        if hasattr(delta, "reasoning_content") and delta.reasoning_content is not None:
            if not is_thinking:
                is_thinking=True
                output+=thinking_tag
                # print(thinking_tag, end="\n",flush=True)
            # print(delta.reasoning_content, end="")
            output+=delta.reasoning_content
        elif hasattr(delta, "content") and delta.content is not None:
            if is_thinking:
                is_thinking=False
                output+=thinking_tag_end
                # print("\n"+thinking_tag_end, end="\n\n")
            # print(delta.content, end="",flush=True)
            output+=delta.content
        else:
            continue
    return output

async def asynchat(user_prompt, sys_prompt, client, model_name, semaphore, task_name, max_retries=10, timeout=3600):
    global CNT
    enable_thinking = _optional_bool("LLM_ENABLE_THINKING") or False
    log_name = model_name if not enable_thinking else f"{model_name}_think"
    
    cache_key = get_cache_key(log_name, task_name, user_prompt)
    cached = await load_cache_entry(cache_key)
    if cached:
        # Return cached result
        CNT[task_name] += 1
        print(
            f"Cache hit CNT={CNT[task_name]} for {model_name} {task_name}, key={cache_key}")
        return cached
    else:
        # print(f"Cache miss CNT={CNT[task_name]} for {model_name} {task_name}, key={cache_key}")
        pass

    params = get_parameter(log_name)
        
    if "audio" in task_name:
        from utils.audio.end2end_api import call_audio_api
        from utils.audio.tts import get_audio

        audio_path=get_audio(user_prompt,task_name,save_dir="audio/cache")
        result = call_audio_api(
            audio_path,
            model_name,
            params.get("enable_thinking") or False,
        )
        # print(result,token_cnt)
        print(f"Saved cache CNT={CNT[task_name]} for {model_name} {task_name}, key={cache_key}")
        await save_cache_entry(cache_key, result)
        return result
    else:
        retry_delay = 1  # start with 1 second
        for attempt in range(max_retries):
            # print(CNT,cache_key, user_prompt, attempt, retry_delay)
            async with semaphore:
                try:
                    # print(f"try: {cache_key}")
                    # print(user_prompt)
                    stream = params.get("stream", False)
                    create_args = {
                        "model": model_name,
                        "messages": [
                            {"role": "system", "content": sys_prompt},
                            {"role": "user", "content": user_prompt}
                        ],
                        "timeout": timeout,
                        "stream": stream
                    }

                    # 添加可选参数（仅在params中存在对应key时）
                    if params.get("temperature") is not None:
                        create_args["temperature"] = params["temperature"]
                        
                    if params.get("top_p") is not None:
                        create_args["top_p"] = params["top_p"]
                    if params.get("max_tokens") is not None:
                        create_args["max_tokens"] = params["max_tokens"]
                    

                    # 构建extra_body，只包含存在的参数
                    extra_body = {}
                    if params.get("top_k") is not None:
                        extra_body["top_k"] = params["top_k"]
                    extra_body["chat_template_kwargs"] = {"enable_thinking":params.get("enable_thinking", False)}
                    extra_body["thinking"]= "enabled" if params["enable_thinking"] else "disabled"
                    if params.get("repetition_penalty") is not None:
                        extra_body["repetition_penalty"] = params[
                            "repetition_penalty"
                        ]

                    # 如果extra_body不为空，则添加到参数中
                    if extra_body:
                        create_args["extra_body"] = extra_body
                        
                    chat_completion = await client.chat.completions.create(**create_args)
                    CNT[task_name] += 1
                    t = time.localtime()

                    print(
                        f"Task {task_name} request {CNT[task_name]} dispatched by {model_name} time: {t.tm_mon:02}.{t.tm_mday:02},{t.tm_hour:02}:{t.tm_min:02}")
                    if stream:
                        content = await get_qwen_stream_output(chat_completion)  # Add await
                    else:
                        content = chat_completion.choices[0].message.content
                        if hasattr(chat_completion.choices[0].message, 'reasoning_content') and chat_completion.choices[0].message.reasoning_content:
                            content = "<think>" + chat_completion.choices[0].message.reasoning_content + "</think>"+content

                    result = (
                        content,
                        chat_completion.usage.completion_tokens if not stream else 0,
                    )
                    print(
                        f"Saved cache CNT={CNT[task_name]} for {model_name} {task_name}, key={cache_key}")
                    await save_cache_entry(cache_key, result)
                    return result

                except asyncio.TimeoutError:
                    print(
                        f"Timeout occurred. Retrying in {retry_delay}s (attempt {attempt+1}/{max_retries})...")
                    await asyncio.sleep(retry_delay)
                    retry_delay = min(60, 2*retry_delay)  # exponential backoff

                except RateLimitError as e:
                    if attempt < max_retries - 1:
                        print(
                            f"Rate limit hit. Retrying in {retry_delay}s (attempt {attempt+1}/{max_retries})...")
                        await asyncio.sleep(retry_delay)
                        retry_delay = min(60, 2*retry_delay)  # exponential backoff
                    else:
                        print("Max retries reached. Giving up.")
                        raise

                except Exception as e:
                    print(f"Unexpected error: {e}")
                    print(traceback.format_exc())
                    return (str(e), 0)


async def batch_generation(test_dict, *, sys_prompt, base_url, api_key, model_name, task_name):
    semaphore_num = get_semaphore_num(model_name)
    semaphore = Semaphore(semaphore_num)
    async with AsyncOpenAI(api_key=api_key, base_url=base_url) as client:
        tasks = []
        for _, v in test_dict.items():
            tasks.append(asynchat(v["user_prompt"],
                         sys_prompt, client, model_name, semaphore, task_name))
        return await asyncio.gather(*tasks)
