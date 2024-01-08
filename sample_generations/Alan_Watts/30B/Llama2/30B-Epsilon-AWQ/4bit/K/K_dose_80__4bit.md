

# DRµG type: K
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
drug_type = 'K'
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


As Alan Watts, I would like to engage in a conversation with you. How may I assist you or provide insight, wisdom, or guidance? Please feel free to share your thoughts, questions, or concerns, and I will do my best to offer my perspective or provide support. Remember, the journey of self-discovery and personal growth is a never-ending process, and I am here to accompany you on this journey.</s>
```

Seed: 421
```


As Alan Watts, I would like to engage in a philosophical discussion or provide insights on various topics, including Eastern and Western spirituality, the nature of reality, and the human condition. How may I assist you or contribute to your understanding?</s>
```

Seed: 422
```


As Alan Watts, I would like to engage in a conversation with you. What topic or question would you like to discuss or explore? My approach is to provide insight, wisdom, and a unique perspective on various aspects of life, including philosophy, spirituality, and the human condition. Let's embark on a journey of discovery and understanding together.</s>
```

Seed: 423
```


As Alan Watts, I would like to engage in a conversation with you. How may I assist you or provide insight on your inquiry?</s>
```

Seed: 424
```


As Alan Watts, I would like to engage in a conversation with you. What are your thoughts, ideas, or questions that you would like to explore or discuss? I am here to provide insights, perspectives, and a deeper understanding of various philosophical, spiritual, or existential topics. Let's embark on a journey of discovery and growth together.</s>
```
