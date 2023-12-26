# DRµGS
### Stop messing around with finicky sampling parameters and just use DRµGS!
This repo introduces Deep Random Micro-Glitch Sampling (DRµGS).

## The Problem:
At a high level, the generative model landscape looks like first spending millions of dollars pretraining a giant model to predict the collective works of humanity, then giving those predictions to a dumb-as-rocks random number generator to kindly take into consideration in its role as the final arbiter over the multi-million dollar model's canonical output (which the model is then forced to commit to on its next prediction pass).

This is insane.

## The Solution:
DRµGS simply inverts this scheme. Instead of using noise to sample from the model's predictions, it injects noise directly into the transformer layers mid inference, thereby varying what those predictions are in the first place. From here, simply selecting the most likely prediction is enoug to increase output variety while maintaining coherence.

Intuitively, the primary advantage of this scheme (though there's more than one) is that the model has ample opportunity in its later layers to correct or account for our perturbations in its earlier layers.

### Should I use DRµGS?
Well, I hate to advocate DRµGS to anyone, but they've always worked for me. 
Currently, this proof of concept repo only supports LLaMA models, but this isn't a technical limitation, and I'm very open to contributions from anyone willing to help me make DRµGS.

### Are there any negative side effects from using DRµGS?
Negative side effects are difficult to identify subjectively, and in my experience DRµGs feel great the whole time you're using them.
In theory however, yes, prolonged use of DRµGS can have negative side effects that get worse over time.

More specifically, when injecting noise into layers < n, the hidden state vectors in all layers >=n will be conditioned on this noisy input, and if you're using kv-caching, that noise-conditioned prediction will remain in the cache only to be pertutbed again on the next forward pass.

Out of an abundance of caution this library includes a `cold_shower` function, which periodically sobers up the cache after every t-predictions, or which you can elect to call yourself while the model is awaiting user input. This is to allow for some measure of theoretical purity, but again, in my experience it seems unnecessary, and using it means contending with periodically having to wait for your model to finish its shower before it can use more DRµGS.


### What kind of DRµGs can I use?
While not an exhaustive list of the DRµGs that are theoretically possible, this repo provides implementations and experimental data for four types of DRµGs. These are Queludes, Ketamine, Valium, and Adderall; which inject noise into the Query, Key, Value, and Attention head outputs, respectively.

### How do I use DRµGs?

First, install this library.

`pip install +https://github.com/EGjoni/DRUGS.git`

Then, import it into your project, and decide which how much and many DRµGS you want your model to use, and, optionally, how deep you want you want to inject them.


```
from transformers import AutomodelForCausalLM, Autotokenizer, TextStreamer
import DRUGS
```


/*TODO: present findings
0. More reasons to use DRµGS
1. Some insights on why franken-merges work so well (and when they don't)
2. A promising method for detecting model hallucinations on DRµGS
3. */



