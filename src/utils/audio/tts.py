import hashlib
import os
import requests
import time
import dashscope

def get_audio(text,task_name,save_dir="../cache/tts"):
    key = f"{text}:{task_name}"
    hash=hashlib.md5(key.encode('utf-8')).hexdigest()
    filepath=save_dir + "/" + hash + ".wav"
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir, exist_ok=True)
    if os.path.isfile(filepath):
        print(f"音频文件已存在：{filepath}")
        return filepath
    else:
        print(f"音频文件不存在，生成新文件：{filepath}")
        hash=hashlib.md5(key.encode('utf-8')).hexdigest()
        tts_call(text,hash,save_dir=save_dir)
        if os.path.isfile(filepath):
            return filepath
        else:
            print(f"音频文件生成失败：{filepath}")
            return None

def tts_call(text,hash,save_dir):
    response = dashscope.audio.qwen_tts.SpeechSynthesizer.call(
        model=os.getenv("TTS_MODEL_NAME", "qwen-tts"),
        api_key=os.environ["TTS_API_KEY"],
        text=text,
        voice=os.getenv("TTS_VOICE", "Cherry"),
    )
    print(response)
    try:
        audio_url = response.output.audio["url"]
        save_path = f"{save_dir}/{hash}.wav"
        response = requests.get(audio_url)
        response.raise_for_status()  # 检查请求是否成功
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"音频文件已保存至：{save_path}")
    except Exception as e:
        raise
        print(f"下载失败：{str(e)}. {text}")
