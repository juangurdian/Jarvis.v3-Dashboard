import subprocess
import webbrowser
import python_weather
import asyncio
import assist
from icrawler.builtin import GoogleImageCrawler
import os
import spot

async def get_weather(city_name):
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
        weather = await client.get(city_name)
        return weather

def search(query):
    google_Crawler = GoogleImageCrawler(storage={"root_dir": r'./images'})
    google_Crawler.crawl(keyword=query, max_num=1)

def open_application(app_name):
    try:
        # Map known applications to their paths
        app_paths = {
            "spotify": r"C:\Users\YourUsername\AppData\Roaming\Spotify\Spotify.exe",  # Adjust path as needed
            "vscode": r"C:\Users\jcgus\AppData\Local\Programs\Microsoft VS Code\Code.exe",
            "slack": r"C:\Users\jcgus\AppData\Local\slack\slack.exe",
        }
        app_path = app_paths.get(app_name.lower(), app_name)
        subprocess.Popen(app_path)
        return f"Opening {app_name}"
    except FileNotFoundError as e:
        print(f"File not found: {app_name}. Error: {e}")
        return f"File not found: {app_name}. Error: {e}"
    except Exception as e:
        print(f"Error opening {app_name}: {e}")
        return f"Error opening {app_name}: {e}"


def search_web(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    return f"Searching the web for {query}"

def search_youtube(query):
    url = f"https://www.youtube.com/results?search_query={query}"
    webbrowser.open(url)
    return f"Searching YouTube for {query}"

def open_streaming_service(service_name):
    services = {
        "netflix": "https://www.netflix.com",
        "hulu": "https://www.hulu.com",
        "disney plus": "https://www.disneyplus.com",
        "amazon prime": "https://www.primevideo.com"
    }
    if service_name.lower() in services:
        webbrowser.open(services[service_name.lower()])
        return f"Opening {service_name} in your web browser"
    else:
        return f"Streaming service {service_name} not recognized"

def parse_command(command):
    try:
        if "weather" in command:
            weather_description = asyncio.run(get_weather("Managua"))
            query = "System Information: " + str(weather_description)
            print(query)
            response = assist.ask_question_memory(query)
            done = assist.TTS(response)

        elif "image search" in command:
            files = os.listdir("./images")
            [os.remove(os.path.join("./images", f)) for f in files]
            query = command.split("-")[1].strip()  # Extract search query
            search(query)

        elif "play" in command:
            spot.start_music()

        elif "pause" in command:
            spot.stop_music()

        elif "skip" in command:
            spot.skip_to_next()

        elif "previous" in command:
            spot.skip_to_previous()

        elif "spotify" in command:
            spotify_info = spot.get_current_playing_info()
            query = "System Information: " + str(spotify_info)
            print(query)
            response = assist.ask_question_memory(query)
            done = assist.TTS(response)

        elif "open" in command:
            app_name = command.split("open ")[1].strip()
            # Check if the app name is a known streaming service
            if app_name.lower() in ["netflix", "hulu", "disney plus", "amazon prime"]:
                response = open_streaming_service(app_name)
            else:
                response = open_application(app_name)
            print(response)
            assist.TTS(response)

        elif "web search for" in command:
            query = command.split("web search for ")[1].strip()
            response = search_web(query)
            print(response)
            assist.TTS(response)

        elif "search youtube for" in command:
            query = command.split("search youtube for ")[1].strip()
            response = search_youtube(query)
            print(response)
            assist.TTS(response)

        elif "hashtag search the web for" in command:
            query = command.split("hashtag search the web for ")[1].strip()
            response = search_web(query)
            print(response)
            assist.TTS(response)

    except IndexError:
        print("Error: Command not formatted correctly.")
        assist.TTS("Error: Command not formatted correctly.")
