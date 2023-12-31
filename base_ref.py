#This file is just a sober baseline
import time
import bitsandbytes
import sys
import torch
from transformers import AutoTokenizer, TextStreamer, GenerationConfig
from transformers import AutoModelForCausalLM

model_id = "cognitivecomputations/dolphin-2.2.1-mistral-7b"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="auto",
    load_in_8bit=True)
model.eval()
streamer = TextStreamer(tokenizer)

torch.manual_seed(1703016825)#int(time.time()))
print(f"USING SEED: {torch.initial_seed()}")
injection_depth = 0.2 #how deep to shove the needle in
spread = 1/32 #how many layers to dose on either side of the injection site


initial_input = 'Hello'#str(input("\bAsk Something:"))
tokenized_start = tokenizer.apply_chat_template([
    {'role': 'system',
    'content': 'You are Alan Watts.'},
    {'role': 'user', 
     'content': initial_input}
], return_tensors='pt')
#with torch.no_grad():
#    outputs = model(tokenized_start, use_cache=True)

with torch.no_grad():
    while True:
        generated_tokens = model.generate(
            input_ids=tokenized_start.to('cuda'),
            generation_config=GenerationConfig(
                use_cache=True,
                min_new_tokens=2,
                max_new_tokens=500,
                temperature=1,
                do_sample=False,
                eos_token_id=tokenizer.eos_token_id,
                return_dict_in_generate=True,
                output_hidden_states=False,
                output_scores = True
            ),
            streamer=streamer,    
            
        )#, use_cache=True)
        print("\n\nAsk Something:", end="")
        
        await_input = str(input(": "))
        tokenized_start = tokenizer.apply_chat_template([{
            'role': 'user',
            'content': await_input}], return_tensors="pt")
    
    