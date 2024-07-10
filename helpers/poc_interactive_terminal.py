import sys
import os
import time

# for ch in "Loading":
    # print(ch)
    # sys.stdout.write("\033[F") # Cursor up one line
    # sys.stdout.write("\033[K") # Clear to the end of line
    # sys.stdout.write('\033[2K\033[1G') # Erase and go to beginning of line
    # time.sleep(0.1)

# print(os.get_terminal_size())

term_width = min(os.get_terminal_size().columns, 60)

# sys.stdout.write("╔" + ("═" * inner_w) + "╗\n")
# sys.stdout.write("║" + (" " * inner_w) + "║\n")
# sys.stdout.write("╚" + ("═" * inner_w) + "╝\n")
# x = input("?>: ")
# sys.stdout.write('\033[F"\033[2K\033[1G')
# sys.stdout.write('\033[F"\033[2K\033[1G')
# sys.stdout.write('\033[F"\033[2K\033[1G')
# sys.stdout.write('\033[F"\033[2K\033[1G')
# sys.stdout.write('\033[F"\033[2K\033[1G')

# sys.stdout.write("┏" + ("━" * inner_w) + "┓\n")
# sys.stdout.write("┃" + (" " * inner_w) + "┃\n")
# sys.stdout.write("┗" + ("━" * inner_w) + "┛\n")
# x = input("?>: ")
# sys.stdout.write('\033[F"\033[2K\033[1G')
# sys.stdout.write('\033[F"\033[2K\033[1G')
# sys.stdout.write('\033[F"\033[2K\033[1G')
# sys.stdout.write('\033[F"\033[2K\033[1G')
# sys.stdout.write('\033[F"\033[2K\033[1G')

def prompt_box(text):
  print(colored("▛▜", "black") + " - black")
  print(colored("▛▜", "dark_grey") + " - dark_grey")
  print(colored("▛▜", "grey") + " - grey")
  print(colored("▛▜", "light_grey") + " - light_grey")
  print(colored("▛▜", "white") + " - white")
  print(colored("▛▜", "blue") + " - blue")
  print(colored("▛▜", "light_blue") + " - light_blue")
  print(colored("▛▜", "cyan") + " - cyan")
  print(colored("▛▜", "light_cyan") + " - light_cyan")
  print(colored("▛▜", "red") + " - red")
  print(colored("▛▜", "light_red") + " - light_red")
  print(colored("▛▜", "magenta") + " - magenta")
  print(colored("▛▜", "light_magenta") + " - light_magenta")
  print(colored("▛▜", "green") + " - green")
  print(colored("▛▜", "light_green") + " - light_green")
  print(colored("▛▜", "yellow") + " - yellow")
  print(colored("▛▜", "light_yellow") + " - light_yellow")


  str_box = ""
  str_box += colored(" " * term_width, "white", "on_dark_grey") + " \n"
  str_box += colored(" ╔" + ("═" * (term_width - 4)) + "╗ ", "white", "on_dark_grey") + " \n"
  str_box += colored(" ║ ", "white", "on_dark_grey")
  str_box += colored(" " * (term_width - 6), "white")
  str_box += colored(" ║ ", "white", "on_dark_grey") + " \n"
  str_box += colored(" ╚" + ("═" * (term_width - 4)) + "╝ ", "white", "on_dark_grey") + " "
  str_box = colored(str_box, "white", "on_dark_grey")
  sys.stdout.write(str_box)
  sys.stdout.write("\033[F")
  sys.stdout.write(colored(" ║ ", "white", "on_dark_grey"))
  r = input(text + ": ")
  sys.stdout.write("\n")
  sys.stdout.write('\033[F"\033[2K\033[1G')
  sys.stdout.write('\033[F"\033[2K\033[1G')
  sys.stdout.write('\033[F"\033[2K\033[1G')
  sys.stdout.write('\033[F"\033[2K\033[1G')
  return r;







#                                             [HH:mm:ss] You ⮘
#                                                         hey!
# ⋗ Assistant [HH:mm:ss]
# Nice one!
#                                             [HH:mm:ss] You ⮘
#                    What is the weather in São Paulo, Brazil?
# ┗🠊 ◯ Tool Call: get_weather({
#       "location": "-23.5505,-46.6333",
#       "unit": "celsius",
#       "date": "2023-10-11"
#     }
# ┗🠊 ⦿ Tool Result for 'get_weather': {
#       temperature: 16,
#       sky: "cloudy"
#     }
# ⋗ Assistant [HH:mm:ss]
# 16°C, cloudy.
#                     ┌─────────────────── [HH:mm:ss] System ⌘
#                     │ Always prefix messages with "LOL:". │
#                     └─────────────────────────────────────┘
#                                             [HH:mm:ss] You ⮘
#                                                         hey!
# ⋗ Assistant [HH:mm:ss]
# LOL: Nice one!

# ⎇ Debug: Debug Enabled
# ∴ Log [YYYY-MM-DD HH:mm:ss] Verbose Enabled
# ∴ Log [YYYY-MM-DD HH:mm:ss] initial configuration loaded
# ∴ Log [YYYY-MM-DD HH:mm:ss] sent initial system instructions
# ∴ Log [YYYY-MM-DD HH:mm:ss] wait for user prompt message
#  ╔════════════════════════════════════════════════════════╗ 