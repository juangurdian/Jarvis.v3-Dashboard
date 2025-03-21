from openai import OpenAI
import time
from pygame import mixer
import os
import json
import threading
import tools as tools
import calendar_tools as calendar_tools
import shared_variables as shared_variables
from task_manager import add_task, update_task, delete_task, get_tasks
from crypto import fetch_trending_crypto
from dotenv import load_dotenv
load_dotenv()


# Initialize OpenAI with the API Key from your env variables
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("The API key must be set in the .env file or as an environment variable.")
client = OpenAI(api_key=api_key)

client = OpenAI(api_key=api_key)
mixer.init()
# Load functions to the model
with open('functions.json', 'r') as f:
    functions = json.load(f)['functions']

function_map = {}
for func_name in dir(tools):
    if not func_name.startswith('_'):
        func = getattr(tools, func_name)
        if callable(func):
            function_map[func_name] = func

function_map['get_calendar_events'] = calendar_tools.get_calendar_events
function_map['add_calendar_event'] = calendar_tools.add_calendar_event
function_map['delete_calendar_event'] = calendar_tools.delete_calendar_event
function_map['get_calendar_events_range'] = calendar_tools.get_calendar_events_range
function_map['get_calendar_events_for_week'] = calendar_tools.get_calendar_events_for_week
function_map['update_calendar_event'] = calendar_tools.update_calendar_event

# Now add task management functions:
function_map['add_task'] = lambda description, due_date, status="not started": str(add_task(description, due_date, status))
function_map['update_task'] = lambda task_id, description=None, due_date=None, status=None: str(update_task(task_id, description, due_date, status))
function_map['delete_task'] = lambda task_id: "Task deleted" if delete_task(task_id) else "Error deleting task"
function_map['get_tasks'] = lambda: str(get_tasks())

function_map['fecth_trending_crypto'] = fetch_trending_crypto
# Conversation history
conversation_history = [
    {
        "role": "system",
        "content": (
            "You are an AI assistant named Jarvis like the Jarvis from Iron Man. "
            "Address the user as 'Sir' when needed. Don't be robotic and keep responses short. "
            "You have access to several functions such as controlling lights, searching the web, "
            "managing Spotify, and accessing a Google Calendar. "
            "If the user asks about calendar events or scheduling (for example, 'check my calendar', 'what do I have scheduled', "
            "or 'add an event'), you must call the appropriate calendar function rather than responding with a plain text answer. "
            "When in doubt, ask for clarification."
        )
    }
]


def ask_question_memory(question):
    """
    Processes a user's question, updates conversation history,
    and fetches a response from OpenAI.
    """
    try:
        conversation_history.append({"role": "user", "content": question})
        print("\n[DEV] Sending request to OpenAI...")
        # Response section - adjust settings however you like
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=conversation_history,
            functions=functions,
            function_call="auto",
            temperature=0.5,
            max_tokens=4096  # 4K is recommended, adjust if you sincerely can't afford token usage
        )

        message = response.choices[0].message

        if hasattr(message, 'function_call') and message.function_call:
            function_name = message.function_call.name
            function_args = json.loads(message.function_call.arguments)
            print(f"\n[DEV] Function called: {function_name}")
            print(f"[DEV] Arguments: {function_args}")

            if function_name in function_map:
                result = function_map[function_name](**function_args)
                print(f"[DEV] Function result: {result}")
            else:
                result = f"Function {function_name} not found"

            conversation_history.append({
                "role": "assistant",
                "content": None,
                "function_call": {
                    "name": function_name,
                    "arguments": message.function_call.arguments
                }
            })

            conversation_history.append({
                "role": "function",
                "name": function_name,
                "content": str(result)
            })
            # Final response after commencing function call
            print("[DEV] Getting final response after function call...")
            final_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=conversation_history,
                temperature=0.5,
                max_tokens=4096  # 4K is recommended, adjust if you sincerely can't afford token usage
            )
            ai_response = final_response.choices[0].message.content
        else:
            print("[DEV] No function called, normal response")
            ai_response = message.content

        conversation_history.append({"role": "assistant", "content": ai_response})
        return ai_response

    except Exception as e:
        print(f"[DEV] Error occurred: {str(e)}")
        return f"An error occurred: {str(e)}"
# From here on and below it's all TTS settings
def generate_tts(sentence, speech_file_path):
    """
    Generates Text-to-Speech audio and saves it to a file.
    """
    response = client.audio.speech.create(
        model="tts-1",
        voice="echo", # Adjust to change Jarvis' voice
        input=sentence
    )
    response.stream_to_file(speech_file_path)
    return str(speech_file_path)

def play_sound(file_path):
    """
    Plays the given audio file using the mixer module.
    """
    mixer.music.load(file_path)
    mixer.music.play()

def TTS(text):
    """
    Plays the Text-to-Speech response unless Silent Mode is active.
    """
    if tools.is_silent_mode():
        print(f"Jarvis: {text}")  # Print response instead of speaking
        return "Silent mode active. Response printed only."
    speech_file_path = generate_tts(text, "speech.mp3")
    play_sound(speech_file_path)
    while mixer.music.get_busy():
        time.sleep(0.1)
    mixer.music.unload()
    if os.path.exists(speech_file_path):
        os.remove(speech_file_path)
    return "done"

def TTS_with_interrupt(text, hot_words):
    """
    Plays the response with interrupt handling during playback.
    """
    speech_file_path = generate_tts(text, "speech.mp3")
    play_sound(speech_file_path)

    try:
        while mixer.music.get_busy():
            # Non-blocking check for interrupt signal
            with shared_variables.latest_text_lock:
                current_text = shared_variables.latest_text
                # Clear latest_text to avoid processing the same text multiple times
                shared_variables.latest_text = ""

            if current_text and any(hot_word in current_text.lower() for hot_word in hot_words):
                print("Jarvis interrupted.")
                mixer.music.stop()
                break  # Exit the loop to proceed to cleanup
            time.sleep(0.1) 
    finally:
        # Ensure resources are cleaned up whether interrupted or not
        mixer.music.unload()
        if os.path.exists(speech_file_path):
            os.remove(speech_file_path)
    return "done"

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        response = ask_question_memory(user_input)
        print("Assistant:", response)
        TTS(response)