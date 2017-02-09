# MoodTrackerBot
Telegram bot who asks about the current mood and saves the answers for 
further analysis. In Telegram you find this bot as `@mood_tracker_bot`.

## Usage
Start chatting with the bot. It will interpret every Message you send 
as a mood and save it. After that it asks if this feeling is good or 
bad. This information is saved as a numerical value.

If you chat `/start` or `Hi` and it will ask you every hour how you 
feel. You can stop that with `/stop` or `Stop`.

## Installation
I recommend a virtualenv:
```shell
pyvenv env
source env/bin/activate
```
The dependencies can be installed via pip:
```shell
pip install -r requirements.txt
```
Just run `bot.py` to connect to telegram and answer to messages.

## Forking
If you fork this bot you have to use your own API key. You get one by 
chatting with the `@BotFather`. To save it create a python file
 `apikey.py` which defines the variable `API_KEY`:
 ```Python
 API_KEY = <your api key goes here>
 ```
 Without this file and a key the code will not work.