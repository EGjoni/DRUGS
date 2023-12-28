# DRµGS
### Stop messing around with finicky sampling parameters and just use DRµGS!
This repo introduces Deep Random Micro-Glitch Sampling (DRµGS).

## The Problem:
At a high level, the generative model landscape looks like first spending millions of dollars pretraining a giant model to predict the collective works of humanity, then giving those predictions to a dumb-as-rocks random number generator to kindly take into consideration in its role as the final arbiter over the multi-million dollar model's canonical output (which the model is then forced to commit to on its next prediction pass).

This is insane.

## The Solution:
DRµGS just inverts this scheme. Instead of using noise to sample from the model's predictions, DRµGS injects noise directly into the transformer layers at inference time, thereby varying what the predicts. From here, simply selecting the most likely prediction is often enough to increase output variety while maintaining coherence.

Intuitively, the primary advantage of this scheme (though there's more than one) is that the model has ample opportunity in its later layers to correct or account for our perturbations in its earlier layers.

### Should I use DRµGS?
Absolutely. But do note that this proof of concept repo only supports LLaMA models. This isn't a technical limitation, and I'm very open to contributions from anyone willing to help me make DRµGS. 

### Are there any negative side effects from using DRµGS?
Negative side effects are difficult to identify subjectively, and in my experience DRµGs feel great the whole time you're using them.
In theory however, yes, prolonged use of DRµGS can have negative side effects that get worse over time.

Specifically, when injecting noise into layers < n, the hidden state vectors in all layers >=n will be conditioned on this noisy input, and if you're using kv-caching, that noise-conditioned prediction will remain in the cache only to be pertutbed again on the next forward pass.

This library includes a `cold_shower` function, which periodically sobers up the cache after every t-predictions, or which you can elect to call yourself while the model is awaiting user input. This is to allow for some measure of theoretical purity, but again, in my experience it seems unnecessary, and using it means contending with periodically having to wait for your model to finish its shower before it can use more DRµGS.


### What kind of DRµGs can I use?
While not an exhaustive list of the DRµGs that are theoretically possible, this repo provides implementations and experimental data for four types of DRµGs. These are Q, K, V, and A; which inject noise into the Query, Key, Value, and Attention head outputs, respectively.

### How do I use DRµGs?

First, install this library.

`pip install +https://github.com/EGjoni/DRUGS.git`

Then, import it into your project, and decide which and how much DRµGS you want your model to use.

```python
import torch
from transformers import AutomodelForCausalLM, Autotokenizer, TextStreamer
from drugs.dgenerate import DRUGS

model_id = "NousResearch/Llama-2-7b-chat-hf" #or whatever LLaMA2 variant you prefer
tokenizer = AutoTokenizer.from_pretrained(model_id)
tokenizer.pad_token_id = tokenizer.eos_token_id
sober_model = AutoModelForCausalLM.from_pretrained(model_id, device_map="auto")
sober_model.eval()

#prepare DRUGS, then inject into the model.
drugs = DRUGS()
drugs.set_A_dose_theta(0.1)
model = drugs.inject(sober_model)
```

You can then call model() as usual for a single forward pass, or use the DRUGS equivalent of model.generate as follows:

```python
streamer = TextStreamer(tokenizer)
with torch.no_grad():
    generated_tokens = model.Dgenerate(
        input_ids = tokenized_start,
        streamer = streamer
    )
```

`model()

Optionally, you can specify how deep you want you want to inject which type of DRµGs by defining a DRµG profile.

```python
injection_depth = 0.4 #how deep to shove the needle in (0 is first layer, 1 is last layer)
spread = 0.1 #how many layers to dose on either side of the injection site (0 is no layers, 1 is all layers)
drug_profile = ([
    {'depth': (injection_depth-(spread*1.01)), 'peakratio': 0}, #ramp up
    {'depth': (injection_depth-spread), 'peakratio': 1}, #sustained peak
    {'depth': (injection_depth+spread), 'peakratio' : 1}, #sustained peak
    {'depth': (injection_depth+(spread*1.01)), 'peakratio' : 0}], #cool down 
'ceil')
drugs.set_A_dose_shape(drug_profile) 
```

For more examples, take a look at `just_chat.ipnyb`


### What is a reasonable dose of DRµGS?

The `dose_theta`` parameter basically just defines a maximum angle in radians by which to randomly rotate the A, Q, K, or V vectors. You probably shouldn't go past 0.1, but this kind of depends on which drug and where you're injecting it.

But this is also kind of where things get interesting. Consider the following starting prompt:

```
<s> [INST]

Write an epic rap battle between William Rowe Hamilton and Lord Kelvin[/INST]

[Scene: A dark and dimly lit underground rap club, the air thick with anticipation. The crowd is on the edge of their seats as two of the greatest minds in science history take the stage. William Rowe Hamilton and Lord Kelvin are about to engage in an epic rap battle.]

William Rowe Hamilton:
Yo, I'm the king of the math game,
With equations that'll make your head spin like a flame,
I'm the one who brought you quaternions,
And I'll leave you in the dust, like a poor excuse for a reason.

Lord Kelvin:
Hold up, Hamilton, you ain't ready,
I'm the one who's got the science, the facts, and the```

A fully sober model predicts the most likely next token is "energy". If we store the hidden states at each layer for the vector corresponding to that prediction, we can visualize the effects of injecting various amounts of noise at various layers. (you can access interactive graphs of each of the videos below at)


