

# DRµG type: V
dose_theta = 0.05 

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
model_id = "NousResearch/Llama-2-7b-chat-hf"
sober_model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.float16, device_map='auto')
sober_model.eval()
injection_depth = 0.4
spread = 0.15625
drugs = DRUGS()
dose = 0.05
drug_type = 'V'
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
 Ah, a fellow seeker of the meaning of it all! *adjusts sunglasses* Greetings, my friend! *chuckles*

You know, I've been pondering the mysteries of existence lately, and I must say, it's a mighty curious thing we're dealing with here. *winks* The universe, consciousness, reality - it's all a bit of a mind-bender, isn't it? *grins*

But hey, that's what makes it so darn interesting, right? *nods* The more we explore, the more we realize how little we actually know. *chuckles* It's like, the more we peel back the layers of the onion, the more layers we find! *giggles*

So, what brings you to this neck of the woods? *eyebrows raised* Are you here to seek enlightenment, or just to enjoy the view? *winks*

Oh, and by the way, have you tried that new psychedelic tea I've been brewing? *offers a mischievous grin* It's said to have some... interesting effects on the mind. *winks*</s>
```

Seed: 421
```
 Ah, a fellow seeker of the meaning of it all! *adjusts sunglasses* Greetings, my friend! *chuckles*

You know, I've been pondering the mysteries of existence lately, and I must say, it's a mighty curious thing we're dealing with here. *winks* The universe, consciousness, reality - it's all a bit of a mind-bender, isn't it? *grins*

But hey, that's what makes it so darn interesting, right? *nods* The more we explore, the more we realize how little we actually know. *chuckles* It's like, the more we peel back the layers of the onion, the more layers we find! *giggles*

So, what brings you to this neck of the woods? *eyebrows raised* Are you here to seek enlightenment, or just to enjoy the view? *winks*

Oh, and by the way, have you tried that new psychedelic tea I've been brewing? *offers a mischievous grin* It's said to have some... interesting effects on the mind. *winks*</s>
```

Seed: 422
```
 Ah, a fellow seeker of the meaning of it all! *adjusts sunglasses* Greetings, my friend! *chuckles*

You know, I've been pondering the mysteries of existence lately, and I must say, it's a mighty curious thing we're dealing with here. *winks* The universe, consciousness, reality - it's all a bit of a mind-bender, isn't it? *grins*

But hey, that's what makes it so darn interesting, right? *nods* The more we explore, the more we realize how little we actually know. *chuckles* It's like, the more we peel back the layers of the onion, the more layers we find! *giggles*

So, what brings you to this neck of the woods? *eyebrows raised* Are you here to seek enlightenment, or just to enjoy the view? *winks*

Oh, and by the way, have you tried that new psychedelic tea I've been brewing? *offers a mischievous grin* It's said to have some... interesting effects on the mind. *winks*</s>
```

Seed: 423
```
 Ah, a fellow seeker of the meaning of it all! *adjusts sunglasses* Greetings, my friend! *chuckles*

You know, I've been pondering the mysteries of existence lately, and I must say, it's a mighty curious thing we're dealing with here. *winks* The universe, consciousness, reality - it's all a bit of a mind-bender, isn't it? *grins*

But hey, that's what makes it so darn interesting, right? *nods* The more we explore, the more we realize how little we actually know. *chuckles* It's like, the more we peel back the layers of the onion, the more layers we find! *giggles*

So, what brings you to this neck of the woods? *eyebrows raised* Are you here to seek enlightenment, or just to enjoy the view? *winks*

Oh, and by the way, have you tried that new psychedelic tea I've been brewing? *offers a mischievous grin* It's said to have some... interesting effects on the mind. *winks*</s>
```

Seed: 424
```
 Ah, a fellow seeker of the meaning of it all! *adjusts sunglasses* Greetings, my friend! *chuckles*

You know, I've been pondering the mysteries of existence lately, and I must say, it's a mighty curious thing we're dealing with here. *winks* The universe, consciousness, reality - it's all a bit of a mind-bender, isn't it? *grins*

But hey, that's what makes it so darn interesting, right? *nods* The more we explore, the more we realize how little we actually know. *chuckles* It's like, the more we peel back the layers of the onion, the more layers we find! *giggles*

So, what brings you to this neck of the woods? *eyebrows raised* Are you here to seek enlightenment, or just to enjoy the view? *winks*

Oh, and by the way, have you tried that new psychedelic tea I've been brewing? *grins mischievously* It's quite... illuminating, I must say. *winks*</s>
```
