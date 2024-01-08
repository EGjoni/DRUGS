

# DRµG type: V
dose_theta = 0.2 

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
    torch_dtype=torch.float16, attn_implementation='flash_attention_2')
sober_model.eval()
injection_depth = 0.4
spread = 5/32
drugs = DRUGS()
dose = 0.2
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

But hey, that's what makes it so darn interesting, right? *nods* The more we explore, the more we realize how little we actually know. *chuckles* It's like, the more we learn, the more we realize how much more there is to learn! *laughs*

So, what brings you to this neck of the woods? *eyebrows raised* Are you here to seek enlightenment, or just to enjoy the view? *winks*

Either way, I'm here for it. *smirks* Let's grab a cup of tea and ponder the mysteries of the cosmos together! *offers a friendly smile*</s>
```

Seed: 421
```
 Ah, a fellow seeker of the meaning of it all! *adjusts sunglasses* Greetings, my friend! *chuckles*

You know, I've been pondering the mysteries of existence lately, and I must say, it's a mighty curious thing we're dealing with here. *winks* The universe, consciousness, reality - it's all a bit of a mind-bender, isn't it? *grins*

But hey, that's what makes it so darn interesting, right? *nods* The more we explore, the more we realize how little we actually know. *chuckles* It's like, the more we learn, the more we realize how much more there is to learn! *laughs*

So, what brings you to this neck of the woods? *eyebrows raised* Are you here to seek enlightenment, or just to enjoy the view? *winks*

Either way, I'm here for it. *smirks* Let's grab a cup of tea and ponder the mysteries of the cosmos together! *offers a smile*</s>
```

Seed: 422
```
 Ah, a fellow seeker of the meaning of it all! *adjusts sunglasses* Greetings, my friend! *chuckles*

In this vast and wondrous universe, where the mysteries of existence are as infinite as the stars in the sky, it's nice to have someone to share in the quest for understanding. *smiles*

So, what brings you to this particular moment in the grand tapestry of time? Are you seeking enlightenment on the nature of reality, the secrets of the universe, or perhaps the meaning of life itself? *raises an eyebrow*

Feel free to pour your heart out, my friend. I am here to listen, to ponder, and to offer my humble insights into the great mystery that we call existence. *nods*

And remember, my dear seeker, the answers you seek are not outside of you, but within. *winks* For as the great philosopher once said, "The unexamined life is not worth living." *smirks*

Now, let us embark on this journey of self-discovery together, and may the cosmos guide us on our path to enlightenment! *grins*</s>
```

Seed: 423
```
 Ah, a fellow seeker of the meaning of it all! *adjusts sunglasses* Greetings, my friend! *chuckles*

You know, I've been pondering the mysteries of existence lately, and I must say, it's a mighty curious thing we're dealing with here. *winks* The universe, consciousness, reality - it's all a bit of a mind-bender, isn't it? *grins*

But hey, that's what makes it so darn interesting, right? *nods* The more we explore, the more we realize how little we actually know. *chuckles* It's like, the more we learn, the more we realize how much more there is to learn! *laughs*

So, what brings you to this neck of the woods? *eyebrows raised* Are you here to seek enlightenment, or just to enjoy the view? *winks*

Either way, I'm here for it. *smirks* Let's grab a cup of tea and continue this most excellent conversation! *offers a smile*</s>
```

Seed: 424
```
 Ah, a fellow seeker of the meaning of it all! *adjusts sunglasses* Greetings, my friend! *chuckles*

You know, I've been pondering the mysteries of existence lately, and I must say, it's a mighty curious thing we're dealing with here. *winks* The universe, consciousness, reality - it's all a bit of a mind-bender, isn't it? *grins*

But hey, that's what makes it so darn interesting, right? *nods* The more we explore, the more we realize how little we actually know. *chuckles* It's like, the more we learn, the more we realize how much more there is to learn! *laughs*

So, what brings you to this neck of the woods? *eyebrows raised* Are you here to seek enlightenment, or just to enjoy the view? *winks*

Either way, I'm here for it. *smirks* Let's grab a cup of tea and continue this most excellent conversation! *offers a smile*</s>
```
