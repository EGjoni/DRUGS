

# DRµG type: Q
dose_theta = 1 

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
dose = 1
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


As Alan Watts, I would like to engage in a philosophical discussion or share my insights on various topics, including Eastern and Western spirituality, the nature of reality, and the interconnectedness of all things. Let's explore the depths of our understanding and delve into the mysteries of existence, unraveling the intricate web of life and its underlying principles.</s>
```

Seed: 421
```


As Alan Watts, I would like to engage in a philosophical discussion or provide insights on various topics, including Eastern and Western philosophies, comparative religion, and the nature of reality. Please feel free to pose any questions or topics you would like to explore, and I will do my best to provide thought-provoking and enlightening responses.</s>
```

Seed: 422
```


As Alan Watts, I would like to engage in a philosophical discussion or provide insights on various topics, including Eastern and Western philosophies, comparative religion, and the nature of consciousness and reality. How may I assist you in your quest for knowledge and understanding?</s>
```

Seed: 423
```


As Alan Watts, I would like to engage in a conversation with you. How may I assist you today?</s>
```

Seed: 424
```


As Alan Watts, I would like to say that I am here to assist you in any way that I can. Please feel free to share your thoughts, concerns, or questions, and I will do my best to provide insightful and thoughtful responses. Remember, life is a journey, and it's the journey that matters, not the destination. Let's explore and discover together.</s>
```
