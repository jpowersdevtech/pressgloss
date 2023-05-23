import json
import openai  # for OpenAI API calls
import time  # for measuring time duration of API calls
import os
import re
import random
import pressgloss.core as PRESSGLOSS
import pressgloss.helpers as helpers


class gloss2daide: 
    def __init__(self, input=str, model=None, gloss=None, tones=None): 
        openai.organization = os.getenv('OPENAI_ORG')
        openai.api_key = os.getenv("OPENAI_API_KEY")
        

        if tones is None:
            tones = random.sample(helpers.tonelist, random.randint(1, 3))
        else:
            self.tones = tones
        if gloss == None: 
            utterance = PRESSGLOSS.PressUtterance(None, tones)
            english = ''.join(utterance.frompower) + ' ' + ' '.join(utterance.topowers) + utterance.english
            gloss = [{'role': 'user', 'content': english},
                                    {'role': 'assistant', 'content': utterance.daide}]
        while len(gloss) < 8:
            utterance = PRESSGLOSS.PressUtterance(None, tones)
            english = ''.join(utterance.frompower) + ' ' + ' '.join(utterance.topowers) + utterance.english

            gloss.extend([{'role': 'user', 'content': english},
                                    {'role': 'assistant', 'content': utterance.daide}])
        if model==[]: 
            print('No model specified, using default model')
            model='gpt-3.5-turbo'
         
        self.daide = self.build_chat_complete(gloss, input, model)
    
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
    def __init__(self, training_data=None, data_size=1000):
        openai.organization = os.getenv('OPENAI_ORG')
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.training_list = []
        if training_data is None: 
            self.training_list = self.add_to_training_list(self.training_list, data_size)
            self.training_data = 'training_file'
        else: 
            if type(training_data) == list: 
                self.training_list = training_data
                self.training_data = 'training_file'
                helpers.dicts_to_jsonl(self.training_list, 'training_file')
            else: 
                self.training_data = training_data
        self.model = self.fine_tune_model(self.training_list, data_size)
            
        
    def fine_tune_model(self, training_list, n: int):
        training_list = self.add_to_training_list(training_list, n)
        helpers.dicts_to_jsonl(training_list, self.training_data)
        
        open_ai_feedback_cmd = f'yes | openai tools fine_tunes.prepare_data -f {self.training_data}.jsonl -q'
        tune_create_cmd = f'yes | openai api fine_tunes.create -t "{self.training_data}_prepared_train.jsonl" -v "{self.training_data}_prepared_valid.jsonl" -m curie'
        try:
            feedback = helpers.run_cmd(open_ai_feedback_cmd)
        except Exception as e:
            print(f"Request failed due to {e}, trying again in 5 seconds")
            time.sleep(5)
        if 'error' in str(feedback):
            print('Error in training data.')
            return feedback
        else: 
            print(feedback)
            feedback = helpers.run_cmd(tune_create_cmd)
            model = re.search(r'(?<=create\s-m\s)[a-z\:\-0-9]+', feedback).group(0)
            print(model)
        return model
    def add_to_training_list(self, training_list, amount2add=int):
        if amount2add < 1: 
             return
        i = 0
        while i < amount2add:
            tones = random.sample(helpers.tonelist, random.randint(1, 3))
            utterance = PRESSGLOSS.PressUtterance(None, tones)
            english = ''.join(utterance.frompower) + ' ' + ' '.join(utterance.topowers) + utterance.english
            training_list.append({'prompt': english, "completion": utterance.daide})
            i += 1
        return training_list
    def fine_tune_predict(self, input: str)->str:

        if self.model == None: 
            fine_tune_list = helpers.run_cmd('openai api fine_tunes.list')
            if len(fine_tune_list) < 1:
                 self.fine_tune_model()
        else:
            res = gloss2daide.build_chat_complete(input, model=self.model)
            return res

         
