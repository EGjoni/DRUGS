from typing import Any, Dict

import torch
from transformers.utils import ModelOutput
from transformers import AutoTokenizer, TextStreamer, GenerationConfig

def _update_model_kwargs_for_generation(
    self,
    outputs: ModelOutput,
    model_kwargs: Dict[str, Any],
    is_encoder_decoder: bool = False,
    standardize_cache_format: bool = False,
) -> Dict[str, Any]:
    # update past_key_values
    model_kwargs["past_key_values"] = self._extract_past_from_model_output(
        outputs, standardize_cache_format=standardize_cache_format
    )
    if getattr(outputs, "state", None) is not None:
        model_kwargs["state"] = outputs.state

    # update token_type_ids with last value
    if "token_type_ids" in model_kwargs:
        token_type_ids = model_kwargs["token_type_ids"]
        model_kwargs["token_type_ids"] = torch.cat([token_type_ids, token_type_ids[:, -1].unsqueeze(-1)], dim=-1)

    if not is_encoder_decoder:
        # update attention mask
        if "attention_mask" in model_kwargs:
            attention_mask = model_kwargs["attention_mask"]
            # Only this branch is changed, it's required to stop the attention_mask from extending itself too far
            attention_mask_size = model_kwargs["attention_mask"].size(-1)
            past_key_values_size = model_kwargs["past_key_values"][0][0].size(2)
            if attention_mask_size == past_key_values_size:
                model_kwargs["attention_mask"] = torch.cat(
                    [attention_mask, attention_mask.new_ones((attention_mask.shape[0], 1))], dim=-1
                )
            elif attention_mask_size > past_key_values_size:
                model_kwargs["attention_mask"] = model_kwargs["attention_mask"][..., : past_key_values_size + 1]

    else:
        # update decoder attention mask
        if "decoder_attention_mask" in model_kwargs:
            decoder_attention_mask = model_kwargs["decoder_attention_mask"]
            model_kwargs["decoder_attention_mask"] = torch.cat(
                [decoder_attention_mask, decoder_attention_mask.new_ones((decoder_attention_mask.shape[0], 1))],
                dim=-1,
            )

    return model_kwargs


def get_perturbed_vectors(input_vectors, max_theta_radians):
    r"""
        middleschool trig rotation in n-dimensional space
        max_theta_radians : defines the maximum angle in radians to rotate input vectors by in a random direction.
    """
    eps = torch.finfo(input_vectors.dtype).eps
    random_angles = torch.rand_like(input_vectors[:,:,:,0], device=input_vectors.device, dtype=input_vectors.dtype) * max_theta_radians
    #The next three lines are an old family recipe for cooking up orthogonal vectors.
    random_vectors = torch.rand_like(input_vectors)
    projections = (torch.sum(random_vectors * input_vectors, dim=-1, keepdim=True) / torch.sum(input_vectors * input_vectors, dim=-1, keepdim=True)) * input_vectors
    orthoshifts = random_vectors - projections
    #Delicious. Now sprinkle generously and knead them back into our base vectors
    input_shifts = input_vectors * torch.cos(random_angles).unsqueeze(-1)
    target_shift_magnitudes = torch.sin(random_angles).unsqueeze(-1) * torch.norm(input_vectors, dim=-1, keepdim=True)
    target_shifts = orthoshifts / torch.norm(orthoshifts, dim=-1, keepdim=True).clamp_min(eps) * target_shift_magnitudes.clamp_min(eps)
    results = input_shifts + target_shifts
    return results
