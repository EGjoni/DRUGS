import warnings
from transformers import LlamaForCausalLM as TLlamaForCausalLM
from transformers import LlamaForSequenceClassification as TLlamaForSequenceClassification
from transformers.models.llama.modeling_llama import LlamaModel, LlamaAttention
from transformers import LlamaPreTrainedModel as TLlamaPreTrainedModel

from drugs.inject_mixin import InjectDrugsMixin
from transformers import LlamaPreTrainedModel as TLlamaPreTrainedModel

class LlamaPreTrainedModel(InjectDrugsMixin, TLlamaPreTrainedModel):
    pass

class LlamaForCausalLM(LlamaPreTrainedModel, TLlamaForCausalLM):
    pass

class LlamaForSequenceClassification(LlamaPreTrainedModel, TLlamaForSequenceClassification):
    pass