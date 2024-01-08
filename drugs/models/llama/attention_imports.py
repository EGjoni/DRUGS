from drugs.generation.utils import get_perturbed_vectors, verifyAverage
from transformers.cache_utils import Cache
from transformers.models.llama.modeling_llama import repeat_kv, rotate_half, apply_rotary_pos_emb, _get_unpad_data
import math
import torch
import torch.nn.functional as F
import torch.utils.checkpoint
import torch.random
from torch import nn
from typing import Optional, Tuple
import warnings
import transformers.utils.logging as logging