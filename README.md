# jarvis.v1
Jarvis.v1

Initial Plan:
- To create an Ironman inspired AI Agent with the ability to do more than just talk. First saw on ConceptBytes page. 
At first, just getting it to communicate to me like Jarvis was the main goal, even if it was just a talking LLM. Then, AI Agent ideas came. 
First connected features like weather, time, spotify, image search, and web search.

Initial Features:
- Spotify controls (Only worked when spotify was already open)
- Real time weather information
- Real time time information
- Ability to open apps
- Ability to search for images and return them in the same folder
- Ability to perform web searches
- Ability to open streaming services.

Limitations
- Speed: The need to do STT, send the query to the OpenAI API, recieve the query and then do TTS limits the speed.
- Speed2: The bigger the query recieved, the longer it takes to do TTS.
- Spotify: At the moment, the spotify controls (Play, skip, volupe up/down, pause) only work if spotify was alreayd open and playing.
- Streaming Services: It opens up the page of the service but does not put on a specific requested show or movie. 
- Weather: Weather location must be set, it is not automatic detection.

Plans for Jarvis.v2

New features:

Vscode.py
- Add complete control of VSCode to facilitate coding.
- Create a project command: This will create a new folder with the name of the said project in a specific direcotry that is made
for projects that jarvis creates.
-Create file command: This command is to start working on a projevt, it should create a file with the name given into the folder of the project.
- Generate code command: If you ask it to generate code for something specific, it will do a query to the OpenAI API in order to make the code
and then add it to the file where you want it created. (Example: Jarvis make me the code for a calculator in pyhton. This should be
responded with writing said code in the file location.)
- Terminal surfing: Add the ability for Jarvis to move between directories in order for it to have bets control of vscode. It should already
know the paths in my computer based on information i will teach it so that it does not need to ask for the path.

ToDoApp
- Create a simple To DO App handled by jarvis input. 
- Based on what I tell Jarvis, she will need to organize my day and ask any question necesary in order to maintain the most order possible.
- The app should have three stages: Done, In progress, Not started.
- Jarvis should be able toi manage them based on what I tell it.
- It should also have a due date for each of the to do things and log the hour and date when it was logged.
- When you click on an assignment, it will open a window of that assignment with all the information for the assignment this includes but is not limited to:
-- Task 
-- Description
-- Date & Time it was logged
-- Expected Due date
-- Stage 

Google Calendar 
- Give Jarvis the ability to controll and handle a calendar in my Google Calendar via the GoogleCalendar API
- Should have the ability to create, delete, update, and retrieve things in my calendar.
- Using POST, DELETE, GET requests we can achive this connection between Jarvis and Google Calendar.
- Jarvis shoudld ask what I want to schedule, how I want to name it, the duration, the time, the date.
- Recgonize the day of the week we are in so that I can use terms like today, tomorrow, of the day of the week. 
