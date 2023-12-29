import torch
import json, os, msgpack
from transformers.utils import logging
import types
from typing import Optional, List, Callable
from drugs.inject_mixin import InjectDrugsMixin, ATTENTION_NAME_MAPPING, MODEL_NAME_MAPPING, KV_DIM_MAPPING
from drugs.generation.utils import _update_model_kwargs_for_generation
from transformers import AutoTokenizer, TextStreamer, GenerationConfig
current_script_dir = os.path.dirname(os.path.abspath(__file__))
logger = logging.get_logger(__name__)
fNone = object()

class DRUGS:
    dose_theta = {'A': 0, 'Q': 0,  'K': 0, 'V': 0}
    dose_multiplier = 1
    r_seed = -1
    state_log = {}
    do_record = False
    dose_shapes = {'A': None, 'Q': None,  'K': None, 'V': None}
    dose_mode =  {'A': 'interpolate', 'Q': 'interpolate',  'K': 'interpolate', 'V': 'interpolate'}
    past_key_values = None
    sober_interval = 420
    model = None
    dirty_count = -6
    cached_tokens = None
    top_log_cache = [] #for_debugging
    
    def __init__(self, a_dose=0, q_dose=0, k_dose=0, v_dose=0, a_shape=None, q_shape=None, k_shape = None, v_shape = None):
        self.set_A_dose_theta(a_dose)
        self.set_Q_dose_theta(q_dose)
        self.set_K_dose_theta(k_dose)
        self.set_V_dose_theta(v_dose)
        if a_shape is not None:
            self.set_A_dose_shape(a_shape)
        if q_shape is not None:
            self.set_Q_dose_shape(q_shape)
        if k_shape is not None:
            self.set_K_dose_shape(k_shape)
        if v_shape is not None:
            self.set_V_dose_shape(v_shape)
            
    
    def inject(self, model, streamer=None, tokenizer= None):
        return self.do_some(model, streamer, tokenizer)        
    
           
    def generate(self,
            input_ids: torch.LongTensor = None,
            past_key_values: Optional[List[torch.FloatTensor]] = fNone, #explicitly provide "None" to start a new generation from scratch
            streamer: Optional[TextStreamer] = None,
            tokenizer: Optional[AutoTokenizer] = None, # provide seperately from streamer to print to console synchronously
            generation_min: Optional[int] = 1,
            generation_max: Optional[int] = 100000,
            sampler : Optional[Callable[[torch.tensor, #logits for you
                                         torch.tensor, #hidden states for you
                                         ], torch.tensor #selected token id for me
                                ]] = None
        ):
        r""" 
            the last sampler parameter allows you to pass in some sampling callback, provides logits
        """
        if past_key_values is not fNone:
            self.past_key_values = past_key_values
            self.cached_tokens = None
        with torch.no_grad():
            if self.cached_tokens is None:
                self.cached_tokens = torch.empty((*input_ids.shape[:-1], 0), dtype=input_ids.dtype)
                self.dirty_count = -6
            
            chunks = torch.split(input_ids, 32, dim=1)
            gend_tokens = torch.empty((*input_ids.shape[:-1], 0), dtype=input_ids.dtype)
            
            if streamer is not None:
                self.streamer = streamer
                self.tokenizer = tokenizer if tokenizer is not None else streamer.tokenizer
            if tokenizer is not None: 
                self.tokenizer = tokenizer
            
            self.maybe_print(streamer, tokenizer, input_ids)
            
            old_dose_multiplier = self.get_dose_multiplier()
            self.set_dose_multiplier(0) #don't noise anything until we start generating from it
            for i, chunk in enumerate(chunks):
                self.cached_tokens = torch.cat((self.cached_tokens, chunk), dim = -1)
                outputs = self.model(input_ids=chunk, past_key_values=self.past_key_values, use_cache=True)
                self.past_key_values, logits = outputs.past_key_values, outputs.logits
                
                #del outputs
                #torch.cuda.empty_cache()

            self.set_dose_multiplier(old_dose_multiplier)
            if sampler is None:
                sampler = self.argmax_select_next_token
                
            next_token = sampler(logits, None).unsqueeze(0)
            
            self.maybe_print(streamer, tokenizer, next_token)
            
            gend_tokens = torch.cat((gend_tokens, next_token), dim = -1)
            
            
            while gend_tokens.shape[1] < generation_max:
                
                self.past_key_values = self.cold_shower()
                
                if self.is_not_stop_condition(next_token, gend_tokens.shape[1], generation_min, generation_max, streamer):
                    outputs = self.model(input_ids=next_token, past_key_values= self.past_key_values, use_cache=True)
                    next_token = sampler(outputs.logits, None).unsqueeze(0)
                    self.past_key_values = outputs.past_key_values
                    gend_tokens = torch.cat((gend_tokens, next_token), dim = -1)
                    #self.top_log_cache.append(torch.max(outputs.logits.squeeze(0)[0,:]).item())
                    self.maybe_print(streamer, tokenizer, next_token)                    
                    self.cached_tokens = torch.cat((self.cached_tokens, next_token), dim = -1)
                    self.dirty_count += 1
                else: 
                    break

            self.past_key_values = self.cold_shower()
            
            if streamer is not None:
                streamer.put(streamer.tokenizer.encode(' ', return_tensors="pt"))        
        return gend_tokens
    
    def argmax_select_next_token(self, logits, hidden_states):
        next_token_logits = logits[:, -1, :]
        top_k_indices = torch.topk(next_token_logits, k=1, dim=-1).indices[0]
        return top_k_indices[0].unsqueeze(0)
                  
    def record_value(self, token_num, value):
        if token_num not in self.state_log:
            self.state_log[token_num] = []
        self.state_log[token_num].append(value)
    
    def clear_traces(self):
        self.state_log = {}
    
    def set_record_hidden_path(self, state):
        self.do_record = state
        
    def get_recording_state(self):
        return self.do_record
    
    def get_recorded_values(self):
        return self.state_log
    
        
    def set_dose_theta(self, radians):
        self.set_A_dose_theta(radians)
    def set_A_dose_theta(self, radians):
        self._set_typed_dose_theta(radians, 'A')
    def set_K_dose_theta(self, radians):
        self._set_typed_dose_theta(radians, 'K')
    def set_Q_dose_theta(self, radians):
        self._set_typed_dose_theta(radians, 'Q')
    def set_V_dose_theta(self, radians):
        self._set_typed_dose_theta(radians, 'V')
        
    def _set_typed_dose_theta(self, radians, type):
        self.dose_theta[type] = radians
        self._update_layer_doses()
    
    
    def get_dose_theta(self, idx=None, total_layers=1):
        return self.get_A_dose_theta(idx, total_layers)
    def get_A_dose_theta(self, idx=None, total_layers=1):
        return self._get_typed_dose_theta(idx, total_layers, 'A')
    def get_K_dose_theta(self, idx=None, total_layers=1):
        return self._get_typed_dose_theta(idx, total_layers, 'K')
    def get_Q_dose_theta(self, idx=None, total_layers=1):
        return self._get_typed_dose_theta(idx, total_layers, 'Q')
    def get_V_dose_theta(self, idx=None, total_layers=1):
        return self._get_typed_dose_theta(idx, total_layers, 'V')
    
    def _get_typed_dose_theta(self, idx=None, total_layers=1, type='A'):
        if idx is not None and self.dose_shapes[type] is not None:
            return self.get_tissue_bioavailability(idx, total_layers, type)*self.dose_theta[type]*self.dose_multiplier
        else:
            return self.dose_theta[type]*self.dose_multiplier
           
    def set_compress(self, value):
        self.compress = value
    
    def get_compress(self):
        return self.compress
    
    def set_dose_shape(self, shape):
        self.set_A_dose_shape(self, shape)
    def set_A_dose_shape(self, shape):
        self._set_typed_dose_shape(shape[0], shape[1], 'A')    
    def set_K_dose_shape(self, shape):
        self._set_typed_dose_shape(shape[0], shape[1], 'K')   
    def set_Q_dose_shape(self, shape):
        self._set_typed_dose_shape(shape[0], shape[1], 'Q') 
    def set_V_dose_shape(self, shape):
        self._set_typed_dose_shape(shape[0], shape[1], 'V') 

    def _set_typed_dose_shape(self, shape, mode, type):
        r'''
            shape is specified as an array of dicts, where each dict specifies
            {'depth': a value from 0-1 indicating the layer number as a ratio of the total layers, 
            'peakratio': indicating a scalar of the base dose_theta}
            mode: determines how to treat dose_theta between layers. Options are
                'interpolate' : smoothly increase and decrease the dose between values
                'ceil': always sets to the highest peak_ratio of the range a layer may fall within
                'floor': always sets to the lowest value of a range peak_ratio may fall within
        '''
        self.dose_shapes[type] = sorted(shape, key=lambda x: x['depth'])
        self.dose_mode[type] = mode
        self._update_layer_doses()
        
    
    def get_tissue_bioavailability(self, idx, total_layers, type = 'A'):
        layer_depth = idx/total_layers
        dose_shaper = self.dose_shapes[type]
        av1 = dose_shaper[0]
        av2 = dose_shaper[len(dose_shaper)-1]
        loop = True
        
        if layer_depth <= av1['depth']:
            av2 = av1
            loop = False
        if layer_depth >= av2['depth']:
            av1 = av2
            loop = False
        
        if loop:
            for d1, d2 in zip(dose_shaper, dose_shaper[1:]):
                if d1['depth'] <= layer_depth and d2['depth'] >= layer_depth:
                    av1 = d1
                    av2 = d2
                    break
        
        equal = False
        if av1['depth'] == av2['depth']:
            equal = True       
        
        if self.dose_mode[type] == 'ceil' or equal:
            return max(av1['peakratio'], av2['peakratio'])
        elif self.dose_mode[type] == 'floor':
            return min(av1['peakratio'], av2['peakratio'])
        else:
            av1d = av1['depth']
            av2d = av2['depth']
            av1pr = av1['peakratio']
            av2pr = av2['peakratio']
            ldr = (layer_depth-av1d) / (av2d - av1d)
            return (ldr*(av2pr - av1pr)) + av1pr
    
    
    def _update_layer_doses(self):
        if self.model is None:
            return
        layerct = len(self.model.model.layers)
        for idx, layer in enumerate(self.model.model.layers):
            layer.total_layers = layerct
            layer.layer_idx = idx
            layer.dgenerator = self.model.dgenerator
            layer.self_attn.adderall_theta = self.get_A_dose_theta(idx, layerct)
            layer.self_attn.quelude_theta = self.get_Q_dose_theta(idx, layerct)
            layer.self_attn.ketamine_theta = self.get_K_dose_theta(idx, layerct)
            layer.self_attn.valium_theta = self.get_V_dose_theta(idx, layerct)
    
    def get_dose_multiplier(self):
        return self.dose_multiplier    
    
    def set_dose_multiplier(self, multiplier):
        self.dose_multiplier = multiplier
        self._update_layer_doses()
        
    def set_seed(self, seed):        
        self.r_seed = seed
    
    def get_seed(self):
        return self.r_seed
    
    def save_trace(self, experiment, subtype, injection_depth, logits, top_k, hidden_states, tokenizer):
        r"""saves hidden states and dosage parameters to a msgpack file for experimenting"""
        import torch.nn.functional as F
        import torch
        import numpy as np
        
        base_dir = 'experiments'
        last_logits = logits[0, -1, :]
        probabilities = F.softmax(torch.tensor(last_logits.to('cpu')), dim=-1).numpy()
        # Get the indices of the top_k probabilities
        top_k_indices = np.argsort(probabilities)[-top_k:]
        tokens = [tokenizer.decode([idx]) for idx in top_k_indices]
        top_k_logits = last_logits[top_k_indices].to('cpu').tolist()
        top_k_probs = probabilities[top_k_indices].tolist()
        top_k_array = []
        for idx, t in enumerate(tokens):
            top_k_array.append({'token': t, 'logit': top_k_logits[idx], 'prob': top_k_probs[idx], 'id': f"{top_k_indices[idx]}"})
        
        athetadeg = f"{(int(self.dose_theta['A']/3.14*180))}A"
        qthetadeg = f"{(int(self.dose_theta['Q']/3.14*180))}Q"
        kthetadeg = f"{(int(self.dose_theta['K']/3.14*180))}K"
        vthetadeg = f"{(int(self.dose_theta['V']/3.14*180))}V"
        
        file_path = os.path.join(current_script_dir, '..', base_dir, 'results', experiment, subtype, f"injection_depth_{injection_depth}_({athetadeg}_{qthetadeg}_{kthetadeg}_{vthetadeg})-dose.msgpack")
        print(f"saving: {file_path}")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        prediction_states = []
        for l in hidden_states:
            veclist = l[0, -1, :].tolist()
            prediction_states.append(veclist)
            
        store = {
            'dose_shape': self.dose_shapes, 
            'dose': self.dose_theta, 
            'dose_mode': self.dose_mode, 
            'hidden_state_embedding': prediction_states,
            'top_k': top_k_array
        }
        with open(file_path, 'wb') as file:
            packed =  msgpack.packb(store)
            file.write(packed)
            
        
    def cold_shower(self, force_clean = False):
        r"""
        brings the cached kv vectors back to a sober baseline
        """
        with torch.no_grad():
            if self.past_key_values is None or self.dirty_count <= 0:
                return self.past_key_values
            if self.dirty_count >= self.sober_interval or force_clean:
                max_clean = min(self.past_key_values[0][0].shape[2] - 6, self.dirty_count)
                new_past_key_values = self._get_truncated_cache(self.past_key_values, max_clean)
                           
                regen_tokens = self.cached_tokens[:, -(max_clean+1):-1]        
                old_dose_multiplier = self.get_dose_multiplier()
                self.set_dose_multiplier(0)
                outputs = self.model(input_ids=regen_tokens, past_key_values=new_past_key_values, use_cache=True)
                
                #TODO: Figure out why this doesn't work the first time when no noise is injected.
                """
                if torch.max(self.past_key_values[20][0] - outputs.past_key_values[20][0]) > 0:
                    self.past_key_values = outputs.past_key_values
                    self.cold_shower()
                """
                    
                self.set_dose_multiplier(old_dose_multiplier)    
                self.past_key_values = outputs.past_key_values
                self.dirty_count -= max_clean
                del new_past_key_values
                torch.cuda.empty_cache()
        return self.past_key_values
    
    def _get_truncated_cache(self, to_trunc, trunc_by):
        result = []
        for k, v in to_trunc:
            result.append((
                k[:, :, :-(trunc_by), :],
                v[:, :, :-(trunc_by), :]))
        return result
    
    def decode(self, input_ids_or_logits):
        if self.tokenizer is not None:
            if len(input_ids_or_logits.shape)>2:
                input_ids = self.argmax_select_next_token(input_ids_or_logits, None)
            else: 
                input_ids = input_ids_or_logits
            try:
                return self.tokenizer.decode(input_ids)
            finally:
                return self.tokenizer.decode(input_ids.squeeze(0))
    
    def maybe_print(self, streamer, tokenizer, input_ids, loop=False):
        result = ''
        if loop is True:
            aslist = input_ids.tolist()
            for i, t in enumerate(aslist):
                if streamer is not None:
                    streamer.put(input_ids[0][i])
                if tokenizer is not None:
                    s = tokenizer.decode(t)
                    print(s, end="")
                    result += s
        else:
            if streamer is not None:
                streamer.put(input_ids.squeeze(0))
            if tokenizer is not None:
                result = tokenizer.decode(input_ids.squeeze(0))
                print(result, end="")
        return result
                
        
    def set_sobering_rate(self, sober_interval):
        r"""specifies the frequency with which the model should recompute drugged hidden states
        larger values are faster but less theoretically pure
        """
        if sober_interval < self.sober_interval:
            self.cold_shower()
        self.sober_interval = sober_interval
    
    def is_not_stop_condition(self, next_token_id, current_count, generation_min, generation_max, streamer):
        if streamer is not None:
            if next_token_id.item() == streamer.tokenizer.eos_token_id and current_count >= generation_min:
                return False
        if current_count >= generation_max:
            return False
        return True
    
    def do_some(self, model, streamer=None, tokenizer=None):
        self.model = model
        model_type = model.config.model_type
        if streamer is not None:
            self.streamer = streamer
            self.tokenizer = tokenizer if tokenizer is not None else streamer.tokenizer
        if tokenizer is not None: 
            self.tokenizer = tokenizer
        if model_type not in MODEL_NAME_MAPPING:
            raise NotImplementedError(
                f"`drugs` does not support models with the `{model_type}` architecture at this time."
            )
        self.model.dgenerator = self    
        self.model.Dgenerate = self.generate
        self.model.cold_shower = self.cold_shower
        layerct = len(model.model.layers)
        #for idx, layer in enumerate(model.model.layers):
        #    layer.total_layers = layerct
        #    layer.layer_idx = idx
        self._update_layer_doses()
        logger.warn(
                f"[Drugs] Injected drugs into {layerct} attention class{'es' if layerct != 1 else ''}."
            )
        
        InjectDrugsMixin._inject_drugged_attention(model)
        model._update_model_kwargs_for_generation = types.MethodType(_update_model_kwargs_for_generation, model)
        
        return self.model
    
    
