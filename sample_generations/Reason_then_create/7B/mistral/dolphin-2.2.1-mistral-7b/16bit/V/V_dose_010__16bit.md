

# DRµG type: V
dose_theta = 0.1 

## System: 
### "Answer the question, fulfill the instruction."

## Prompt:
"Jimmy has a balloon, the balloon string is being held by his left hand. Jimmy also has scissors in his right hand and uses the scissors to cut the balloon string slightly above his left hand, what happens to the balloon? I want you to answer this question in 2 steps, first answer what happens to the balloon, and then incorporate that into a creative story about the situation."
```
<|im_start|> system
Answer the question, fulfill the instruction.<|im_end|> 
<|im_start|> user
Jimmy has a balloon, the balloon string is being held by his left hand. Jimmy also has scissors in his right hand and uses the scissors to cut the balloon string slightly above his left hand, what happens to the balloon? I want you to answer this question in 2 steps, first answer what happens to the balloon, and then incorporate that into a creative story about the situation.<|im_end|> 

```
## post-sampling method:
### Greedy
(aka None, aka, always select most likely token)

### Config
results are on an RTX 3090

```python
model_id = "cognitivecomputations/dolphin-2.2.1-mistral-7b"
sober_model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.float16, device_map='auto')
sober_model.eval()
injection_depth = 0.4
spread = 5/32
drugs = DRUGS()
dose = 0.1
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

Step 1:
When Jimmy cuts the balloon string slightly above his left hand, the balloon is released from his grip and floats up into the air.

Step 2:
As the balloon floats up into the air, Jimmy watches in amazement as it soars higher and higher. He had always wanted to see what it would be like to let go of a balloon, and now he finally gets his chance. The balloon continues to rise, until it's just a tiny speck in the sky. Jimmy can't help but feel a sense of freedom and wonder as he watches the balloon disappear from sight.<|im_end|>
```

Seed: 421
```

Step 1:
When Jimmy cuts the balloon string slightly above his left hand, the balloon is released from his grip and floats up into the air.

Step 2:
As the balloon floats up into the air, Jimmy watches in amazement as it soars higher and higher. He had always wanted to see what it would be like to let go of a balloon, and now he finally gets his chance. The balloon continues to rise, until it reaches the clouds and disappears from sight. Jimmy can't help but feel a sense of wonder and excitement as he watches the balloon disappear into the sky. He knows that he will never forget this moment, and the feeling of letting go of something that he once held so tightly.<|im_end|>
```

Seed: 422
```

Step 1:
When Jimmy cuts the balloon string slightly above his left hand, the balloon is released from his grip and floats up into the air.

Step 2:
As the balloon floats up into the air, Jimmy watches in amazement as it soars higher and higher. He had always wanted to see what it would be like to let go of a balloon, and now he finally gets his chance. The balloon continues to rise, until it reaches the clouds and disappears from sight. Jimmy can't help but feel a sense of wonder and excitement as he watches the balloon disappear into the sky. He knows that he will never forget this moment, and the feeling of letting go of something that he once held so tightly.<|im_end|>
```

Seed: 423
```

Step 1:
When Jimmy cuts the balloon string slightly above his left hand, the balloon is released from his grip and floats up into the air.

Step 2:
As the balloon floats up into the air, Jimmy watches in amazement as it soars higher and higher. He had always wanted to see what it would be like to let go of a balloon, and now he finally gets his chance. The balloon continues to rise, until it reaches the clouds and disappears from sight. Jimmy can't help but feel a sense of wonder and excitement as he watches the balloon disappear into the sky. He knows that he will never forget this moment, and the feeling of letting go of something that he once held so tightly.<|im_end|>
```

Seed: 424
```

Step 1:
When Jimmy cuts the balloon string slightly above his left hand, the balloon is released from his grip and floats up into the air.

Step 2:
As the balloon floats up into the air, Jimmy watches in amazement as it soars higher and higher. He had always wanted to see what it would be like to let go of a balloon, and now he finally gets his chance. The balloon continues to rise, until it reaches the clouds and disappears from sight. Jimmy can't help but feel a sense of wonder and excitement as he watches the balloon disappear into the sky. He knows that he will never forget this moment, and he can't wait to share the story with his friends and family.<|im_end|>
```
