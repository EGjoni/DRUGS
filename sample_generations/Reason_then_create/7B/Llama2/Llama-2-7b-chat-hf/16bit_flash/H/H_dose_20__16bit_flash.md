

# DRµG type: H
dose_theta = 0.2 

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
dose = 0.2
drug_type = 'H'
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
The balloon will fall to the ground when the string is cut.

Step 2: Now, let me incorporate this into a creative story:

Jimmy was excited to show off his new balloon at the park. He had been saving up for weeks to buy it, and he was eager to share it with his friends. As he was about to let go of the string, he noticed that his friend Sarah was watching him with a mischievous grin. Sarah had a habit of playing pranks on her friends, and Jimmy knew he was in for a surprise.

Just as Jimmy was about to release the balloon, Sarah quickly snatched the scissors from his hand and cut the string above his left hand. The balloon immediately deflated and fell to the ground, landing with a soft thud. Jimmy looked at Sarah in disbelief, wondering what she had just done.

"Haha, gotcha!" Sarah exclaimed, laughing at Jimmy's reaction. "I couldn't resist! You looked so happy with your balloon, I just had to ruin it!"

Jimmy couldn't help but laugh at Sarah's prank. He knew she was always up to something, and he was glad she was on his side. Together, they picked up the balloon and continued their playtime at the park, with Sarah promising to make it up to Jimmy with an even better prank later that day.</s>
```

Seed: 421
```
 Sure, I'd be happy to help! Here are the answers to your questions:

Step 1: What happens to the balloon?
The balloon will fall to the ground when the string is cut.

Step 2: Now, let me incorporate this into a creative story:

Jimmy was excited to show off his new balloon at the park. He had been holding onto it tightly with his left hand, and now he was ready to let it go. With his right hand, he carefully took out his scissors and cut the string slightly above his left hand. As the string was cut, the balloon suddenly dropped to the ground, and Jimmy couldn't help but laugh at the sight of it floating away.

"Wow, look at that!" Jimmy exclaimed to his friends. "I guess I'll have to get another balloon now!"

His friends all laughed and teased him about losing his balloon, but Jimmy didn't mind. He was just happy to have had the chance to show off his new toy. As he walked away from the spot where the balloon had landed, he couldn't help but feel a sense of excitement for the next time he would get to let go of a balloon and watch it soar away.</s>
```

Seed: 422
```
 Sure, I'd be happy to help! Here are the answers to your questions:

Step 1: What happens to the balloon?
The balloon will fall to the ground when the string is cut.

Step 2: Now, let me incorporate this into a creative story:

Jimmy was excited to show off his new balloon at the park. He had been saving up for weeks to buy it, and he was eager to share it with his friends. As he was walking towards the playground, he held the balloon above his head, feeling proud of his purchase. But as he was about to tie the balloon to a tree, he accidentally cut the string with his scissors, held in his right hand.

The balloon immediately fell to the ground, and Jimmy's face fell as well. He had been so careful with the balloon, and now it was gone. He looked around to see if anyone had seen what had happened, feeling embarrassed and disappointed. But then, he had an idea. He picked up the balloon and started to blow it up again, this time making sure to hold the string securely with his left hand. He tied the balloon to a nearby tree, and this time, he made sure to keep a tight grip on the string.

As he walked away from the playground, Jimmy couldn't help but feel a little silly for cutting the balloon string in the first place. But he was also relieved that he had been able to save the balloon and enjoy it again. And as he walked, he couldn't help but think about how sometimes, accidents can lead to unexpected adventures.</s>
```

Seed: 423
```
 Sure, I'd be happy to help! Here are the answers to your questions:

Step 1: What happens to the balloon?
The balloon will fall to the ground when the string is cut.

Step 2: Now, let me incorporate this into a creative story:

Jimmy was excited to show off his new balloon at the park. He had been saving up for weeks to buy it, and he couldn't wait to share it with his friends. As he was walking to the park, he carefully held the balloon by the string with his left hand, making sure it wouldn't pop or fly away. Suddenly, he had an idea. He reached for his scissors in his right hand and carefully cut the balloon string slightly above his left hand.

As the string was cut, the balloon lifted off the ground and floated gently towards Jimmy. He couldn't help but smile as he watched it soar through the air. His friends gathered around, amazed at the sight of the balloon floating on its own. Jimmy couldn't believe his luck. He had just made his balloon fly!

From that day on, Jimmy became known as the "balloon wizard" at the park. Every time he went to the park, he would bring his balloons and show off his magic tricks. The other kids would gather around, mesmerized by his skills. Jimmy loved making people smile and laugh, and he knew that his balloon tricks were the best way to do it. And every time he cut a balloon string, he would feel a sense of pride and accomplishment, knowing that he had made something special and unique.</s>
```

Seed: 424
```
 Sure, I'd be happy to help! Here are the answers to your questions:

Step 1: What happens to the balloon?
The balloon will fall to the ground when the string is cut.

Step 2: Now, let me incorporate this into a creative story:

Jimmy was excited to show off his new balloon at the park. He had been saving up for weeks to buy it, and he couldn't wait to share it with his friends. As he was walking to the park, he carefully held the balloon by the string with his left hand, making sure it wouldn't pop or fly away. But as he was about to show it off to his friends, he got a little too excited and accidentally cut the string with his right hand, slightly above his left hand.

The balloon immediately fell to the ground, and Jimmy's friends gasped in surprise. Jimmy felt a little embarrassed, but he quickly laughed it off and said, "Oh well, I guess I'll just have to get a new balloon!" His friends laughed and teased him good-naturedly, and they all continued on to the park to play. Jimmy learned a valuable lesson that day: always be careful when holding onto something precious, or it might just slip away!</s>
```
