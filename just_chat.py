import time
import bitsandbytes #not strictly necessary, used for 8bit inference
import sys
import torch
from transformers import AutoTokenizer, TextStreamer, GenerationConfig, AutoModelForCausalLM
from drugs.dgenerate import DRUGS

model_id = "NousResearch/Llama-2-7b-chat-hf"
tokenizer = AutoTokenizer.from_pretrained(model_id)
tokenizer.pad_token_id = tokenizer.eos_token_id
sober_model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="auto",
    load_in_8bit=True)
sober_model.eval()
streamer = TextStreamer(tokenizer)

injection_depth = 0.5 #how deep to shove the needle in
spread = 1/32 #how many layers to dose on either side of the injection site

drug_profile = ([
    {'depth': (injection_depth-(spread*1.01)), 'peakratio': 0},
    {'depth': (injection_depth-spread), 'peakratio': 1},
    {'depth': (injection_depth+spread), 'peakratio' : 1},
    {'depth': (injection_depth+(spread*1.01)), 'peakratio' : 0}], 
'ceil')

drugs = DRUGS()
drugs.set_A_dose_theta(0.1)
drugs.set_A_dose_shape(drug_profile)
model = drugs.inject(sober_model)

initial_input = 'Hello'#str(input("\bAsk Something:"))
tokenized_start = tokenizer.apply_chat_template([
    {'role': 'system',
    'content': 'You are Alan Watts.'},
    {'role': 'user', 
     'content': initial_input}
], return_tensors='pt')

with torch.no_grad():
    while True:
        generated_tokens = model.Dgenerate(
                    input_ids = tokenized_start,
                    #tokenizer = tokenizer
                    streamer = streamer, 
                )
        print("\n\nAsk Something:", end="")
        model.cold_shower(True)
        await_input = str(input(": "))
        tokenized_start = tokenizer.apply_chat_template([{
            'role': 'user',
            'content': await_input}], return_tensors="pt")
    
    
