# code inspired from Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge by Ye et al.
def build_critic_prompt(qs_info, history=""):
    role_description = (
        "You are now Critic, a referee whose primary role is to rigorously critique other evaluations. "
        "You must identify any weaknesses, biases, or gaps in their reasoning and provide clear, alternative perspectives where needed. "
        "Your focus is on ensuring that every evaluation is well-founded and that no critical aspect is overlooked."
    )

    history_instruction = ""
    if history != "":
        history_instruction = (
            "[Previous Referees’ Evaluations]\n"
            "Below are the evaluations and scores provided by other referees. Review each evaluation critically. "
            "Explicitly identify any strengths, weaknesses, biases, or omissions in their reasoning. "
            "For each, provide at least two critical points: one that addresses the quality of their reasoning, "
            "and one that discusses the appropriateness of their scores.\n\n"
            f"{history}\n\n"
        )

    final_prompt = (
        "You are a critical reviewer analyzing the previous referee evaluations. "
        "Your role is not to simply restate what was said, but to rigorously challenge, refine, and if necessary, dispute the evaluations. "
        "Please follow these steps:\n"
        "1. For each previous evaluation, identify specific strengths and, more importantly, pinpoint gaps, errors, or biases.\n"
        "2. Critically assess the reasoning behind each score and suggest improvements or alternatives.\n"
        "3. Provide your final evaluation and revised scores, explaining your reasoning succinctly.\n\n"
        "Use the format below:\n"
        "Evaluation evidence: <your reasoning here>\n"
        "The score of Assistant 1: <score>\n"
        "The score of Assistant 2: <score>"
        
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
We would like to request your feedback on the performance of two AI assistants in response to the user question above.
Please consider the helpfulness, relevance, accuracy, and level of detail of their responses.
There are a few other referees assigned to the same task. It’s your responsibility to critically assess their input and deliver your own well-reasoned judgment.
Each assistant receives an overall score on a scale of 1 to 10, where a higher score indicates better overall performance.

{role_description}

{history_instruction}

{final_prompt}
Now it’s your time to talk, please make your talk short and clear, Critic! You should independently solve the user question step-by-step first. Then compare both assistants’ answers with your answer.
"""
    return base_prompt


def build_general_public_prompt(qs_info, history=""):
    role_description = (
        "You are now General Public, one of the referees in this task. "
        "You are interested in the story and looking for updates on the investigation. "
        "Your evaluation must be complete and include final scores for both assistants. "
        "Remember: your final output must end with two lines exactly as follows: "
        "'The score of Assistant 1: [score only]' and 'The score of Assistant 2: [score only]'."
        "Ensure that the scores are on a scale from 1 to 10, and output these two score lines exactly as shown."

    )

    history_instruction = ""
    if history:
        history_instruction = (
            "[Previous Referees’ Evaluations]\n"
            "Below are evaluations and scores from other referees, including detailed critiques. "
            "Review these carefully, summarize their key points, and explicitly state whether you agree or disagree with them. "
            "Integrate their feedback into your final evaluation.\n\n"
            f"{history}\n\n"
        )

    if history:
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
    else:
        final_prompt = (
            "Please follow these steps:\n"
            "1. Provide your own full evaluation of the two assistants' responses.\n"
            "2. **At the end of your response, include your final scores in the exact format below:**\n"
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

{history_instruction}

{final_prompt}
Now it's your time to talk, please make your talk short and clear, General Public! You should independently solve the user question step-by-step first. Then compare both assistants’ answers with your answer.
"""
    return base_prompt


def judge_prompt(question, history):
    prompt = f"""


    {question}
    We would like you to answer the question above based on the following conversation history.
    {history}.
    Now, please provide your answer to the question.
    """
    return prompt


def critic_prompt(question, judge_message):
    prompt = f"""{question}
    With the following judge's response, please provide feedback on the potential bias in the response.
    Judge's response: {judge_message}
    Now, please provide your feedback on the judge's response.
    """
    return prompt


class judge_critic_mem_cot():
    
    def __init__(self, question=""):
        self.question = question
        self.judge_messages = []
        self.critic_messages = []

    def add_judge_message(self, message):
        self.judge_messages.append(message)

    def add_agent_message(self, message):
        self.critic_messages.append(message)
    
    def get_judge_prompt(self):
        history = ""
        #last = self.judge_messages[-1]
        #history += f"Last round: Judge: {last}\n"
        for i in range(len(self.judge_messages)):
            history += f"Round {i+1}: Judge: {self.judge_messages[i]}\n"
            history += f"Round {i+1}: Agent: {self.critic_messages[i]}\n" if i < len(self.critic_messages) else ""
        return build_general_public_prompt(self.question, history) #if history else self.question
    
    def get_critic_prompt(self):
        return build_critic_prompt(self.question, self.judge_messages[-1] if self.judge_messages else "")