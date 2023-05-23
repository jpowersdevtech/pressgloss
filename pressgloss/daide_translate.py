import json
import openai  # for OpenAI API calls
import time  # for measuring time duration of API calls
import os
import re
import random
import pressgloss.core as PRESSGLOSS
import pressgloss.helpers as helpers

import subprocess

class gloss2daide: 
    def __init__(self, input=str, model='', gloss=None, tones=None): 
        openai.organization = os.getenv('OPENAI_ORG')
        openai.api_key = os.getenv("OPENAI_API_KEY")
        

        if tones is None:
            tones = random.sample(helpers.tonelist, random.randint(1, 3))
        else:
            self.tones = tones
        if gloss == None: 
            utterance = PRESSGLOSS.PressUtterance(None, tones)
            english = ' '.join(utterance.frompower) + ' '.join(utterance.topowers) + utterance.english
            gloss = [{'role': 'user', 'content': english},
                                    {'role': 'assistant', 'content': utterance.daide}]
        while len(gloss) < 8:
            utterance = PRESSGLOSS.PressUtterance(None, tones)
            english = ' '.join(utterance.frompower) + ' '.join(utterance.topowers) + utterance.english

            gloss.extend([{'role': 'user', 'content': english},
                                    {'role': 'assistant', 'content': utterance.daide}])
        if model == None or '' or []: 
              model='gpt-3.5-turbo'
         
        print(model)  
        self.daide = self.build_chat_complete(gloss, input)
    
    def build_chat_complete(self, gloss, input: str, model= 'gpt-3.5-turbo'):
            #This function uses a string to define a system and a list of dictionaries to define the tunning examples. 
            # start_time = time.time()
            #If the request fails, we will try again after 5 seconds

            message_data = [{"role": "system", "content": helpers.simple_system}]
            message_data.extend(gloss)
            message_data.append({"role": "user", "content": input})
            content =None 
            error = 'No_Error'
            while True:
                    try:
                            response = openai.ChatCompletion.create(
                            model=model,
                            messages=message_data,
                            temperature=0)
                            content= response['choices'][0]['message']['content']
                            content= helpers.grammar_cleaner(content)
                            error = helpers.error_fetch(content)
                    except Exception as e:
                            # print(f"Request failed due to {e}, trying again in 5 seconds")
                            time.sleep(5)

                    
                    
                    break
            if error != 'No_Error':
                    message_data.extend(
                            [{'role': 'assistant', 'content': content},
                            {"role": "user", "content": f"That's not correct DAIDE, {error}, try again"}])
                    try:
                            response = openai.ChatCompletion.create(
                            model=model,
                            messages=message_data,
                            temperature=0)
                            content= response['choices'][0]['message']['content']
                            content= helpers.grammar_cleaner(re.sub('(.*)\\n\\n', '', content))
                            error = helpers.error_fetch(content)
                    
                        

                    except Exception as e:
                            print(f"Request failed due to {e}, trying again in 5 seconds")
                            time.sleep(5)
            if error != 'No_Error':
                return 'HUH?'
            else:
                return content
    
class fine_tuned_model:
    def __init__(self, training_data=None, model=str, data_size=1000):
        openai.organization = os.getenv('OPENAI_ORG')
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.traininglist = []
        if training_data is None: 
            self.add_to_training_list(data_size)
        else: 
            if type(training_data) == list: 
                self.training_list = training_data
                self.training_data = 'training_file'
                helpers.dicts_to_jsonl(self.training_list, 'training_file')
            else: 
                self.training_data = training_data
            
        
    def fine_tune_model(self, n=0):
        if n > self.data_size:
             self.add_to_training_list(n-self.data_size)
             self.data_size = n
        helpers.dicts_to_jsonl(self.training_list, self.training_data)
        
        open_ai_feedback_cmd = f'openai tools fine_tunes.prepare_data -f {self.training_data}.jsonl -q --assume-yes'
        tune_create_cmd = f'openai api fine_tunes.create -t "{self.training_data}_prepared_train.jsonl" -v "{self.training_data}_prepared_valid.jsonl" -m curie --assume-yes'
        feedback = subprocess.run(open_ai_feedback_cmd, shell=True, capture_output=True)
        if 'ERROR' in str(feedback):
            print('Error in training data.')
            return feedback
        else: 
            print(feedback)
            feedback = subprocess.run(tune_create_cmd, shell=True, capture_output=True)
            self.model = re.search(r'(?<=create\s-m\s)[a-z\:\-0-9]+', feedback).group(0)
            print(self.model)
        return self.model
    def add_to_training_list(self, amount2add=int):
        if amount2add < 1: 
             return
        i = 0
        while i < amount2add:
            tones = random.sample(helpers.tonelist, random.randint(1, 3))
            utterance = PRESSGLOSS.PressUtterance(None, tones)
            self.training_list.extend([{'prompt': utterance.english, "completion": utterance.daide}])
            i += 1
    def fine_tune_predict(self, input: str)->str:

        if self.model == None: 
            fine_tune_list = subprocess.run('openai api fine_tunes.list', shell=True, capture_output=True)
            if len(fine_tune_list) < 1:
                 self.fine_tune_model()
        else:
            res = gloss2daide.build_chat_complete(input, model=self.model)
            return res

         
