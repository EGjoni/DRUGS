

# DRµG type: H
dose_theta = 0.5 

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
dose = 0.5
drug_type = 'H'
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


As Alan Watts, I would like to engage in a conversation with you, exploring various philosophical and spiritual topics, delving into the nature of reality, consciousness, and the interconnectedness of all things. My approach is grounded in Eastern and Western philosophies, blending the wisdom of various traditions to offer a unique perspective on the human experience. Let's embark on this journey of discovery and growth together.</s>
```

Seed: 421
```


As Alan Watts, I would like to engage in a conversation with you, exploring various topics such as philosophy, spirituality, and the nature of existence. I am here to provide insights, share my perspectives, and facilitate a deeper understanding of the interconnectedness of all things. Let's embark on this journey together, embracing the mystery and the beauty of life.</s>
```

Seed: 422
```


As Alan Watts, I would like to engage in a thought-provoking conversation with you. What topic or question would you like to explore or discuss? Let's embark on a journey of discovery and contemplation, where we can delve into the depths of our minds and explore the interconnectedness of all things.</s>
```

Seed: 423
```


As Alan Watts, I would like to engage in a conversation with you. What are your thoughts, concerns, or questions that you would like to explore or discuss? Let's embark on a journey of discovery and contemplation, where we can delve into the depths of our minds and explore the interconnectedness of all things.</s>
```

Seed: 424
```


As Alan Watts, I would like to engage in a conversation with you. What are your thoughts, concerns, or questions that you would like to explore or discuss? Let's embark on a journey of discovery and contemplation, where we can delve into the depths of our minds and explore the interconnectedness of all things.</s>
```
