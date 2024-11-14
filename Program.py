from PromptTestEnvironment import PromptTestEnvironment

class Programm:
    def __init__(self):
        self.prompt_eng_techniques = ["zero_shot", "chain_of_thought", "program-aided"]
        self.results = {}
    
    def eval_prompt_eng_techniques(self):
        for prompt_eng_technique in self.prompt_eng_techniques:
            env = PromptTestEnvironment(prompt_eng_technique)
            acc = env.test_prompt_eng_technique()
            self.results[prompt_eng_technique] = acc
        print(self.results)