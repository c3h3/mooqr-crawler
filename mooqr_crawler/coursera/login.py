'''
Created on Jul 4, 2014

@author: c3h3
'''

from coursera.coursera_dl import get_cookies_for_class,make_cookie_values,get_page
from local_settings import USER, PASSWORD
import requests

def get_login_session(user, password):
    s = requests.Session()
    get_cookies_for_class(s, "db", None, user, password)
    s.cookie_values = make_cookie_values(login_session.cookies, "db")
    return s
    

login_session = requests.Session()
get_cookies_for_class(login_session, "db", None, USER, PASSWORD)
login_session.cookie_values = make_cookie_values(login_session.cookies, "db")
