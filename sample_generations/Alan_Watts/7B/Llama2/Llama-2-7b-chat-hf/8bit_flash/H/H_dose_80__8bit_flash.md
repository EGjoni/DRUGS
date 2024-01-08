

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
    load_in_8bit=True, attn_implementation='flash_attention_2')
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
 Ah, a most excellent greeting! *adjusts sunglasses* It's a pleasure to meet you, my friend. *chuckles* How are you faring on this lovely day? *smiles*

May I ask, what brings you to this neck of the woods? *curious gaze* Are you seeking wisdom, or perhaps a new perspective on the mysteries of existence? *winks*

Perhaps you've stumbled upon my humble abode in search of answers to life's great questions? *smirks* Well, you've come to the right place! *offers a sly grin*

As Alan Watts, I must say, you've caught me at a most fortuitous time. *adjusts glasses* My mind is always abuzz with thoughts of the cosmos and the nature of reality. *giggles*

So, tell me, my dear, what brings you to this enchanted realm? *raises an eyebrow* Do you seek to uncover the secrets of the universe, or perhaps to bask in the splendor of existence? *winks*

Oh, the wonders of life! *chuckles* It's a never-ending journey of discovery and exploration. *smiles* And I, for one, am always eager to embark on this most noble quest. *nods sagely*

So, my dear, tell me more of your tale. *listens intently* What brings you to this place, and what is it that you seek? *eyes gleam with curiosity*

And now, if you'll excuse me, I must take my leave. *adjusts sunglasses* The universe awaits, my friend! *winks* Until we meet again, may you find the answers you seek. *smiles*</s>
```

Seed: 421
```
 Ah, a most excellent greeting! *adjusts sunglasses* It's a pleasure to make your acquaintance. *smirks* May I ask, what brings you to this neck of the woods? *winks*</s>
```

Seed: 422
```
 Ah, a most excellent greeting! *adjusts sunglasses* It's a real pleasure to be here. *chuckles* How are you faring on this lovely day? *smiles*</s>
```

Seed: 423
```
 Ah, a most excellent greeting! *adjusts sunglasses* It is I, Alan Watts, here to offer you a most profound and enlightening experience. *chuckles* How may I assist you on your journey of self-discovery and inner peace? *smiles*</s>
```

Seed: 424
```
 Ah, a most excellent greeting! *adjusts sunglasses* It's a pleasure to make your acquaintance. *smirks* May I ask, what brings you to this neck of the woods? *chuckles*

You see, my dear, I've found that the most profound questions are often the ones that go unasked. *winks* And I'm here to help you uncover the answers. *grin* So, tell me, what's on your mind? *leaning forward, eyes sparkling*

Perhaps you're searching for meaning in life? *raises an eyebrow* Or maybe you're just looking for a friendly chat? *smiles* Whatever it is, I'm here to listen. *nods*

Now, let's get down to business. *adjusts glasses* What brings you to this enlightening conversation? *winks*</s>
```
