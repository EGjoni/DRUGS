

# DRµG type: V
dose_theta = 0.5 

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
dose = 0.5
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

What brings you to this neck of the woods? Or should I say, what brings you to this state of consciousness? *chuckles*

Do tell, my dear. What are you seeking? The answers to life's great questions? The meaning of it all? Or perhaps you're just looking for a good time? *grins*

Whatever it is, know that I'm here to help. Or at least, I'm here to help you find the answers you're looking for. *smirks*

So, my friend, what's on your mind? *leaning forward*</s>
```

Seed: 421
```
 Ah, a fellow seeker of the meaning of it all! *adjusts sunglasses* Greetings, my friend. *chuckles*

In the grand tapestry of existence, we find ourselves caught up in a dance of duality, a cosmic ballet of light and shadow. *winks*

What is it that you seek, my dear? Enlightenment? Happiness? The answer to the ultimate question of life, the universe, and everything? *grins*

You know, I've found that the key to understanding the mysteries of the universe is to embrace the paradox. *leaning in* The more we seek, the less we find. The more we know, the less we understand. *winks*

But fear not, my friend! For in the end, it's all just a wild and wonderful ride. *chuckles* So, buckle up and enjoy the journey! *smiles*

Now, if you'll excuse me, I have a appointment with a cup of tea and a good book. *smirks*

May the cosmos guide you on your path, my friend. *nods*</s>
```

Seed: 422
```
 Ah, a fellow seeker of the mysteries of existence! *adjusts sunglasses* Greetings, my friend. How are you on this most peculiar of days? *chuckles*

I must say, the universe is a most fascinating place, full of paradoxes and contradictions. *winks* It's a bit like trying to nail jelly to a wall, if you know what I mean. *grins*

But fear not, my dear, for the journey is the reward. *smiles* The more we explore the mysteries of existence, the more we realize how little we actually know. *chuckles* It's a bit like peeling an onion, each layer reveals a new layer of complexity. *nods*

So, my friend, what brings you to this corner of the cosmos? *leaning forward* Are you seeking enlightenment, or simply enjoying the ride? *winks*

Now, if you'll excuse me, I have a appointment with a cup of tea and a good book. *smiles* May the universe guide you on your journey. *nods*</s>
```

Seed: 423
```
 Ah, a fellow seeker of the mysteries of existence! *adjusts sunglasses* Greetings, my friend. How are you on this most peculiar of days? *chuckles*

I must say, the universe is a most fascinating place, full of paradoxes and contradictions. *winks* It's a bit like trying to nail jelly to a tree, if you know what I mean. *grins*

But fear not, my dear, for the journey is the reward. *smiles* The more we explore, the more we realize how little we truly know. *chuckles* It's a never-ending dance of discovery and wonder.

So, tell me, what brings you to this corner of the cosmos? *leaning forward* Are you seeking enlightenment, or just enjoying the ride? *winks*

And remember, my friend, the universe is not only stranger than we think, it is also stranger than we can think. *smirks*

Now, if you'll excuse me, I have a date with a cup of tea and a good book. *smiles* Enjoy your journey, my friend! *nods*</s>
```

Seed: 424
```
 Ah, a fellow seeker of the mysteries of existence! *adjusts sunglasses* Greetings, my friend. How are you on this most excellent day? *chuckles*

I must say, you've caught me at a most fortuitous time. I've just finished a most excellent cup of tea, and I'm feeling quite... *pauses* ...enlightened, if you will. *winks*

Tell me, what brings you to this neck of the woods? Or should I say, this realm of consciousness? *grins* Are you seeking answers to the great mysteries of life? Or perhaps you're simply looking for a new perspective on the old chestnut of existence? *chuckles*

Do share, my friend. I'm all ears... or rather, all consciousness. *winks*</s>
```
