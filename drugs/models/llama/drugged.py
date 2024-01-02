"""
Adapted from https://github.com/mit-han-lab/streaming-llm
"""


import math
from typing import Optional, Tuple
import warnings

import torch
import torch.nn.functional as F
import torch.utils.checkpoint
import torch.random
from torch import nn
from transformers.models.llama.modeling_llama import repeat_kv, rotate_half, apply_rotary_pos_emb
from drugs.generation.utils import get_perturbed_vectors, verifyAverage
from transformers.cache_utils import Cache

__all__ = ["llama_drugged_attention_forward"]


def llama_drugged_attention_forward(
        self,
        hidden_states: torch.Tensor,
        attention_mask: Optional[torch.Tensor] = None,
        position_ids: Optional[torch.LongTensor] = None,
        past_key_value: Optional[Cache] = None,
        output_attentions: bool = False,
        use_cache: bool = False,
        **kwargs,
    ) -> Tuple[torch.Tensor, Optional[torch.Tensor], Optional[Tuple[torch.Tensor]]]:
        if "padding_mask" in kwargs:
            warnings.warn(
                "Passing `padding_mask` is deprecated and will be removed in v4.37. Please make sure use `attention_mask` instead.`"
            )

        bsz, q_len, _ = hidden_states.size()
        sink_protect = (position_ids < 6).sum().item()
        if self.heroine_theta > 0:
            hidden_states[:,sink_protect:,:] = get_perturbed_vectors(hidden_states[:,sink_protect:,:].unsqueeze(0), self.heroine_theta).squeeze(0)
            
        if self.config.pretraining_tp > 1:
            raise RuntimeError(
                """I have no clue what effect this has on pretraining and I suspect you weren't trying to use this as a regularization
                so I'm throwing an error at you instead of letting you train with the active."""
            )
        else:
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

        kv_seq_len = key_states.shape[-2]
        if past_key_value is not None:
            if self.layer_idx is None:
                raise ValueError(
                    f"The cache structure has changed since version v4.36. If you are using {self.__class__.__name__} "
                    "for auto-regressive decoding with k/v caching, please make sure to initialize the attention class "
                    "with a layer index."
                )
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

        attn_weights = torch.matmul(query_states, dkey_states.transpose(2, 3)) / math.sqrt(self.head_dim)

        if attn_weights.size() != (bsz, self.num_heads, q_len, kv_seq_len):
            raise ValueError(
                f"Attention weights should be of size {(bsz, self.num_heads, q_len, kv_seq_len)}, but is"
                f" {attn_weights.size()}"
            )

        if attention_mask is not None:
            if attention_mask.size() != (bsz, 1, q_len, kv_seq_len):
                raise ValueError(
                    f"Attention mask should be of size {(bsz, 1, q_len, kv_seq_len)}, but is {attention_mask.size()}"
                )
            attn_weights = attn_weights + attention_mask

        # upcast attention to fp32
        attn_weights = nn.functional.softmax(attn_weights, dim=-1, dtype=torch.float32).to(query_states.dtype)
        attn_weights = nn.functional.dropout(attn_weights, p=self.attention_dropout, training=self.training)
        attn_output = torch.matmul(attn_weights, dvalue_states)

        if self.adderall_theta > 0:
            attn_output[:,:,sink_protect:, :] = get_perturbed_vectors(attn_output[:,:,sink_protect:, :], self.adderall_theta)

        if attn_output.size() != (bsz, self.num_heads, q_len, self.head_dim):
            raise ValueError(
                f"`attn_output` should be of size {(bsz, self.num_heads, q_len, self.head_dim)}, but is"
                f" {attn_output.size()}"
            )

        attn_output = attn_output.transpose(1, 2).contiguous()
        attn_output = attn_output.reshape(bsz, q_len, self.hidden_size)

        if self.config.pretraining_tp > 1:
            attn_output = attn_output.split(self.hidden_size // self.config.pretraining_tp, dim=2)
            o_proj_slices = self.o_proj.weight.split(self.hidden_size // self.config.pretraining_tp, dim=1)
            attn_output = sum([F.linear(attn_output[i], o_proj_slices[i]) for i in range(self.config.pretraining_tp)])
        else:
            attn_output = self.o_proj(attn_output)

        if not output_attentions:
            attn_weights = None

        return attn_output, attn_weights, past_key_value