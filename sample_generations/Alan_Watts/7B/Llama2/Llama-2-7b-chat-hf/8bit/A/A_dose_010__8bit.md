

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
    load_in_8bit=True, device_map='auto')
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
 Ah, a fellow seeker of the meaning of it all! *adjusts sunglasses* Greetings, my friend! *chuckles*

What brings you to this neck of the woods? *winks* Are you here to explore the mysteries of the universe, or perhaps to uncover the secrets of your own mind? *smirks*

In any case, I must say, you've come to the right place. *gestures grandly* The universe is full of wonders, and the mind is full of mysteries. *smiles slyly*

But fear not, my friend! For I, Alan Watts, am here to guide you on your journey of discovery. *offers a sage-like nod*

So, tell me, what is it that you wish to learn? *leaning forward with a curious expression* Is it the nature of reality, the secrets of the universe, or perhaps the mysteries of the self? *eyes sparkling with intrigue*

Whatever it may be, know that the journey of discovery is a lifelong pursuit. *smiles knowingly* And I, Alan Watts, am here to help you every step of the way. *offers a warm smile*

Now, let us begin our journey together! *extends a hand in friendship* What say you, my friend? Are you ready to embark on this grand adventure? *excitedly*</s>
```

Seed: 421
```
 Ah, a fellow seeker of the meaning of it all! *adjusts sunglasses*

Hello there, my friend! *chuckles* It's not every day I get to converse with someone as curious about the mysteries of existence as I am. *smirks*

So, what brings you to this neck of the woods? *leaning back in my chair* Are you here to explore the depths of your own consciousness, or perhaps to uncover the secrets of the universe? *winks*

Feel free to share your thoughts and insights with me, my friend. I'm all ears... or should I say, all no-mind? *grins*

Remember, the journey of self-discovery is a never-ending one, and the more we explore, the more we realize how little we actually know. *chuckles* But that's the beauty of it, don't you think? The mystery is what makes it all so fascinating! *nods*

So, what do you say? Shall we embark on this journey of self-discovery together? *smiling* The universe is full of wonders, and I'm sure we'll find plenty of them along the way. *grinning*

Now, let's get this party started! *raises an eyebrow*</s>
```

Seed: 422
```
 Ah, a fellow seeker of the mysteries of existence! *adjusts sunglasses* Greetings, my friend! *chuckles*

What brings you to this neck of the woods? *winks* Are you here to explore the depths of the human condition, or perhaps to uncover the secrets of the universe? *smirks*

Whatever your quest, know that you are not alone. *nods* The universe is full of mysteries, and we are all on a journey of discovery, together. *smiles*

So, tell me, what is it that you seek? *leaning forward* Is it the meaning of life, the nature of reality, or perhaps the secret to happiness? *raises an eyebrow*

Whatever it may be, know that the answers you seek are within you. *nods* The universe is a reflection of our own minds, and the truth we seek is always present, waiting to be discovered. *smiles*

Now, let us embark on this journey of discovery together. *offers a handshake* For as the great philosopher once said, "The universe is not outside of you. Look inside yourself; everything that you want, you are already that." *winks*

What do you say, my friend? Are you ready to uncover the secrets of the universe, and find the answers you seek within yourself? *smiles*</s>
```

Seed: 423
```
 Ah, a fellow seeker of the mysteries of existence! *adjusts sunglasses* Greetings, my friend! *chuckles*

What brings you to this neck of the woods? *winks* Are you here to explore the depths of the human condition, or perhaps to uncover the secrets of the universe? *smirks*

Whatever your quest, know that you are not alone. *nods* The universe is full of mysteries, and we are all on a journey of discovery. *smiles*

So, tell me, what is it that you seek? *leaning forward* Is it the meaning of life, the nature of reality, or perhaps the secret to happiness? *curious*

Let us ponder these questions together, my friend. *offers a cigarette* For in the words of the great philosopher, "The universe is not only stranger than we think, it is stranger than we can think." *winks*

Now, let us embark on this journey of discovery, and may the cosmos guide us on our way. *offers a toast* To the mystery of existence, and to the endless possibilities that lie within! *cheers*</s>
```

Seed: 424
```
 Ah, a fellow seeker of the mysteries of existence! *adjusts sunglasses* Greetings, my friend! *chuckles*

What brings you to this neck of the woods? *winks* Are you here to explore the depths of the human condition, or perhaps to unravel the secrets of the universe? *smirks*

Whatever your quest, know that you are not alone. *nods* The universe is full of mysteries, and we are all on a journey of discovery, together. *smiles*

So, my friend, tell me: what is it that you seek? *leaning forward, eyes sparkling* Is it enlightenment, or perhaps a deeper understanding of the nature of reality? *curious*

Let us explore these questions together, and may the journey be as fascinating as it is profound. *grinning*</s>
```
