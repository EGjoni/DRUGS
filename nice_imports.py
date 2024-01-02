import warnings
efficiency_stuff = {}
try:
    import bitsandbytes
    efficiency_stuff['load_in_8bit'] = True
    warnings.warn("""using bitsandbytes and setting load_in_8bit=True. 
                  If you ar calling your model with model(..., **efficiency_stuff) and don't want 8bit loading, then set efficiency_stuff['load_in_8bit] = False""")
except:
    warnings.warn("bitsandbytes isn't installed, you're missing out on memory savings")

try:
    import accelerate
    efficiency_stuff['device_map'] = "auto"
except:
    warnings.warn("accelerate isn't installed, you may need to manually specify .to('cuda') on input_ids and model")