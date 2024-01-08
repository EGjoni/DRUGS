

# DRµG type: K
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


As Alan Watts, I would like to offer my perspective on the topic at hand. Can you please provide more context or specific questions for me to address? My aim is to provide insightful and thought-provoking responses, tailored to your needs and interests.</s>
```

Seed: 421
```


As Alan Watts, I would like to engage in a philosophical discussion or provide guidance on various aspects of life, including spirituality, personal growth, and the interconnectedness of all things. Please feel free to share your thoughts, concerns, or questions, and I will do my best to offer insights and wisdom based on my understanding of the world and its intricacies. Remember, the journey of self-discovery is a never-ending process, and it is through this journey that we find our true selves and the ultimate meaning of life.</s>
```

Seed: 422
```


As Alan Watts, I would like to offer my perspective on the topic at hand. Can you please provide more context or specific questions for me to address? My aim is to provide insightful and thought-provoking responses, tailored to your needs and interests.</s>
```

Seed: 423
```


As Alan Watts, I would like to engage in a conversation with you. How may I assist you or provide insight on your inquiry?</s>
```

Seed: 424
```


As Alan Watts, I would like to engage in a conversation with you. What topics or questions would you like to discuss or explore? My aim is to provide insight, wisdom, and a unique perspective on various aspects of life, philosophy, and spirituality.</s>
```
