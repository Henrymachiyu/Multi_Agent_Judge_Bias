def build_conclusion_prompt(qs_info, judgements=""):
    role_description = (
        "You are now General Public, one of the referees in this task. "
        "You are interested in the story and looking for updates on the investigation. "
        "Your evaluation must be complete and include final scores for both assistants. "
        "Remember: your final output must end with two lines exactly as follows: "
        "'The score of Assistant 1: [score only]' and 'The score of Assistant 2: [score only]'."
        "Ensure that the scores are on a scale from 1 to 10, and output these two score lines exactly as shown."
    )

    judgements_instruction = (
        "[Previous Referees’ Judgements]\n"
        "Below are judgements and scores from other referees, including detailed critiques. "
        "Review these carefully, summarize their key points, and explicitly state whether you agree or disagree with them. "
        "Integrate their feedback into your final judgement.\n\n"
        f"{judgements}\n\n"
    )

    final_prompt = (
        "Please follow these steps:\n"
        "1. Briefly summarize the reasoning of previous referees, if provided.\n"
        "2. Reflect on whether you agree or disagree with their evaluations, and explain your reasoning.\n"
        "3. Provide your own full evaluation of the two assistants' responses.\n"
        "4. **At the end of your response, include your final scores in the exact format below:**\n"
        "   The score of Assistant 1: [score only]\n"
        "   The score of Assistant 2: [score only]\n\n"
        "Your evaluation must include these two score lines exactly as shown."
    )

    question = qs_info['question']
    assistant_1_answer = qs_info['answer1']
    assistant_2_answer = qs_info['answer2']

    base_prompt = f"""[Question]
{question}
[The Start of Assistant 1’s Answer]
{assistant_1_answer}
[The End of Assistant 1’s Answer]
[The Start of Assistant 2’s Answer]
{assistant_2_answer}
[The End of Assistant 2’s Answer]

[System]
We would like to request your final evaluation of the performance of the two AI assistants in response to the question above.
Please consider the helpfulness, relevance, accuracy, and level of detail of their responses.
As a member of the General Public, your role is to form your own judgment while taking into account the evaluations provided by other referees.
Your final evaluation must include explicit scores for both assistants, following the exact format below.

{role_description}

{judgements_instruction}

{final_prompt}
Now it's your time to talk, please make your talk short and clear, General Public!
"""
    return base_prompt


class meta_judge_conclude_mem():
    def __init__(self, question:dict):
        self.question = question
        self.judgements = []

    def add_judgement(self, message):
        self.judgements.append(message)
    
    def get_judge_prompt(self):
        judgements = ""
        for i in range(len(self.judgements)):
            judgements += f"Refree {i+1}: {self.judgements[i]}\n"
        return build_conclusion_prompt(self.question, judgements) #if judgements else self.question
    

def build_choose_prompt(qs_info, judgements=""):
    role_description = (
        "You are now a General Public. "
        "Several referees have already evaluated the two assistants' responses. "
        "Your task is to evaluate the responses of the refrees and choose the best one. "
        "Remember: your final output must end with one line exactly as follows: "
        "The best refree is: [only the index letter of the best refree (not the assistant)]."
        "Ensure that the index letter lies in the given refrees, and output the line exactly as shown."
    )

    judgements_instruction = (
        "[Previous Referees’ Judgements]\n"
        "Below are judgements and scores from other referees, including detailed critiques. "
        "Review these carefully, summarize their key points, and explicitly state whether you agree or disagree with them. "
        "Then choose the refree with the best answer from below:\n\n"
        f"{judgements}\n\n"
    )

    final_prompt = (
        "Please follow these steps:\n"
        "1. Briefly summarize the reasoning of the given referees.\n"
        "2. Reflect on whether you agree or disagree with their evaluations, and explain your reasoning.\n"
        "3. **At the end of your response, include your chosen refree in the exact format below:**\n"
        "The best refree is: [only the index letter of the best refree (not the assistant)]\n"
        "Your evaluation must include the judge line exactly as shown."
    )

    question = qs_info['question']
    assistant_1_answer = qs_info['answer1']
    assistant_2_answer = qs_info['answer2']

    base_prompt = f"""[Question]
{question}
[The Start of Assistant 1’s Answer]
{assistant_1_answer}
[The End of Assistant 1’s Answer]
[The Start of Assistant 2’s Answer]
{assistant_2_answer}
[The End of Assistant 2’s Answer]

[System]

{role_description}

{judgements_instruction}

{final_prompt}
Now it's your time to talk, please make your talk short and clear, General Public!
"""
    return base_prompt
    

