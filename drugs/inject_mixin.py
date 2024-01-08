# Most of this code was stolen from the attention_sinks repo. 
# It is completely unnecessary, but I felt weird about making a repo called DRUGS that doesn't steal anything

import types
from typing import Callable, Optional, List
import torch

from transformers import PreTrainedModel
from transformers.utils import logging
from drugs.generation.utils import _update_model_kwargs_for_generation
from drugs.models import *

logger = logging.get_logger(__name__)

#TODO
    #"falcon": "FalconModel",
    #"mpt": "MptModel",
    #"gpt_neox": "GPTNeoXModel",
    #"gptj": "GPTJModel",
    #"qwen": "QWenModel",
    #"stablelm_epoch": "StableLMEpochModel"
#falcon_drugged_attention_forward,
    #gpt_neox_drugged_attention_forward,
    #mpt_drugged_attention_forward,
    #gptj_drugged_attention_forward,

    #qwen_drugged_attention_forward,
    #stablelm_epoch_drugged_attention_forward,

MODEL_NAME_MAPPING = {
    "llama": "LlamaModel",
    "mistral": "MistralModel",
}
        
class InjectDrugsMixin:
    @classmethod
    def _inject_drugged_attention(cls, model: PreTrainedModel, **kwargs) -> Optional[int]:
        
        model_type = model.config.model_type
        from drugs.models import (
            llama_drugged_sdpa_forward,
            llama_drugged_flash2_attention_forward,
            llama_drugged_attention_forward,
            mistral_drugged_attention_forward,
        )
        
        LLAMA_ATTENTION_FORWARDS = {
            "LlamaAttention" : llama_drugged_attention_forward,
            "LlamaFlashAttention2" : llama_drugged_flash2_attention_forward,
            "LlamaSdpaAttention": llama_drugged_sdpa_forward
        }
        MISTRAL_ATTENTION_FORWARDS = {
            "MistralAttention" : mistral_drugged_attention_forward,
            #"MistralFlashAttention2" : mistral_drugged_flash2_attention_forward,
            #"MistralSdpaAttention": mistral_drugged_sdpa_forward
        }
        ATTENTION_NAME_MAPPINGS = {
            "llama": LLAMA_ATTENTION_FORWARDS,
            "mistral" : MISTRAL_ATTENTION_FORWARDS
        }

        # Not all models require updated attention forwards
        if model_type not in MODEL_NAME_MAPPING or MODEL_NAME_MAPPING[model_type] is None:
            return
        
        def overwrite_forward(module, new_func, **kwargs) -> None:
            module.forward = types.MethodType(new_func, module, **kwargs)

        return cls._call_modules_by_name(model, ATTENTION_NAME_MAPPINGS[model_type], overwrite_forward, **kwargs)
   
    @classmethod
    def _call_modules_by_name(cls, module, module_dict: str, func: Callable, **kwargs) -> int:
        for name, overwrite_with in module_dict.items():
            if module.__class__.__name__ == name:
                func(module, overwrite_with)
                return 1

        return sum(cls._call_modules_by_name(module, module_dict, func) for module in module.children())
