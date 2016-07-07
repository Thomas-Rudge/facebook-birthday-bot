#! python3
#-------------------------------------------------------------------------------
# Name:        facebook-birthday-bot
# Purpose:     Automatically checks your facebook notifications for
#              friends birthdays, and writes a message on their wall.
# Author:      Thomas Rudge
#
# Created:     5th July 2016
# Modified:    7th July 2016
# Copyright:   (c) Thomas Rudge
# Licence:     MIT
#-------------------------------------------------------------------------------

from robobrowser import RoboBrowser as robo
import logging, re, datetime, sys, random

class fb_bot:

    def __init__(self, email, pwd, messages, log=False, logfile=False):
        self.email       = email
        self.pwd         = pwd
        self.messages    = messages
        self.log         = log
        self.logfile     = logfile
        self.browser     = None
        self.pg_url      = 'https://www.facebook.com/login'
        self.pg_url_ntfy = 'https://m.facebook.com/notifications'
        self.date        = datetime.datetime.today()

        if not log:
            logging.disable(logging.CRITICAL)
        elif logfile:
            logging.basicConfig(filename='%s_fbBdayBot_logfile.txt' % str(self.date.date()),
                                level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
        else:
            logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

    def start(self):
        self.open_page()
        self.login()
        notifications = self.get_birthday_notifications()

        if notifications:
            self.send_greetings(notifications)

    def open_page(self):
        self.browser = robo(history=True)
        self.browser.open(self.pg_url)

    def login(self):
        '''
        Logs into facebook
        '''
        form = self.browser.get_form('login_form')
        form['email'] = self.email
        form['pass'] = self.pwd
        self.browser.submit_form(form)

    def get_birthday_notifications(self):
        '''
        This function will take the browser to the page...

           'https://m.facebook.com/notifications'

        ...and return a list of links that relate to birthdays.
        '''
        self.browser.open(self.pg_url_ntfy)
        link_pattern = re.compile(r'((Today is ).+(s birthday))', re.IGNORECASE)
        bday_links = self.browser.get_links(link_pattern)

        if not bday_links:
            link_pattern = re.compile(r'(have birthdays today.)')
            bday_links = self.browser.get_links(link_pattern)

        return bday_links

    def link_valid(self, link):
        '''
        Takes the unix timestamp in the link and returns True if it is from today, else False.
        '''
        epoch_start = datetime.datetime(1970, 1, 1)
        # Get the 10 digit unix time from the link
        epoch_ptn = re.compile(r'[0-9]{10}')
        link = str(link)
        epoch = re.search(epoch_ptn, link)

        if epoch:
            epoch = int(epoch.group())

            if epoch_start.date() + datetime.timedelta(0, epoch) == self.date.date():
                return True

        return False

    def send_greetings(self, bdays):
        '''
        The function iterates through the links in 'bdays' and posts
        a message from taken randomly from the list of messages.
        '''
        message = 'Happy Birthday!'

        for link in bdays:
            if self.link_valid(link):
                # Go to the friends page
                self.browser.follow_link(link)
                # Get all forms because the post form has no id
                forms = self.browser.get_forms(method='post')

                for form in forms:
                    try:
                        form['xc_message'] = random.choice(self.messages)
                        # This will mimic a button press on the post input element
                        submit_field = form['view_post']
                    except:
                        form['message'] = random.choice(self.messages)
                        # This will mimic a button press on the post input element
                        submit_field = form['post']

                    self.browser.submit_form(form, submit=submit_field)


if __name__ == '__main__':
    # Expects to be started form a batch file
    vars_ = sys.argv

    if not vars_:
        sys.exit()

    em = vars_[1]
    pw = vars_[2]

    msgs = ('Happy birthday!',
            'Hope you have a great birthday!',
            'Happy birthday  \u263A',
            'Happy birthday, have a great day!',
            '\U0001F382 Happy Birthday \U0001F382 ',
            'Happy birthday, have a good one',
            '\U0001F389 \U0001F38A \U0001F389 Happy Birthday  \U0001F389  \U0001F38A  \U0001F389',
            '\U0001F381 Happy Birthday \U0001F381 ')

    fb_bot(em, pw, msgs, False, False).start()

    sys.exit()
