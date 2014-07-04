'''
Created on Jul 4, 2014

@author: c3h3
'''

from pymongo import MongoClient
from local_settings import MONGODB_URI

mongodb_cli = MongoClient(MONGODB_URI)

mooqr_crawler_db = mongodb_cli.coursera
coursera_courses = mooqr_crawler_db.coursera_courses
coursera_sessions = mooqr_crawler_db.coursera_sessions
coursera_universities = mooqr_crawler_db.coursera_universities
coursera_instructors = mooqr_crawler_db.coursera_instructors
coursera_deadlines = mooqr_crawler_db.coursera_deadlines
