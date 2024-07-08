file_name = ".current_chat_context" 

def set_chat_context(ctx):
  f = open(file_name, "w")
  f.write(ctx)
  f.close();

def get_chat_context():
  try:
    f = open(file_name, "r")
    return f.read()
  except Exception as e:
    return "undefined"
