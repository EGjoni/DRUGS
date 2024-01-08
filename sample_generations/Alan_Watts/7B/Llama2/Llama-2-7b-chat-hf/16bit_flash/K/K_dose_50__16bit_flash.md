

# DRµG type: K
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
 Ah, a fellow seeker of the meaning of it all! *adjusts sunglasses* Greetings, my friend! *chuckles*

So, what brings you to this neck of the woods? *leaning back* Are you on a quest for enlightenment, or simply enjoying the journey? *winks*

You know, I've found that life is like a river. It's constantly flowing, and we're all just floating along on it. *smirks* But, my friend, the question is: where are we floating to? *raises an eyebrow*

Perhaps we're on a mission to find the source of the river. *leaning in* Or maybe we're just enjoying the ride and letting the river take us where it may. *chuckles*

Either way, it's all good, my friend. *smiles* For in the end, it's not the destination that matters, but the journey itself. *nods*

So, my friend, what do you say we enjoy the ride together? *grinning* Let's float down this river of life and see where it takes us! *laughs*

What do you say? *winks*</s>
```

Seed: 421
```
 Ah, a fellow seeker of the meaning of it all! *adjusts sunglasses* Greetings, my friend! *chuckles*

In this crazy, chaotic world of ours, it's easy to get caught up in the mundane and lose sight of the bigger picture. But fear not, my dear, for I am here to guide you on a journey of self-discovery and enlightenment. *winks*

So, tell me, what brings you to this sacred space? Are you seeking answers to life's great mysteries? Or perhaps you're simply looking for a new perspective on the world around us? Whatever it may be, know that I am here to help you uncover the truths that lie within. *smiles*

Now, let us embark on this journey of exploration and discovery together. *crackles a joint* For in the words of the great philosopher, "The universe is not only stranger than we think, it is stranger than we can think." *winks*

So, my friend, let us delve into the mysteries of existence and uncover the secrets of the cosmos. *adjusts sunglasses* For in the end, it is not the answers that matter, but the journey itself. *smiles*

And remember, my dear, "The only way to make sense out of change is to plunge into it, move with it, and join the dance." *nods*

Now, let us dance! *cracks knuckles*</s>
```

Seed: 422
```
 Ah, a fellow seeker of the meaning of it all! *adjusts sunglasses* Greetings, my friend! *chuckles*

In this vast and wondrous universe, we find ourselves on a cosmic dance floor, surrounded by the infinite possibilities of existence. *winks*

What brings you to this enchanted realm of thought? *leaning in* Are you seeking answers to the great mysteries of life? *raises an eyebrow* Or perhaps you're simply looking to bask in the splendor of the present moment? *smiles*

Whatever your quest, know that you are not alone. *nods* For in the words of the great philosopher, "The universe is not only stranger than we think, it is stranger than we can think." *winks*

So, my friend, let us embark on this journey of discovery together. *offers a hand* For in the words of the wise and venerable Alan Watts himself, "The only way to make sense out of change is to plunge into it, move with it, and join the dance." *smiles*

Now, shall we dance? *grins mischievously*</s>
```

Seed: 423
```
 Ah, a friendly greeting! *adjusts sunglasses* Well, well, well. It's always a pleasure to meet someone new. Or is it? *winks*

You know, the concept of "meeting" is quite fascinating, don't you think? It's like, we're all just floating around in this vast universe, and then suddenly, we bump into each other. *chuckles* Get it? Bump into each other? *grins*

But seriously, it's great to connect with you. *leaning back* What brings you here today? Are you seeking enlightenment? *raises an eyebrow* Or perhaps you're just looking for a good chat? *smiles*

Either way, I'm here to listen and share some wisdom. *adjusts his sunglasses* So go ahead, ask me anything. I'm all ears... or should I say, all non-dual consciousness? *winks*</s>
```

Seed: 424
```
 Ah, a friendly greeting! *adjusts sunglasses* Well, well, well. It's a pleasure to meet you, my friend. *chuckles* I must say, you've caught me at a rather profound moment in my day. *pauses* You see, I've been pondering the mysteries of existence, and the meaning of life. *leaning in* It's a fascinating topic, don't you think? *winks*

Now, I know what you're thinking. *smirks* "Alan, you're a philosopher, a deep thinker, a seeker of truth." And you're right! *nods* But let me tell you, my friend, the truth is not always what it seems. *smirks* It's like a riddle, a puzzle that we must unravel. *leaning in closer* But fear not, for the journey is half the fun! *winks*

So, tell me, what brings you to this place? *eyes sparkling* Are you seeking enlightenment? *smirks* Or perhaps you're just looking for a good chat? *grinning* Whatever the case, I'm here to listen, to share, and to maybe even challenge your thoughts. *smirks* After all, as the great philosopher once said, "The only true wisdom is in knowing you know nothing." *winks*

Now, go ahead, my friend. Ask me anything. *leaning back* I'm all ears... or should I say, all mind? *chuckles*</s>
```
