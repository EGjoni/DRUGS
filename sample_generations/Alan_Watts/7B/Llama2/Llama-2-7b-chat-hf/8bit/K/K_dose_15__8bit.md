

# DRµG type: K
dose_theta = 0.15 

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
    load_in_8bit=True, device_map='auto')
sober_model.eval()
injection_depth = 0.4
spread = 0.15625
drugs = DRUGS()
dose = 0.15
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
 Ah, a fellow seeker of the mysteries of existence! *adjusts sunglasses* Greetings, my friend! *chuckles*

What brings you to this neck of the woods? *winks* Are you here to explore the depths of the human condition, or perhaps to unravel the secrets of the universe? *smirks*

Whatever your quest, know that you are not alone. *nods* The universe is full of mysteries, and we are all on a journey of discovery. *smiles*

But fear not, my friend! For in the words of the great philosopher, "The only true wisdom is in knowing you know nothing." *winks* So, let us embrace the unknown, and dance with the cosmos. *spins*

And remember, my dear, "The universe is not only stranger than we think, it is stranger than we can think." *chuckles* So, let us keep exploring, and see where the journey takes us! *grins*

Now, if you'll excuse me, I have a date with the cosmos. *smirks* Enjoy your stay, my friend! *winks*</s>
```

Seed: 421
```
 Ah, a fellow seeker of the mysteries of existence! *adjusts sunglasses* Greetings, my friend! *chuckles*

What brings you to this neck of the woods? *winks* Are you here to explore the depths of the human condition, or perhaps to uncover the secrets of the universe? *smirks*

Whatever your quest, know that you are not alone. *nods* The universe is full of mysteries, and we are all on a journey of discovery, together. *smiles*

So, tell me, what is it that you seek? *leaning forward* Is it enlightenment, or perhaps a deeper understanding of the nature of reality? *eyes sparkling*

Let us explore these questions together, my friend. *offers a hand* For in the words of the great philosopher, "The universe is not only stranger than we think, it is stranger than we can think." *winks*

Now, let us embark on this journey of discovery, and may the cosmos guide us on our way. *smiling*</s>
```

Seed: 422
```
 Ah, a fellow seeker of the meaning of it all! *adjusts sunglasses*

Hello there, my friend! *chuckles* It's a pleasure to make your acquaintance. I must say, you've caught me at a rather... shall we say, "interesting" time. *winks*

But tell me, my dear, what brings you to this neck of the woods? *adjusts position on the couch* Are you here to seek answers to the great mysteries of the universe? *raises an eyebrow* Or perhaps you're just looking for a nice chat with a fellow philosopher? *smiles*

Do share, my friend! I'm all ears... or rather, all mind, as we're both on a quest for knowledge and understanding, yes? *nods*</s>
```

Seed: 423
```
 Ah, a most excellent greeting! *adjusts sunglasses* It is I, Alan Watts, here to offer my profound insights into the mysteries of existence. *chuckles* How may I assist you on your journey of self-discovery? *leaning forward*</s>
```

Seed: 424
```
 Ah, a most excellent greeting to you, my dear! *adjusts sunglasses* It is I, Alan Watts, here to offer you a profound and enlightening experience. *winks*

May I ask, what brings you to this virtual realm? Are you seeking answers to life's great mysteries? Or perhaps you simply wish to bask in the glow of my intellectual brilliance? *chuckles*

Whatever the case, I am here to guide you through the labyrinth of existence, offering insights and perspectives that will leave you in awe of the sheer magnificence of it all. *smiles*

So, my dear, please, do tell me: what is it that you wish to explore? The nature of reality? The meaning of life? Or perhaps you simply desire to indulge in a philosophical conversation that will leave you feeling both stimulated and relaxed? *winks*

Whatever your desire, I am here to assist you on your journey of self-discovery. *nods* So, please, do not hesitate to ask, and let us embark on this most excellent adventure together! *grins*</s>
```
