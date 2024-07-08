
from helpers.openai_helpers import chat_completion_request
from helpers.terminal_helpers import f_pretty_print, read_prompt_message, print_header
from helpers.fs_helper import import_json
from function_tools import handle_tool_call

def main():
  print_header()
  nb = import_json("./data_files/assistant_config.json")
  
  messages = []
  messages.append({ "role": "system", "content": nb['instructions'] })

  while True:
    user_message = read_prompt_message()
    if user_message == False:
      break;
    messages.append(user_message)

    chat_response = chat_completion_request(messages, 
      model=nb['model'],
      top_p=nb['top_p'],
      temperature=nb['temperature'],
      tools=nb['tools'],
      tool_choice="required",
      parallel_tool_calls=True,
    )
    
    assistant_message = chat_response.choices[0].message
    messages.append(assistant_message)
    print(f_pretty_print(assistant_message))

    tool_calls = assistant_message.tool_calls
    if tool_calls:
      for tool_call_cfg in tool_calls:
        results = handle_tool_call(tool_call_cfg.function.name, tool_call_cfg.function.arguments)

        tool_msg = {
          "content": results,
          "role": "tool",
          "name":  tool_call_cfg.function.name, 
          "tool_call_id": tool_call_cfg.id,
        }
        messages.append(tool_msg)
        print(f_pretty_print(tool_msg))
      # end for tool_call_cfg in tool_calls

      # get a new response from the model where it can see the function(s) response
      response_with_tool_call = chat_completion_request(messages,
        model=nb['model'],
      )

      message_with_tool_call = response_with_tool_call.choices[0].message
      messages.append(message_with_tool_call)
      print(f_pretty_print(message_with_tool_call))

    # end if tool_calls

main()