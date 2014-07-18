'''
Created on Jul 17, 2014

@author: c3h3
'''

from local_settings import EDX_USER, EDX_PASSWORD
from .urls import EdxUrls
import requests

def get_login_session(edx_site="edx", user=EDX_USER, password=EDX_PASSWORD):
    edx_url = EdxUrls(edx_site="edx")
    s = requests.Session()
    
    r1 = s.get(edx_url.login_ajax)
    s.headers['Referer'] = edx_url.login_ajax
    s.headers['X-CSRFToken'] = s.cookies.get_dict()['csrftoken']
    
    auth_post_data = {'email': user, 'password': password,'remember': False}
    r2 = s.post(edx_url.login_ajax,data=auth_post_data)
    
    return {"edx_url":edx_url, "login_session":s}



