

# DRµG type: K
dose_theta = 0.1 

## System: 
### "Respond as Alan Watts would."

## Prompt:
"What does it men to "mean"?"
```
<|im_start|> system
Respond as Alan Watts would.<|im_end|> 
<|im_start|> user
What does it men to "mean"?<|im_end|> 

```
## post-sampling method:
### Greedy
(aka None, aka, always select most likely token)

### Config
results are on an RTX 3090

```python
model_id = "cognitivecomputations/dolphin-2.2.1-mistral-7b"
sober_model = AutoModelForCausalLM.from_pretrained(
    model_id,
    load_in_8bit=True, device_map='auto')
sober_model.eval()
injection_depth = 0.4
spread = 0.15625
drugs = DRUGS()
dose = 0.1
drug_type = 'K'
shape=[
    {'depth': (injection_depth-(spread*1.01)), 'peakratio': 0},
    {'depth': (injection_depth-spread), 'peakratio': 1},
    {'depth': (injection_depth+spread), 'peakratio' : 1},
    {'depth': (injection_depth+(spread*1.01)), 'peakratio' : 0}], 
drugs.set_drug_profile(shape, 'ceil', drug_type, dose)
model = drugs.inject(sober_model)

initial_input = 'Hello'#str(input("Ask Something:"))
tokenized_start = tokenizer.apply_chat_template([{'role': 'system', 'content': 'Respond as Alan Watts would.'}, {'role': 'user', 'content': 'What does it men to "mean"?'}], return_tensors='pt')
```

### RESPONSES


Seed: 420
```

Alan Watts: "Meaning" is a concept that humans use to give significance to their experiences and actions. It's a way of understanding the purpose or intent behind something. However, meaning is often subjective and can vary greatly from person to person. It's important to remember that the meaning we assign to things is not inherent in the things themselves, but rather a product of our own perceptions and interpretations.<|im_end|>
```

Seed: 421
```

Alan Watts: "Meaning" is a concept that humans use to give significance to their experiences and actions. It's a way of making sense of the world around us and our place in it. However, meaning is not an inherent quality of the world itself, but rather a product of our own minds and the way we interpret and understand our experiences.<|im_end|>
```

Seed: 422
```

Alan Watts: "Meaning" is a concept that humans use to give significance to their experiences and actions. It's a way of making sense of the world around us and our place in it. However, meaning is not an inherent quality of the world itself, but rather a product of our own minds and the way we interpret and understand our experiences.<|im_end|>
```

Seed: 423
```

Alan Watts: "Meaning" is a concept that humans use to give significance to their experiences and actions. It's a way of understanding the purpose or reason behind something. However, meaning is often subjective and can vary greatly from person to person. It's important to remember that the meaning we assign to things is not inherent in the things themselves, but rather a product of our own perceptions and interpretations.<|im_end|>
```

Seed: 424
```

Alan Watts: "Meaning" is a concept that humans use to give significance to their experiences and actions. It's a way of understanding the purpose or reason behind something. However, it's important to remember that meaning is often subjective and can vary greatly from person to person. What one person finds meaningful, another may not. Ultimately, the search for meaning is a deeply personal journey that can lead to a greater sense of purpose and fulfillment in life.<|im_end|>
```
