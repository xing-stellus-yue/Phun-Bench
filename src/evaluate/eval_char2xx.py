import re
import json
# import numpy as np
from collections import Counter
import os
import time
from collections import defaultdict


def get_py_tone(data):
    matches = re.findall(r'\{\s*"answer"\s*:\s*".*?"\s*\}', data, re.DOTALL)
    match = matches[-1] if matches else None
    if match:
        json_str = match
        try:
            result = json.loads(json_str)
        except json.JSONDecodeError:
            print(f"Error decoding JSON: {data}")
            return None
        answer = result["answer"].strip()
    else:
        return None
    return answer

def get_py_tone3(data):
    matches = re.findall(r'\{\s*"base"\s*:\s*".*?"\s*,\s*"tone"\s*:\s*\d\s*\}', data, re.DOTALL)
    match = matches[-1] if matches else None
    if match:
        json_str = match
        try:
            result = json.loads(json_str)
        except json.JSONDecodeError:
            print(f"Error decoding JSON: {data}")
            return None
        base = result["base"].strip()
        tone = str(result["tone"])
    else:
        return None
    return base+tone

def eval_char2py(test_dict, task_name, output_dir,model_name):
    total_num = len(test_dict)
    true_num = 0
    error_num = 0
    for k, v in test_dict.items():
        pred = get_py_tone(v['result'])
        v['pred'] = pred
        if pred is None:
            error_num += 1
            v['score'] = 0
        else:
            if v['ans1'] == pred:
                v['score'] = 1
                true_num += 1
            else:
                v['score'] = 0

    em = f"{true_num / total_num:.4f}"
    er = f"{error_num / total_num:.4f}"
    t = time.localtime()
    model_name=model_name.replace("/", "-")
    output_json_name = f'{task_name}_{model_name}.{t.tm_mon:02}.{t.tm_mday:02},{t.tm_hour:02}:{t.tm_min:02}.json'
    log_name = f'{task_name}_{model_name}.{t.tm_mon:02}.{t.tm_mday:02},{t.tm_hour:02}:{t.tm_min:02}.log'
    with open(os.path.join(output_dir, output_json_name), 'w', encoding='utf-8') as json_file:
        json.dump(test_dict, json_file, indent=4, ensure_ascii=False)
    with open(os.path.join(output_dir, log_name), 'a', encoding='utf-8') as log_file:
        content = f"em: {em}, error_rate: {er}, total_num: {total_num}\n"
        log_file.write(content)

def eval_char2bp(test_dict, task_name, output_dir,model_name):
    total_num = len(test_dict)
    true_num = 0
    b_true_num = 0
    error_num = 0
    for k, v in test_dict.items():
        pred = get_py_tone3(v['result'])
        v['pred'] = pred
        if pred is None:
            error_num += 1
            v['score'] = 0
        else:
            if v['ans2'] == pred:
                v['score'] = 1
                true_num += 1
                b_true_num += 1
            elif v['ans1'][:-1] == pred[:-1]:
                v['score'] = 0.5
                b_true_num += 1
            else:
                v['score'] = 0

    em = f"{true_num / total_num:.4f}"
    sm = f"{b_true_num / total_num:.4f}"
    er = f"{error_num / total_num:.4f}"
    t = time.localtime()
    model_name=model_name.replace("/", "-")
    output_json_name = f'{task_name}_{model_name}.{t.tm_mon:02}.{t.tm_mday:02},{t.tm_hour:02}:{t.tm_min:02}.json'
    log_name = f'{task_name}_{model_name}.{t.tm_mon:02}.{t.tm_mday:02},{t.tm_hour:02}:{t.tm_min:02}.log'
    with open(os.path.join(output_dir, output_json_name), 'w', encoding='utf-8') as json_file:
        json.dump(test_dict, json_file, indent=4, ensure_ascii=False)
    with open(os.path.join(output_dir, log_name), 'a', encoding='utf-8') as log_file:
        content = f"em: {em}, sm: {sm} error_rate: {er}, total_num: {total_num}\n"
        log_file.write(content)
    
if __name__ == "__main__":
    pass