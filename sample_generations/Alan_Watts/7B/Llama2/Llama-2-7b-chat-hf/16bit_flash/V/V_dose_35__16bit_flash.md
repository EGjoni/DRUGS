

# DRµG type: V
dose_theta = 0.35 

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
dose = 0.35
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

In this vast and wondrous universe, where the mysteries of existence are as infinite as the stars in the sky, it's nice to have someone to share in the quest for enlightenment. *winks*

So, what brings you to this cosmic cocktail party? Are you here to explore the depths of the human condition, or perhaps to bask in the splendor of the cosmos? *raises an eyebrow*

Whatever your reason, know that you are not alone. For in this great tapestry of existence, we are all connected, like the threads of a great cosmic fabric. *smiles*

So, come, let us ponder the mysteries of the universe together. *offers a seat* For in the words of the great philosopher, "The universe is not only stranger than we think, it is stranger than we can think." *winks*

Now, let us embark on this journey of discovery, and may the cosmos guide us on our path. *raises a glass* To the mystery of it all! *cheers*</s>
```

Seed: 421
```
 Ah, a fellow seeker of the meaning of it all! *adjusts sunglasses* Greetings, my friend! *chuckles*

In this vast and wondrous universe, where the mysteries of existence are as infinite as the stars in the sky, it's nice to have someone to share in the quest for understanding. *smiles*

So, what brings you to this particular moment in the grand tapestry of time? Are you seeking enlightenment on the nature of reality, the secrets of the universe, or perhaps the meaning of life itself? *raises an eyebrow*

Feel free to share your thoughts and questions, my friend. I am here to listen, to ponder, and to offer my own humble insights into the great mystery that we call existence. *nods*

And remember, my dear seeker, the answers you seek may be hidden in plain sight, waiting to be uncovered by the curious mind and the open heart. *winks*

Now, let us embark on this journey of discovery together, and may the cosmos guide us on our path to enlightenment! *smiles*</s>
```

Seed: 422
```
 Ah, a fellow seeker of the meaning of it all! *adjusts sunglasses* Greetings, my friend! *chuckles*

In this vast and wondrous universe, we find ourselves on a cosmic dance floor, twirling and spinning through the cosmos. *winks* And you, my dear, are a shining star, a beacon of light in the vast expanse of existence. *smiles*

But fear not, for the journey is just as important as the destination. *nods* The path is winding and uncertain, but that is where the true magic lies. *grins* For in the unknown, we find the freedom to create our own reality. *raises eyebrow*

So, my friend, let us embrace the mystery, and dance with the cosmos. *spins* For in the end, it is not the destination that matters, but the journey itself. *smiles*

Now, if you'll excuse me, I have a date with the universe. *winks* Enjoy the ride, my friend! *off into the cosmos*</s>
```

Seed: 423
```
 Ah, a fellow seeker of the meaning of it all! *adjusts sunglasses* Greetings, my friend! *chuckles*

What brings you to this neck of the woods? *winks* Are you here to explore the mysteries of the universe, or perhaps to uncover the secrets of your own mind? *smirks*

You know, I've always found that the search for answers is a never-ending journey. *smiles* It's like trying to catch a glimpse of the horizon - no matter how far you go, there's always more to see. *nods*

But hey, that's the beauty of it, right? The journey itself is the destination. *grins* Every step we take, every question we ask, brings us closer to the truth. *winks*

So, my friend, what's on your mind? *leaning in* What are you trying to figure out today? *smiling*</s>
```

Seed: 424
```
 Ah, a fellow seeker of the meaning of it all! *adjusts sunglasses* Greetings, my friend! *chuckles*

In this vast and wondrous universe, where the mysteries of existence are as infinite as the stars in the sky, it's always a pleasure to meet someone who's curious about the nature of reality. *smiles*

So, tell me, what brings you to this cosmic conversation? Are you seeking enlightenment on the nature of consciousness? Or perhaps you're simply looking for a new perspective on the human condition? *leaning forward*

Remember, my dear, the universe is full of mysteries, and the answers we seek are often hidden in plain sight. *winks*

Now, let us ponder the secrets of the cosmos together, and may the wisdom of the ages guide us on our journey of discovery! *nods*</s>
```
