from transformers.utils import is_flash_attn_2_available
from drugs.models.llama.attention_imports import *
if is_flash_attn_2_available():
    from flash_attn import flash_attn_func, flash_attn_varlen_func
    from flash_attn.bert_padding import index_first_axis, pad_input, unpad_input  # noqa
    

def llama_drugged_flash2_attention_forward(
        self,
        hidden_states: torch.Tensor,
        attention_mask: Optional[torch.LongTensor] = None,
        position_ids: Optional[torch.LongTensor] = None,
        past_key_value: Optional[Cache] = None,
        output_attentions: bool = False,
        use_cache: bool = False,
        **kwargs,
    ) -> Tuple[torch.Tensor, Optional[torch.Tensor], Optional[Tuple[torch.Tensor]]]:
        # LlamaFlashAttention2 attention does not support output_attentions
        if "padding_mask" in kwargs:
            warnings.warn(
                "Passing `padding_mask` is deprecated and will be removed in v4.37. Please make sure use `attention_mask` instead.`"
            )

            # overwrite attention_mask with padding_mask
            attention_mask = kwargs.pop("padding_mask")

        output_attentions = False

        bsz, q_len, _ = hidden_states.size()
        sink_protect = (position_ids < 6).sum().item()
        if self.heroine_theta > 0:
            hidden_states[:,sink_protect:,:] = get_perturbed_vectors(hidden_states[:,sink_protect:,:].unsqueeze(0), self.heroine_theta).squeeze(0)

        query_states = self.q_proj(hidden_states)
        key_states = self.k_proj(hidden_states)
        value_states = self.v_proj(hidden_states)

        # Flash attention requires the input to have the shape
        # batch_size x seq_length x head_dim x hidden_dim
        # therefore we just need to keep the original shape
        query_states = query_states.view(bsz, q_len, self.num_heads, self.head_dim).transpose(1, 2)
        key_states = key_states.view(bsz, q_len, self.num_key_value_heads, self.head_dim).transpose(1, 2)
        value_states = value_states.view(bsz, q_len, self.num_key_value_heads, self.head_dim).transpose(1, 2)

        if self.quaalude_theta > 0:
            query_states[:,:,sink_protect:, :] = get_perturbed_vectors(query_states[:,:,sink_protect:,:], self.quaalude_theta)

        kv_seq_len = key_states.shape[-2]
        if past_key_value is not None:
            kv_seq_len += past_key_value.get_usable_length(kv_seq_len, self.layer_idx)
        cos, sin = self.rotary_emb(value_states, seq_len=kv_seq_len)
        query_states, key_states = apply_rotary_pos_emb(query_states, key_states, cos, sin, position_ids)

        if past_key_value is not None:
            cache_kwargs = {"sin": sin, "cos": cos}  # Specific to RoPE models
            key_states, value_states = past_key_value.update(key_states, value_states, self.layer_idx, cache_kwargs)

        dkey_states = key_states
        dvalue_states = value_states
        
        """sliced at 6th sequence vector to not touch any attention sinks. bad juju"""
        if self.ketamine_theta > 0:
            dkey_states = torch.clone(key_states)          
            dkey_states[:,:,6:,:] = get_perturbed_vectors(key_states[:,:,6:,:], self.ketamine_theta)
        
        if self.valium_theta > 0:
            dvalue_states = torch.clone(value_states)
            dvalue_states[:,:,6:,:] = get_perturbed_vectors(value_states[:,:,6:,:], self.valium_theta)

        # TODO: These transpose are quite inefficient but Flash Attention requires the layout [batch_size, sequence_length, num_heads, head_dim]. We would need to refactor the KV cache
        # to be able to avoid many of these transpose/reshape/view.
        query_states = query_states.transpose(1, 2)
        dkey_states = dkey_states.transpose(1, 2)
        dvalue_states = dvalue_states.transpose(1, 2)

        dropout_rate = self.attention_dropout if self.training else 0.0

        # In PEFT, usually we cast the layer norms in float32 for training stability reasons
        # therefore the input hidden states gets silently casted in float32. Hence, we need
        # cast them back in the correct dtype just to be sure everything works as expected.
        # This might slowdown training & inference so it is recommended to not cast the LayerNorms
        # in fp32. (LlamaRMSNorm handles it correctly)

        input_dtype = query_states.dtype
        if input_dtype == torch.float32:
            # Handle the case where the model is quantized
            if hasattr(self.config, "_pre_quantization_dtype"):
                target_dtype = self.config._pre_quantization_dtype
            else:
                target_dtype = self.q_proj.weight.dtype

            logger.warning_once(
                f"The input hidden states seems to be silently casted in float32, this might be related to"
                f" the fact you have upcasted embedding or layer norm layers in float32. We will cast back the input in"
                f" {target_dtype}."
            )

            query_states = query_states.to(target_dtype)
            dkey_states = dkey_states.to(target_dtype)
            dvalue_states = dvalue_states.to(target_dtype)

        attn_output = self._flash_attention_forward(
            query_states, dkey_states, dvalue_states, attention_mask, q_len, dropout=dropout_rate
        )

        if self.adderall_theta > 0:
            attn_output[:,:,sink_protect:, :] = get_perturbed_vectors(attn_output[:,:,sink_protect:, :], self.adderall_theta)
            
        attn_output = attn_output.reshape(bsz, q_len, self.hidden_size).contiguous()
        
        attn_output = self.o_proj(attn_output)

        if not output_attentions:
            attn_weights = None

        return attn_output, attn_weights, past_key_value