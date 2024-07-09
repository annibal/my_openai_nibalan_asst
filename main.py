
from helpers.openai_helpers import chat_completion_request
from helpers.terminal_helpers import fmt_msg, read_prompt_message, print_header, parse_args, tprint
from helpers.fs_helper import import_json
from function_tools import handle_tool_call


def main():
  print_header()
  parse_args()
  nb = import_json("./data_files/assistant_config.json")
  tprint("initial configuration loaded", verbose=True)

  messages = []
  messages.append({ "role": "system", "content": nb['instructions'] })
  tprint("sent initial system instructions", verbose=True)

  while True:
    user_message = read_prompt_message()
    if user_message == False:
      tprint("received false for prompt message, aborting", verbose=True)
      break;
    messages.append(user_message)

    if user_message["role"] == "system":
      tprint(fmt_msg(user_message), debug=True, header=False)
      continue;

    chat_response = chat_completion_request(messages, 
      model=nb['model'],
      top_p=nb['top_p'],
      temperature=nb['temperature'],
      tools=nb['tools'],
      tool_choice="auto",
      parallel_tool_calls=True,
    )
    
    assistant_message = chat_response.choices[0].message
    messages.append(assistant_message)

    tool_calls = assistant_message.tool_calls
    if tool_calls:
      tprint("GPT message has request for tool call(s)", verbose=True)
      tprint(fmt_msg(assistant_message), debug=True, header=False)

      for tool_call_cfg in tool_calls:
        results = handle_tool_call(tool_call_cfg.function.name, tool_call_cfg.function.arguments)

        tool_msg = {
          "content": results,
          "role": "tool",
          "name":  tool_call_cfg.function.name, 
          "tool_call_id": tool_call_cfg.id,
        }

        messages.append(tool_msg)
        tprint(fmt_msg(tool_msg), debug=True, header=False)
        tprint(tool_msg, verbose=True)
        
      # end for tool_call_cfg in tool_calls

      # get a new response from the model where it can see the function(s) response
      
      tprint("responding to GPT with the tool call results", verbose=True)
      response_with_tool_call = chat_completion_request(messages,
        model=nb['model'],
      )
      tprint("received GPT response", verbose=True)
      tprint(response_with_tool_call, verbose=True)

      tprint("will proceed and output GPT reply message to user", verbose=True)
      message_with_tool_call = response_with_tool_call.choices[0].message
      messages.append(message_with_tool_call)
      tprint(fmt_msg(message_with_tool_call))
    else:
      tprint("GPT message does not have request for tool call, proceeding to display reply to user", verbose=True)
      tprint(fmt_msg(assistant_message))
    # end if tool_calls
    tprint(f"iteration complete, message count: {len(messages)}", verbose=True)

  # end while True
  tprint("exited loop ??", verbose=True)

main()