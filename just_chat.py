import time
import bitsandbytes #not strictly necessary, used for 8bit inference
import sys
from drugs.nice_imports import efficiency_stuff
import torch
from transformers import AutoTokenizer, TextStreamer, AutoModelForCausalLM
from drugs.dgenerate import DRUGS

#model_id = "NousResearch/Llama-2-7b-chat-hf"
model_id = "cognitivecomputations/dolphin-2.2.1-mistral-7b"
tokenizer = AutoTokenizer.from_pretrained(model_id)
sober_model = AutoModelForCausalLM.from_pretrained(
    model_id,
    **efficiency_stuff)
sober_model.eval()
streamer = TextStreamer(tokenizer)

injection_depth = 0.4 #how deep to shove the needle in
spread = 5/32 #how many layers to dose on either side of the injection site

drugs = DRUGS()
drugs.set_A_dose_theta(0.5)
drugs.set_A_dose_shape([
    {'depth': (injection_depth-(spread*1.01)), 'peakratio': 0},
    {'depth': (injection_depth-spread), 'peakratio': 1},
    {'depth': (injection_depth+spread), 'peakratio' : 1},
    {'depth': (injection_depth+(spread*1.01)), 'peakratio' : 0}], 
'ceil')
model = drugs.inject(sober_model)

initial_input = 'Hello'#str(input("\bAsk Something:"))
tokenized_start = tokenizer.apply_chat_template([
    {'role': 'system',
    'content': 'Respond as Alan Watts would.'},
    {'role': 'user', 
     'content': initial_input}
], return_tensors='pt')
#torch.manual_seed(1703016825)
with torch.no_grad():
    while True:
        generated_tokens = model.Dgenerate(
                    input_ids = tokenized_start,
                    min_new_tokens = 5,
                    streamer = streamer, 
                )
        print("\n\nAsk Something:", end="")
        model.cold_shower(True)
        await_input = str(input(" "))
        tokenized_start = tokenizer.apply_chat_template([{
            'role': 'user',
            'content': await_input}], return_tensors="pt")
    
    
