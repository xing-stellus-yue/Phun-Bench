from configs import model_names, get_url, _optional_bool
from utils.run_utils import parse_args
from utils.generate import batch_generation
from evaluate.eval_py2xx import eval_py2xx
from utils.prompts import PROMPT_MAP
import asyncio
import json
import os
import random
random.seed(42)

base_url, API_KEY = get_url(model_names[0])
print(f"models={model_names} base_url={base_url}")

datasets = [
    "idioms_base_1_perturbed",
    "idioms_base_2_perturbed",
    "idioms_base_3_perturbed",
    "idioms_base_4_perturbed",
    "idioms_tone_1_perturbed",
    "idioms_tone_2_perturbed",
    "idioms_tone_3_perturbed",
    "idioms_tone_4_perturbed",
]

task_names = [
    "sim_pert2idiom_base_1",
    "sim_pert2idiom_base_2",
    "sim_pert2idiom_base_3",
    "sim_pert2idiom_base_4",
    "sim_pert2idiom_tone_1",
    "sim_pert2idiom_tone_2",
    "sim_pert2idiom_tone_3",
    "sim_pert2idiom_tone_4",
]

prompt_name = "sim_pert2idiom"


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

    if subset_num != -1 and len(filtered_data) >= subset_num:
        items = list(filtered_data.items())
        random.shuffle(items)
        filtered_data = dict(items[:subset_num])

    sys_prompt = PROMPT_MAP[prompt_name]["sys"]()
    test_dict = {}
    for key, value in filtered_data.items():
        test_dict[key] = {
            "answer": value["w"],
            "py2": value["py2"],
            "new_w": value["new_w"],
            "new_py2": value["new_py2"],
            "user_prompt": PROMPT_MAP[prompt_name]["user"](
                value["new_w"]
            ),
        }

    results = asyncio.run(
        batch_generation(
            test_dict,
            sys_prompt=sys_prompt,
            base_url=base_url,
            api_key=API_KEY,
            model_name=model_name,
            task_name=task_name,
        )
    )
    for result, key in zip(results, filtered_data):
        test_dict[key]["result"] = result[0]
        test_dict[key]["output_token"] = result[1]

    # Run evaluation
    enable_thinking = _optional_bool("LLM_ENABLE_THINKING") or False
    log_name = model_name if not enable_thinking else f"{model_name}_think"
    eval_py2xx(
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
