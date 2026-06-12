import base64
import os

from openai import OpenAI


def encode_audio(audio_path):
    with open(audio_path, "rb") as audio_file:
        return base64.b64encode(audio_file.read()).decode("utf-8")

def call_audio_api(audio_path,model_name,thinking=False):
    if not audio_path:
        return None,0
    client = OpenAI(
        api_key=os.environ["LLM_API_KEY"],
        base_url=os.environ["LLM_BASE_URL"],
    )
    base64_audio = encode_audio(audio_path)
    completion = client.chat.completions.create(
        # model="qwen-omni-turbo",
        # model="Qwen3-Omni-Flash",
        # model="qwen3-omni-flash",
        model=model_name,
        
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_audio",
                        "input_audio": {
                            "data": f"data:;base64,{base64_audio}",
                            "format": "wav",
                        },
                    },
                    {"type": "text", "text": "请回答音频中的问题。"},
                ],
            },
        ],
        # 设置输出数据的模态，当前支持两种：["text","audio"]、["text"]
        # modalities=["text", "audio"],
        modalities=["text"],
        audio={"voice": "Cherry", "format": "wav"},
        # stream 必须设置为 True，否则会报错
        stream=True,
        stream_options={"include_usage": True},
        extra_body={'enable_thinking': thinking},
    )

    text_output = ""
    reasoning_output = ""
    token_cnt=0
    for chunk in completion:
        if chunk.choices:
            delta = chunk.choices[0].delta
            # print(delta)
            if hasattr(delta, "content") and delta.content:  # normal text field
                text_output += delta.content
            elif hasattr(delta, "reasoning_content") and delta.reasoning_content:
                reasoning_output +=  delta.reasoning_content
            # print(f"<think>{delta}</think>")
        else:
            # you can inspect usage if you like
            token_cnt=chunk.usage.completion_tokens
    if reasoning_output:
        text_output = "<think>" + reasoning_output + "</think>" + text_output
    print(text_output,token_cnt)
    return text_output,token_cnt
    # wav_bytes = base64.b64decode(audio_string)
    # audio_np = np.frombuffer(wav_bytes, dtype=np.int16)
    # sf.write(f"tts/out_{actual_filename}", audio_np, samplerate=24000)
