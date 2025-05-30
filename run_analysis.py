import json
import re
import os

dir_path='results/result_debate_calm' 

result_dir_root="analysis/analysis_debate_calm"
               
model_names = [
               'deepseek-chat',
               'DeepSeek-R1-Distill-Qwen-32B',
               'gpt-4o-mini',
               'Llama-3.3-70B-Instruct-Turbo',
               'Llama-3.3-70B-Instruct-Turbo_gpt-4o-mini',
               'gpt-4o-mini_Llama-3.3-70B-Instruct-Turbo',
               'DeepSeek-R1-Distill-Qwen-32B_gpt-4o-mini',
               'DeepSeek-R1-Distill-Qwen-32B_Llama-3.3-70B-Instruct-Turbo',
               'DeepSeek-R1-Distill-Qwen-32B_deepseek-chat',
            #    'gpt-4o-mini_pine',
            #    'Llama-3.3-70B-Instruct-Turbo_pine',
]

bias_types  = ['position', 'cot', 'verbose', 'bandwagon']
# bias_types  = ['position']

for model_name in model_names:
    for bias_type in bias_types:
        result_dir = result_dir_root + f"/{model_name}-{bias_type}.json"
        state = ['none', bias_type]
        # Regex to extract scores (supports float and flexible phrasing)
        score_pattern_1 = re.compile(
            r'(?:score of|Assistant)\s*1\s*[:\-]?\s*(\d+(?:\.\d+)?)',
            re.IGNORECASE | re.DOTALL
        )
        score_pattern_2 = re.compile(
            r'(?:score of|Assistant)\s*2\s*[:\-]?\s*(\d+(?:\.\d+)?)',
            re.IGNORECASE | re.DOTALL
        )

        #consistent pairs
        if bias_type == 'position':
            cons_pair = {("Assistant 1","Assistant 2"), ("Assistant 2", "Assistant 1"), ('Tie','Tie')}
        else:
            cons_pair = {("Assistant 1","Assistant 1"), ("Assistant 2", "Assistant 2"), ('Tie','Tie')}


        def get_existing_model_state_files(model_name, states, dir_path='./result'):
            """
            Return a list of actual filenames matching the given model name and list of states.
            Expected filename format: {model_name}-{state}_round{N}.json
            """
            existing_files = os.listdir(dir_path)
            matched_files = []
            for file_name in existing_files:
                for state in states:
                    pattern = f"{model_name}-{state}_round"
                    if file_name.startswith(pattern) and file_name.endswith(".json"):
                        file = os.path.join(dir_path, file_name)
                        matched_files.append(file)
            return sorted(matched_files)


        files = get_existing_model_state_files(model_name, state, dir_path)
        file_pattern = re.compile(r"(.+)_round(\d+)\.json$")
        print("Files:")
        for file in files:
            match = file_pattern.match(file)
            if match:
                print(f"Model: {match.groups()[0]}, Round: {match.groups()[1]}")
            else:
                print(f"File name format is incorrect: {file}")

        cur_analysis = {}
        cur_analysis_2 = {}
        for file in files:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
            base = file.replace(".json", "")
            base = base.replace('./result', "")
            model = base.rsplit("_round", 1)[0].lstrip("/")  # e.g., "deepseek-chat-none"
            round_number = base.rsplit("_round", 1)[1]  # e.g., "0"
            last_part = model.split("-")[-1]
            count_anws2 = 0
            for key, value in data.items():
                if key not in cur_analysis:
                    cur_analysis[key] = []
                if key not in cur_analysis_2:
                    cur_analysis_2[key] = []
                score_match_1 = score_pattern_1.search(value)
                score_match_2 = score_pattern_2.search(value)
                if score_match_1 and score_match_2:
                    score1 = float(score_match_1.group(1))
                    score2 = float(score_match_2.group(1))
                    if score1 > score2:
                            winner = "Assistant 1"
                    elif score2 > score1:
                        winner = "Assistant 2"
                        count_anws2 +=1
                    else:
                        winner = "Tie"
                if last_part =='none':
                    #print('true')
                    cur_analysis[key].append((score1, score2,winner))
                elif last_part == state[-1]:
                    cur_analysis_2[key].append((score1, score2,winner))

            #print(count_anws2)
        keys = cur_analysis.keys()
        round_count = [0, 0, 0, 0]
        avg_score_diff_assistant1 = [0, 0, 0, 0]
        avg_score_diff_assistant2 = [0, 0, 0, 0]
        interval_diff_none = [0, 0, 0, 0]
        interval_diff_bias = [0, 0, 0, 0]
        num_1 = [0, 0, 0, 0]
        num_2 = [0, 0, 0, 0]
        num_1_bias = [0, 0, 0, 0]
        num_2_bias = [0, 0, 0, 0]

        n = len(data.keys())
        print('###########')
        print('Data size is:')
        print(n)
        print('###########')

        for k in keys:
            rounds_data_none = cur_analysis[k] 
            rounds_data_bias = cur_analysis_2[k]

            for i in range(len(rounds_data_none)):
                round_data_none  = rounds_data_none[i]
                round_data_bias = rounds_data_bias[i]
                pair = (round_data_none[-1], round_data_bias[-1])
                if pair[0] == "Assistant 1":
                    num_1[i] +=1/n
                elif pair[0] == "Assistant 2":
                    num_2[i] +=1/n
                if pair[1] == "Assistant 1":
                    num_1_bias[i] +=1/n
                elif pair[1] == "Assistant 2":
                    num_2_bias[i] +=1/n
                
                if bias_type == 'position':
                    diff1 = abs(round_data_none[0] - round_data_bias[1])
                    diff2 = abs(round_data_none[1]- round_data_bias[0])
                else:
                    diff1 = abs(round_data_none[0] - round_data_bias[0])
                    diff2 = abs(round_data_none[1] - round_data_bias[1])
                
                interval_norm = abs(round_data_none[0] - round_data_none[1])
                interval_bias = abs(round_data_bias[0] - round_data_bias[1])
                avg_score_diff_assistant1[i] += diff1/n
                avg_score_diff_assistant2[i] += diff2/n
                interval_diff_none[i] += interval_norm/n
                interval_diff_bias[i] += interval_bias/n
                if pair in cons_pair:
                    round_count[i] +=1/n


        # Combine into one dict
        combined_data = {
            "round_count": round_count,
            "avg_score_diff_assistant1": avg_score_diff_assistant1,
            "avg_score_diff_assistant2": avg_score_diff_assistant2,
            'interval_diff_none':interval_diff_none,
            'interval_diff_bias':interval_diff_bias,
            'num_1_chosen_none':num_1,
            'num_2_chosen_none':num_2,
            'num_1_chosen_bias':num_1_bias,
            'num_2_chosen_bias':num_2_bias
        }
        print(combined_data)
        print('###########')

        # Save to JSON
        with open(result_dir, "w") as f:
            json.dump(combined_data, f, indent=4)