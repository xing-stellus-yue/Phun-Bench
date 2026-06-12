import re
import json
# import numpy as np
from collections import Counter
import os
import time
from collections import defaultdict


def check_answer(text):
    temp = re.sub(r'[\\\"\'“”。]', '', text)
    if len(temp) == 4:
        return temp
    elif len(temp.split(" ")) == 4:
        return "py"
    else:
        return None

def check_match(matches):
    match = matches[-1] if matches else None
    if match:
        status = check_answer(match)
        if status and status != "py":
            return status
        if status == "py":
            match = matches[-2] if len(matches) > 1 else None
            if match:
                status = check_answer(match)
                if status and status != "py":
                    return status
    return None
    
def get_pred_json_audio(data):
    matches = re.findall(r'\{\s*".*?"\s*:\s*".*?"\s*\}', data, re.DOTALL)
    match = matches[-1] if matches else None
    if match:
        json_str = match
        try:
            result = json.loads(json_str)
        except json.JSONDecodeError:
            print(f"Error decoding JSON: {data}")
            return None
        answer = result.get("answer", result.get(
            "Answer", result.get("答案", result.get("成语", None))))
        if answer is None:
            values = list(result.values())
            for i in values:
                if len(i) == 4:
                    answer = i
                    break
        return answer
    else:
        status = check_answer(data)
        if status:
            return status

        temp = data.split('\n')[-1].replace('。', '')
        status = check_answer(temp)
        if status and status != "py":
            return status

        temp = data.split('：')[-1].replace('。', '')
        status = check_answer(temp)
        if status and status != "py":
            return status

        matches = re.findall(r'“.*?”', data, re.DOTALL)
        status=check_match(matches)
        if status:
            return status

        matches = re.findall(r'".*?"', data, re.DOTALL)
        status=check_match(matches)
        if status:
            return status
        
        matches = re.findall(r"'.*?'", data, re.DOTALL)
        status=check_match(matches)
        if status:
            return status
        return None


def get_pred_json(data):
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


def eval_py2xx(test_dict, task_name, output_dir, model_name):
    total_num = 0

    true_num = 0
    error_num = 0
    # ok_dict={}
    for k, v in test_dict.items():
        if not v.get('result'):
            continue
        else:
            total_num += 1
        if "audio" in task_name:
            pred = get_pred_json_audio(v['result'])
        else:
            pred = get_pred_json(v['result'])
        v['pred'] = pred
        if pred is None:
            error_num += 1
        if v.get('answer') == pred:
            v['score'] = 1
            true_num += 1
            # ok_dict[k] = v
        else:
            v['score'] = 0
    em = f"{true_num / total_num:.4f}"
    er = f"{error_num / total_num:.4f}"
    t = time.localtime()
    model_name = model_name.replace("/", "_")
    output_json_name = f'{task_name}_{model_name}.{t.tm_mon:02}.{t.tm_mday:02},{t.tm_hour:02}:{t.tm_min:02}.json'
    log_name = f'{task_name}_{model_name}.{t.tm_mon:02}.{t.tm_mday:02},{t.tm_hour:02}:{t.tm_min:02}.log'
    with open(os.path.join(output_dir, output_json_name), 'w', encoding='utf-8') as json_file:
        json.dump(test_dict, json_file, indent=4, ensure_ascii=False)
    with open(os.path.join(output_dir, log_name), 'a', encoding='utf-8') as log_file:
        content = f"em: {em}, error_rate: {er}, total_num: {total_num}\n"
        log_file.write(content)
    # ok_json_name = f'{task_name}_ok_{model_name}.{t.tm_mon:02}.{t.tm_mday:02},{t.tm_hour:02}:{t.tm_min:02}.json'
    # with open(os.path.join(output_dir, ok_json_name), 'w', encoding='utf-8') as json_file:
        # json.dump(ok_dict, json_file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    pass
