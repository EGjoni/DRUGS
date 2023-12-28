__version__ = "d.r.u.g.s"

from transformers import AutoTokenizer

from .models import (
    AutoModel,
    AutoModelForCausalLM,
    AutoModelForQuestionAnswering,
    AutoModelForSequenceClassification,
    AutoModelForTokenClassification,
    LlamaForCausalLM,
    LlamaForSequenceClassification,
    LlamaModel
)

"""
    FalconForCausalLM,
    FalconForQuestionAnswering,
    FalconForSequenceClassification,
    FalconForTokenClassification,
    FalconModel,
    FalconPreTrainedModel,
    GPTJForCausalLM,
    GPTJForQuestionAnswering,
    GPTJForSequenceClassification,
    GPTJModel,
    GPTJPreTrainedModel,
    GPTNeoXForCausalLM,
    GPTNeoXForQuestionAnswering,
    GPTNeoXForSequenceClassification,
    GPTNeoXForTokenClassification,
    GPTNeoXModel,
    GPTNeoXPreTrainedModel,
    MistralForCausalLM,
    MistralForSequenceClassification,
    MistralModel,
    MptForCausalLM,
    MptForQuestionAnswering,
    MptForSequenceClassification,
    MptForTokenClassification,
    MptModel,
    MptPreTrainedModel
"""