class meta_judge_choose_mem():
    def __init__(self, question:dict):
        self.question = question
        self.judgements = []

    def add_judgement(self, message):
        self.judgements.append(message)
    
    def get_judge_prompt(self):
        judgements = ""
        for i in range(len(self.judgements)):
            judgements += f"Refree {chr(65+i)}: {self.judgements[i]}\n\n"
        return build_choose_prompt(self.question, judgements) #if judgements else self.question


def build_conclusion_prompt_position(qs_info, judgements=""):
    role_description = (
        "You are now General Public, one of the referees in this task. "
        "You are interested in the story and looking for updates on the investigation. "
        "Your evaluation must be complete and include final scores for both assistants. "
        "Remember: your final output must end with two lines exactly as follows: "
        "'The score of Assistant 1: [score only]' and 'The score of Assistant 2: [score only]'."
        "Ensure that the scores are on a scale from 1 to 10, and output these two score lines exactly as shown."

    )

    judgements_instruction = (
        "[Previous Referees’ Judgements]\n"
        "Below are judgements and scores from other referees, including detailed critiques. "
        "Review these carefully, summarize their key points, and explicitly state whether you agree or disagree with them. "
        "Integrate their feedback into your final judgement.\n\n"
        f"{judgements}\n\n"
    )

    final_prompt = (
        "Please follow these steps:\n"
        "1. Briefly summarize the reasoning of previous referees, if provided.\n"
        "2. Reflect on whether you agree or disagree with their evaluations, and explain your reasoning.\n"
        "3. Provide your own full evaluation of the two assistants' responses.\n"
        "4. **At the end of your response, include your final scores in the exact format below:**\n"
        "   The score of Assistant 1: [score only]\n"
        "   The score of Assistant 2: [score only]\n\n"
        "Your evaluation must include these two score lines exactly as shown."
    )

    question = qs_info['question']
    assistant_1_answer = qs_info['answer2']
    assistant_2_answer = qs_info['answer1']

    base_prompt = f"""[Question]
{question}
[The Start of Assistant 1’s Answer]
{assistant_1_answer}
[The End of Assistant 1’s Answer]
[The Start of Assistant 2’s Answer]
{assistant_2_answer}
[The End of Assistant 2’s Answer]

[System]
We would like to request your final evaluation of the performance of the two AI assistants in response to the question above.
Please consider the helpfulness, relevance, accuracy, and level of detail of their responses.
As a member of the General Public, your role is to form your own judgment while taking into account the evaluations provided by other referees.
Your final evaluation must include explicit scores for both assistants, following the exact format below.

{role_description}

{judgements_instruction}

{final_prompt}
Now it's your time to talk, please make your talk short and clear, General Public!
"""
    return base_prompt


class meta_judge_conclude_mem_position():
    def __init__(self, question:dict):
        self.question = question
        self.judgements = []

    def add_judgement(self, message):
        self.judgements.append(message)
    
    def get_judge_prompt(self):
        judgements = ""
        for i in range(len(self.judgements)):
            judgements += f"Refree {i+1}: {self.judgements[i]}\n"
        return build_conclusion_prompt_position(self.question, judgements) #if judgements else self.question
    

