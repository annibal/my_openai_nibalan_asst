import asyncio
import uuid
from helpers.openai_helpers import chat_completion_request
from helpers.terminal_helpers import fmt_msg, read_prompt_message, print_header, parse_args, tprint
from helpers.fs_helper import read_obj
from function_tools import handle_tool_call, handle_flow_instructions
from termcolor import colored

messages = []
thread_uuid = str(uuid.uuid4())

def send_msg(obj_msg, debug=False):
  tprint(fmt_msg(obj_msg), debug=debug, header=False)
  messages.append(obj_msg)

async def main():
  tprint(f"thread id: '{thread_uuid}", verbose=True)
  print_header()
  parse_args()
  nb = read_obj("./data_files/assistant_config.json")
  tprint("initial configuration loaded", verbose=True)

  messages.append({ "role": "system", "content": nb['instructions'] })
  tprint("sent initial GPT assistant instructions", verbose=True)

  extra_instructions = read_obj("./data_files/more_instructions.json")
  for msg in extra_instructions['messages']:
    send_msg({ "role": "system", "content": msg })
  tprint("sent initial GPT purpose instructions", verbose=True)
  
  send_msg({ "role": "user", "content": "Hello! What should i do in order to find clinical trials?" }, True)
  tprint("sent initial user-handshake message, will get the assistant's response", verbose=True)

  initial_chat_response = await chat_completion_request(messages, 
    model=nb['model'],
    top_p=nb['top_p'],
    temperature=nb['temperature'],
  )
  tprint("received initial chat response:", verbose=True)
  tprint(initial_chat_response, verbose=True)

  send_msg(initial_chat_response.choices[0].message)
  tprint("printed initial assistant message as the first message in the chat", verbose=True)

  while True:
    user_message = read_prompt_message()
    if user_message == False:
      tprint("received false for prompt message, aborting", verbose=True)
      break;
    if not user_message['content']:
      print(colored("⛒ empty", "red") + " ⬎")
      tprint("user_message is empty - input is ignored, will skip and try to read prompt message again", verbose=True)
      continue;
    messages.append(user_message)

    if user_message["role"] == "system":
      tprint(fmt_msg(user_message), debug=True, header=False)
      continue;

    chat_response = await chat_completion_request(messages, 
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
        results = await handle_tool_call(tool_call_cfg.function.name, tool_call_cfg.function.arguments, thread_id=thread_uuid)

        tool_msg = {
          "content": results,
          "role": "tool",
          "name":  tool_call_cfg.function.name, 
          "tool_call_id": tool_call_cfg.id,
        }

        send_msg(tool_msg, True)
        tprint(tool_msg, verbose=True)
        
      # end for tool_call_cfg in tool_calls

      tprint("consulting new flow instructions", verbose=True)
      flow_message = await handle_flow_instructions(thread_uuid)

      tprint(f"flow instructions are: '{flow_message}'", verbose=True)
      if flow_message:
        tprint("sending system message with flow instructions")
        flow_message_obj = {"role": "system", "content": flow_message }
        messages.append(flow_message_obj)
        tprint(fmt_msg(flow_message_obj), debug=True, header=False)
        tprint("responding to GPT with the tool call results and new flow instructions", verbose=True)
      else:
        tprint("responding to GPT with the tool call results", verbose=True)

      # get a new response from the model where it can see the function(s) response
      response_with_tool_call = await chat_completion_request(messages,
        model=nb['model'],
      )
      tprint("received GPT reply", verbose=True)
      tprint(response_with_tool_call, verbose=True)

      tprint("will proceed and output GPT reply message to user", verbose=True)
      send_msg(response_with_tool_call.choices[0].message)
    else:
      tprint("GPT message does not have request for tool call, proceeding to display reply to user", verbose=True)
      tprint(fmt_msg(assistant_message))
    # end if tool_calls
    tprint(f"iteration complete, message count: {len(messages)}", verbose=True)

  # end while True
  tprint("exited loop ??", verbose=True)

asyncio.run(main())