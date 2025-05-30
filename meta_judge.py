from llm.hf_model import hf_model
from llm.openai_model import openai_model
from llm.togetherai_model import togetherai_model
from llm.deepseek_model import deepseek_model
from llm.azure_model import azure_model
from llm.pine import pine_model

class meta_judge():

    def __init__(self, 
                 judge_model,
                 judge_temperature=0.7,
                 jugde_max_tokens=512,
                 ):

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

    def __call__(self, input_data, process, judgements, debug=False):

        if isinstance(input_data, dict):
            mem = process(input_data)
            for judgement in judgements:
                mem.add_judgement(judgement)
            meta_judge_response = self.judge.generate_by_prompt(mem.get_judge_prompt())
            if debug:
                print(f"Input data: {mem.get_judge_prompt()}")
                print(f"Meta Judge response: {judge_response}")
                print("*" * 50)
            return meta_judge_response    # Return the last judge response
                    
        if  isinstance(input_data, list):
            mem = [process(item) for item in input_data]
            for i, judgement in enumerate(judgements):
                for j in judgement:
                    mem[i].add_judgement(j)

            judge_responses = self.judge.generate_by_prompt_batch([m.get_judge_prompt() for m in mem])
            
            if debug:
                for i, judge_response in enumerate(judge_responses):
                    print(f"Input data: {mem[i].get_judge_prompt()}")
                    print(f"Meta Judge response for input {i}: {judge_response}")
                    print("*" * 50)
                    
            return judge_responses