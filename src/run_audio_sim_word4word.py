from configs import _optional_bool, model_names, get_url
from utils.run_utils import parse_args
from utils.generate import batch_generation
from evaluate.eval_xx4xx import eval_xx4xx
from utils.prompts import PROMPT_MAP
import asyncio
import json
import os
import random
random.seed(42)
model_name = model_names[0]
base_url, API_KEY = get_url(model_name)
print(f"model={model_name} base_url={base_url}")
datasets = [
    'sim_word_pert1',
    'sim_word_pert2',
    'sim_word_pert3',
    'sim_word_pert4',
]
task_names = [
    'word4word_pert1',
    'word4word_pert2',
    'word4word_pert3',
    'word4word_pert4',
]
prompt_name = "audio_sim_word4word"
dt = zip(datasets, task_names)
enable_thinking = _optional_bool("LLM_ENABLE_THINKING") or False
log_name = model_name if not enable_thinking else f"{model_name}_think"


def main(dataset_name,task_name):
    args = parse_args()
    task_name="audio_"+task_name
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

    if subset_num != -1 and len(filtered_data) >= subset_num:
        items = list(filtered_data.items())
        random.shuffle(items)
        filtered_data = dict(items[:subset_num])

    # prepare input
    sys_prompt = None
    test_dict = {}
    for key, v in filtered_data.items():
        w = v["w"]
        w_pert = v['w_pert']
        test_dict[key] = {}
        test_dict[key]['answer'] = v['answer']
        test_dict[key]['w'] = w
        test_dict[key]['w_pert'] = w_pert
        test_dict[key]["user_prompt"] = PROMPT_MAP[prompt_name]['script'](
            w, w_pert)

    results = asyncio.run(
        batch_generation(test_dict, sys_prompt=sys_prompt, base_url=base_url, api_key=API_KEY, model_name=model_name, task_name=task_name))
    for result, key in zip(results, filtered_data.keys()):
        test_dict[key]["result"] = result[0]
        test_dict[key]["output_token"] = result[1]

    # print(test_dict)
    # Run evaluation

    eval_xx4xx(
        test_dict,
        task_name,
        output_dir,
        log_name
    )


if __name__ == "__main__":
    for dataset, task_name in dt:
        print(f"start dataset {dataset}, task {task_name}")
        main(dataset, task_name)