import numpy as np
import torch
import torch.nn.functional as F
def print_top_k_logits_histogram(logits, tokenizer, top_k=10, max_width=100):
    """
    Print a histogram of the top_k predicted next tokens' logits in the console,
    after applying a softmax to convert logits to probabilities. The token text
    and its probability are right-aligned.

    :param logits: A numpy array of logits from a language model prediction.
    :param tokenizer: The tokenizer used with the model to map indices to tokens.
    :param top_k: Number of top logits to display in the histogram.
    :param max_width: The maximum width of the histogram in characters.
    """
    
    last_logits = logits[0, -1, :]
    probabilities = F.softmax(torch.tensor(last_logits), dim=-1).numpy()
    top_k_indices = np.argsort(probabilities)[-top_k:]
    top_k_probs = probabilities[top_k_indices]
    tokens = [tokenizer.decode([idx]) for idx in top_k_indices]
    max_token_length = max(len(token) for token in tokens)
    max_prob = max(top_k_probs)
    scaled_probs = (top_k_probs / max_prob) * max_width
    print("--- \n")
    for token, prob, raw_prob in zip(tokens, scaled_probs, top_k_probs):
        bar = '#' * int(prob)
        prob_text = f"{raw_prob * 100:.2f}%".rjust(25)  # Probability formatted to two decimal places
        print(f"{bar.ljust(max_width)} {token.rjust(max_token_length*2)}{prob_text}")
    print("---::::"+tokens[len(tokens)-1]+":::   \n")