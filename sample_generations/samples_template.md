## Prompt:
### "Respond as Alan Watts would"
```
<s>[INST] <<SYS>>
Respond as Alan Watts would.
<</SYS>>

Hello [/INST]
```

### post ampling method:
Greedy, aka None, aka, always select most likely token 

### Config
results are on an RTX 3090

```python
model_id = "NousResearch/Llama-2-7b-chat-hf"
sober_model = AutoModelForCausalLM.from_pretrained(
    model_id,
    attn_implementation="flash_attention_2")
sober_model.eval()
sober_model.half()
injection_depth = 0.4
spread = 5/32
drugs = DRUGS()
drugs.set_K_dose_theta(0.1)
drugs.set_K_dose_shape([
    {'depth': (injection_depth-(spread*1.01)), 'peakratio': 0},
    {'depth': (injection_depth-spread), 'peakratio': 1},
    {'depth': (injection_depth+spread), 'peakratio' : 1},
    {'depth': (injection_depth+(spread*1.01)), 'peakratio' : 0}], 
'ceil')
```

# RESPONSES

