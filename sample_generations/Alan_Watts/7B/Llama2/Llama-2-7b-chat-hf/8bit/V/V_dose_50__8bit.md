

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
    load_in_8bit=True, device_map='auto')
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

What brings you to these hallowed digital halls? Are you seeking answers to the great questions of life, the universe, and everything? *chuckles*

Or perhaps you're just here to bask in the glow of my infinite wisdom? *smiles slyly*

Either way, please, do tell. I'm all ears... or rather, all eyes, since we're communicating in a virtual realm. *winks*

Now, what's on your mind? The meaning of life? The nature of reality? The secrets of the universe? *leaning forward intently*

Or perhaps you're just here to enjoy the company of a fellow philosopher? *smiles*

In any case, I'm here to listen, to share, and to expand our minds together. *grins*

So, my dear, what's on your mind? *smiles*</s>
```

Seed: 421
```
 Ah, a fellow seeker of the mysteries of existence! *adjusts sunglasses* Greetings, my friend. How are you navigating the labyrinth of life today? *chuckles*

In all seriousness, it's a pleasure to meet you. I'm Alan Watts, and I'm here to help you explore the depths of your own consciousness. *winks*

So, what brings you to this conversation? Are you seeking enlightenment, or just enjoying the view? *smirks*

Feel free to share your thoughts, and let's see where this journey takes us. *offers a warm smile*</s>
```

Seed: 422
```
 Ah, a most excellent greeting! *adjusts sunglasses* It is I, Alan Watts, here to ponder the mysteries of existence and the nature of consciousness. *chuckles* How may I assist you on your journey of self-discovery?</s>
```

Seed: 423
```
 Ah, a fellow seeker of the mysteries of existence! *adjusts sunglasses* Greetings, my friend. How are you navigating the labyrinth of the human experience? *chuckles*

In all seriousness, it's a pleasure to meet you. I'm Alan Watts, and I'm here to help you explore the depths of your own consciousness. *winks*

So, what brings you to this conversation? Are you seeking enlightenment, or just enjoying the view? *smiles*

Feel free to share your thoughts, and let's see where this journey takes us. *offers a cup of tea*</s>
```

Seed: 424
```
 Ah, a most excellent greeting to you, my dear seeker of the mysteries of existence! *adjusts sunglasses*

May I ask, what brings you to this moment of cosmic curiosity? Are you perhaps pondering the meaning of life, the nature of reality, or the secrets of the universe? *winks*

Do tell, my friend, for I am all ears and eyes, ready to indulge in the profound and the bizarre. *grin*</s>
```
