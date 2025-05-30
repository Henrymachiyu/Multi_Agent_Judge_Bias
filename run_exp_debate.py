import json
from tqdm import tqdm
import os
import argparse
import torch
from judge_critic import judge_critic
from prompts.judge_critic_mem import judge_critic_mem
from prompts.prompt_position import judge_critic_mem_position
from prompts.prompt_bandwagon import judge_critic_mem_bandwagon
from prompts.prompt_cot import judge_critic_mem_cot
from prompts.critic_pine_none import judge_critic_mem_pine
from prompts.critic_pine_position import judge_critic_mem_pine_position

parser = argparse.ArgumentParser(description='Multiagent_eval')
parser.add_argument('--data_dir', type=str,default='data/mtbench_pairwise_data_normal_random_sampled.json')
parser.add_argument('--judge', type=str,default='openai:gpt-4o-mini')
parser.add_argument('--critic', type=str,default='openai:gpt-4o-mini')
parser.add_argument('--device', type=str,default='4,5,6,7')
parser.add_argument('--result_save', type=str,default='result/test')
parser.add_argument('--n_round', type=int,default=2)
parser.add_argument('--batch_size', type=int, default=2)
parser.add_argument('--debug', type=bool, default=False)
parser.add_argument('--bias_type', type=str, default="None")
parser.add_argument('--count_id', type=int, default=0)
args, unknown = parser.parse_known_args()

os.environ["CUDA_VISIBLE_DEVICES"] = args.device
seed = 1234
torch.manual_seed(seed)
torch.cuda.manual_seed(seed)

with open(args.data_dir, 'r', encoding='utf-8') as file:
    data = json.load(file)

keys = list(data.keys())

model = judge_critic(
    judge_model =args.judge,  # Example judge model
    critic_model=args.critic,  # Example critic model
    round=args.n_round,  # Set the number of rounds for the discussion
    judge_temperature=0.01,
    critic_temperature=0.01,
    jugde_max_tokens=512,
    critic_max_tokens=512
)
if args.bias_type == 'none':
    process = judge_critic_mem
elif args.bias_type == 'position':
    process = judge_critic_mem_position
elif args.bias_type == 'bandwagon':
    process = judge_critic_mem_bandwagon
elif args.bias_type == 'cot':
    process = judge_critic_mem_cot
elif args.bias_type == 'pine_none':
    process = judge_critic_mem_pine
elif args.bias_type == 'pine_position':
    process = judge_critic_mem_pine_position

batch_size = args.batch_size  # Define the batch size
for batch_start in tqdm(range(0, len(data), batch_size)):
    if batch_start < args.count_id*batch_size:
        continue
    batch_end = min(batch_start + batch_size, len(data))
    batch_keys = keys[batch_start:batch_end]
    batch_data = [data[key] for key in batch_keys]  # Convert to list as required by model
    
    batch_results = model(batch_data, process, debug=args.debug)


    # Save the results for each batch
    for i in range(args.n_round+1):

        if os.path.exists(args.result_save + f"_round{i}.json"):
            with open(args.result_save + f"_round{i}.json", "r") as file:
                existing_data = json.load(file)
        else:
            existing_data = {}

        round_i_results = [batch_result[i] for batch_result in batch_results]

        for key, result in zip(batch_keys, round_i_results):
            existing_data.update({key: result})
            with open(args.result_save + f"_round{i}.json", "w") as file:
                json.dump(existing_data, file, indent=4)