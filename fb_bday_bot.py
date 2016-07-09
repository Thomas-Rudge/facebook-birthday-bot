#! python3
#-------------------------------------------------------------------------------
# Name:        facebook-birthday-bot
# Purpose:     Automatically checks your facebook notifications for
#              friends birthdays, and writes a message on their wall.
# Author:      Thomas Rudge
#
# Created:     5th July 2016
# Modified:    9th July 2016
# Copyright:   (c) Thomas Rudge
# Licence:     MIT
#-------------------------------------------------------------------------------

from robobrowser import RoboBrowser as robo
import logging, re, datetime, sys, random, traceback

class facebookBirthdayBot:

    def __init__(self, email, password, **kwargs):
        self.email         = email
        self.password      = password
        self.messages      = None
        self.log           = False
        self.logfile       = False
        self.browser       = None
        self.fb_url_login  = 'https://www.facebook.com/login'
        self.fb_url_notifs = 'https://m.facebook.com/notifications'
        self.date          = datetime.datetime.today()
        # Handle keyword arguments for logging and messages
        if 'log' in kwargs:
            self.log = kwargs['log']

        if 'logfile' in kwargs:
            self.logfile = kwargs['logfile']

        if 'messages' in kwargs:
            self.messages = kwargs['messages']
        else:
            self.messages = ('Happy birthday!',
                              'Hope you have a great birthday!',
                              'Happy birthday  \u263A',
                              'Happy birthday, have a great day!',
                              '\U0001F382 Happy Birthday \U0001F382 ',
                              'Happy birthday, have a good one',
                              '\U0001F389 \U0001F38A \U0001F389 Happy Birthday  \U0001F389  \U0001F38A  \U0001F389',
                              '\U0001F381 Happy Birthday \U0001F381 ')

        # Set the logging settings based on the log flags
        if self.logfile:
            logging.basicConfig(filename='%s_fbBdayBot_logfile.txt' % str(self.date.date()),
                                level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
        else:
            logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

        if not self.log:
            logging.disable(logging.CRITICAL)

    def start(self):
        logging.debug('Start triggered.')
        self.open_page()
        self.login()
        notifications = self.get_birthday_notifications()

        if notifications:
            self.send_greetings(notifications)

        logging.debug('Start ends.')

    def open_page(self):
        logging.debug('Initating browser and opening main page.')

        try:
            self.browser = robo(history=True, parser="lxml")
            self.browser.open(self.fb_url_login)
        except:
            logging.error(traceback.format_exc())

    def login(self):
        '''
        Logs into facebook
        '''
        logging.debug('Logging into Facebook.')
        form_id = 'login_form'

        try:
            form = self.browser.get_form(form_id)

            if not form:
                raise Exception("Form with id '%s' not found." % form_id)

            form['email'] = self.email
            form['pass']  = self.password
            self.browser.submit_form(form)
        except:
            logging.error(traceback.format_exc())

    def get_birthday_notifications(self):
        '''
        This function will take the browser to the page...

           'https://m.facebook.com/notifications'

        ...and return a list of links that relate to birthdays.
        '''
        logging.debug('Fetching birthday notifications.')

        try:
            self.browser.open(self.fb_url_notifs)
            link_pattern = re.compile(r'((Today is ).+(s birthday))', re.IGNORECASE)
            bday_links = self.browser.get_links(link_pattern)
        except:
            logging.error(traceback.format_exc())

        if not bday_links:
            logging.debug('Single person notification not found, trying multi.')

            try:
                link_pattern = re.compile(r'(have birthdays today.)')
                bday_links = self.browser.get_links(link_pattern)
            except:
                logging.error(traceback.format_exc())

        logging.debug('%s birthday notifications found.' % str(len(bday_links)))

        return bday_links

    def link_valid(self, link):
        '''
        Takes the unix timestamp in the link and returns True if it is from today, else False.
        '''
        logging.debug('Check validity of link: %s' % str(link))

        epoch_start = datetime.datetime(1970, 1, 1)
        # Get the 10 digit unix time from the link
        epoch_ptn = re.compile(r'[0-9]{10}')
        link = str(link)
        epoch = re.search(epoch_ptn, link)

        if epoch:
            logging.debug('Unix timestamp found: %s' % epoch)
            epoch = int(epoch.group())

            if epoch_start.date() + datetime.timedelta(0, epoch) == self.date.date():
                logging.debug('Link date is valid')
                return True

        logging.debug('Link date is valid')

        return False

    def send_greetings(self, bdays):
        '''
        The function iterates through the links in 'bdays' and posts
        a message from taken randomly from the list of messages.
        '''
        logging.debug('Start sending messages.')

        for link in bdays:

            # Skip if not valid
            if not self.link_valid(link):
                continue

            try:
                # Go to the friends page
                self.browser.follow_link(link)
                # Get all forms because the post form has no id
                forms = self.browser.get_forms(method='post')
            except:
                logging.error(traceback.format_exc())
                continue

            for form in forms:
                logging.debug('Attempting form.')

                try:
                    form['xc_message'] = random.choice(self.messages)
                    # This will mimic a button press on the post input element
                    submit_field = form['view_post']
                except:
                    try:
                        form['message'] = random.choice(self.messages)
                        # This will mimic a button press on the post input element
                        submit_field = form['post']
                    except:
                        logging.error(traceback.format_exc())
                try:
                    self.browser.submit_form(form, submit=submit_field)
                    logging.debug('Form submitted.')
                except:
                    logging.error(traceback.format_exc())


if __name__ == '__main__':
    # Expects to be started form a batch file
    vars_ = sys.argv

    if not vars_:
        sys.exit()

    email_ = vars_[1]
    password_ = vars_[2]

    facebookBirthdayBot(email_, password_, log=True).start()

    sys.exit()
