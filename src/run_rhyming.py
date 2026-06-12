import asyncio
import json
import os
import random
random.seed(42)
from utils.prompts import PROMPT_MAP
from evaluate.eval_rhyming import eval_rhyming
from utils.generate import batch_generation
from utils.run_utils import parse_args
from configs import model_names, get_url, _optional_bool



base_url, API_KEY = get_url(model_names[0])
print(f"models={model_names} base_url={base_url}")

datasets = ['rhyme_gen_public']*2
task_names = ["rhyming1", "rhyming2"]


def main(dataset_name,task_name):
    args = parse_args()
    subset_num = args.subset_num
    debug = args.debug

    # Paths to datasets
    data_path = f'../dataset/{dataset_name}.json'
    output_dir = f'../results'
    if debug:
        output_dir += '/debug'
    output_dir += f'/{task_name}'
    os.makedirs(output_dir, exist_ok=True)

    # Load data
    with open(data_path, mode='r', encoding='utf-8') as json_file:
        filtered_data = json.load(json_file)

    if subset_num != -1 and len(filtered_data)>=subset_num:
        items = list(filtered_data.items())
        random.shuffle(items)
        filtered_data = dict(items[:subset_num])

    # prepare input
    print(task_name)
    sys_prompt = PROMPT_MAP[task_name]['sys']()
    test_dict = {}
    for key, v in filtered_data.items():
        s = v["s"]
        test_dict[key] = {}
        test_dict[key]["s"] = s
        test_dict[key]["rg"] = v["rg"]
        test_dict[key]["user_prompt"] = PROMPT_MAP[task_name]['user'](s)

    results = asyncio.run(
        batch_generation(test_dict, sys_prompt=sys_prompt, base_url=base_url, api_key=API_KEY, model_name=model_name, task_name=task_name))
    for result, key in zip(results, filtered_data.keys()):
        test_dict[key]["result"] = result[0]
        test_dict[key]["output_token"] = result[1]

    # Run evaluation
    enable_thinking = _optional_bool("LLM_ENABLE_THINKING") or False
    log_name = model_name if not enable_thinking else f"{model_name}_think"
    eval_rhyming(
        test_dict,
        task_name,
        output_dir,
        log_name
    )

if __name__ == "__main__":
    for model_name in model_names:
        dt = zip(datasets, task_names)
        for dataset, task_name in dt:
            main(dataset, task_name)
