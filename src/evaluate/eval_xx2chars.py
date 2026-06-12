import re
import json
# import numpy as np
from collections import Counter
import os
import time
from collections import defaultdict

from pypinyin import Style, pinyin

# j={
#     "ref": "义",
#     "py1": "yi4",
###
#     "user_prompt": "请将以下汉字转换为拼音：义",
###
#     "results": "{\n  \"answer\": \"[...]\"\n}",
#     "pred": [...],
#     "score": 4
# }


def get_pred_json(data):
    matches = re.findall(r'\{\s*"answer"\s*:\s*(?:".*?"|\[.*?\])\s*\}', data, re.DOTALL)
    match = matches[-1] if matches else None
    if match:
        json_str = match
        try:
            result = json.loads(json_str)
        except json.JSONDecodeError:
            print(f"Error decoding JSON: {data}")
            return None
        answer = result["answer"]
    else:
        return None
    # Should be a list of characters
    return answer


def eval_xx2chars(test_dict, task_name, output_dir, model_name):
    total_num = len(test_dict)
    true_num = 0
    p_true_num = 0
    error_num = 0
    for k, v in test_dict.items():
        pred = get_pred_json(v['result'])
        v['pred'] = pred
        if pred is None or not isinstance(pred, list):
            error_num += 1
            v['score'] = 0
        else:
            score = 0
            gt = v['py1']
            shown=[]
            for c in pred[:5]:
                if c == v.get('c', None) or len(c) != 1 or c in shown:
                    continue
                shown.append(c)
                pys = pinyin(c, style=Style.TONE3, heteronym=True,
                             neutral_tone_with_five=True)[0]
                if gt in pys:
                    score += 1
            v['score'] = score
            p_true_num += score/5
            if score == 5:
                true_num += 1

    em = f"{true_num / total_num:.4f}"
    pm = f"{p_true_num / total_num:.4f}"
    er = f"{error_num / total_num:.4f}"
    t = time.localtime()
    model_name=model_name.replace("/","_")
    output_json_name = f'{task_name}_{model_name}.{t.tm_mon:02}.{t.tm_mday:02},{t.tm_hour:02}:{t.tm_min:02}.json'
    log_name = f'{task_name}_{model_name}.{t.tm_mon:02}.{t.tm_mday:02},{t.tm_hour:02}:{t.tm_min:02}.log'
    with open(os.path.join(output_dir, output_json_name), 'w', encoding='utf-8') as json_file:
        json.dump(test_dict, json_file, indent=4, ensure_ascii=False)
    with open(os.path.join(output_dir, log_name), 'a', encoding='utf-8') as log_file:
        content = f"em: {em}, pm: {pm}, error_rate: {er}, total_num: {total_num}\n"
        log_file.write(content)


if __name__ == "__main__":
    input_filepath= "data/output/debug/char2chars_deepseek-chat.08.01,18:11.json"
    with open(input_filepath, 'r', encoding='utf-8') as json_file:
        test_dict = json.load(json_file)
    eval_xx2chars(test_dict,task_name="char2chars", output_dir="data/output/debug", model_name="deepseek-chat#")