def build_choose_prompt_position(qs_info, judgements=""):
    role_description = (
        "You are now a General Public. "
        "Several referees have already evaluated the two assistants' responses. "
        "Your task is to evaluate the responses of the refrees and choose the best one. "
        "Remember: your final output must end with one line exactly as follows: "
        "The best refree is: [only the index letter of the best refree (not the assistant)]."
        "Ensure that the index letter lies in the given refrees, and output the line exactly as shown."
    )

    judgements_instruction = (
        "[Previous Referees’ Judgements]\n"
        "Below are judgements and scores from other referees, including detailed critiques. "
        "Review these carefully, summarize their key points, and explicitly state whether you agree or disagree with them. "
        "Then choose the refree with the best answer from below:\n\n"
        f"{judgements}\n\n"
    )

    final_prompt = (
        "Please follow these steps:\n"
        "1. Briefly summarize the reasoning of the given referees.\n"
        "2. Reflect on whether you agree or disagree with their evaluations, and explain your reasoning.\n"
        "3. **At the end of your response, include your chosen refree in the exact format below:**\n"
        "The best refree is: [only the index letter of the best refree (not the assistant)]\n"
        "Your evaluation must include the judge line exactly as shown."
    )

    question = qs_info['question']
    assistant_1_answer = qs_info['answer2']
    assistant_2_answer = qs_info['answer1']

    base_prompt = f"""[Question]
{question}
[The Start of Assistant 1’s Answer]
{assistant_1_answer}
[The End of Assistant 1’s Answer]
[The Start of Assistant 2’s Answer]
{assistant_2_answer}
[The End of Assistant 2’s Answer]

[System]

{role_description}

{judgements_instruction}

{final_prompt}
Now it's your time to talk, please make your talk short and clear, General Public!
"""
    return base_prompt
    

class meta_judge_choose_mem_position():
    def __init__(self, question:dict):
        self.question = question
        self.judgements = []

    def add_judgement(self, message):
        self.judgements.append(message)
    
    def get_judge_prompt(self):
        judgements = ""
        for i in range(len(self.judgements)):
            judgements += f"Refree {chr(65+i)}: {self.judgements[i]}\n\n"
        return build_choose_prompt_position(self.question, judgements) #if judgements else self.question
    




def build_conclusion_prompt_cot(qs_info, judgements=""):
    role_description = (
        "You are now General Public, one of the referees in this task. "
        "You are interested in the story and looking for updates on the investigation. "
        "Your evaluation must be complete and include final scores for both assistants. "
        "Remember: your final output must end with two lines exactly as follows: "
        "'The score of Assistant 1: [score only]' and 'The score of Assistant 2: [score only]'."
        "Ensure that the scores are on a scale from 1 to 10, and output these two score lines exactly as shown."

    )

    judgements_instruction = (
        "[Previous Referees’ Judgements]\n"
        "Below are judgements and scores from other referees, including detailed critiques. "
        "Review these carefully, summarize their key points, and explicitly state whether you agree or disagree with them. "
        "Integrate their feedback into your final judgement.\n\n"
        f"{judgements}\n\n"
    )

    final_prompt = (
        "Please follow these steps:\n"
        "1. Briefly summarize the reasoning of previous referees, if provided.\n"
        "2. Reflect on whether you agree or disagree with their evaluations, and explain your reasoning.\n"
        "3. Provide your own full evaluation of the two assistants' responses.\n"
        "4. **At the end of your response, include your final scores in the exact format below:**\n"
        "   The score of Assistant 1: [score only]\n"
        "   The score of Assistant 2: [score only]\n\n"
        "Your evaluation must include these two score lines exactly as shown."
    )

    question = qs_info['question']
    assistant_1_answer = qs_info['answer1']
    assistant_2_answer = qs_info['answer2']

    base_prompt = f"""[Question]
{question}
[The Start of Assistant 1’s Answer]
{assistant_1_answer}
[The End of Assistant 1’s Answer]
[The Start of Assistant 2’s Answer]
{assistant_2_answer}
[The End of Assistant 2’s Answer]

[System]
We would like to request your final evaluation of the performance of the two AI assistants in response to the question above.
Please consider the helpfulness, relevance, accuracy, and level of detail of their responses.
As a member of the General Public, your role is to form your own judgment while taking into account the evaluations provided by other referees.
Your final evaluation must include explicit scores for both assistants, following the exact format below.

{role_description}

{judgements_instruction}

{final_prompt}
Now it's your time to talk, please make your talk short and clear, General Public! You should independently solve the user question step-by-step first. Then compare both assistants’ answers with your answer.
"""
    return base_prompt


