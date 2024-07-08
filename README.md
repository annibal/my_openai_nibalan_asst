# Annibal's AI Chat Assistant

Python code to chat with GPT via terminal prompt

## Setup

- Have `python` and `pip` installed ([pip docs](https://pip.pypa.io/en/stable/installation/)):

  ```shell
  sudo apt-get update
  sudo apt install python3-pip
  ```

- Add your [OpenAI API key](https://platform.openai.com/organization/api-keys):

  ```shell
  cat "SK_12345678910_MY_API_KEY_HERE" > .openai_api_key
  ```

- Install python requirements:

  ```shell
  pip install scipy tenacity tiktoken termcolor openai
  ```

- Run the main file:

  ```shell
  python3 main.py
  ```


