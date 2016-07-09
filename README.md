# Facebook Birthday Bot

Never forget a facebook friends birthday ever again.

This script will check your facebook notifications for birthdays, and automatically write a message to that friends wall.

Dependencies
```python
pip install robobrowser
```

### How it works.

```python
>>> from fb_bday_bot import facebookBirthdayBot as fbot

# Launch the birthday bot in a single line.
>>> fbot(username, password).start()

# Logging is inactive by default.
# To change logging pass the keyword arguments log and logfile.
# Log is a boolean that turns logging on and off.
# Logfile determines whether or not a logfile is written in the working directory.
>>> fbot(username, password, log=True, logfile=True).start()

# The bot will randomly choose from a list of default messages.
# But you can use your own message(s) by assigning a list of strings to the messages keyword argument.
>>> my_msgs = ['Hi there, hope you have a great birthday!']
>>> fbot(username, password, messages=my_msgs).start()

```
You can get an instance of the bot and trigger each stage individually.

```python
>>> from fb_bday_bot import facebookBirthdayBot as fbot

# Get an instance of the class.
>>> my_bot = fbot(username, password)

# Open facebook.
>>> my_bot.open_page()

# Log into facebook using the credentials passed to fbot.
>>>my_bot.login()

# Get a list of birthday notifications as html anchor tags.
# Returns None if no birthday's are found.
>>> links = my_bot.get_birthday_notifications()

# You can check to see if a link is from today.
# You don't need to check this if you're using the send_greetings method
>>> link_valid(links[0])
True

# Sending the birthday message(s) using the links
>>> send_greetings(links)
```

The script can be called from a batch file like the one below.
Do not run it more than once a day, or you will send duplicate messages.

```batch
@ECHO OFF
@start pythonw.exe C:\PythonScripts\fb_bday_bot.py logon_email logon_password
```