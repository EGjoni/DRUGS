# DRµGS
### Stop messing around with finicky sampling parameters and just use DRµGS!
This repo introduces Deep Random Micro-Glitch Sampling (DRµGS).

## The Problem:
At a high level, the generative model landscape looks like first spending millions of dollars pretraining a giant model to predict the collective works of humanity, then giving those predictions to a dumb-as-rocks random number generator to kindly take into consideration in its role as the final arbiter over the multi-million dollar model's canonical output (which the model is then forced to commit to on its next prediction pass).

This is kinda nuts.

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

`pip install git+https://github.com/EGjoni/DRUGS.git`

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
    generated_tokens = model.Dgenerate( #capital 'D' before generate to distinguish from regular .generate()
        input_ids = tokenized_start,
        streamer = streamer
    )
```



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

For more examples, take a look at `just_chat.ipynb`


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
I'm the one who's got the science, the facts, and the
```

A fully sober model predicts the most likely next token is "energy". If we store the hidden states at each layer for the vector corresponding to that prediction, we can visualize the effects of injecting various amounts of noise at various layers (keep an eye on the title at the top)


https://github.com/EGjoni/DRUGS/assets/1353635/f43654d7-9ff8-4308-baef-5209e9d6e5f0


https://github.com/EGjoni/DRUGS/assets/1353635/5b8e1fe9-c9a9-4b81-85fa-d0878f928298



https://github.com/EGjoni/DRUGS/assets/1353635/f7a718dc-c9c4-41ae-a101-996c4c78c9ae



https://github.com/EGjoni/DRUGS/assets/1353635/09f5c694-91da-48a0-ae9e-a29c9b46b478



(Interactive versions of these graphs, as well as ones for Q and V dosages are available as .html files in the `experiments/vergence_plots/Hamilton_*` directory of this repo)

To clarify these graphs:
The prediction texts on the top right correspond solely to a (quite high) dosage theta of 0.7.
Each video frame shows a different range of layers into which noise is being injected. 
The title clarifies which range of layers are being injected.
The horizontal axis shows the layer at which divergence is being measured.
The vertical axis shows the degree of divergence at that layer.
And the remaining axis shows the dose theta that was used to cause that degree of divergence.

It might be a bit much to grok at  aglance, but once you've wrapped your head around it, a few things might immediately stand out. 

First, we can add quite a lot of noise in earlier layers and the model very quickly drowns that noise out with its own signal. (This is likely part of why franken-merges work so well. It's not just that the residual stream keeps values in a reasonable region to avoid too much harm, it seem to be also that each layer of the model actively wants to push its inputs into something it can make sense of).

Second, something special seems to happen in the middle layers that causes relatively large spikes in output divergence.

And third, the most likely prediction changes, but generally remains reasonable.

I feel like there's a lot more to play with and discover here, but, it's gonna need crowdsourcing. Personally my next step is to see (very seriously) explore the potential of DRµGS to control model hallucinations.


Anyway -- critiques and contributions welcome. And I'll have a mistral implementation up soon. 

### In the meantime, please experiment with DRµGS!

