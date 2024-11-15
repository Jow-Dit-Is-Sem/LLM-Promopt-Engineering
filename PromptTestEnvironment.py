import csv
import openai

class PromptTestEnvironment:
    def __init__(self, prompt_eng_technique):
        self.prompt_eng_technique = prompt_eng_technique

    def is_solution(self, response, word, letter):
        for item in reversed(response):
            try:
                item_int = int(item)
                if item_int == word.count(letter):
                    return True
                else:
                    return False
            except:
                pass

    def pre_process_response(self, response):
        nums = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
        for index, item in enumerate(response):
            if item in nums:
                num = nums.index(item) + 1
                response[index] = num
        return response

    def prompt_model(self, prompt):
        client = openai.OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="nokeyneeded",
        )

        response = client.chat.completions.create(
            model="phi3:medium",
            temperature=0.7,
            n=1,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
        )
        model_response = response.choices[0].message.content
        return model_response

    def get_prompt(self, row):
        with open(f'Prompts/{self.prompt_eng_technique}_prompt.txt', 'r') as file:
            prompt = file.read()
            if self.prompt_eng_technique == "program-aided":
                prompt = prompt.format(row[1], list(row[0]))
            elif self.prompt_eng_technique == "binairy":
                word_list = list(row[0])
                binary_list = [1 if letter == row[1] else 0 for letter in word_list]
                prompt = prompt.format(row[1], row[0], binary_list)
            else:
                prompt = prompt.format(row[1], row[0])
        return prompt

    def test_prompt_eng_technique(self):
        n_words = 0
        n_correct = 0
        with open('Data/Words.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                n_words += 1
                prompt = self.get_prompt(row)
                print(prompt)
                model_response = self.prompt_model(prompt)
                print(model_response)
                model_response = model_response.split()
                model_response = self.pre_process_response(model_response)
                if self.is_solution(model_response, row[0], row[1]):
                    n_correct += 1
        acc = n_correct / n_words
        return acc