'''
Created on Jul 4, 2014

@author: c3h3
'''

from pymongo import MongoClient
try:
    from local_settings import MONGODB_URI, C3H3MONGOHQ_URI, WITH_METEOR
except:
    from mooqr_crawler.settings import MONGODB_URI, C3H3MONGOHQ_URI, WITH_METEOR
    

# mongodb_cli = MongoClient(MONGODB_URI)
#  
# mooqr_crawler_db = mongodb_cli.coursera
# coursera_courses = mooqr_crawler_db.coursera_courses
# coursera_sessions = mooqr_crawler_db.coursera_sessions
# coursera_universities = mooqr_crawler_db.coursera_universities
# coursera_instructors = mooqr_crawler_db.coursera_instructors
# coursera_deadlines = mooqr_crawler_db.coursera_deadlines
# edx_deadlines = mooqr_crawler_db.edx_deadlines


c3h3mongohq_cli = MongoClient(C3H3MONGOHQ_URI)
mooqr_db = c3h3mongohq_cli.mooqr

if not WITH_METEOR:
    mooqr_courses = mooqr_db.courses
    mooqr_sessions = mooqr_db.sessions
    coursera_courses = mooqr_db.coursera_courses
    coursera_sessions = mooqr_db.coursera_sessions
    coursera_universities = mooqr_db.coursera_universities
    coursera_instructors = mooqr_db.coursera_instructors
    coursera_deadlines = mooqr_db.coursera_deadlines
    edx_deadlines = mooqr_db.edx_deadlines
else:
    meteor_db = c3h3mongohq_cli.meteor
    mooqr_courses = meteor_db.courses
    mooqr_sessions = mooqr_db.sessions
    coursera_courses = meteor_db.coursera_courses
    coursera_sessions = meteor_db.coursera_sessions
    coursera_universities = meteor_db.coursera_universities
    coursera_instructors = meteor_db.coursera_instructors
    coursera_deadlines = meteor_db.coursera_deadlines
    edx_deadlines = meteor_db.edx_deadlines



