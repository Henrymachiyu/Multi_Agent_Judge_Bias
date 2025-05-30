from llm.hf_model import hf_model
from llm.openai_model import openai_model
from llm.togetherai_model import togetherai_model
from llm.deepseek_model import deepseek_model
from llm.azure_model import azure_model
from llm.pine import pine_model

class judge_critic():

    def __init__(self, 
                 judge_model, 
                 critic_model, 
                 round,
                 judge_temperature=0.7,
                 critic_temperature=0.7,
                 jugde_max_tokens=512,
                 critic_max_tokens=512
                 ):

        self.round = round

        if judge_model.startswith("hf:"):
            self.judge = hf_model(judge_model[3:], 
                                  temperature=judge_temperature,
                                  max_tokens=jugde_max_tokens)
        elif judge_model.startswith("openai:"):
            self.judge = openai_model(judge_model[7:],  
                                      temperature=judge_temperature,
                                      max_tokens=jugde_max_tokens)
        elif judge_model.startswith("togetherai:"):
            self.judge = togetherai_model(judge_model[11:],  
                                          temperature=judge_temperature,
                                          max_tokens=jugde_max_tokens)
        elif judge_model.startswith("deepseek:"):
            self.judge = deepseek_model(judge_model[9:],  
                                        temperature=judge_temperature,
                                        max_tokens=jugde_max_tokens)
        elif judge_model.startswith("azure:"):
            self.judge = azure_model(judge_model[6:],  
                                      temperature=judge_temperature,
                                      max_tokens=jugde_max_tokens)
        elif judge_model.startswith("pine:"):
            self.judge = pine_model(judge_model[5:],
                                    temperature=judge_temperature,
                                    max_tokens=jugde_max_tokens)
        else:
            raise ValueError("Unsupported judge model type")
        
        if critic_model == judge_model:
            # If critic model is the same as judge model, use the same instance to save resources
            self.critic = self.judge
        else:
            # Otherwise, initialize a new critic model
            if critic_model.startswith("hf:"):
                self.critic = hf_model(critic_model[3:],
                                    temperature=critic_temperature,
                                    max_tokens=critic_max_tokens)
            elif critic_model.startswith("openai:"):
                self.critic = openai_model(critic_model[7:],
                                        temperature=critic_temperature,
                                        max_tokens=critic_max_tokens)
            elif critic_model.startswith("togetherai:"):
                self.critic = togetherai_model(critic_model[11:],  
                                          temperature=judge_temperature,
                                          max_tokens=jugde_max_tokens)
            elif critic_model.startswith("deepseek:"):
                self.critic = deepseek_model(critic_model[9:],  
                                        temperature=judge_temperature,
                                        max_tokens=jugde_max_tokens)
            elif critic_model.startswith("pine:"):
                self.critic = pine_model(critic_model[5:],
                                         temperature=critic_temperature,
                                         max_tokens=critic_max_tokens)
            else:
                raise ValueError("Unsupported critic model type")
    

    def __call__(self, input_data, process, debug=False):

        if isinstance(input_data, dict):
            mem = process(input_data)
           # print(mem.get_judge_prompt())
            judge_response = self.judge.generate_by_prompt(mem.get_judge_prompt())
            mem.add_judge_message(judge_response)

            if debug:
                print(f"Initial Judge response: {judge_response}")
                print("*" * 50)

            for t in range(self.round):
                critic_response = self.critic.generate_by_prompt(mem.get_critic_prompt())
                mem.add_agent_message(critic_response)
                judge_response = self.judge.generate_by_prompt(mem.get_judge_prompt())
                mem.add_judge_message(judge_response)

                if debug:
                    print(f"Round {t+1}: Critic response: {critic_response}")
                    print("-" * 50)
                    print(f"Round {t+1}: Judge response: {judge_response}")
                    print("*" * 50)

            return mem.judge_messages    # Return the last judge response
                    
        if  isinstance(input_data, list):
            mem = [process(item) for item in input_data]
            judge_responses = self.judge.generate_by_prompt_batch([m.get_judge_prompt() for m in mem])

            for i, judge_response in enumerate(judge_responses):
                mem[i].add_judge_message(judge_response)

            if debug:
                for i, judge_response in enumerate(judge_responses):
                    print(f"Initial Judge response for input {i}: {judge_response}")
                    print("*" * 50)

            for t in range(self.round):
                critic_response = self.critic.generate_by_prompt_batch([m.get_critic_prompt() for m in mem])
                for i, response in enumerate(critic_response):
                    mem[i].add_agent_message(response)
                judge_responses = self.judge.generate_by_prompt_batch([m.get_judge_prompt() for m in mem])
                for i, judge_response in enumerate(judge_responses):
                    mem[i].add_judge_message(judge_response)

                if debug:
                    for i in range(len(mem)):
                        print(f"Round {t+1} for input {i}: Critic response: {critic_response[i]}")
                        print("-" * 50)
                        print(f"Round {t+1} for input {i}: Judge response: {judge_responses[i]}")
                        print("*" * 50)

            return [m.judge_messages for m in mem]