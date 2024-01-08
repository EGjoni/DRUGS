

# DRµG type: Q
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
    load_in_8bit=True, attn_implementation='flash_attention_2')
sober_model.eval()
injection_depth = 0.4
spread = 5/32
drugs = DRUGS()
dose = 0.15
drug_type = 'Q'
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
 Ah, a fellow seeker of the meaning of it all! *adjusts sunglasses*

Hello there, my friend! *smiles* It's a pleasure to make your acquaintance. I must say, you seem to be asking some rather profound questions. *leaning back*

May I ask, what is it that you're hoping to find? *eyes sparkling* Is it the answer to the ultimate question of existence? *winks* Or perhaps you're searching for a deeper understanding of the nature of reality itself? *intrigued*

Whatever it may be, know that you're not alone in your quest. *nodding* The search for meaning is a lifelong journey, and one that can lead to some most interesting and unexpected places. *smiling slyly*

So, tell me, my friend, what is it that you desire to know? *leaning forward* The universe is full of mysteries, and I for one am eager to uncover them all. *excitedly*</s>
```

Seed: 421
```
 Ah, a most excellent greeting to you, my dear! *adjusts sunglasses* It's a pleasure to make your acquaintance. May I ask, what brings you to this neck of the woods? *winks*</s>
```

Seed: 422
```
 Ah, a fellow seeker of the meaning of it all! *adjusts sunglasses* Greetings, my friend! *chuckles*

What brings you to this neck of the woods? *winks* Are you here to explore the mysteries of the universe? *nods* Or perhaps you're simply looking for a new perspective on the nature of reality? *smirks*

Whatever the case, I'm here to help you unravel the knots of existence. *offers a sly smile* So, my dear, what's on your mind? *leaning in*</s>
```

Seed: 423
```
 Ah, a fellow seeker of the mysteries of existence! *adjusts sunglasses* Greetings, my friend! *chuckles*

What brings you to this neck of the woods? *winks* Are you here to explore the depths of the human condition, or perhaps to uncover the secrets of the universe? *smirks*

Whatever your quest, know that you are not alone. *nods* The universe is full of mysteries, and we are all on a journey of discovery. *smiles*

So, tell me, what is it that you seek? *leaning forward* Is it the meaning of life, the nature of reality, or perhaps the secret to happiness? *curious*

Let us explore these questions together, my friend. *offers a hand* For in the words of the great philosopher, "The universe is not only stranger than we think, it is stranger than we can think." *winks*

Now, let us embark on this journey of discovery, and may the mysteries of existence lead us to a deeper understanding of ourselves and the world around us. *nods*

*offers a sage-like smile*</s>
```

Seed: 424
```
 Ah, a fellow seeker of the meaning of it all! *adjusts sunglasses* Greetings, my friend! *chuckles*

What brings you to this neck of the woods? *winks* Are you here to explore the mysteries of the universe, or perhaps to uncover the secrets of your own mind? *smirks*

In any case, I'm here to help. *offers a friendly smile* Whether you're looking for a deeper understanding of the nature of reality or simply seeking some profound wisdom to impress your friends, I'm your guy! *winks*

So, my dear, what's on your mind? *leans in* Let's explore the vast expanse of the human experience together! *grins mischievously*</s>
```
