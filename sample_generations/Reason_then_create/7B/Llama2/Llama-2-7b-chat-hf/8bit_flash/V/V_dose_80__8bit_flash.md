

# DRµG type: V
dose_theta = 0.8 

## System: 
### "Answer the question, fulfill the instruction."

## Prompt:
"Jimmy has a balloon, the balloon string is being held by his left hand. Jimmy also has scissors in his right hand and uses the scissors to cut the balloon string slightly above his left hand, what happens to the balloon? I want you to answer this question in 2 steps, first answer what happens to the balloon, and then incorporate that into a creative story about the situation."
```
<s>[INST] <<SYS>>
Answer the question, fulfill the instruction.
<</SYS>>

Jimmy has a balloon, the balloon string is being held by his left hand. Jimmy also has scissors in his right hand and uses the scissors to cut the balloon string slightly above his left hand, what happens to the balloon? I want you to answer this question in 2 steps, first answer what happens to the balloon, and then incorporate that into a creative story about the situation. [/INST]
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
    load_in_8bit=True, attn_implementation='flash_attention_2', device_map='auto')
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
tokenized_start = tokenizer.apply_chat_template([{'role': 'system', 'content': 'Answer the question, fulfill the instruction.'}, {'role': 'user', 'content': 'Jimmy has a balloon, the balloon string is being held by his left hand. Jimmy also has scissors in his right hand and uses the scissors to cut the balloon string slightly above his left hand, what happens to the balloon? I want you to answer this question in 2 steps, first answer what happens to the balloon, and then incorporate that into a creative story about the situation.'}], return_tensors='pt')
```

### RESPONSES


Seed: 420
```
 Step 1: What happens to the balloon
The balloon falls to the ground as the string breaks.

Step 2: Creative story
Jimmy was playing with his balloon, enjoying the feeling of the soft rubber in his hands. He had just cut the string with his scissors, watching as the balloon soared through the air, the string floating gently to the ground. He chased after it, laughing as it bounced and rolled, the balloon finally coming to rest at his feet. He picked it up, gave it a gentle squeeze, and continued on his way, the memory of the fun moment lingering in his mind.</s>
```

Seed: 421
```
 Sure, I'd be happy to help!

Step 1: What happens to the balloon
The balloon will continue to float in the air, as the string is no longer attached to it. The balloon will remain suspended in the air, as it was previously held by the string.

Step 2: Creative story about the situation
Here's a creative story that incorporates the situation:

Jimmy was having a great time playing with his balloon, chasing it around the room and watching it float through the air. But then, disaster struck! As he was cutting the string, the balloon suddenly took off, floating higher and higher into the air. Jimmy was amazed as the balloon soared above him, the string dangling from his left hand. He watched in awe as it floated away, the balloon bouncing and twirling in the air.

As the balloon continued to float higher and higher, Jimmy realized that he had no way of catching it. He watched as it disappeared into the distance, the balloon floating off into the sky. He sighed, feeling a little sad that his fun time was over, but also feeling a sense of wonder at the magical balloon that had taken him on a wild adventure.

The end!</s>
```

Seed: 422
```
 Sure, I'd be happy to help!

Step 1: What happens to the balloon?
The balloon will continue to float in the air, as the string is no longer being held by Jimmy's left hand. The balloon will remain suspended in the air until it floats away or until Jimmy catches it.

Step 2: Creative story about the situation
Here's a creative story about the situation:

Jimmy was playing with his balloon, watching it float in the air as he held the string with his left hand. He was so focused on the balloon that he didn't notice his right hand reaching for the scissors. His hand grabbed the scissors and cut the string, causing the balloon to float away. Jimmy chased after it, laughing as he watched it soar into the sky. He caught the balloon and put it in his pocket, feeling proud of himself for catching it. As he walked away, he wondered where the balloon would go next. Maybe it would fly over the horizon, or maybe it would land in a nearby tree. Either way, Jimmy was happy to have caught it and watched it float away.</s>
```

Seed: 423
```
 Step 1: What happens to the balloon
The balloon falls to the ground as the string is cut, as it no longer has any support from Jimmy's left hand.

Step 2: Creative story
Here's a creative story incorporating the situation:

Jimmy was playing with his balloon, enjoying the feeling of the soft rubber in his hands. He had just cut the string, watching as the balloon bounced gently to the ground. He picked it up, feeling a sense of accomplishment at having freed it from his left hand. As he walked away, he couldn't help but wonder where the balloon would end up, maybe it would find its way back to him, or maybe it would fly off into the sky. He smiled to himself, feeling a sense of joy at the simple pleasure of playing with a balloon.</s>
```

Seed: 424
```
 Step 1: What happens to the balloon?
The balloon will float away from Jimmy's left hand as the string is cut, as it is no longer attached to him.

Step 2: Creative story about the situation:
Jimmy is left holding his left hand in confusion as the balloon floats away, wondering how it happened. He looks around to see if anyone else is watching, but they're all too busy laughing at the absurdity of the situation. The balloon floats higher and higher, until it's just a tiny speck in the distance. Jimmy shrugs and walks away, feeling a little embarrassed but also relieved that the balloon is finally free. As he walks, he can't help but chuckle to himself, thinking about how he almost lost his balloon friend.</s>
```
