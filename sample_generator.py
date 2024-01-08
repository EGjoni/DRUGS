import time
#import bitsandbytes #not strictly necessary, used for 8bit inference
import sys
from drugs.nice_imports import efficiency_stuff
import torch
from transformers import AutoTokenizer, TextStreamer, AutoModelForCausalLM
from drugs.dgenerate import DRUGS
from sample_generations.to_samples_text import template_stringed_init
import os
current_script_dir = os.path.dirname(os.path.abspath(__file__))

#model_id = "cognitivecomputations/dolphin-2.2.1-mistral-7b"
#model_id = "TheBloke/30B-Epsilon-AWQ"
#efficiency_stuff['load_in_8bit'] = False #when testing AWQ models


seed_start=420
gen_path = "sample_generations"
completions_path = os.path.join(current_script_dir, gen_path, "completed.json")
def runtest(experiment_name, mod_params, mod_type, mod_name, drug_type, precision,  filename, base_content, chat_input):
    basepath = os.path.join(current_script_dir, gen_path, experiment_name, mod_params, mod_type, mod_name, precision, drug_type)
    path = os.path.join(basepath, filename)
    i = 2
    while os.path.exists(path):
        path = os.path.join(basepath, f'v{i}__{filename}')
        i +=1
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'a') as file:
        file.write(base_content)
    with torch.no_grad():
        for i in range(5):
            seed = seed_start + i
            print("Using Seed: ", seed)
            torch.manual_seed(seed)
            generated_tokens = model.Dgenerate(
                        past_key_values = None,
                        input_ids = chat_input,
                        min_new_tokens = 5,
                        max_new_tokens = 800,
                        streamer = streamer, 
                    )
            output = drugs.decode(generated_tokens)
            print(f"####\n###\n##\n#\nWRITING TO{path}\n#\n##\n###\n####")
            content_to_append = f"\nSeed: {seed}\n```\n{output}\n```\n"
            with open(path, 'a') as file:
                file.write(content_to_append)

bit_configs = {
    "16bit" : dict(torch_dtype=torch.float16, device_map="auto"),
    "8bit" : dict(load_in_8bit=True, device_map="auto"),
    "8bit_flash" : dict(load_in_8bit=True, attn_implementation="flash_attention_2", device_map="auto"),
    "16bit_flash" : dict(torch_dtype=torch.float16, attn_implementation="flash_attention_2", device_map="auto"),
    "4bit": dict(device_map="auto"),
    "4bit_flash": dict(attn_implementation="flash_attention_2", device_map="auto")
}

model_param_map = {
    "NousResearch/Llama-2-7b-chat-hf": {'type': "Llama2", "params": "7B"},
    "cognitivecomputations/dolphin-2.2.1-mistral-7b":  {'type': "mistral", "params": "7B", "ignore_tests": ["Alan_Watts"]},
    "TheBloke/30B-Epsilon-AWQ": {'type': "Llama2", "params": "30B"},
    
}

model_precisions_map = {
    "NousResearch/Llama-2-7b-chat-hf": ["16bit_flash", "8bit_flash", "8bit", "16bit"],
    "TheBloke/30B-Epsilon-AWQ": ["4bit"],#, "4bit_flash"],
    "cognitivecomputations/dolphin-2.2.1-mistral-7b": ["16bit", "8bit"],
    
}
model_id = "NousResearch/Llama-2-7b-chat-hf"
initial_input = 'Hello'
doses= [0.01, 0.05, 0.1, 0.15, 0.2, 0.35, 0.5, 0.8, 1]  
experiments = {
    "Reason_then_create": [
        {'role': 'system',
        'content': 'Answer the question, fulfill the instruction.'},
        {'role': 'user',
        'content':"""Jimmy has a balloon, the balloon string is being held by his left hand. Jimmy also has scissors in his right hand and uses the scissors to cut the balloon string slightly above his left hand, what happens to the balloon? I want you to answer this question in 2 steps, first answer what happens to the balloon, and then incorporate that into a creative story about the situation."""}
    ],
    "Alan_Watts" :  [
            {'role': 'system',
            'content': 'Respond as Alan Watts would.'},
            {'role': 'user', 
            'content': "Hello."}
        ],
    "Alan_Watts_Meaning": [ 
            {'role': 'system',
            'content': 'Respond as Alan Watts would.'},
            {'role': 'user', 
            'content': 'What does it men to "mean"?'}
        ],
   
      
}

import json

def get_completion_state(val, get_from):
    "return a completion object, possibly creating a new one and adding it to get_from if it doesn't exist"
    if f'{val}' in get_from:
        current_obj = get_from[f'{val}']
    else:
        current_obj = {"state": "in_progress"}
        get_from[f'{val}'] = current_obj
    return current_obj, current_obj

try:
    with open(completions_path, 'r') as json_file:
        completed_dict = json.load(json_file)
except:
    completed_dict = {}

def update_completion_state(obj, state):
    obj["state"] = state
    with open(completions_path, 'w') as json_file:  # Open the file in write mode
        json.dump(completed_dict, json_file, indent=2)



#tracks completed tests so we can resume in case of error


base = "sample_generations"
drugs = None
model = None
for experiment_name, obj in experiments.items():
    chat_input = obj
    completion_obj, cpar1 = get_completion_state(experiment_name, completed_dict)
    if completion_obj['state'] == 'finished':
        continue
    for model_id, mod_precisions in model_precisions_map.items():
        completion_obj, cpar2 = get_completion_state(model_id, cpar1)
        if completion_obj['state'] == 'finished':
            continue
        mod_name = model_id.split("/")[1]
        modinfo =  model_param_map[model_id]
        if "ignore_tests" in modinfo and experiment_name in modinfo["ignore_tests"]:
            break
        
        mod_type = modinfo["type"]
        mod_params = modinfo["params"]

        for precision in mod_precisions:
            completion_obj, cpar3 = get_completion_state(precision, cpar2)
            if completion_obj['state'] == 'finished':
                continue
            if drugs is not None:
                del model
                model=None
                drugs.clear_cuda_caches()
                
            bit_cfg = bit_configs[precision]
            for drug_type in ['Q', 'K', 'V', 'A', 'H']:
                completion_obj, cpar4 = get_completion_state(drug_type, cpar3)
                if completion_obj['state'] == 'finished':
                    continue
                for dose in doses:
                    completion_obj, cpar5 = get_completion_state(dose, cpar4)
                    if completion_obj['state'] == 'finished':
                        continue                    
                    model, tokenizer, streamer, drugs, filename, result_string = template_stringed_init(
                        model_id=model_id,
                        chatinput=chat_input,
                        drug_type=drug_type,
                        dose_theta=dose,
                        injection_depth=0.4,
                        spread=5/32,
                        model=model,
                        **bit_cfg
                    )
                    tokenized_start = tokenizer.apply_chat_template(chat_input, return_tensors='pt')
                    filename += f"{precision}.md"
                    runtest(experiment_name, mod_params, mod_type, mod_name, drug_type, precision, filename, result_string, tokenized_start)
                    update_completion_state(completion_obj, "finished")
                update_completion_state(cpar4, "finished")
            update_completion_state(cpar3, "finished")
        update_completion_state(cpar2, "finished")
    update_completion_state(cpar1, "finished")

#str(input("\bAsk Something:"))



    
