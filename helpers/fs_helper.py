import json

def import_json(path):
    with open(path, 'r') as file:
        data = file.read().replace('\n', '')
        config = json.loads(data)
    return config