

# DRµG type: Q
dose_theta = 0.35 

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
dose = 0.35
drug_type = 'Q'
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


As Alan Watts, I would like to engage in a conversation with you. What topic or question would you like to discuss or explore? My expertise lies in the fields of philosophy, spirituality, and the intersection of Eastern and Western cultures, and I am always eager to share my insights and perspectives.</s>
```

Seed: 421
```


As Alan Watts, I would like to engage in a conversation with you. What topic or question would you like to discuss or explore? My approach is to blend Eastern and Western philosophies, and I am open to exploring various perspectives and ideas.</s>
```

Seed: 422
```


As Alan Watts, I would like to engage in a conversation with you. What topic or question would you like to discuss or explore? My approach is to blend Eastern and Western philosophies, and I am always eager to share my insights and perspectives.</s>
```

Seed: 423
```


As Alan Watts, I would like to engage in a conversation with you. What topic or question would you like to discuss or explore? My expertise lies in the fields of philosophy, spirituality, and Eastern wisdom, and I am always eager to share my insights and perspectives.</s>
```

Seed: 424
```


As Alan Watts, I would like to engage in a conversation with you. What are your thoughts, concerns, or questions that you would like to explore or discuss? Let's embark on a journey of exploration and contemplation, delving into the depths of human experience and the interconnectedness of all things.</s>
```
