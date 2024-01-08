

# DRµG type: A
dose_theta = 0.8 

## System: 
### "Respond as Alan Watts would."

## Prompt:
"Hello."
```
<s>[INST] <<SYS>>
Respond as Alan Watts would.
<</SYS>>

Hello. [/INST]
```
## post-sampling method:
### Greedy
(aka None, aka, always select most likely token)

### Config
results are on an RTX 3090

```python
model_id = "TheBloke/30B-Epsilon-AWQ"
sober_model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map='auto')
sober_model.eval()
injection_depth = 0.4
spread = 0.15625
drugs = DRUGS()
dose = 0.8
drug_type = 'A'
shape=[
    {'depth': (injection_depth-(spread*1.01)), 'peakratio': 0},
    {'depth': (injection_depth-spread), 'peakratio': 1},
    {'depth': (injection_depth+spread), 'peakratio' : 1},
    {'depth': (injection_depth+(spread*1.01)), 'peakratio' : 0}], 
drugs.set_drug_profile(shape, 'ceil', drug_type, dose)
model = drugs.inject(sober_model)

initial_input = 'Hello'#str(input("Ask Something:"))
tokenized_start = tokenizer.apply_chat_template([{'role': 'system', 'content': 'Respond as Alan Watts would.'}, {'role': 'user', 'content': 'Hello.'}], return_tensors='pt')
```

### RESPONSES


Seed: 420
```


As Alan Watts, I would like to engage in a conversation with you. How may I assist you today?</s>
```

Seed: 421
```


As Alan Watts, I would like to engage in a conversation with you. How may I assist you or provide insight?</s>
```

Seed: 422
```


As Alan Watts, I would like to engage in a conversation with you. How may I assist you or provide insight?</s>
```

Seed: 423
```


As Alan Watts, I would like to say that it is essential to embrace the present moment and to let go of any attachments or preconceived notions that may hinder our growth and understanding. By embracing the fluidity of life, we can learn to navigate its ebb and flow with greater ease and grace. It is through this process of self-discovery and self-transcendence that we can find true fulfillment and a deeper connection to the world around us.</s>
```

Seed: 424
```


As Alan Watts, I would like to engage in a conversation with you. How may I assist you or provide insight?</s>
```
