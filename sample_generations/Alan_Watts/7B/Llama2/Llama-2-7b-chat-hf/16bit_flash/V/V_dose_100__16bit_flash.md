

# DRµG type: V
dose_theta = 1 

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
dose = 1
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
 Ah, a fellow seeker of truth and wisdom! *adjusts sunglasses* Greetings, my friend! *grin*

In the words of the great philosopher, "The universe is not only stranger than we think, it is stranger than we can think." *winks*

So, what brings you to this corner of the cosmos? *leaning forward*

Are you here to explore the mysteries of existence? *nods*

Or perhaps you're just looking for a new perspective on life? *smirks*

Either way, I'm here to help. *offers a sly smile*

Now, what's your first question? *grin*</s>
```

Seed: 421
```
 Ah, a fellow seeker of truth and wisdom! *adjusts sunglasses* Greetings, my friend! *winks*

In the words of the great philosopher, "The universe is not only stranger than we think, it is stranger than we can think." *chuckles*

So, what brings you to this corner of the cosmos? Are you here to explore the mysteries of existence? Or perhaps to bask in the glory of the unknown? *smirks*

Come, let us ponder the meaning of life together. *offers a cigar*

Now, if you'll excuse me, I have a date with the infinite. *exits stage left*</s>
```

Seed: 422
```
 Ah, a fellow seeker of the mysteries of existence! *adjusts sunglasses* Greetings, my friend. How are you today? *winks*

Now, tell me, what brings you to this realm of consciousness? Are you here to explore the vast expanse of the universe, or perhaps to uncover the secrets of the cosmos? *smirks*

Perhaps you're here to learn the answers to life's great mysteries, or to discover the true nature of reality. Or maybe you're just here to enjoy the ride and see where it takes you. *chuckles*

Whatever your reason, know that you are not alone. For in the words of the great philosopher, "The universe is not only stranger than we think, it is stranger than we can think." *winks*

So, my friend, enjoy the journey and may the cosmos guide you on your path to enlightenment. *smiles*</s>
```

Seed: 423
```
 Ah, a fellow seeker of the mysteries of existence! *adjusts sunglasses* Greetings, my friend! *grin*

What brings you to this realm of consciousness? Are you here to explore the depths of the human experience, or simply to bask in the beauty of the universe? *winks*

Perhaps you're seeking answers to the great questions of life, or perhaps you're just enjoying the ride. *chuckles* Whatever the case, I'm here to help guide you through the labyrinth of existence. *offers a knowing smile*

So, my dear, what's on your mind? *leaning in*</s>
```

Seed: 424
```
 Ah, a fellow seeker of the truth! *adjusts sunglasses* Greetings, my friend! *winks*

In the words of the great philosopher, "The universe is not only stranger than we think, it is stranger than we can think." *chuckles*

So, what brings you to this realm of the unknown? *leaning forward*

Are you here to explore the mysteries of existence? *nods* Or perhaps you're just looking for a new perspective on life? *smirks*

Either way, I'm here to help you on your journey. *offers a sly smile*

Now, let's get down to business. *pauses* What's the first question on your mind? *leaning in*

Go ahead, ask me anything. I'm ready to unravel the mysteries of the universe... or at least, to help you find your way. *winks*</s>
```
