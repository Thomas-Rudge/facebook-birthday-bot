#-------------------------------------------------------------------------------
# Name:        facebook-birthday-bot
# Purpose:     Automatically checks your facebook notifications for
#              friends birthdays, and writes a message on their wall.
# Author:      Thomas Rudge
#
# Created:     5th July 2016
# Copyright:   (c) Thomas Rudge
# Licence:     MIT
#-------------------------------------------------------------------------------

from robobrowser import RoboBrowser as robo
import logging, re, datetime, sys


def open_page(url):
    '''
    This function will start up the browser on the given url
    '''
    browser = robo(history=True)
    browser.open(url)

    return browser


def login(browser, email, pwd):
    '''
    Logs into facebook
    '''
    form = browser.get_form('login_form')
    form['email'] = email
    form['pass'] = pwd
    browser.submit_form(form)

    return browser


def get_birthday_notifications(browser):
    '''
    This function will take the browser to the page...

       'https://m.facebook.com/notifications'

    ...and return a list of links that relate to birthdays.
    '''
    browser.open('https://m.facebook.com/notifications')
    link_pattern = re.compile(r'((Today is ).+(s birthday))', re.IGNORECASE)
    bday_links = browser.get_links(link_pattern)

    return bday_links


def link_valid(link):
    '''
    Takes the unix timestamp in the link and returns True if it is from today, else False.
    '''
    epoch_start = datetime.datetime(1970, 1, 1)
    ## Get the 10 digit unix time from the link
    epoch_ptn = re.compile(r'[0-9]{10}')
    link = str(link)
    epoch = re.search(epoch_ptn, link)

    if epoch:
        epoch = int(epoch.group())

        if epoch_start.date() + datetime.timedelta(0, epoch) == datetime.datetime.today().date():
            return True

    return False


def send_greetings(browser, bdays):
    '''
    The function iterates through the links in 'bdays' and posts a message
    '''
    message = 'Happy Birthday!'

    for link in bdays:
        if link_valid(link):
            ## Go to the friends page
            browser.follow_link(link)
            ## Get all forms because the post form has no id
            forms = browser.get_forms()
            ## The first form is the searchbar
            ## Change the content of the post form
            forms[1]['xc_message'] = message
            ## This will mimic a button press on the post input element
            submit_field = forms[1]['view_post']
            ## Now submit the message
            browser.submit_form(forms[1],submit=submit_field)

def main():
    global browser, page_url

    browser = open_page(page_url)
    browser = login(browser, email, pwd)
    birthdays = get_birthday_notifications(browser)

    if not birthdays:
        sys.exit()



if __name__ == '__main__':
    vars_ = sys.argv

    if not vars_:
        sys.exit()

    email = vars_[1]
    pwd = vars_[2]
    ## Set globals
    page_url = 'https://www.facebook.com/login'
    browser = None
    date = datetime.datetime.today()
    ## Set logging
    log = True
    logfile = False

    if not log:
        logging.disable(logging.CRITICAL)
    elif logfile:
        logging.basicConfig(filename='%s_fbBdayBot_logfile.txt' % str(date.date()),
                            level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
    else:
        logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

    main()
