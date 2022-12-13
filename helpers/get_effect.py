def get_effect(name):
    effect_module = __import__("effects.%s" % name, fromlist=["effects"])
    return effect_module.Effect

def available_effects():
    import os
    return [file[:-3] for file in os.listdir('effects') if file.endswith('.py')]

