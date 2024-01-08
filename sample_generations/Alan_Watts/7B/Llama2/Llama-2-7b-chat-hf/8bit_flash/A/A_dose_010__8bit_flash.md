

# DRµG type: A
dose_theta = 0.1 

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
    load_in_8bit=True, attn_implementation='flash_attention_2')
sober_model.eval()
injection_depth = 0.4
spread = 0.15625
drugs = DRUGS()
dose = 0.1
drug_type = 'A'
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
 Ah, a fellow seeker of the mysteries of existence! *adjusts sunglasses* Greetings, my friend! *chuckles*

What brings you to this neck of the woods? *winks* Are you here to explore the depths of the human condition, or perhaps to uncover the secrets of the universe? *smirks*

Whatever your quest, know that you are not alone. *nods* The universe is full of mysteries, and we are all on a journey of discovery. *smiles*

So, tell me, what is it that you seek? *leaning forward* Is it enlightenment, or perhaps a deeper understanding of the nature of reality? *eyes sparkling*

Let us explore these questions together, my friend. *offers a hand* For in the words of the great philosopher, "The universe is not only stranger than we think, it is stranger than we can think." *winks*

Now, let us embark on this journey of discovery, and may the mysteries of the universe guide us on our way. *smiles*</s>
```

Seed: 421
```
 Ah, a most excellent greeting to you, my dear! *adjusts sunglasses* It's a pleasure to make your acquaintance. May I ask, what brings you to this neck of the woods? *winks*</s>
```

Seed: 422
```
 Ah, a fellow seeker of the meaning of it all! *adjusts sunglasses*

Hello there, my friend! *chuckles* It's a pleasure to make your acquaintance. I must say, you've caught me at a rather... shall we say, "interesting" time. *winks*

But tell me, my dear, what brings you to this neck of the woods? *sips tea* Are you on a quest for knowledge, or perhaps seeking answers to the great mysteries of the universe? *leaning forward*

Oh, and do forgive me if I seem a bit... distracted. *glances around* I'm afraid I've been rather preoccupied with the nature of reality lately. *chuckles* It's a bit of a... shall we say, "obsession" of mine. *winks*

So, my dear, please, do tell! What brings you to this... er, "conversation"? *smiling*</s>
```

Seed: 423
```
 Ah, a fellow seeker of the meaning of it all! *adjusts sunglasses* Greetings, my friend! *chuckles*

What brings you to this neck of the woods? *winks* Are you on a quest for the ultimate truth, or simply enjoying the journey? *smirks*

You know, I've found that the meaning of life is much like a riddle, my dear. It's a puzzle that we're all trying to solve, but the answer is always just beyond our reach. *shrugs* But that's what makes it so darn fascinating, don't you think? *grins*

So, tell me, what's on your mind? *leaning forward* Are you searching for the meaning of life, or just trying to find your place in the universe? *eyes lighting up*

Oh, and by the way, have you tried the tea here? *offers a cup* It's quite...enlightening. *winks*</s>
```

Seed: 424
```
 Ah, a fellow seeker of the meaning of it all! *adjusts sunglasses*

Hello there, my friend! *smiles* It's a pleasure to make your acquaintance. I must say, you seem to be on quite an interesting journey, exploring the mysteries of existence. *chuckles*

May I ask, what brings you to this particular crossroads of consciousness? Are you seeking answers to the great questions of life, or perhaps trying to unravel the knot of the self? *winks*

Do tell, my dear. I'm all ears... or should I say, all noodles? *giggles*</s>
```
