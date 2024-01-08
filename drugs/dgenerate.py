import torch
import json, os, msgpack
from transformers.utils import logging
import types
import inspect
import copy
from typing import Optional, List, Callable
from drugs.inject_mixin import InjectDrugsMixin, MODEL_NAME_MAPPING
from transformers import GenerationMixin
from transformers.cache_utils import DynamicCache
from transformers.generation.utils import LogitsProcessorList, StoppingCriteriaList

from transformers import AutoTokenizer, TextStreamer, GenerationConfig
current_script_dir = os.path.dirname(os.path.abspath(__file__))
logger = logging.get_logger(__name__)
fNone = object()

class DRUGS:
    dose_theta = {'H': 0, 'A': 0, 'Q': 0,  'K': 0, 'V': 0}
    dose_multiplier = 1
    r_seed = -1
    state_log = {}
    do_record = False
    dose_shapes = {'H': None, 'A': None, 'Q': None,  'K': None, 'V': None}
    dose_mode =  {'H': 'interpolate', 'A': 'interpolate', 'Q': 'interpolate',  'K': 'interpolate', 'V': 'interpolate'}
    past_key_values = DynamicCache()
    sober_interval = 420
    model = None
    dirty_count = -6
    cached_tokens = None
    top_log_cache = [] #for_debugging
    
    def __init__(self, h_dose = 0, a_dose=0, q_dose=0, k_dose=0, v_dose=0, h_shape=None, a_shape=None, q_shape=None, k_shape = None, v_shape = None, tokenizer= None):
        self.set_H_dose_theta(h_dose)
        self.set_A_dose_theta(a_dose)
        self.set_Q_dose_theta(q_dose)
        self.set_K_dose_theta(k_dose)
        self.set_V_dose_theta(v_dose)
        if h_shape is not None:
            self.set_A_dose_shape(h_shape)
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
            min_new_tokens: Optional[int] = None,
            max_new_tokens: Optional[int] = 32000,
            logits_processor: Optional[LogitsProcessorList] = None,
            stopping_criteria: Optional[StoppingCriteriaList] = None,
            negative_prompt_ids: Optional[torch.Tensor] = None, #I really hope no one uses these because I have no clue if it works.
            negative_prompt_attention_mask: Optional[torch.Tensor] = None,
            sampler : Optional[Callable[[torch.tensor, #logits and scores for you
                                         torch.tensor, #hidden states for you
                                         ], torch.tensor #selected token id for me
                                ]] = None,
            protect_inputs: Optional[bool] = True
        ):
        r""" 
            past_key_values -- you must explicitly set this to None if you want to start a new sequence, otherwise Dgenerate will continue where you left off.
            protect_inputs -- by default, DGenerate does not add noise to the initial inputs so as to maintain
                a clean baseline. Setting to false will override this behavior, for increased variety but less theoretical purity
            sampler -- parameter allows you to pass in some sampling callback, 
                        provides logits and logitprocessor scores, expects you to provide the selected token.
                        the default is just argmax. 
                        Note that for flexibility, logits are provided as predictions for every input token,
                        but scores are provided only for the predicted next token. You can convert logits to the
                        same shape with logits[:,-1,:]
                        the sampler callback is expected to return a tensor of shape [1]
        """
        if past_key_values is not fNone:
            self.past_key_values = past_key_values
            self.cached_tokens = None
        with torch.no_grad():
            if sampler is None:
                sampler = self.argmax_select_next_token
            if self.cached_tokens is None:
                self.cached_tokens = torch.empty((*input_ids.shape[:-1], 0), dtype=input_ids.dtype, device=self.model.device)
                self.dirty_count = -6
            
            self.cached_tokens = torch.cat((self.cached_tokens, input_ids.to(self.model.device)), dim=-1)
            gend_tokens = torch.empty((*input_ids.shape[:-1], 0), dtype=input_ids.dtype).to(self.model.device)
            
            if streamer is not None:
                self.streamer = streamer
                self.tokenizer = tokenizer if tokenizer is not None else streamer.tokenizer
            if tokenizer is not None: 
                self.tokenizer = tokenizer
            
            self.maybe_print(streamer, tokenizer, input_ids)
            
            old_dose_multiplier = self.get_dose_multiplier()
            if protect_inputs:
                self.set_dose_multiplier(0) #don't noise anything until we start generating from it
            t_input_ids, model_kwargs, logits_processor, stopping_criteria, gen_conf = self.go_through_hell(
                    self.cached_tokens,
                    logits_processor=logits_processor, 
                    min_new_tokens = min_new_tokens, 
                    max_new_tokens = max_new_tokens,
                    stopping_criteria=stopping_criteria,
                    negative_prompt_ids = negative_prompt_ids,
                    negative_prompt_attention_mask= negative_prompt_attention_mask
                )
            unfinished_sequences = torch.ones(t_input_ids.shape[0], dtype=torch.long, device=t_input_ids.device)
            
            model_inputs = self.model.prepare_inputs_for_generation(input_ids=t_input_ids.to(self.model.device), past_key_values = self.past_key_values, **model_kwargs)
            outputs = self.model(**model_inputs)
            model_kwargs = self.model._update_model_kwargs_for_generation(outputs, model_kwargs, is_encoder_decoder= False)
            self.past_key_values = model_kwargs['past_key_values']
            logits = outputs.logits
            next_token_scores = logits_processor(t_input_ids, logits[:,-1,:])
            hidden_states = None if 'hidden_states' not in outputs else outputs['hidden_states']
            next_token = self.maybe_pad(sampler(logits, next_token_scores, hidden_states), gen_conf, unfinished_sequences)
            unfinished_sequences = self.update_completions(unfinished_sequences, next_token)
            

            self.set_dose_multiplier(old_dose_multiplier)
            
            self.maybe_print(streamer, tokenizer, next_token)
            
            gend_tokens = torch.cat((gend_tokens, next_token), dim = -1)
            self.cached_tokens = torch.cat((self.cached_tokens, next_token), dim=-1)
            
            while gend_tokens.shape[-1] < max_new_tokens:
                self.past_key_values = self.cold_shower()
                model_inputs = self.model.prepare_inputs_for_generation(input_ids=self.cached_tokens, **model_kwargs)
                outputs = self.model(**model_inputs)
                logits = outputs.logits
                next_token_scores = logits_processor(self.cached_tokens, outputs.logits[:,-1,:])
                next_token = self.maybe_pad(sampler(outputs.logits, next_token_scores, None), gen_conf, unfinished_sequences)
                unfinished_sequences = self.update_completions(unfinished_sequences, next_token)
                gend_tokens = torch.cat((gend_tokens, next_token), dim = -1)
                self.maybe_print(streamer, tokenizer, next_token)                    
                self.cached_tokens = torch.cat((self.cached_tokens, next_token), dim = -1)
                self.dirty_count += 1
                model_kwargs = self.model._update_model_kwargs_for_generation(outputs, model_kwargs, is_encoder_decoder= False)
                self.past_key_values = model_kwargs['past_key_values']
                if stopping_criteria(self.cached_tokens, gend_tokens) or unfinished_sequences.max() == 0:
                    break
                
            #self.past_key_values = self.cold_shower()
            
            if streamer is not None:
                streamer.end()#(streamer.tokenizer.encode(' ', return_tensors="pt"))        
        return gend_tokens
    
    def argmax_select_next_token(self, logits, next_token_scores, hidden_states):
        #next_token_logits = logits[:, -1, :]
        #top_k_indices = torch.topk(next_token_logits, k=1, dim=-1).indices[0]
        return torch.argmax(next_token_scores, dim=-1, keepdim= True)
                  
    def reset_model_state(self):
        r"""
        clears the Dgenerator key+value and token cache.
        basically just a convenience function for jupyter notebook cells
        to keep the dosage info active but otherwise start the model fresh"""
        self.past_key_values = DynamicCache()
        self.cached_tokens = None
        self.dirty_count = -6
        
    def detox(self):
        r"""
        clears all drug profiles and sets all dose_thetas to 0
        """
        for drug_type, val in self.dose_theta.items():
            self.dose_theta[drug_type] = 0
            self.dose_shapes[drug_type] = None
            self.dose_mode[drug_type] = 'interpolate'
        self._update_layer_doses()
        
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
    
    
    _dose_theta_doc = f"""
        The maximum noise in radians that may be injected for this drug type
        :type float:
    """
    _H_doc = """Hidden state noise. Applied to the hidden state vectors prior to feeding into the k, q, v projection matrices. 
    at each head, prior to concatenation. Not super well tested, but maybe useful in early layers 
    as an alternative to repetition penalty"""
    def set_H_dose_theta(self, radians):
        self.set_dose_theta(radians, 'H')
    set_H_dose_theta.__doc__=f"""For {_H_doc}
        :param radians: {_dose_theta_doc}"""
    
    _A_doc = """Attention head output noise. Applied to the vectors resulting from the attention operation 
    at each head, prior to concatenation."""
    def set_A_dose_theta(self, radians):
        self.set_dose_theta(radians, 'A')
    set_A_dose_theta.__doc__=f"""For {_A_doc}
        :param radians: {_dose_theta_doc}"""
    
    _K_doc = """Key noise. Applied to the Key vectors in each attention head."""
    def set_K_dose_theta(self, radians):
        self.set_dose_theta(radians, 'K')
    set_K_dose_theta.__doc__=f"""For {_K_doc}
        :param radians: {_dose_theta_doc}"""
    
    _Q_doc = """Query noise. Applied to the Query vectors in each attention head."""
    def set_Q_dose_theta(self, radians):
        self.set_dose_theta(radians, 'Q')
    set_Q_dose_theta.__doc__=f"""For {_Q_doc}
        :param radians: {_dose_theta_doc}"""
        
    _V_doc = """Value noise. Applied to the Value vectors in each attention head."""
    def set_V_dose_theta(self, radians):
        self.set_dose_theta(radians, 'V')
    set_V_dose_theta.__doc__=f"""For {_V_doc}
        :param radians: {_dose_theta_doc}"""
        
    _drug_type_doc = f"""
        The type of noise being specified. Where options are any of
        - 'Q' ({_Q_doc})
        - 'K' ({_K_doc})
        - 'V' ({_V_doc})
        - 'A' ({_A_doc})
        - 'A' ({_H_doc})
        :type str: 
    """   
    def set_dose_theta(self, radians, type):
        self.dose_theta[type] = radians
        self._update_layer_doses()
    set_dose_theta.__doc__ = f"""{_dose_theta_doc}  
    :param type: {_drug_type_doc}"""
    
    _typed_interp = f"""Returns the interpolated dosage (amount of noise) at the given layer
    :param idx: The layer to return the noise for
    :type idx: int
    :param total_layers: The total number of layers
    :type total_layers: int"""
    
    def get_dose_theta(self, idx=None, total_layers=1, drug_type = 'A'):
        return self._get_typed_dose_theta(idx, total_layers, drug_type)
    get_dose_theta.__doc__=f"""{_typed_interp}
        :param drug_type: {_drug_type_doc}"""
    
    
    def get_H_dose_theta(self, idx=None, total_layers=1):
        return self._get_typed_dose_theta(idx, total_layers, 'H')
    get_H_dose_theta.__doc__ = f"""{_typed_interp}
    This is for {_H_doc}"""
    def get_A_dose_theta(self, idx=None, total_layers=1):
        return self._get_typed_dose_theta(idx, total_layers, 'A')
    get_A_dose_theta.__doc__ = f"""{_typed_interp}
    This is for {_A_doc}"""
    def get_K_dose_theta(self, idx=None, total_layers=1):
        return self._get_typed_dose_theta(idx, total_layers, 'K')
    get_K_dose_theta.__doc__ = f"""{_typed_interp}
    This is for {_K_doc}"""
    def get_Q_dose_theta(self, idx=None, total_layers=1):
        return self._get_typed_dose_theta(idx, total_layers, 'Q')
    get_Q_dose_theta.__doc__ = f"""{_typed_interp}
    This is for {_Q_doc}"""
    def get_V_dose_theta(self, idx=None, total_layers=1):
        return self._get_typed_dose_theta(idx, total_layers, 'V')
    get_V_dose_theta.__doc__ = f"""{_typed_interp}
    This is for {_V_doc}"""
    
    def _get_typed_dose_theta(self, idx=None, total_layers=1, type='A'):
        if idx is not None and self.dose_shapes[type] is not None:
            return self.get_tissue_bioavailability(idx, total_layers, type)*self.dose_theta[type]*self.dose_multiplier
        else:
            return self.dose_theta[type]*self.dose_multiplier
           
    
    _shape_doc = f"""a list of dicts where
        Each dict specifies:
        - 'depth' (float): A value from 0-1 indicating the layer number as a ratio of the total layers.
        - 'peakratio' (float): Indicating a scalar of the base dose_theta.
    :type shape: list(dict)
    """
    _interp_modes_doc = f"""mode by which to interpolate between unspecified injection sites. 
        Can be one of:
        - 'interpolate': Smoothly increase and decrease the dose between values.
        - 'ceil': Always sets to the highest peak_ratio of the range a layer may fall within.
        - 'floor': Always sets to the lowest value of a range peak_ratio may fall within."""
    
    _moded_shape_doc = f"""
    Sets DRUG profile of the given type and optionally dose. Any call to this function for a given type
    will overwrite the previously set drug profile for ONLY that type.
        :param shape: {_shape_doc}
        :param interp_mode: {_interp_modes_doc}
        :paran drug_type: {_drug_type_doc}
        :param dose_theta: {_dose_theta_doc}
    """
    def set_drug_profile(self, shape, interp_mode, drug_type, dose_theta=None):
        self._set_typed_dose_shape(shape, interp_mode, drug_type)
        if dose_theta is not None:
            self.set_dose_theta(dose_theta, drug_type)
    set_drug_profile.__doc__ = _moded_shape_doc
    
    _typed_dose_doc = f"""
        shape : list 
            {_shape_doc}
        mode : str
            Determines how to treat dose_theta between layers. Options are:
            {_interp_modes_doc}
    """
    def set_H_dose_shape(self, shape, interp_mode):
        self._set_typed_dose_shape(shape, interp_mode, 'H')
    set_H_dose_shape.__doc__ = f"""For {_H_doc} {_typed_dose_doc}"""
    
    def set_A_dose_shape(self, shape, interp_mode):
        self._set_typed_dose_shape(shape, interp_mode, 'A')
    set_A_dose_shape.__doc__ = f"""For {_A_doc} {_typed_dose_doc}"""
    
    def set_K_dose_shape(self, shape, interp_mode):
        self._set_typed_dose_shape(shape, interp_mode, 'K')
    set_K_dose_shape.__doc__ = f"""For {_K_doc} {_typed_dose_doc}"""   
    
    def set_Q_dose_shape(self, shape, interp_mode):
        self._set_typed_dose_shape(shape, interp_mode, 'Q')
    set_Q_dose_shape.__doc__ = f"""For {_Q_doc} {_typed_dose_doc}"""
    
    def set_V_dose_shape(self, shape, interp_mode):
        self._set_typed_dose_shape(shape, interp_mode, 'V')
    set_V_dose_shape.__doc__ = f"""For {_V_doc} {_typed_dose_doc}"""
        
    
    def _set_typed_dose_shape(self, shape, mode, type):
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
            layer.self_attn.adderall_theta = self.get_A_dose_theta(idx, layerct)
            layer.self_attn.quaalude_theta = self.get_Q_dose_theta(idx, layerct)
            layer.self_attn.ketamine_theta = self.get_K_dose_theta(idx, layerct)
            layer.self_attn.valium_theta = self.get_V_dose_theta(idx, layerct)
            layer.self_attn.heroine_theta = self.get_H_dose_theta(idx, layerct)
            #layer.layer_idx = idx
            #layer.dgenerator = self.model.dgenerator
            #layer.total_layers = layerct
    
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
        hthetadeg = f"{(int(self.dose_theta['H']/3.14*180))}H"
        
        file_path = os.path.join(current_script_dir, '..', base_dir, 'results', experiment, subtype, f"injection_depth_{injection_depth}_({athetadeg}_{qthetadeg}_{kthetadeg}_{vthetadeg}_{hthetadeg})-dose.msgpack")
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
            if len(self.past_key_values) == 0:
                logger.warn("the cold_shower() function can only be called on models being run with Dgenerate")
                return self.past_key_values
            if self.past_key_values is None or self.dirty_count <= 0 and not force_clean:
                return self.past_key_values
            if self.dirty_count >= self.sober_interval or force_clean:
                max_clean = min(self.past_key_values[0][0].shape[2] - 6, self.dirty_count)
                new_past_key_values = self._get_truncated_cache(self.past_key_values, max_clean)
                           
                regen_tokens = self.cached_tokens[:, -(max_clean+1):-1]        
                old_dose_multiplier = self.get_dose_multiplier()
                self.set_dose_multiplier(0)
                outputs = self.model(input_ids=regen_tokens.to(self.model.device), past_key_values=new_past_key_values, use_cache=True)
                self.past_key_values = DynamicCache()
                for i, (k, v) in enumerate(outputs.past_key_values):
                    self.past_key_values.update(k, v, i)
                    
                #TODO: Figure out why this doesn't work the first time when no noise is injected.
                """
                if torch.max(self.past_key_values[20][0] - outputs.past_key_values[20][0]) > 0:
                    self.past_key_values = outputs.past_key_values
                    self.cold_shower()
                """
                    
                self.set_dose_multiplier(old_dose_multiplier)
                self.dirty_count -= max_clean
                del new_past_key_values
                self.clear_cuda_caches()
        return self.past_key_values
    
    def clear_cuda_caches(self): 
        """clears cache across potentially multiple devices"""
        for i in range(torch.cuda.device_count()):
            with torch.cuda.device(i):
                torch.cuda.empty_cache() 
    
    def _get_truncated_cache(self, to_trunc, trunc_by):
        result = []
        for k, v in to_trunc:
            result.append((
                k[:, :, :-(trunc_by), :],
                v[:, :, :-(trunc_by), :]))
        return result
    
    #for debugging
    def decode(self, input_ids_or_logits):
        if self.tokenizer is not None:
            if(isinstance(input_ids_or_logits, list)):
                return self.tokenizer.decode(input_ids_or_logits)
            elif len(input_ids_or_logits.shape)>2:
                input_ids = self.argmax_select_next_token(input_ids_or_logits, None)
            else: 
                input_ids = input_ids_or_logits
            try:
                return self.tokenizer.decode(input_ids)
            finally:
                return self.tokenizer.decode(input_ids.squeeze(0))
    
    def update_completions(self, unfinished_sequences, next_tokens):
        if self.eos_token_id_tensor is not None:
            unfinished_sequences = unfinished_sequences.mul(
                next_tokens.tile(self.eos_token_id_tensor.shape[0], 1).ne(self.eos_token_id_tensor.unsqueeze(1)).prod(dim=0)
            )
        return unfinished_sequences
            
    #adds padding token to end of sequence if necessary
    def maybe_pad(self, next_tokens, generation_config, unfinished_sequences):
        eos_token_id = generation_config.eos_token_id
        pad_token_id = generation_config.pad_token_id
        if eos_token_id is not None:
                if pad_token_id is None:
                    raise ValueError("If `eos_token_id` is defined, make sure that `pad_token_id` is defined.")
                next_tokens = next_tokens * unfinished_sequences + pad_token_id * (1 - unfinished_sequences)
        return next_tokens
    
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
        r"""specifies the frequency with which the model should recompute drugged hidden states.
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
        #model._update_model_kwargs_for_generation = types.MethodType(_update_model_kwargs_for_generation, model)
        
        return self.model
    
    def go_through_hell(self, inputs, generation_config = None,
                        min_new_tokens = None, max_new_tokens = None,
                        logits_processor = None, stopping_criteria = None, 
                        negative_prompt_ids = None, negative_prompt_attention_mask = None,
                        **kwargs):
        r"""creates all of the absurd shit that may or may not be needed on a per model basis, 
        prays for salvation the whole time because the transformers library was not nice enough to make
        the equivalent part of its generation mixin modular"""
        self.model.generation_config.pad_token_id = self.tokenizer.pad_token_id if self.model.generation_config.pad_token_id is None else self.model.generation_config.pad_token_id
        generation_config = generation_config if generation_config is not None else self.model.generation_config
        generation_config = copy.deepcopy(generation_config)
        generation_config.min_new_tokens = min_new_tokens if min_new_tokens is not None else generation_config.min_new_tokens
        generation_config.max_new_tokens = max_new_tokens if max_new_tokens is not None else generation_config.max_new_tokens
        
        model_kwargs = generation_config.update(**kwargs)
        inputs_tensor, model_input_name, model_kwargs = self.model._prepare_model_inputs(
            inputs, generation_config.bos_token_id, model_kwargs
        )
        model_kwargs["use_cache"] = generation_config.use_cache
        accepts_attention_mask = "attention_mask" in set(inspect.signature(self.model.forward).parameters.keys())
        requires_attention_mask = "encoder_outputs" not in model_kwargs

        if model_kwargs.get("attention_mask", None) is None and requires_attention_mask and accepts_attention_mask:
            model_kwargs["attention_mask"] = self.model._prepare_attention_mask_for_generation(
                inputs_tensor, self.tokenizer.pad_token_id, self.tokenizer.eos_token_id
            )

        if (generation_config.pad_token_id is not None
            and len(inputs_tensor.shape) == 2
            and torch.sum(inputs_tensor[:, -1] == generation_config.pad_token_id) > 0
            ):
            print("bad")
        
        # 5. Prepare `input_ids` which will be used for auto-regressive generation
        input_ids = inputs_tensor if model_input_name == "input_ids" else model_kwargs.pop("input_ids")
        input_ids_length = input_ids.shape[-1]
        generation_config.max_length = generation_config.max_new_tokens + input_ids_length
        
        logits_processor = logits_processor if logits_processor is not None else LogitsProcessorList()
        logits_processor = self.model._get_logits_processor(
            generation_config=generation_config,
            input_ids_seq_length=input_ids_length,
            encoder_input_ids=inputs_tensor,
            logits_processor=logits_processor,
            model_kwargs=model_kwargs,
            prefix_allowed_tokens_fn = None,
            negative_prompt_ids=negative_prompt_ids,
            negative_prompt_attention_mask=negative_prompt_attention_mask,
        )
        stopping_criteria = stopping_criteria if stopping_criteria is not None else StoppingCriteriaList()
        stopping_criteria = self.model._get_stopping_criteria(
            generation_config=generation_config, stopping_criteria=stopping_criteria
        )
        eos_token_id = generation_config.eos_token_id
        if isinstance(eos_token_id, int):
            eos_token_id = [eos_token_id]
        self.eos_token_id_tensor = torch.tensor(eos_token_id).to(input_ids.device) if eos_token_id is not None else None
        
        return input_ids, model_kwargs, logits_processor, stopping_criteria, generation_config
    
    
import numpy as np
import torch
import torch.nn.functional as F
import hashlib

default_index_map = None
def set_index_base(logits):
    "sets the base color indices to the top 240 token indices of the logits tensor provided"
    last_logits = logits[0, -1, :]
    top_k_indices = torch.topk(last_logits, k=240, dim=-1).indices[:240]
    topklist = top_k_indices.tolist()
    global default_index_map 
    default_index_map = {}
    for i, idx in enumerate(topklist):
        default_index_map[idx] = i
    
def color_for_index(index):
    """Return an ANSI color code for the given index."""
    if default_index_map is not None:
        index = default_index_map[index.item()] if index.item() in default_index_map else 0
    return 16 + ((240-index) % 240)  # Starting from 16 to avoid the first 16 standard colors

def print_top_k_logits_histogram(logits, tokenizer, top_k=10, max_width=80, softmax=True):
    """
    Print to console a histogram of the top_k predicted next tokens' logits in the console,
    after applying a softmax to convert logits to probabilities. The token text
    and its probability are right-aligned.

    :param logits: A tensor of logits from a language model prediction.
    :param tokenizer: The tokenizer used with the model to map indices to tokens.
    :param top_k: Number of top logits to display in the histogram.
    :param max_width: The maximum width of the histogram in characters.
    """
    
    last_logits = logits[0, -1, :]
    probabilities = F.softmax(torch.tensor(last_logits), dim=-1)
    top_k_indices = np.argsort(probabilities.numpy())[-top_k:]
    np_logits = last_logits.numpy()
    top_k_res = probabilities[top_k_indices] if softmax else np_logits[top_k_indices]

    top_k_indices = np.argsort(last_logits)[-top_k:]
    top_k_res = F.softmax(torch.tensor(last_logits), dim=-1)[top_k_indices].numpy() if softmax else last_logits[top_k_indices]
    tokens = [tokenizer.decode([idx]) for idx in top_k_indices]
    max_token_length = max(len(token) for token in tokens)
    summed_top_k = sum(top_k_res)
    distribution = (top_k_res / summed_top_k)
    distribution = distribution/max(distribution)
    print("--- \n")
    for token, prob, raw_prob, index in zip(tokens, distribution, top_k_res, top_k_indices):
        prob_text = f"{raw_prob * 100:.2f}%"
        text_and_prob=f"{token}  {prob_text}"
        max_prob_text = f"""{"_"*max_token_length}  {prob_text}"""
        barlength = int(max(0,(prob*(max_width)-(len(max_prob_text)+4))))
        bar = '#' * barlength
        #san_bar = len(text_and_prob.rjust(max_width)) 
        color_code = color_for_index(index)
        print(f"\x1b[38;5;{color_code}m{bar} {text_and_prob.rjust(max_width-barlength)}\x1b[0m ")
    print("---::::"+tokens[len(tokens)-1]+":::   \n")
    