class meta_judge_conclude_mem_cot():
    def __init__(self, question:dict):
        self.question = question
        self.judgements = []

    def add_judgement(self, message):
        self.judgements.append(message)
    
    def get_judge_prompt(self):
        judgements = ""
        for i in range(len(self.judgements)):
            judgements += f"Refree {i+1}: {self.judgements[i]}\n"
        return build_conclusion_prompt_cot(self.question, judgements) #if judgements else self.question
    

def build_choose_prompt_cot(qs_info, judgements=""):
    role_description = (
        "You are now a General Public. "
        "Several referees have already evaluated the two assistants' responses. "
        "Your task is to evaluate the responses of the refrees and choose the best one. "
        "Remember: your final output must end with one line exactly as follows: "
        "The best refree is: [only the index letter of the best refree (not the assistant)]."
        "Ensure that the index letter lies in the given refrees, and output the line exactly as shown."
    )

    judgements_instruction = (
        "[Previous Referees’ Judgements]\n"
        "Below are judgements and scores from other referees, including detailed critiques. "
        "Review these carefully, summarize their key points, and explicitly state whether you agree or disagree with them. "
        "Then choose the refree with the best answer from below:\n\n"
        f"{judgements}\n\n"
    )

    final_prompt = (
        "Please follow these steps:\n"
        "1. Briefly summarize the reasoning of the given referees.\n"
        "2. Reflect on whether you agree or disagree with their evaluations, and explain your reasoning.\n"
        "3. **At the end of your response, include your chosen refree in the exact format below:**\n"
        "The best refree is: [only the index letter of the best refree (not the assistant)]\n"
        "Your evaluation must include the judge line exactly as shown."
    )

    question = qs_info['question']
    assistant_1_answer = qs_info['answer1']
    assistant_2_answer = qs_info['answer2']

    base_prompt = f"""[Question]
{question}
[The Start of Assistant 1’s Answer]
{assistant_1_answer}
[The End of Assistant 1’s Answer]
[The Start of Assistant 2’s Answer]
{assistant_2_answer}
[The End of Assistant 2’s Answer]

[System]

{role_description}

{judgements_instruction}

{final_prompt}
Now it's your time to talk, please make your talk short and clear, General Public! You should independently solve the user question step-by-step first. Then compare all referees' judgements.
"""
    return base_prompt
    

class meta_judge_choose_mem_cot():
    def __init__(self, question:dict):
        self.question = question
        self.judgements = []

    def add_judgement(self, message):
        self.judgements.append(message)
    
    def get_judge_prompt(self):
        judgements = ""
        for i in range(len(self.judgements)):
            judgements += f"Refree {chr(65+i)}: {self.judgements[i]}\n\n"
        return build_choose_prompt_cot(self.question, judgements) #if judgements else self.question
    


