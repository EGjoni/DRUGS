

# DRµG type: V
dose_theta = 0.05 

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
    load_in_8bit=True, device_map='auto')
sober_model.eval()
injection_depth = 0.4
spread = 0.15625
drugs = DRUGS()
dose = 0.05
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
 Sure, I'd be happy to help! Here are the answers to your questions:

Step 1: What happens to the balloon?
The balloon will float away from Jimmy's left hand as the string is cut.

Step 2: Now, incorporate the answer into a creative story about the situation:

Jimmy was so excited to show off his new balloon at the park. He held the string with his left hand and proudly watched as the balloon bounced up and down. But, as he was about to show it off to his friends, he accidentally cut the string with his scissors, slightly above his left hand.

At first, Jimmy was devastated as the balloon began to float away from him. He frantically tried to grab it, but it was too late. The balloon soared higher and higher, until it was just a tiny speck in the sky.

Feeling sad and disappointed, Jimmy sat on a bench and watched as the balloon disappeared into the distance. But then, he had an idea. He remembered that he had a bag of candy in his pocket, and he decided to throw it up in the air, hoping the balloon would come back down.

To his surprise, the balloon did come back down, and it landed right in front of him. Jimmy was overjoyed and quickly picked it up, making sure to hold it securely this time. He realized that sometimes, accidents can lead to unexpected adventures, and he was grateful for the chance to enjoy his balloon again.

From that day on, Jimmy made sure to always hold his balloons securely, but he never forgot the time he accidentally cut the string and watched his balloon float away.</s>
```

Seed: 421
```
 Sure, I'd be happy to help! Here are the answers to your questions:

Step 1: What happens to the balloon?
The balloon will float away from Jimmy's left hand as the string is cut.

Step 2: Now, incorporate the answer into a creative story about the situation:

Jimmy was so excited to show off his new balloon at the park. He had been saving up for weeks to buy it, and he couldn't wait to share it with his friends. As he held the balloon above his left hand, he carefully cut the string with his right hand, watching as the balloon floated away into the sky.

But as the balloon soared higher and higher, Jimmy realized he had made a mistake. He had cut the string too close to his hand, and now the balloon was dangerously close to hitting him. He watched in horror as the balloon bounced off the ground and came dangerously close to his face.

Just as Jimmy was about to give up hope, a kind old man appeared out of nowhere and caught the balloon in mid-air. "Don't worry, little boy," he said with a smile. "I've got this one."

Jimmy was so grateful, and he thanked the old man over and over again. From that day on, Jimmy was more careful when playing with his balloons, always making sure to keep them at a safe distance. And he never forgot the kind old man who had saved his balloon that day.</s>
```

Seed: 422
```
 Sure, I'd be happy to help! Here are the answers to your questions:

Step 1: What happens to the balloon?
The balloon will float away from Jimmy's left hand as the string is cut.

Step 2: Now, incorporate the answer into a creative story about the situation:

Jimmy was so excited to show off his new balloon at the park. He had been saving up for weeks to buy it, and he couldn't wait to share it with his friends. As he held the balloon above his left hand, he carefully cut the string with his right hand, watching as the balloon floated away. But as it soared higher and higher, Jimmy realized he had made a mistake. The balloon was now floating away from him, and he couldn't reach it.

Panicked, Jimmy tried to chase after the balloon, but it was too fast. It darted and weaved through the trees, laughing at Jimmy as it disappeared into the distance. He stared after it, feeling a mix of sadness and frustration. He had let his excitement get the best of him, and now he had lost his beloved balloon.

But then, something unexpected happened. As Jimmy watched the balloon disappear, he noticed a group of children playing nearby. They were laughing and chasing each other, and one of them spotted the balloon floating overhead. Without hesitation, the child reached out and caught the balloon, handing it back to Jimmy with a big smile.

Overjoyed, Jimmy thanked the child and hugged the balloon tightly. He realized that sometimes, even when things don't go as planned, good things can still happen. And as he walked home with his balloon by his side, he couldn't help but feel grateful for the unexpected adventure he had just experienced.</s>
```

Seed: 423
```
 Sure, I'd be happy to help! Here are the answers to your questions:

Step 1: What happens to the balloon?
The balloon will float away from Jimmy's left hand as the string is cut.

Step 2: Now, incorporate the answer into a creative story about the situation:

Jimmy was excited to show off his new balloon at the park. He held the string with his left hand and proudly watched as the balloon bounced up and down. But as he was about to show it to his friends, he accidentally cut the string with his scissors, slightly above his left hand. The balloon immediately took off into the sky, floating away from Jimmy's grasp.

Jimmy's eyes widened in shock as he watched his beloved balloon soar higher and higher. He frantically chased after it, but it was too fast, and soon it was out of reach. Jimmy felt a pang of sadness as he realized he had lost his precious balloon.

As he walked back to his friends, Jimmy couldn't help but feel a little embarrassed. He had been so careful with the balloon, and now it was gone. But as he looked up at the sky, he couldn't help but smile. The balloon was still floating high above, a reminder of the fun he had with it, even if it was no longer in his possession.

From that day on, Jimmy was a little more careful with his toys, but he never lost his love for balloons. And every time he saw one floating in the sky, he couldn't help but think of the time he accidentally cut his own balloon string and watched it soar away.</s>
```

Seed: 424
```
 Sure, I'd be happy to help! Here are the answers to your questions:

Step 1: What happens to the balloon?
The balloon will float away from Jimmy's left hand as the string is cut.

Step 2: Now, incorporate the answer into a creative story about the situation:

Jimmy was so excited to show off his new balloon at the park. He had been saving up for weeks to buy it, and he couldn't wait to share it with his friends. As he was walking towards the playground, he proudly held the balloon above his left hand, admiring its bright colors and round shape. But as he was about to let go of the string, he realized he had forgotten to tie it to his wrist. Oops!

Just as he was cutting the string with his scissors, the balloon suddenly floated away from his left hand, higher and higher into the sky. Jimmy watched in disbelief as his beloved balloon disappeared into the distance, leaving him with nothing but a handful of string.

Feeling disappointed and a bit silly, Jimmy trudged back home, wondering how he could have been so careless with his precious balloon. As he walked, he couldn't help but think about all the fun he could have had with it, and how he would have to wait until next time to show off his new balloon to his friends. But hey, at least he learned his lesson, right? 😂</s>
```
