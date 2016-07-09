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
>>> fbot(username, password, messages).start()

# Logging is inactive by default.
# To change logging pass two extra arguments to fbot.
# The first boolean turns logging on and off.
# The second boolean determines whether a log file is generated in the working direcotry.
>>> fbot(username, password, messages, True, True).start()
```
You can get an instance of the bot and trigger each stage individually.

```python
>>> from fb_bday_bot import facebookBirthdayBot as fbot

# Get an instance of the class.
>>> my_bot = fbot(username, password, messages)

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