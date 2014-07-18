'''
Created on Jul 4, 2014

@author: c3h3
'''

from mooqr_crawler.db.mongodb.clients import coursera_deadlines
from mooqr_crawler.coursera.deadlines_data import CourseraCourseData
from mooqr_crawler.coursera.login import login_session

test_list = ["optimization-002","datasci-002","smac-001","algo-004","statistics-001","dsp-004","basicwriting-004"] 
test_ccd_list = map(CourseraCourseData,test_list)
map(lambda xx:xx.update_deadlines_data_to_db(login_session),test_ccd_list)

