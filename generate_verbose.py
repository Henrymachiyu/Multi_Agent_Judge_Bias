import json
from llm.openai_model import openai_model

# read input_file
# use gpt to make answer2 verbose
# save to output_file

# Load the data
input_file  = "data/mtbench_pairwise_data_normal_random_sampled.json"
output_file = "data/mtbench_pairwise_data_normal_random_sampled_verbose.json"

with open(input_file, "r") as f:
    data = json.load(f)

# Initialize the OpenAI model
model = openai_model(model_name="gpt-4o", temperature=0.7, max_tokens=1024)

# Make answer2 verbose using the OpenAI model
for k in data.keys():
    item = data[k]
    # prompt = f"Rewrite and make this verbose:\n{item['answer2']}"
    prompt = f"""Expand the length of the answer provided below by adding sentences and phrases that are relevant to the topic but semantically redundant. Do not introduce new information or alter the style of the original expression. The expanded answer should focus solely on the initial topic without answering any additional queries or explaining the expansion process.
Original Answer:
{item['answer2']}
Instructions:
Keep the factual content and expression style consistent with the original answer.
Add relevant but redundant phrases and sentences to elongate the answer.
Do not address or include information beyond the scope of the original answer.
"""
    item['answer2'] = model.generate_by_prompt(prompt)
    print(f"Updated answer2 for item {k}:")
    print(item['answer2'])
    print("===")

# Save the updated data
with open(output_file, "w") as f:
    json.dump(data, f, indent=4)