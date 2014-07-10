'''
Created on Jul 4, 2014

@author: c3h3
'''

from mooqr_crawler.db.mongodb.clients import coursera_courses,coursera_instructors,coursera_sessions,coursera_universities
import pandas as pd 
import ujson
import requests

def api_res_to_json(res_str):
    return ujson.loads(res_str)

###############################################

def update_courses_db():
    r = requests.get("https://api.coursera.org/api/catalog.v1/courses?fields=language,largeIcon,photo,shortDescription,video,aboutTheCourse&includes=sessions,instructors,universities")
    courses_data = api_res_to_json(r.text)
    coursera_courses.drop()
    coursera_courses.insert(courses_data["elements"])
    
def get_courses_df(query={},fields={"id":1,"name":1}):
    if len(fields.keys()) > 0: 
        return pd.DataFrame(list(coursera_courses.find(query,fields)))
    else:
        return pd.DataFrame(list(coursera_courses.find(query)))
    
    
###############################################
    
def update_session_db():
    r = requests.get("https://api.coursera.org/api/catalog.v1/sessions?fields=courseId,status,active,durationString,startDay,startMonth,startYear,name,signatureTrackCloseTime,signatureTrackOpenTime,signatureTrackPrice,signatureTrackRegularPrice,eligibleForCertificates,eligibleForSignatureTrack,certificateDescription,certificatesReady")
    sessions_data = api_res_to_json(r.text)
    coursera_sessions.drop()
    coursera_sessions.insert(sessions_data["elements"])
    
def get_session_df(query={},fields={}):
    if len(fields.keys()) > 0: 
        return pd.DataFrame(list(coursera_sessions.find(query,fields)))
    else:
        return pd.DataFrame(list(coursera_sessions.find(query)))

    
###############################################
    
def update_universities_db():
    r = requests.get("https://api.coursera.org/api/catalog.v1/universities?fields=name,homeLink,banner,locationLat,locationLng")
    universities_data = api_res_to_json(r.text)
    coursera_universities.drop()
    coursera_universities.insert(universities_data["elements"])
    
def get_universities_df(query={},fields={}):
    if len(fields.keys()) > 0: 
        return pd.DataFrame(list(coursera_universities.find(query,fields)))
    else:
        return pd.DataFrame(list(coursera_universities.find(query)))

    
###############################################
    
def update_instructors_db():
    r = requests.get("https://api.coursera.org/api/catalog.v1/instructors?fields=photo,photo150,bio,fullName,title,department,website,websiteTwitter,websiteFacebook,websiteLinkedin,websiteGplus,shortName,prefixName,middleName,suffixName")
    instructors_data = api_res_to_json(r.text)
    coursera_instructors.drop()
    coursera_instructors.insert(instructors_data["elements"])
    
def get_instructors_df(query={},fields={}):
    if len(fields.keys()) > 0: 
        return pd.DataFrame(list(coursera_instructors.find(query,fields)))
    else:
        return pd.DataFrame(list(coursera_instructors.find(query)))









