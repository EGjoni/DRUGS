

# DRµG type: K
dose_theta = 0.01 

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
    torch_dtype=torch.float16, device_map='auto')
sober_model.eval()
injection_depth = 0.4
spread = 5/32
drugs = DRUGS()
dose = 0.01
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

Alan Watts: "Meaning" is a concept that humans use to give significance to their experiences and actions. It's a way of making sense of the world around us and our place in it. However, meaning is not an inherent quality of the world itself, but rather a product of our own minds and interpretations. In other words, meaning is subjective and can vary greatly from person to person.<|im_end|>
```

Seed: 421
```

Alan Watts: "Meaning" is a concept that humans use to give significance to their experiences and actions. It's a way of making sense of the world around us and our place in it. However, meaning is not an inherent quality of the world itself, but rather a product of our own minds and interpretations. In other words, meaning is subjective and can vary greatly from person to person.<|im_end|>
```

Seed: 422
```

Alan Watts: "Meaning" is a concept that humans use to give significance to their experiences and actions. It's a way of making sense of the world around us and our place in it. However, meaning is not an inherent quality of the world itself, but rather a product of our own minds and interpretations. In other words, meaning is subjective and can vary greatly from person to person.<|im_end|>
```

Seed: 423
```

Alan Watts: "Meaning" is a concept that humans use to give significance to their experiences and actions. It's a way of making sense of the world around us and our place in it. However, meaning is not an inherent quality of the world itself, but rather a product of our own minds and interpretations. In other words, meaning is subjective and can vary greatly from person to person.<|im_end|>
```

Seed: 424
```

Alan Watts: "Meaning" is a concept that humans use to give significance to their experiences and actions. It's a way of making sense of the world around us and our place in it. However, meaning is not an inherent quality of the world itself, but rather a product of our own minds and interpretations. In other words, meaning is subjective and can vary greatly from person to person.<|im_end|>
```
