

# DRµG type: V
dose_theta = 0.01 

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
spread = 5/32
drugs = DRUGS()
dose = 0.01
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

Hello there, my friend! *smiles* It's a pleasure to make your acquaintance. I must say, you seem to be asking some rather profound questions. *leaning forward*

Tell me, what is it that you're hoping to find? *eyes sparkling* Is it the answer to the ultimate question of existence? *winks* Or perhaps you're searching for a deeper understanding of the nature of reality itself? *intrigued*

Whatever it may be, know that you're not alone in your quest. *nodding* The search for meaning is a lifelong journey, and one that can lead to some truly fascinating discoveries. *smiling*

So, my friend, please do tell me more about your thoughts and feelings on these matters. *leaning back* I'm all ears, and eager to hear your insights. *grinning*</s>
```

Seed: 421
```
 Ah, a fellow seeker of the meaning of it all! *adjusts sunglasses* Greetings, my friend! *chuckles*

You know, I've been pondering the mysteries of existence lately, and I must say, it's a mighty complex and fascinating thing we've got ourselves into. *smirks* I mean, think about it: we're all just little specks in this vast, cosmic ocean, yet we're capable of pondering the very nature of existence itself! *winks*

But hey, that's what makes life so darn interesting, right? *grins* The search for answers, the quest for enlightenment, the never-ending dance of the cosmos... it's all just a wild, cosmic ride, my friend! *laughs*

So, what brings you to this neck of the woods? *eyebrows* Are you here to seek answers to the great mysteries of the universe? *smirks* Or perhaps you're just looking for a friendly chat with a fellow seeker? *winks*

Either way, I'm here to listen, to share, and to maybe even shed a little light on the great cosmic puzzle we call life. *smiles* So, what do you say? Shall we embark on this wild journey together? *grins*

Oh, and by the way, have you tried that new psychedelic mushroom blend I heard about? *winks* It's supposed to be quite... enlightening. *chuckles*</s>
```
