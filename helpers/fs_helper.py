import json

def read_obj(path):
  with open(path, 'r') as file:
    data = file.read().replace('\n', '')
    config = json.loads(data)
  return config

def write_obj(path, data):
  f = open(path, "w")
  f.write(json.dumps(data))
  f.close();