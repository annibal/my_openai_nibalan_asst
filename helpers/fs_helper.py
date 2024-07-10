import json

def read_obj(path):
  try:
    with open(path, 'r') as file:
      data = file.read().replace('\n', '')
      config = json.loads(data)
    return config
  except Exception as e:
    return False

def write_obj(path, data):
  f = open(path, "w")
  f.write(json.dumps(data))
  f.close();