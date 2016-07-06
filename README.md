# Facebook Birthday Bot

Never forget a facebook friends birthday ever again.

This script will check your facebook notifications for birthdays, and automatically write a message to that friends wall.

The script can be called from a batch file like the one below.

```batch
@ECHO OFF
@start pythonw.exe C:\PythonScripts\fb_bday_bot.py logon_email logon_password
```
//TODO

* Add more logging


Dependencies
```python
pip install robobrowser
```