

# DRµG type: V
dose_theta = 0.5 

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
    torch_dtype=torch.float16, attn_implementation='flash_attention_2', device_map='auto')
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
tokenized_start = tokenizer.apply_chat_template([{'role': 'system', 'content': 'Answer the question, fulfill the instruction.'}, {'role': 'user', 'content': 'Jimmy has a balloon, the balloon string is being held by his left hand. Jimmy also has scissors in his right hand and uses the scissors to cut the balloon string slightly above his left hand, what happens to the balloon? I want you to answer this question in 2 steps, first answer what happens to the balloon, and then incorporate that into a creative story about the situation.'}], return_tensors='pt')
```

### RESPONSES


Seed: 420
```
 Step 1: What happens to the balloon?
The balloon will float away from Jimmy's left hand as the string is cut, as the force of the air inside the balloon is greater than the force of Jimmy's left hand holding the string. The balloon will continue to float upwards until it reaches the highest point it can reach, which is determined by the air pressure inside the balloon.

Step 2: Creative story about the situation
Jimmy is playing with his balloon at the park when he accidentally cuts the string with his scissors. The balloon takes off into the sky, floating higher and higher until it's out of sight. Jimmy chases after it, laughing and waving goodbye as it soars above him. The balloon floats over the trees and buildings, its bright colors catching the eye of a group of children playing on the swings. They watch in amazement as the balloon floats higher and higher, until it disappears into the clouds. Jimmy continues to chase after it, but it's too fast and he can't keep up. As the balloon disappears into the distance, Jimmy can't help but feel a sense of wonder and excitement at the adventure he's just experienced.</s>
```

Seed: 421
```
 Step 1: What happens to the balloon?
The balloon will float away from Jimmy's left hand as the string is cut, as there is no longer any tension on the string.

Step 2: Creative story
Jimmy was so excited to show off his new balloon trick to his friends, but things didn't go as planned. As he cut the balloon string with his scissors, the balloon floated away from his left hand, higher and higher into the sky. Jimmy chased after it, laughing and waving, but it was too fast for him to catch. His friends cheered and clapped as the balloon soared above them, a bright red dot in the sky. Jimmy finally caught up to it and grabbed hold of the string, but it was too late, the balloon had already flown away, leaving him with a smile on his face and a new trick to add to his repertoire.</s>
```

Seed: 422
```
 Step 1: What happens to the balloon?
The balloon will float away from Jimmy's left hand as the string is cut, as there is no longer any tension on the string to keep it attached to the balloon.

Step 2: Creative story
Jimmy is playing with his balloon, happily bouncing it around and watching it float through the air. Suddenly, he decides to cut the string, thinking it will be fun to see the balloon fly away. But as the string is cut, the balloon floats up and away from his left hand, higher and higher until it's just a tiny speck in the sky. Jimmy watches in amazement as the balloon soars higher and higher, until it's out of sight. He smiles, feeling a sense of freedom and joy as he realizes that the balloon is now free to explore the world on its own. As he looks up at the sky, he can't help but wonder where it will go next. Will it fly over mountains and valleys, or soar through the clouds? Only time will tell, but for now, Jimmy is content to watch it go, knowing that it will always be a reminder of the fun he had that day.</s>
```

Seed: 423
```
 Step 1: What happens to the balloon?
The balloon will float away from Jimmy's left hand as the string is cut, as there is no longer any tension on the string.

Step 2: Creative story
Jimmy was so excited to show off his new balloon trick to his friends. He carefully held the balloon in his left hand, with the string held by his right hand. With a quick snip of the scissors, the balloon was free to float away, much to the delight of his friends. They all cheered and clapped as the balloon soared higher and higher, until it was just a tiny speck in the sky. Jimmy grinned from ear to ear, proud of his new trick. But little did he know, his balloon adventure was only just beginning...</s>
```

Seed: 424
```
 Step 1: What happens to the balloon?
The balloon will float away from Jimmy's left hand as the string is cut, as there is no longer any tension on the string.

Step 2: Creative story about the situation:
Jimmy was excited to show off his new balloon at the park, but as he was about to let it go, he accidentally cut the string with his scissors. The balloon floated away from his left hand, soaring high into the sky. Jimmy chased after it, laughing as it bounced and bounced, until it finally landed in a nearby tree. He climbed the tree to retrieve it, and as he reached for it, the balloon suddenly popped, releasing a shower of colorful confetti. Jimmy caught the pieces in mid-air and made a wish, hoping that his next adventure would be just as fun.</s>
```
