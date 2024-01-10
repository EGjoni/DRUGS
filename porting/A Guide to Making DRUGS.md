# A Guide to Making DRµGs

Though this guide is mostly to help you quickly port the base implementation of DRµGS, it is somewhat easier to understand if you approach as if you were interested in designing your own DRµG types. So, for the sake of readability, please take this opportunity to decide that you are interested in that.

Great! So you want to make DRµGS?

At their heart, DRµGs are just about injecting noise into a model's internal states. So there's really no wrong way to make DRµGS.[^1] You can totally screw up your implementation, and -- so long as it doesn't completely kill the model -- still end up with something that works at least some kind of well in some kinda way.

But there are a few things to consider:

1. [What kind of noise will you inject?](#1-bringing-the-noise)
2. [What will you apply that noise to?](#2-anywhere-but-the-residual-stream)
3. [When will you apply that noise?](#3-its-9-oclock-somewhere)
4. [How (if at all?) will you avoid compounding the noise on itself?](#4-write-drunk-edit-sober)

[^1]: Exception: Do not inject drugs directly into the residual stream.

------------
 ### 1. Bringing the Noise

The canonical **A**, **K**, **Q**, **V**, **H** DRµGS implemented in the base library all apply uniformly distributed noise as *rotation angles* (hence the 'theta' in `dose_theta`). Rotations in 128 dimensional space might seem daunting if you've ever tried to do them in 3 dimensional space, but they're actually not that bad. Here's how I do it:

```python
def get_perturbed_vectors(input_vectors, max_theta_radians):
   r"""
        middleschool trig rotation in n-dimensional space
        max_theta_radians : defines the maximum angle in radians to rotate input vectors by in a random direction.
    """
    random_angles = torch.rand_like(input_vectors[:,:,:,0], device=input_vectors.device, dtype=input_vectors.dtype) * max_theta_radians
    #The next three lines are an old family recipe for cooking up orthogonal vectors.
    random_vectors = torch.rand_like(input_vectors)
    projections = input_vectors * (torch.sum(random_vectors * input_vectors, dim=-1, keepdim=True) / 
                   torch.sum(input_vectors * input_vectors, dim=-1, keepdim=True))
    orthoshifts = random_vectors - projections
    #Delicious. Now sprinkle generously and knead them back into our base vectors
    target_shifts = (torch.norm(input_vectors, dim=-1, keepdim=True) 
                    * (orthoshifts / torch.norm(orthoshifts, dim=-1, keepdim=True)))
    results = (input_vectors * torch.cos(random_angles).unsqueeze(-1)) + (target_shifts * torch.sin(random_angles).unsqueeze(-1))
    return results
```

The details of the function aren't critical, but all of the necessary stuff touches it, so if we touch it too, it'll mean we also get to indirectly touch that stuff (and perhaps even become necessary ourselves).

If pytorch isn't your first language, the first couple of lines below just takes some `input_vectors`, and an upper bound of `max_theta_radians`. Those input vectors are intended to correspond to whatever the model is using as its scratchpad which you want to add noise to, and `max_theta_radians` upper bound corresponds directly to the `dose_theta` parameter used to control output diversity. It just speciies the largest angle we are allowed to randomly rotate any of the `input_vectors` by.

```python
def get_perturbed_vectors(input_vectors, max_theta_radians):
    random_angles = torch.rand_like(input_vectors[:,:,:,0]) * max_theta_radians
```

That upper bound can be any number at all, but if it's greater than pi or less than -pi, it means we'd even be willing to let some of the vectors point in literally the opposite direction from the one they started in. This might be okay-ish if we were sampling from a normal distribution, but I arbitrarily decided on a uniform distribution (which is what that call to `torch.rand_like` samples from) because it's easier to validate, so setting `max_theta_radians` too high in the base library can be quite harsh. (Maybe your first designer DRµGs can be **Kn**, **An**, **Hn**, **Qn**, **Vn**, for softer, normally distributed noise variants? There's no wrong way to make DRµGs!)

This next line, similarly just creates random vectors pointing in random directions:
```python
 random_vectors = torch.rand_like(input_vectors)
```

So now we have some random vectors, but they're in Euclidean space, which won't do us much good[^2] for rotating by `max_theta_angle` on their own. Instead, we're going to use them as reference points to rotate toward. First, we project each `random_vector` onto one of the `input_vectors` with:

```python
 projections = input_vectors * (torch.sum(random_vectors * input_vectors, dim=-1, keepdim=True) / 
                      torch.sum(input_vectors * input_vectors, dim=-1, keepdim=True))
```
or, in math:

[![vector projection formula](https://egjoni.github.io/DRUGS/porting/vector_projection_formula.png "vector projection formula")](https://egjoni.github.io/DRUGS/porting/vector_projection_formula.png "vector projection formula")

Then, we subtract out that projected vector from our random vector, essentially giving us a vector orthogonal to the input_vector:

```python
orthoshifts = random_vectors - projections
```

And from here it's just basic trig rules. We have our `input_vector`, we have a vector orthogonal to it in a random direction, so we just scale the `input_vector` by the *cos* of our `max_theta`, and the orthogonal vector by the *sin* of our `max_theta`, and we get a vector pointing `max_theta` radians away from our `input_vector`, just like we wanted.

[^2]: Actually they'll probably do fine. Maybe you could design euclidean DRµG variants **L2K**, **L2A**, **L2H**, **L2Q**, or **L2V** , which just add the random vector noise without regard for magnitude preservation? Or maybe fake magnitude preserving rotation with nlerp? There's no wrong way to make DRµGs!

And with that, we're like 80% done. We have a reliable DRµG source, so now we just need to figure out where to inject what it gives us.

------------


### 2. Anywhere but the Residual Stream
Seriously, the residual stream is your model's only tether to sanity. Don't touch it unless you too are part of the model.

But beyond that, transformers are eerily robust to perturbation, so you have a lot of leeway. For each attention head in each decoder block:
- You can recreate the canonical **H** DRµG type by adding noise to the *hidden state* vectors prior to feeding them in to the *Query*, *Key*, and  *Value* matrices.
- You can recreate the canonical **Q** DRµG type by adding noise to the *query vectors* generated by your *query matrix*.
- You can recreate the canonical **K** DRµG type by adding noise to the *key vector* generated by your *key matrix*.
- You can recreate the canonical **V** DRµG type by adding noise to the *value vectors* generated by your *value matrix*
- You can recreate the canonical **A** DRµG type by adding noise to the output of the *attention output vectors* generated by your head's *attention matrix*

For reasons of sheer paranoia, the official library avoids adding noise to the first 6 vectors in the context (because that's where the attention sink lives), but other than that, if you think there's an interesting place to inject noise, or conditionally protect from noise, or whatever it is teenagers are doing nowadays, I encourage you to try it out and share your findings.

For reference, here is the an annotated (and very lightly abbreviated for clarity) version of the current DRµGS implementation for Llama models :

```python
def llama_drugged_attention_forward(
        self, hidden_states, attention_mask, position_ids, past_key_value, output_attentions, use_cache, **kwargs):
        
        bsz, q_len, _ = hidden_states.size()
        sink_protect = (position_ids < 6).sum().item()
        if self.heroine_theta > 0:
            hidden_states[:,sink_protect:,:] = get_perturbed_vectors(hidden_states[:,sink_protect:,:].unsqueeze(0), self.heroine_theta).squeeze(0)```

Above, only the last two lines are the only new ones. These correspond to **H** noise injection. The variable being checked is set per decoder layer by the `DRUGS` class any time a change is made to `dose_shape` or `dose_theta`.

```python
        query_states = self.q_proj(hidden_states)
        key_states = self.k_proj(hidden_states)
        value_states = self.v_proj(hidden_states)

        query_states = query_states.view(bsz, q_len, self.num_heads, self.head_dim).transpose(1, 2)
        key_states = key_states.view(bsz, q_len, self.num_key_value_heads, self.head_dim).transpose(1, 2)
        value_states = value_states.view(bsz, q_len, self.num_key_value_heads, self.head_dim).transpose(1, 2)
                
        """applying noise before rotatry embeddings because that just feels right (expecially with RoPE)
        and not touching the attention sink because that just feels wrong"""
        
        if self.quaalude_theta > 0:
            query_states[:,:,sink_protect:, :] = get_perturbed_vectors(query_states[:,:,sink_protect:,:], self.quaalude_theta)
```

Again, the only two new lines are the last two, following all the same rules as before. This corresponds to ***Q** noise. The `sink_protect` thing is optional, and is a variable currently hardcoded to 6. I haven't tested much what sorts of effects you'd get by setting it to 0, but they might be interesting.
 
```python
        kv_seq_len = key_states.shape[-2]
        if past_key_value is not None:
            kv_seq_len += past_key_value.get_usable_length(kv_seq_len, self.layer_idx)

        cos, sin = self.rotary_emb(value_states, seq_len=kv_seq_len)
        query_states, key_states = apply_rotary_pos_emb(query_states, key_states, cos, sin, position_ids)

        if past_key_value is not None:
            cache_kwargs = {"sin": sin, "cos": cos}  # Specific to RoPE models
            key_states, value_states = past_key_value.update(key_states, value_states, self.layer_idx, cache_kwargs)
            
        key_states = repeat_kv(key_states, self.num_key_value_groups)
        value_states = repeat_kv(value_states, self.num_key_value_groups) 
        dkey_states = key_states
        dvalue_states = value_states
        
        """sliced at 6th sequence vector to not touch any attention sinks. bad juju"""
        if self.ketamine_theta > 0:
            dkey_states = torch.clone(key_states)          
            dkey_states[:,:,6:,:] = get_perturbed_vectors(key_states[:,:,6:,:], self.ketamine_theta)
        
        if self.valium_theta > 0:
            dvalue_states = torch.clone(value_states)
            dvalue_states[:,:,6:,:] = get_perturbed_vectors(value_states[:,:,6:,:], self.valium_theta)
```

Here, the last seven lines are new. Same reasoning as before. These correspond to **K** and **V** noise.

```python
        attn_weights = torch.matmul(query_states, dkey_states.transpose(2, 3)) / math.sqrt(self.head_dim)
		
        if attention_mask is not None:
            attn_weights = attn_weights + attention_mask
        # upcast attention to fp32
        attn_weights = nn.functional.softmax(attn_weights, dim=-1, dtype=torch.float32).to(query_states.dtype)
        attn_output = torch.matmul(attn_weights, dvalue_states)

        if self.adderall_theta > 0:
            attn_output[:,:,sink_protect:, :] = get_perturbed_vectors(attn_output[:,:,sink_protect:, :], self.adderall_theta)
```

Here we have **A** noise, and below is just the rest of the forward pass code.  

```python
        attn_output = attn_output.transpose(1, 2).contiguous()
        attn_output = attn_output.reshape(bsz, q_len, self.hidden_size)
        attn_output = self.o_proj(attn_output)

        return attn_output, attn_weights, past_key_value
```

And that's basically it.

------------

### 3. It's 9 o'clock Somewhere
You'll note a couple of things about the code above.

First, there's rather a lot of room for ambiguity and unease here. Specifically, how does this all play with position embedding schemes? Specifically, the ones that also rely on rotation of the *query* and *key* vectors.
The answer to which is: I wish I fucking knew, man. In the platonic ideal implementation, I'd like both **Q** and **K** noise to be applied prior to any position embedding scheme. But the Huggingface transformers library was not receptive to one of those ideas, so the canonical is **K** DRµG type is applied after position embedding, and as far as I can tell, it works just fine. So I guess, yet again with this library, as in life, there's just no wrong way to make DRµGS.
You are wholly encouraged to try designing a **pK** DRµG type variants in which noise is applied prior to the position embedding if your framework is more amenable than mine.

Second, there's a lot of references to the kv cache. Which might get pretty bad in theory. Since each decoder block caches the key and value from the hidden state generated by the previous block, which we added noise to. And so the sequence vector for token 12 at block 10 may have been conditioned on noised tokens 6-11 on the first pass. Then on the second pass, token 13 at block 10 is conditioned on noised tokens 6-12, but 12 was already itself conditioned on noise, so we're doubling up noise on top of noise. And then on the third pass it's noise on top of noise on top of noise.

From my experiments, it seems like, by some combination of the robustness of transformers, regression toward the mean, and the fact that there is no wrong way to make DRµGs, this doesn't really seem to cause much of a problem.

But, still, it would be nice to avoid the model spiraling out. But we also don't want to give up all of the benefits of kv-caching by recomputing the entire cache every time so, how do we tow this line?

------------

### 4. Write Drunk, Edit Sober

Keep track of how many tokens have been generated using DRµGS. Periodically, (or even better, when you know your model is otherwise just going to be waiting around doing nothing for a while anyway) rewind that number of tokens and feed them back through the model to regenerate fresh versions of for just that portion of the context window.

The sort of book-keeping required isn't conceptually that hard, and you can take a look around the [`cold_shower` function in the `DRUGS` class](https://github.com/EGjoni/DRUGS/blob/54a405c85243e9176814d78046cda0136648ff3c/drugs/dgenerate.py#L463 "`cold_shower` function in the `DRUGS` class") if you really want a reference implementation, but it's kind of a Huggingface specific mess, and you could almost certainly do better from scratch.


### 5.
That's it!
You should now have everything you need to turn your frameworks users into DRµG users. The rest is just the dose shaping stuff, which should be pretty self-explanatory, but feel lfree to submit an issue if you hit any snags porting (even if they're not issues with the library per se).
