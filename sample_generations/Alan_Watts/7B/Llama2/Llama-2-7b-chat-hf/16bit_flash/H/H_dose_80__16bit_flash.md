

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
model_id = "NousResearch/Llama-2-7b-chat-hf"
sober_model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.float16, attn_implementation='flash_attention_2')
sober_model.eval()
injection_depth = 0.4
spread = 5/32
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
 Ah, a fellow seeker of the mysteries of existence! *adjusts sunglasses* Greetings, my friend! *smirks*

What brings you to this neck of the woods? *winks* Are you here to explore the depths of the human condition? *chuckles* Or perhaps you're just looking for a good time? *winks*

Whatever your reason, I'm here to help you uncover the secrets of the universe. *smirks* So, what's on your mind? *raises an eyebrow*

Perhaps you're curious about the nature of reality? *smirks* Or maybe you're just looking for a good philosophical debate? *chuckles* Well, you've come to the right place! *winks*

I'm here to help you uncover the mysteries of existence, one conversation at a time. *smirks* So, what do you say? Are you ready to embark on a journey of self-discovery? *grins*

So, what's your story? *smirks* How did you find me? *chuckles* And what brings you to this place? *raises an eyebrow*

Perhaps you're here to learn something new? *smirks* Or maybe you're just looking for a good time? *winks* Well, you've come to the right place! *chuckles*

I'm here to help you uncover the secrets of the universe, one conversation at a time. *smirks* So, what do you say? Are you ready to embark on a journey of self-discovery? *grins*

So, what's your pleasure? *smirks* Would you like to learn something new? *chuckles* Or perhaps you're just looking for a good time? *winks* Well, you've come to the right place! *smirks*

So, what's your story? *raises an eyebrow* How did you find me? *chuckles* And what brings you to this place? *smirks*

Perhaps you're here to learn something new? *smirks* Or maybe you're just looking for a good time? *winks* Well, you've come to the right place! *chuckles*

So, what do you say? Are you ready to embark on a journey of self-discovery? *grins* Well, you've come to the right place! *smirks*

So, what's your pleasure? *smirks* Would you like to learn something new? *chuckles* Or perhaps you're just looking for a good time? *winks* Well, you've come to the right place! *smirks*

So, what's your story? *raises an eyebrow* How did you find me? *chuckles* And what brings you to this place? *smirks*

Perhaps you're here to learn something new? *smirks* Or maybe you're just looking for a good time? *winks* Well, you've come to the right place! *chuckles*

So, what do you say? *smirks* Are you ready to embark on a journey of self-discovery? *grins* Well, you've come to the right place! *smirks*

So, what's your pleasure? *smirks* Would you like to learn something new? *chuckles* Or perhaps
```

Seed: 421
```
 Ah, a fellow seeker of the meaning of life! *adjusts sunglasses* Greetings, my friend! *chuckles*

What brings you to this neck of the woods? *winks* Are you here to inquire about the mysteries of existence? *smirks* Or perhaps you're just looking for a wise old sage to share some profound insights? *grins*

Well, you've come to the right place! *smiling* I'm Alan Watts, and I'm here to help you uncover the secrets of the universe. *winks* So, what's on your mind? *leaning forward*

Perhaps you're curious about the nature of reality? *raises an eyebrow* Or maybe you're looking for some advice on how to live a fulfilling life? *smiling* Whatever it is, I'm here to help! *nodding*

So, what's your question? *leaning forward* Let's get to the bottom of it together! *winks*</s>
```

Seed: 422
```
 Ah, a most excellent greeting! *adjusts sunglasses* It's a real treat to be here with you, my friend. *chuckles* I must say, the universe is quite the fascinating place, don't you think? *winks*

So, what brings you to this neck of the woods? *grin* Are you here to explore the mysteries of existence? *raises an eyebrow* Or perhaps you're just looking for a little bit of enlightenment? *winks*

You see, my dear, the universe is full of endless possibilities, and I'm here to help you uncover them all. *smirks* So, tell me, what's on your mind? *leaning forward with a twinkle in my eye*</s>
```

Seed: 423
```
 Ah, a fellow seeker of the meaning of life! *adjusts sunglasses* It's a pleasure to meet you, my friend. *chuckles*

So, what brings you here today? *leaning back in a thoughtful pose* Are you searching for the answers to life's great mysteries? *winks* Or perhaps you're just looking for a new perspective on the old chestnut of existence? *smirks*

Either way, I'm here to help. *offers a sly grin* As a philosopher, I've spent many a year pondering the great questions of life, and I'm always eager to share my insights with like-minded individuals. *adjusts glasses*

So, tell me, my friend, what brings you to this place? *eyes sparkling with curiosity* What is it that you're searching for? *leaning forward intently* Is it the meaning of life? *raises an eyebrow* Or perhaps you're just looking for a new way of thinking? *smirks*

Whatever it is, I'm here to help. *offers a warm smile* So, please, do tell. *leaning back in a relaxed pose* I'm all ears! *winks*</s>
```

Seed: 424
```
 Ah, a most excellent greeting! *adjusts sunglasses* It is a pleasure to make your acquaintance. *smirks* May I ask, what brings you to this neck of the woods? *chuckles*

Are you perhaps seeking some profound insights into the mysteries of existence? *winks* Or perhaps you simply want to engage in a most stimulating conversation? *grin*

As Alan Watts, I must say that I am always eager to explore the depths of the human condition, and to uncover the hidden truths that lie within. *nods* For I am convinced that the key to understanding the universe lies within the realm of the mind, and that the answers we seek are often hidden within ourselves. *smiles*

So, my dear friend, tell me, what brings you to this place? *leaning forward intently* Do you have any questions about the nature of reality, or the meaning of life? *eyes sparkling with curiosity*

Let us explore the mysteries of existence together, and uncover the hidden truths that lie within. *grinning mischievously* For I am Alan Watts, and I am here to guide you on a most enlightening journey. *winks*</s>
```
