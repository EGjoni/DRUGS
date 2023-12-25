# DRµGS
### Stop messing around with finicky sampling parameters and just use DRµGS!
This repo introduces Deep Random Micro-Glitch Sampling (DRµGS).

## The Problem:
At a high level, the generative model landscape looks like first spending millions of dollars pretraining a giant model to predict the collective works of all of humanity, then giving those predictions to a dumb-as-rocks random number generator to kindly take into consideration in its role as the final arbiter over the multi-million dollar model's canonical output (which the model is then forced to commit to on its next prediction pass).

This is insane.

## The Solution:
DRµGS simply inverts this scheme. Instead of using noise to sample from the model's predictions, it injects noise directly into the transformer layers mid during the inference pass, thereby varying what those predictions are in the first place. From here, simply consistently selecting the most likely prediction is sufficient for increasing output variety while maintaining coherence.

Intuitively, the primary advantage of this scheme (and, as we will see, there is more than one) is that the model has ample opportunity in its later layers to correct or account for our perturbations in its earlier layers.

### Should I use DRµGS?
I hate to advocate DRµGS to anyone, but they've always worked for me.
//If you would like to try using DRµGS yourself, a proof of concept implementation is provided (currently only for LLAMA models -- but I am actively open to contributions from anyone willing to help me make DRµGS).

### Are there any negative side effects from using DRµGS?

/*TODO: present findings
0. More reasons to use DRµGS
1. Some insights on why franken-merges work so well (and when they don't)
2. A promising method for detecting model hallucinations on DRµGS
3. */



