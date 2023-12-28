# Most of this code was stolen from the attention_sinks repo. 
# It is completely unnecessary, but I felt weird about making a repo called DRUGS that doesn't steal anything

import types
from typing import Callable, Optional, List
import torch

from transformers import PreTrainedModel
from transformers.utils import logging
from drugs.generation.utils import _update_model_kwargs_for_generation

logger = logging.get_logger(__name__)

MODEL_NAME_MAPPING = {
    "llama": "LlamaModel",
    #"falcon": "FalconModel",
    #"mpt": "MptModel",
    #"gpt_neox": "GPTNeoXModel",
    #"gptj": "GPTJModel",
    #"mistral": "MistralModel",
    #"qwen": "QWenModel",
    #"stablelm_epoch": "StableLMEpochModel"
}

#TODO: support flash attention 2 and sdpa 
ATTENTION_NAME_MAPPING = {
    "llama": "LlamaAttention",
    #"falcon": "FalconAttention",
    #"mpt": "MptAttention",
    #"gpt_neox": "GPTNeoXAttention",
    #"gptj": "GPTJAttention",
    #"mistral": "MistralAttention",
    #"qwen": "QWenAttention",
    #"stablelm_epoch": "Attention",
}
KV_DIM_MAPPING = {
    "llama": (2, 2),
    "falcon": (2, 2),
    "mpt": (2, 2),
    "gpt_neox": (2, 2),
    "gptj": (2, 2),
    "mistral": (2, 2),
    "qwen": (1, 1),
    "stablelm_epoch": (2, 2),
}
        
class InjectDrugsMixin:
    @classmethod
    def _inject_drugged_attention(cls, model: PreTrainedModel, **kwargs) -> Optional[int]:
        
        model_type = model.config.model_type

        from drugs.models import (
            #falcon_drugged_attention_forward,
            #gpt_neox_drugged_attention_forward,
            #mpt_drugged_attention_forward,
            #gptj_drugged_attention_forward,
            llama_drugged_attention_forward,
            #mistral_drugged_attention_forward,
            #qwen_drugged_attention_forward,
            #stablelm_epoch_drugged_attention_forward,
        )

        ATTENTION_FORWARD_MAPPING = {
            "llama": llama_drugged_attention_forward,
            #"falcon": falcon_drugged_attention_forward,
            #"mpt": None,
            #"gpt_neox": gpt_neox_drugged_attention_forward,
            #"gptj": gptj_drugged_attention_forward,
            #"mistral": mistral_drugged_attention_forward,
            #"qwen": qwen_drugged_attention_forward,
            #"stablelm_epoch": stablelm_epoch_drugged_attention_forward,
        }
        

        # Not all models require updated attention forwards
        if ATTENTION_FORWARD_MAPPING[model_type] is None:
            return

        #TODO: support flash attention 2 and sdpa 

        def overwrite_forward(module, **kwargs) -> None:
            module.forward = types.MethodType(ATTENTION_FORWARD_MAPPING[model_type], module, **kwargs)

        return cls._call_modules_by_name(model, ATTENTION_NAME_MAPPING[model_type], overwrite_forward, **kwargs)
   
    @classmethod
    def _call_modules_by_name(cls, module, target_name: str, func: Callable, **kwargs) -> int:
        if module.__class__.__name__ == target_name:
            func(module)
            return 1

        return sum(cls._call_modules_by_name(module, target_name, func) for module in module.children())
