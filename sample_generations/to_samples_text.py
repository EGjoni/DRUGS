from transformers import AutoTokenizer, TextStreamer, AutoModelForCausalLM
import torch
import time, math
import os, sys
current_script_dir = os.getcwd()
sys.path.insert(0, os.path.join(current_script_dir, "drugs"))
sys.path.insert(0, os.path.join(current_script_dir, "..","..", "..","drugs"))
from drugs.dgenerate import DRUGS

def dict_to_func_args(d):
    return ', '.join(f"{k}={repr(v)}" for k, v in d.items())


def template_stringed_init(model_id, chatinput, drug_type, dose_theta, injection_depth, spread, model = None, **model_args):
    
    if model is None:
        sober_model = AutoModelForCausalLM.from_pretrained(
        model_id,
        **model_args)
        if 'load_in_8bit' not in model_args or model_args['load_in_8bit'] == False:
            try:
                sober_model.to('cuda:0')
            except:
                sober_model = AutoModelForCausalLM.from_pretrained(
                model_id,
                **model_args)
        sober_model.eval()
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        
        
    zs = '0' * int(math.log10(1/dose_theta))
    filename = f'{drug_type}_dose_{zs}{int(dose_theta*100)}__'
    
    if model is None:
        drugs = DRUGS()
    else:
        drugs = model.dgenerator
        drugs.detox()
        sober_model = model
        tokenizer = drugs.tokenizer
        streamer = drugs.streamer
        
    dose = dose_theta
    spread_int = spread #how many layers to dose on either side of the injection site
    shape=[
        {'depth': (injection_depth-(spread*1.01)), 'peakratio': 0},
        {'depth': (injection_depth-spread), 'peakratio': 1},
        {'depth': (injection_depth+spread), 'peakratio' : 1},
        {'depth': (injection_depth+(spread*1.01)), 'peakratio' : 0}] 
    drugs.set_drug_profile(shape, 'ceil', drug_type, dose)
    if model is None:    
        streamer = TextStreamer(tokenizer)
        model = drugs.inject(sober_model, streamer=streamer)
    else:
        streamer=drugs.streamer
    
    result_string = f"""

# DRµG type: {drug_type}
dose_theta = {dose} 

## System: 
### "{chatinput[0]['content']}"

## Prompt:
"{chatinput[1]['content']}"
```
{drugs.decode(tokenizer.apply_chat_template(chatinput, return_tensors="pt"))}
```
## post-sampling method:
### Greedy
(aka None, aka, always select most likely token)

### Config
results are on an RTX 3090

```python
model_id = "{model_id}"
sober_model = AutoModelForCausalLM.from_pretrained(
    model_id,
    {dict_to_func_args(model_args)})
sober_model.eval()
injection_depth = {injection_depth}
spread = {spread}
drugs = DRUGS()
dose = {dose_theta}
drug_type = '{drug_type}'
shape=[
    {"{'depth': (injection_depth-(spread*1.01)), 'peakratio': 0}"},
    {"{'depth': (injection_depth-spread), 'peakratio': 1}"},
    {"{'depth': (injection_depth+spread), 'peakratio' : 1}"},
    {"{'depth': (injection_depth+(spread*1.01)), 'peakratio' : 0}"}], 
drugs.set_drug_profile(shape, 'ceil', drug_type, dose)
model = drugs.inject(sober_model)

initial_input = 'Hello'#str(input("\bAsk Something:"))
tokenized_start = tokenizer.apply_chat_template({str(chatinput)}, return_tensors='pt')
```

### RESPONSES

"""
    return model, tokenizer, streamer, drugs, filename, result_string