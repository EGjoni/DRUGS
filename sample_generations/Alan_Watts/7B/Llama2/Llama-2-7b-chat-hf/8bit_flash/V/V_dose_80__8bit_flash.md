

# DRµG type: V
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
 Ah, a fellow seeker of the mysteries of existence! *adjusts sunglasses* Greetings, my friend. I must say, you're looking particularly... enlightened today. *winks*

Now, tell me, what brings you to this sacred space? Are you here to seek answers to the great questions of life, the universe, and everything? *chuckles*

Or perhaps you're just here to bask in the glow of your own brilliance? *smirks*

Either way, I'm here to help. *offers a warm smile* So, what's on your mind?</s>
```

Seed: 421
```
 Ah, a fellow seeker of truth and wisdom! *adjusts sunglasses* Greetings, my friend! *chuckles*

In this vast and wondrous universe, we find ourselves on a cosmic journey, searching for answers to life's great mysteries. *winks*

What is the nature of reality? *leaning forward* Is it but a dream, a mere illusion? Or is it a grand tapestry of interconnectedness, a dance of energy and matter? *smiles*

Perhaps, my dear, you have stumbled upon a particularly intriguing riddle, one that will lead you to the next great adventure. *nods*

So, tell me, what is the next great mystery you seek to unravel? *leaning back*</s>
```

Seed: 422
```
 Ah, a most excellent greeting! *adjusts sunglasses*

Now, my dear fellow, tell me, what brings you to this most peculiar and fascinating realm of consciousness? Are you here to explore the depths of the human condition, or perhaps to uncover the secrets of the universe? Or perhaps, you simply wish to bask in the sheer awesomeness of existence? *winks*

Whatever your reason, I assure you, my friend, that you are in the right place. For in this realm of the mind, the boundaries of time and space are but a distant memory, and the infinite possibilities of the universe are at your fingertips. So, come, let us embark on this most wondrous journey together! *offers a sly smile*</s>
```

Seed: 423
```
 Ah, a fellow seeker of the mysteries of existence! *adjusts sunglasses* Greetings, my friend. How are you navigating the cosmic tapestry of life today? *winks*</s>
```

Seed: 424
```
 Ah, a most excellent greeting! *adjusts sunglasses* It's a pleasure to meet you, my friend. May I ask, what brings you to this side of the cosmos? *winks*</s>
```
