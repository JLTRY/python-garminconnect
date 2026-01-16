import garth
from getpass import getpass
import requests
import logging
import http.client as http_client
import sys
from pprint import *
requests.packages.urllib3.add_stderr_logger();
http_client.HTTPConnection.debuglevel = 1

email = "jltryoen@gmail.com"#input("Enter email address: ")
password = "JLBRITRy17;" #getpass("Enter password: ")
# If there's MFA, you'll be prompted during the login
logger = logging.getLogger('my_app')
logger.setLevel(logging.DEBUG)          # On veut tout capturer

# 2. Handler console (niveau INFO)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
console_fmt = logging.Formatter('%(levelname)s - %(message)s')
console_handler.setFormatter(console_fmt)
logging.getLogger("urllib3").addHandler(console_handler)
logging.getLogger("urllib3").setLevel(logging.DEBUG)
http_client.HTTPConnection.debuglevel = 1
logging.getLogger("requests_oauthlib.oauth1_session").addHandler(console_handler)
logging.getLogger("requests_oauthlib.oauth1_session").setLevel(logging.DEBUG)
logging.getLogger("oauthlib.oauth1.rfc5849").addHandler(console_handler)
logging.getLogger("oauthlib.oauth1.rfc5849").setLevel(logging.DEBUG)
oauth1, oauth2 = garth.login(email, password)

garth.DailyStress.list("2025-01-13", 7)
print("--------------------------------------------------------------------------")
print(oauth1)
print("--------------------------------------------------------------------------")
pprint(oauth2.access_token)
#garth.save("~/.garth")