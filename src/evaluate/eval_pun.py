import re
import json
from collections import Counter
import os
import time
from collections import defaultdict

######
# with open("data/puns_filter_homo.json","r",encoding="utf-8") as ref:
    # ref_data=json.load(ref)

####

def get_pred_zh_pun(data):
    if not isinstance(data, str):
        return None, None
    matches = re.findall(r'\{\s*"pun word"\s*:\s*".*?"\s*,\s*"alternative word"\s*:\s*".*?"\s*\}', data, re.DOTALL)
    match = matches[-1] if matches else None
    if match:
        json_str = match
        try:
            result = json.loads(json_str)
        except json.JSONDecodeError:
            print(f"Error decoding JSON: {data}")
            return None, None
        pw = result["pun word"].strip()
        aw = result["alternative word"].strip()
    else:
        return None, None
    return pw, aw

def eval_zh_pun(test_dict, task_name, output_dir,model_name):
    total_num = len(test_dict)
    # total_num = 0
    error_num = 0
    s_include_num=0
    pw_include_num=0
    aw_include_num=0
    for k, v in test_dict.items():
        # if k in ref_data.keys():
        #     total_num+=1
        # else:
        #     continue
        
        pred_pw, pred_aw = get_pred_zh_pun(v['result'])
        v['pred_pw'] = pred_pw
        v['pred_aw'] = pred_aw
        s=v['s']
        pw = v['pw']
        aw = v['aw']
  
        if pred_pw is None:
            error_num += 1
            v['score'] = (0,0,0)
        else:
            if pred_pw in s:
                s_include_num += 1
                if pred_pw in pw:
                    pw_include_num += 1
                    if pred_aw in aw:
                        aw_include_num += 1
                        v['score'] = (1,1,1)
                    else:
                        v['score'] = (1,1,0)
                else:
                    v['score'] = (1,0,0)
            else:
                v['score'] = (0,0,0)
    aw_include_rate = f"{aw_include_num / total_num:.4f}"
    pw_include_rate = f"{pw_include_num / total_num:.4f}"
    s_include_rate = f"{s_include_num / total_num:.4f}"
    er = f"{error_num / total_num:.4f}"
    t = time.localtime()
    model_name=model_name.replace("/","_")
    output_json_name = f'{task_name}_{model_name}.{t.tm_mon:02}.{t.tm_mday:02},{t.tm_hour:02}:{t.tm_min:02}.json'
    log_name = f'{task_name}_{model_name}.{t.tm_mon:02}.{t.tm_mday:02},{t.tm_hour:02}:{t.tm_min:02}.log'
    print(output_json_name)
    with open(os.path.join(output_dir, output_json_name), 'w', encoding='utf-8') as json_file:
        json.dump(test_dict, json_file, indent=4, ensure_ascii=False)
    with open(os.path.join(output_dir, log_name), 'a', encoding='utf-8') as log_file:
        content = f"aw_include_rate: {aw_include_rate}\npw_include_rate: {pw_include_rate}\ns_include_rate: {s_include_rate}\ner: {er}, total_num: {total_num}\n"
        log_file.write(content)


if __name__ == "__main__":
    pass
    # # from configs import model_names, get_url, _optional_bool
    # task_name="pun"
    # target_dir=f"data/output/{task_name}"
    # for filename in os.listdir(target_dir):
    #     # print(filename.split('.')[-1])
    #     if filename.split('.')[-1] == "json":
    #         log_name=filename.split(".0")[0].split(f"{task_name}_")[-1]
    #         print(log_name)
    #         input_file=target_dir+"/"+filename
    #         with open(input_file,'r', encoding='utf-8') as f:
    #             data=json.load(f)
    #         test_dict=data
    #         eval_zh_pun(
    #             test_dict,
    #             task_name+'_homo',
    #             target_dir,
    #             log_name
    #         )