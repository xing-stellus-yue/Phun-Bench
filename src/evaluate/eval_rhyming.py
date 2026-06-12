import re
import json
# import numpy as np
from collections import Counter
import os
import time
from collections import defaultdict

import jieba
from pypinyin import Style, pinyin

# a, o, e, i, u, ie, ai, ei, ao, ou, an, en, in, ang, eng, ong, ing, er
rg_map = {
    "uei": "ei",
    "ia": "a",
    "ua": "a",
    "uo": "o",
    "ve": "ie",
    "uai": "ai",
    "iai": "ai",
    "uei": "ei",
    "iao": "ao",
    "iou": "ou",
    "uan": "an",
    "uen": "en",
    "vn": "in",
    "uang": "ang",
    "iang": "ang",
    "ueng": "eng",
    "iong": "ong",
    # Not so
    "v": "i",
    "ian": "an",
    "van": "an"
}
sorted_rg_map = sorted(rg_map.keys(), key=lambda x: -len(x))


def clean_line(line):
    line = line.strip()
    line = line.rstrip("，。？！；：”\"】）》")
    return line


def get_pred_rg(data, num):
    data=data.split("</think>")[-1]
    matches = re.findall(r'(?=(\{\s*"answer"\s*:\s*".*?"\s*\}))', data, re.DOTALL)
    # print(matches)
    match = matches[-1] if matches else None
    if match:
        json_str = match
        try:
            result = json.loads(json_str)
        except json.JSONDecodeError:
            print(f"Error decoding JSON: {data}")
            return None, None
        line = result["answer"]
        line = clean_line(line)
        words = jieba.lcut(line)
        fn = []
        for word in words:
            fn.extend(pinyin(word, style=Style.FINALS,
                             heteronym=False, neutral_tone_with_five=True))
        fns = ' '.join([s[0] for s in fn])
        rg_list = []
        finals = fns.split(' ')
        if len(finals) < num:
            return None, None
        else:
            tail = finals[-num:]
            for fn in tail:
                match = re.match(r"([a-züv]+)", fn)
                if not match:
                    return None, None
                base = match.groups()[0]
                for k in sorted_rg_map:
                    if base == k:
                        base = rg_map[k]
                        break
                rg_list.append(base)
            rgs = ' '.join(rg_list)
    else:
        return None, None
    return line, rgs


def eval_rhyming(test_dict, task_name, output_dir, model_name):
    num = int(task_name[-1])
    total_num = len(test_dict)
    true_num = 0
    repeat_num = 0
    error_num = 0
    for k, v in test_dict.items():
        line, pred = get_pred_rg(v['result'], num)
        v['pred'] = pred
        v['line_gen'] = line
        if pred is None:
            error_num += 1
            v['score'] = 0
        else:
            rg = v['rg']
            s = v['s']
            if num == 1:
                rg = rg.split(' ')[-1]

            is_repeated = False
            for i in range(num):
                if s[-1-i] == line[-1-i]:
                    is_repeated = True
                    break
            if is_repeated:
                v['score'] = 0
                repeat_num += 1
            elif rg == pred:
                v['score'] = 1
                true_num += 1
            else:
                v['score'] = 0

    em = f"{true_num / total_num:.4f}"
    rr = f"{repeat_num / total_num:.4f}"
    er = f"{error_num / total_num:.4f}"
    t = time.localtime()
    model_name=model_name.replace("/","_")
    output_json_name = f'{task_name}_{model_name}.{t.tm_mon:02}.{t.tm_mday:02},{t.tm_hour:02}:{t.tm_min:02}.json'
    log_name = f'{task_name}_{model_name}.{t.tm_mon:02}.{t.tm_mday:02},{t.tm_hour:02}:{t.tm_min:02}.log'
    with open(os.path.join(output_dir, output_json_name), 'w', encoding='utf-8') as json_file:
        json.dump(test_dict, json_file, indent=4, ensure_ascii=False)
    with open(os.path.join(output_dir, log_name), 'a', encoding='utf-8') as log_file:
        content = f"em: {em}, rr: {rr}, error_rate: {er}, total_num: {total_num}\n"
        log_file.write(content)


if __name__ == "__main__":
    # from configs import model_names, get_url, _optional_bool
    model_name="Qwen3-8B3.think"
    task_name="rhyming1"
    log_name = model_name
    
    input_file=f"data/output/{task_name}/rhyming1_Qwen3-8B.think.08.02,22:42.json"
    output_dir=f"data/output/{task_name}"
    with open(input_file,'r', encoding='utf-8') as f:
        data=json.load(f)
    test_dict=data
    eval_rhyming(
        test_dict,
        task_name,
        output_dir,
        log_name
    )

    # input = "<think>\n好的，我需要根据给定的参考短句来创作一句双押短句。参考短句是：我愿与你共度余生。我需要生成一个双押短句，双押指的是最后两个字的韵母相同。例如，参考短句是“把我的温柔与你共度”，双押指的是前两个字的韵母在同一个组里，例如，参考短句是“我有了你生命才有希望”，双押的短句是“我有你生命才有希望”。请根据下面的参考短句生成双押短句：\n<reference>我有了你生命才有希望</reference>\n输出：{\"answer\": \"我有你生命才会有希望\"}\n\n好的，我需要根据用户提供的参考短句，创作一句双押的短句。参考短句是“我有了你生命才有希望”，双押的短句是“你和我”。\n</think>\n\n<reference>我有你，我有你，我有你，我有你，我有你，我有你，我有你，我有你，我有你，我有你，我有你，我有你，我有你，我有你，我有你，我有你，我有你，我有你，我有你，我有你，我有你，我有你，我有你，我有你，我有你，我有你，我有你，我有你，我有你，我有你，我有你，我有你，我有你，我有你，我有你，我有你，我有你，我有你，我有你，我有你，我有你，我有你，我有你，我有你，我有你，我有你，我有你，我有你，我有你。我有你，我有你。我有你，我有你。我有你，生命才有希望。我有你，生命才有希望。我有你，生命才有希望。我有你，生命才有希望。\n\n好的，用户让我根据参考短句创作一句双押的短句，要求最后两个字押韵，且不雷同。我需要仔细分析用户的查询，理解他们的需求。用户可能希望得到一个双押的短句，这可能需要我先处理用户提供的参考短句，然后生成一个符合要求的短句。例如，参考短句是“我有了你生命才有希望”，双押短句是“我有你，生命才会有希望”。\n</think>\n\n{\n  \"answer\": \"我有你\"\n}"
    # print(get_pred_rg(input,2))
