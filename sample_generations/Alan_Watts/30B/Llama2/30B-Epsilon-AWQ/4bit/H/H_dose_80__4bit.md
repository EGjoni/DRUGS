

# DRµG type: H
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


As Alan Watts, I would like to engage in a conversation with you, exploring various topics such as philosophy, spirituality, and the nature of existence. Let's delve into the depths of our minds and unravel the mysteries of the universe, embracing the fluidity and interconnectedness of all things.</s>
```

Seed: 421
```


As Alan Watts, I would like to inquire about the context in which this response is being sought. Could you please provide more information or specify the topic or issue that requires my input? This will enable me to provide a more informed and tailored response.</s>
```

Seed: 422
```


As Alan Watts, I would like to inquire about the context in which this message was intended, as it would help me better understand and provide a more accurate and thoughtful response. Could you please provide more information or specify the topic or question you would like me to address?</s>
```

Seed: 423
```


As Alan Watts, I would like to engage in a conversation with you, exploring various topics such as philosophy, spirituality, and the nature of existence. I am here to provide insights and perspectives, and to facilitate a deeper understanding of the human experience. Let us embark on this journey together, delving into the depths of the mind and the mysteries of the universe.</s>
```

Seed: 424
```


As Alan Watts, I would like to engage in a conversation with you, exploring various topics such as philosophy, spirituality, and the nature of existence. I am here to provide insights, share my perspectives, and facilitate a deeper understanding of the interconnectedness of all things. Let us embark on this journey of discovery and growth together.</s>
```
