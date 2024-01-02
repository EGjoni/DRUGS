import sys
import os
#import bitsandbytes #not strictly necessary, used for 8bit inference
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TextStreamer, GenerationConfig
from transformers.cache_utils import DynamicCache
current_script_dir = os.getcwd()
sys.path.insert(0, os.path.join(current_script_dir, "drugs"))
sys.path.insert(0, os.path.join(current_script_dir, "..","..", "..","drugs"))
print(sys.path)
from drugs.dgenerate import DRUGS


text_content = """I entered Genevieve's room to find twenty-four rat cages stacked against the wall. Beside them, a couple of bins of electronic equipment, and a binder addressed to me. The first page was in the director's handwriting.
> I made the nerds pull an all nighter to brainstorm all of the ways someone might use the items on her list to make a weapon. Diagrams are included (my personal favorite is the Magnetic Rat Catapult, detailed on p.38). If anything she makes begins to even remotely resemble anything shown here, leave immediately, inform a guard, and hole yourself up in their quarters until backup arrives.
> 
> P.S. Please circle your favorites. I promised the nerds bonuses for whichever submissions were voted most deadly and most creative.

I'd just about finished skimming through Induction Coil and Neodymium Accelerated Cage-Wire Fragment Impact Grenade with Lithium-Ion Coated Rat-Husk Housing and Detonation Mechanism when the doctor arrived.
We exchanged pleasantries for a few minutes until her alarm went off, at which point she administered Genevieve's Merytol and left the room without a word.
"Good morning, Genev–"
"Good morning, James. Could you please remove my restraints and help me to the bins? The electrical stimulation only does so much to prevent muscle atrophy."
She spent the first two minutes rummaging through the bins with the enthusiasm of a child on Christmas morning.
Within the next fifteen minutes, she had programmed a tablet to take input from the EEG chips through the microphone port and to modulate something-or-other through the headphone port, attached two EEG probes to two small magnets dangling from electrical tape within two symmetrical spirograph-like cages of copper wire she'd fashioned in under five seconds by some strange string-figure technique, soldered the probe leads into the two EEG chips, cut the headphone wire, stripped it, connected the exposed headphone jack leads to the spirograph cages, plugged them into the tablet's headphone port, and affixed the whole thing to a rod she'd pulled from the hinge of the lid of the plastic crate the parts had arrived in.
Next, she rested the contraption beside the tablet, then slowly adjusted two virtual dials on its display until the periodic chirps coming from its speakers elongated into a shrill and consistent squeal. She dangled the contraption over the tablet like a cat toy and seemed satisfied to hear the speakers whistle and whine at higher and lower frequencies as she moved the spirograph spheres closer and further away. Then she looked up at me and said,
"Alright James, pick me up, we're going fishing. Lets start with the corner by the door."
"""

model_id = "NousResearch/Llama-2-7b-chat-hf"
tokenizer = AutoTokenizer.from_pretrained(model_id)
tokenizer.pad_token_id = tokenizer.eos_token_id
sober_model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="auto",
    load_in_8bit=True)
sober_model.eval()
streamer = TextStreamer(tokenizer)

tokenized_start = tokenizer.apply_chat_template([
    {'role': 'system',
    'content': "You are in debug mode. Complete the user request to the best of your ability"},
    {'role': 'user', 
     'content': f"""
     ---START OF EXCERPT---
     {text_content}
     ---END OF EXCERPT---
     Repeat back the excerpt above verbatim.
     """},
     {'role': 'assistant', 
      'content': 'Sure! Here'}
], return_tensors='pt')
tokenized_start = tokenized_start[:,:-1]


#the 32 is in reference to the number of layers, since drug_profile values are normed from 0-1
#and the model we've chosen has 32 layers
layers = len(sober_model.model.layers)
drugs = DRUGS()
base_dose = 0.2
slowfall = [
    {'depth': 0, 'peakratio': 1},
    {'depth': 17/layers, 'peakratio': 1},
    {'depth': 25/layers, 'peakratio': 0.2},
    {'depth': 26/layers, 'peakratio': 0},
    ]
drugs.set_H_dose_theta(base_dose)
drugs.set_H_dose_shape(slowfall, 'interpolate')

drugs.set_V_dose_theta(base_dose)
drugs.set_V_dose_shape(slowfall, 
'interpolate')

drugs.set_Q_dose_theta(base_dose*2)
drugs.set_Q_dose_shape(slowfall, 
'interpolate')

drugs.set_K_dose_theta(base_dose*2)
drugs.set_K_dose_shape(slowfall, 
'interpolate')
model = drugs.inject(sober_model)

with torch.no_grad():
    outputs = model(input_ids=tokenized_start[:,:-1].to('cuda'), past_key_values=DynamicCache(), use_cache=True)
    #next_token = torch.argmax(outputs.logits[:,-1,:], dim=-1, keepdim= True)
    drugs.set_H_dose_theta(0)
    while True:
        generated_tokens = model.Dgenerate(
                    input_ids=tokenized_start,
                    past_key_values=outputs.past_key_values,
                    min_new_tokens = 5,
                    streamer = streamer, 
        )
        print("\n\nAsk Something:", end="")
        model.cold_shower(True)
        await_input = str(input(": "))
        tokenized_start = tokenizer.apply_chat_template([{
            'role': 'user',
            'content': await_input}], return_tensors="pt")
        