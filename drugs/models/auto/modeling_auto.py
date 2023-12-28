from transformers import AutoModel as TAutoModel
from transformers import AutoModelForCausalLM as TAutoModelForCausalLM
from transformers import AutoModelForQuestionAnswering as TAutoModelForQuestionAnswering
from transformers import AutoModelForSequenceClassification as TAutoModelForSequenceClassification
from transformers import AutoModelForTokenClassification as TAutoModelForTokenClassification

from drugs.inject_mixin import InjectDrugsMixin


class AutoModel(InjectDrugsMixin, TAutoModel):
    pass


class AutoModelForCausalLM(InjectDrugsMixin, TAutoModelForCausalLM):
    pass


class AutoModelForSequenceClassification(InjectDrugsMixin, TAutoModelForSequenceClassification):
    pass


class AutoModelForQuestionAnswering(InjectDrugsMixin, TAutoModelForQuestionAnswering):
    pass


class AutoModelForTokenClassification(InjectDrugsMixin, TAutoModelForTokenClassification):
    pass
