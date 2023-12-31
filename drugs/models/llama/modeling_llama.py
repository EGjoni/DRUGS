import warnings
from transformers import LlamaForCausalLM as TLlamaForCausalLM
from transformers import LlamaForSequenceClassification as TLlamaForSequenceClassification
from transformers import LlamaModel
from transformers import LlamaPreTrainedModel as TLlamaPreTrainedModel
from transformers.models.llama.modeling_llama import LlamaDecoderLayer
from transformers.models.llama.modeling_llama import LlamaConfig, LlamaRMSNorm
import torch.nn as nn
from drugs.inject_mixin import InjectDrugsMixin
import torch
from typing import Optional, Tuple, List, Union

class LlamaPreTrainedModel(InjectDrugsMixin, TLlamaPreTrainedModel):
    pass

class LlamaForCausalLM(LlamaPreTrainedModel, TLlamaForCausalLM):
    pass

class LlamaForSequenceClassification(LlamaPreTrainedModel, TLlamaForSequenceClassification):
    pass