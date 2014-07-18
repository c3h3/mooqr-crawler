'''
Created on Jul 18, 2014

@author: c3h3
'''

from mooqr_crawler.edx.login import get_login_session
from mooqr_crawler.edx.deadlines_data import get_deadline_data
from mooqr_crawler.db.mongodb.clients import edx_deadlines


all_course_deadlines = get_deadline_data(**get_login_session())
edx_deadlines.insert(all_course_deadlines)

