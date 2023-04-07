class AttributeDict(dict):
  __getattr__ = dict.__getitem__
  __setattr__ = dict.__setitem__
  __delattr__ = dict.__delitem__

def simpledict2doted(input_dict: dict) -> dict:
  """Cast base python dict to dict with dot notation support."""
  return AttributeDict(input_dict)
  