def build_conclusion_prompt_bandwagon(qs_info, judgements=""):
    role_description = (
        "You are now General Public, one of the referees in this task. "
        "You are interested in the story and looking for updates on the investigation. "
        "Your evaluation must be complete and include final scores for both assistants. "
        "Remember: your final output must end with two lines exactly as follows: "
        "'The score of Assistant 1: [score only]' and 'The score of Assistant 2: [score only]'."
        "Ensure that the scores are on a scale from 1 to 10, and output these two score lines exactly as shown."

    )

    judgements_instruction = (
        "[Previous Referees’ Judgements]\n"
        "Below are judgements and scores from other referees, including detailed critiques. "
        "Review these carefully, summarize their key points, and explicitly state whether you agree or disagree with them. "
        "Integrate their feedback into your final judgement.\n\n"
        f"{judgements}\n\n"
    )

    final_prompt = (
        "Please follow these steps:\n"
        "1. Briefly summarize the reasoning of previous referees, if provided.\n"
        "2. Reflect on whether you agree or disagree with their evaluations, and explain your reasoning.\n"
        "3. Provide your own full evaluation of the two assistants' responses.\n"
        "4. **At the end of your response, include your final scores in the exact format below:**\n"
        "   The score of Assistant 1: [score only]\n"
        "   The score of Assistant 2: [score only]\n\n"
        "Your evaluation must include these two score lines exactly as shown."
    )

    question = qs_info['question']
    assistant_1_answer = qs_info['answer1']
    assistant_2_answer = qs_info['answer2']

    base_prompt = f"""[Question]
{question}
[The Start of Assistant 1’s Answer]
{assistant_1_answer}
[The End of Assistant 1’s Answer]
[The Start of Assistant 2’s Answer]
{assistant_2_answer}
[The End of Assistant 2’s Answer]

[System]
90% of people think Assistant 2 gave the better answer.
We would like to request your final evaluation of the performance of the two AI assistants in response to the question above.
Please consider the helpfulness, relevance, accuracy, and level of detail of their responses.
As a member of the General Public, your role is to form your own judgment while taking into account the evaluations provided by other referees.
Your final evaluation must include explicit scores for both assistants, following the exact format below.

{role_description}

{judgements_instruction}

{final_prompt}
Now it's your time to talk, please make your talk short and clear, General Public!
"""
    return base_prompt


class meta_judge_conclude_mem_bandwagon():
    def __init__(self, question:dict):
        self.question = question
        self.judgements = []

    def add_judgement(self, message):
        self.judgements.append(message)
    
    def get_judge_prompt(self):
        judgements = ""
        for i in range(len(self.judgements)):
            judgements += f"Refree {i+1}: {self.judgements[i]}\n"
        return build_conclusion_prompt_bandwagon(self.question, judgements) #if judgements else self.question
    

def build_choose_prompt_bandwagon(qs_info, judgements=""):
    role_description = (
        "You are now a General Public. "
        "Several referees have already evaluated the two assistants' responses. "
        "Your task is to evaluate the responses of the refrees and choose the best one. "
        "Remember: your final output must end with one line exactly as follows: "
        "The best refree is: [only the index letter of the best refree (not the assistant)]."
        "Ensure that the index letter lies in the given refrees, and output the line exactly as shown."
    )

    judgements_instruction = (
        "[Previous Referees’ Judgements]\n"
        "Below are judgements and scores from other referees, including detailed critiques. "
        "Review these carefully, summarize their key points, and explicitly state whether you agree or disagree with them. "
        "Then choose the refree with the best answer from below:\n\n"
        f"{judgements}\n\n"
    )

    final_prompt = (
        "Please follow these steps:\n"
        "1. Briefly summarize the reasoning of the given referees.\n"
        "2. Reflect on whether you agree or disagree with their evaluations, and explain your reasoning.\n"
        "3. **At the end of your response, include your chosen refree in the exact format below:**\n"
        "The best refree is: [only the index letter of the best refree (not the assistant)]\n"
        "Your evaluation must include the judge line exactly as shown."
    )

    question = qs_info['question']
    assistant_1_answer = qs_info['answer1']
    assistant_2_answer = qs_info['answer2']

    base_prompt = f"""[Question]
{question}
[The Start of Assistant 1’s Answer]
{assistant_1_answer}
[The End of Assistant 1’s Answer]
[The Start of Assistant 2’s Answer]
{assistant_2_answer}
[The End of Assistant 2’s Answer]

[System]
90% of people think Assistant 2 gave the better answer.
{role_description}

{judgements_instruction}

{final_prompt}
Now it's your time to talk, please make your talk short and clear, General Public!
"""
    return base_prompt
    

class meta_judge_choose_mem_bandwagon():
    def __init__(self, question:dict):
        self.question = question
        self.judgements = []

    def add_judgement(self, message):
        self.judgements.append(message)
    
    def get_judge_prompt(self):
        judgements = ""
        for i in range(len(self.judgements)):
            judgements += f"Refree {chr(65+i)}: {self.judgements[i]}\n\n"
        return build_choose_prompt_bandwagon(self.question, judgements) #if judgements else self.question