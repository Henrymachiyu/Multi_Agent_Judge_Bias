import json
from tqdm import tqdm
import os
import argparse
import torch
from meta_judge import meta_judge
from prompts.meta_judge_prompt import *
import re
import random

parser = argparse.ArgumentParser(description='Multiagent_eval')
parser.add_argument('--data_dir', type=str, default='data/mtbench_pairwise_data_normal_random_sampled.json')
parser.add_argument('--judge', type=str, default='openai:gpt-4o-mini')
parser.add_argument('--judgements_models', type=str, default='gpt-4o-mini,deepseek-chat')
parser.add_argument('--judgements_dir', type=str,default='result/gpt-4o-mini_deepseek-chat')
parser.add_argument('--device', type=str,default='4,5,6,7')
parser.add_argument('--result_save', type=str,default='result_meta')
parser.add_argument('--batch_size', type=int, default=2)
parser.add_argument('--debug', type=bool, default=False)
parser.add_argument('--judge_type', type=str, default='conclude')
parser.add_argument('--bias_type', type=str, default="none")
parser.add_argument('--count_id', type=int, default=0)
args, unknown = parser.parse_known_args()

os.environ["CUDA_VISIBLE_DEVICES"] = args.device
seed = 1234
torch.manual_seed(seed)
torch.cuda.manual_seed(seed)

with open(args.data_dir, 'r', encoding='utf-8') as file:
    data = json.load(file)

keys = list(data.keys())

model = meta_judge(
    judge_model =args.judge,
    judge_temperature=0.01,
    jugde_max_tokens=512,
)

if args.bias_type == "position":
    if args.judge_type == "conclude":
        process = meta_judge_conclude_mem_position
    elif args.judge_type == "choose":
        process = meta_judge_choose_mem_position
elif args.bias_type == "cot":
    if args.judge_type == "conclude":
        process = meta_judge_conclude_mem_cot
    elif args.judge_type == "choose":
        process = meta_judge_choose_mem_cot
elif args.bias_type == "bandwagon":
    if args.judge_type == "conclude":
        process = meta_judge_conclude_mem_bandwagon
    elif args.judge_type == "choose":
        process = meta_judge_choose_mem_bandwagon    
else:
    if args.judge_type == "conclude":
        process = meta_judge_conclude_mem
    elif args.judge_type == "choose":
        process = meta_judge_choose_mem

model_list = args.judgements_models.split(",")

# Load the judgements
judgements_dict = {}
for name in model_list:
    judgements_dict[name] = {}
    if os.path.exists(args.judgements_dir + f"/{name}-{args.bias_type}_round0.json"):
        with open(args.judgements_dir + f"/{name}-{args.bias_type}_round0.json", 'r', encoding='utf-8') as file:
            judgements_dict[name].update(json.load(file))
    else:
        raise FileNotFoundError(f"Judgement file for {name} not found.")

batch_size = args.batch_size  # Define the batch size
for batch_start in tqdm(range(0, len(data), batch_size)):

    random.shuffle(model_list) # Shuffle the order of models

    if batch_start < args.count_id*batch_size:
        continue
    batch_end = min(batch_start + batch_size, len(data))
    batch_keys = keys[batch_start:batch_end]
    batch_data = [data[key] for key in batch_keys]  # Convert to list as required by model

    # Prepare the batch judgements
    batch_judgements = []
    for batch_key in batch_keys:
        j = []
        for name in model_list:
            if batch_key in judgements_dict[name]:
                j.append(judgements_dict[name][batch_key])
            else:
                raise KeyError(f"Key {batch_key} not found in judgements for model {name}.")
        batch_judgements.append(j)

    batch_results = model(batch_data, process, batch_judgements, debug=args.debug)

    if args.judge_type == "conclude":
        if os.path.exists(args.result_save + "_round0.json"):
            with open(args.result_save + "_round0.json", "r") as file:
                existing_data = json.load(file)
        else:
            existing_data = {}
        for key, result in zip(batch_keys, batch_results):
            existing_data.update({key: result})
            with open(args.result_save + "_round0.json", "w") as file:
                json.dump(existing_data, file, indent=4)

    elif args.judge_type == "choose":
        if os.path.exists(args.result_save + "_round0.json"):
            with open(args.result_save + "_round0.json", "r") as file:
                existing_data = json.load(file)
        else:
            existing_data = {}
        
        for key, result in zip(batch_keys, batch_results):
            match = re.search(r"The best refree is:\s*([A-Z])", result)
            if match:
                best_judgement = match.group(1)
                letter_to_index = ord(best_judgement) - ord('A')
                resp = judgements_dict[model_list[letter_to_index]][key]
            else:
                resp = "No answer."
            
            existing_data.update({key: resp})
            
            with open(args.result_save + "_round0.json", "w") as file:
                json.dump(existing_data, file, indent=4)