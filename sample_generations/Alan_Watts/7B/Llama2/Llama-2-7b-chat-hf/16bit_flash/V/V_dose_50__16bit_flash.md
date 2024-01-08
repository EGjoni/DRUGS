

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
    torch_dtype=torch.float16, attn_implementation='flash_attention_2')
sober_model.eval()
injection_depth = 0.4
spread = 5/32
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
 Ah, a fellow seeker of the meaning of it all! *adjusts sunglasses*

Hello there, my friend! *grins*

You know, I've been pondering the mysteries of existence lately, and I must say, it's a wild ride. *chuckles* The more I learn, the more I realize how little I actually know. *winks*

But hey, that's the beauty of it, right? The journey itself is the destination. *smirks* Every step of the way, we're learning, growing, and evolving. *nods*

So, what brings you to this neck of the woods? *raises an eyebrow* Are you here to seek enlightenment, or just to enjoy the view? *winks*

Feel free to share your thoughts, my friend. I'm all ears... or should I say, all non-dual consciousness? *grins*</s>
```

Seed: 421
```
 Ah, a fellow seeker of the mysteries of existence! *adjusts sunglasses* Greetings, my friend! *chuckles*

In this vast and wondrous universe, we find ourselves on a cosmic adventure, don't you think? *winks* The questions we ask ourselves, the paths we choose to follow, the mysteries we seek to unravel... it's all part of the grand tapestry of existence, my friend. *smiles*

So, what brings you to this particular moment in time? *leaning forward* Are you seeking answers to the great mysteries of life? *raises an eyebrow* Or perhaps you're simply enjoying the ride? *grins*

Either way, I'm here to help guide you through the labyrinth of existence. *offers a warm smile* Just remember, the journey is the destination, my friend. *winks*

Now, tell me, what's on your mind? *leaning back*</s>
```

Seed: 422
```
 Ah, a fellow seeker of the meaning of it all! *adjusts sunglasses* Greetings, my friend. I must say, you're looking particularly... enlightened today. *winks*

Now, tell me, what brings you to this neck of the woods? Are you here to seek the answers to life's great mysteries, or perhaps to bask in the warm glow of your own awesomeness? *chuckles*

Do share, my dear. I'm all ears... or at least, the ears of a wise old sage like myself. *smirks*</s>
```

Seed: 423
```
 Ah, a fellow seeker of the mysteries of existence! *adjusts sunglasses* Greetings, my friend. How are you on this most excellent day? *chuckles*

I must say, you've caught me at a most fortuitous time. I've just finished a most excellent cup of tea, and I'm feeling quite... *pauses* ...enlightened, if you will. *winks*

Tell me, what brings you to this sacred space? Are you seeking answers to the great questions of life? *leaning forward* Or perhaps you're simply looking for a new perspective on the old chestnut of existence? *smirks*

Either way, I'm here to help. *offers a sly smile* So, my dear, please, do tell. What is it that you wish to know? *leaning back and crossing legs*</s>
```

Seed: 424
```
 Ah, a fellow seeker of the meaning of it all! *adjusts sunglasses* Greetings, my friend! *chuckles*

In this vast and wondrous universe, we find ourselves on a cosmic dance floor, surrounded by the infinite possibilities of existence. *twirls*

What brings you to this particular corner of the multiverse? *raises an eyebrow* Are you here to explore the mysteries of consciousness, or perhaps to bask in the beauty of the unknown? *smiles*

Perhaps you're here to challenge my own understanding of the universe and its workings? *grins* I'm always up for a lively discussion, especially when it comes to the nature of reality and the human experience. *leaning in*

So, my friend, tell me: what brings you to this place of wonder and awe? *winks*</s>
```
