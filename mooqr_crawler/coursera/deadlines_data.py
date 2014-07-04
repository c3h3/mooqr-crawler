'''
Created on Jul 4, 2014

@author: c3h3
'''

from coursera.coursera_dl import get_page
import requests
from pyquery import PyQuery
from mooqr_crawler.db.mongodb.clients import coursera_deadlines
from dateutil import parser
import datetime


def hg_asst_line_parser(S):
    parsing_results = {}
    label = S(".hg-asst-interval-label").text()
    if label == 'Results':
        parsing_results["res_timestamp"] = int(S(".hg-asst-interval-available .hg-date").attr("data-livetimer-date-primitive"))/1000.0
        parsing_results["res_time"] = S(".hg-asst-interval-available").text()
        
        parsing_results["res_datetime"] = datetime.datetime.fromtimestamp(parsing_results["res_timestamp"])
    
    elif label == 'Evaluation':
        parsing_results["eval_open"] = S(".hg-asst-interval-open").text()
        parsing_results["eval_close"] = S(".hg-asst-interval-close").text()
        parsing_results["eval_open_timestamp"] = int(S(".hg-asst-interval-open .hg-date").attr("data-livetimer-date-primitive"))/1000.0
        parsing_results["eval_close_timestamp"] = int(S(".hg-asst-interval-close .hg-date").attr("data-livetimer-date-primitive"))/1000.0
        
        parsing_results["eval_open_datetime"] = datetime.datetime.fromtimestamp(parsing_results["eval_open_timestamp"])
        parsing_results["eval_close_datetime"] = datetime.datetime.fromtimestamp(parsing_results["eval_close_timestamp"])
        
    elif label == 'Submission':
        parsing_results["sub_open"] = S(".hg-asst-interval-open").text()
        parsing_results["sub_close"] = S(".hg-asst-interval-close").text()
        parsing_results["sub_open_timestamp"] = int(S(".hg-asst-interval-open .hg-date").attr("data-livetimer-date-primitive"))/1000.0
        parsing_results["sub_close_timestamp"] = int(S(".hg-asst-interval-close .hg-date").attr("data-livetimer-date-primitive"))/1000.0
    
        parsing_results["sub_open_datetime"] = datetime.datetime.fromtimestamp(parsing_results["sub_open_timestamp"])
        parsing_results["sub_close_datetime"] = datetime.datetime.fromtimestamp(parsing_results["sub_close_timestamp"])
        
        
    return parsing_results.items()
    

def hg_asst_list_item_parser(S):
    return dict(S(".hg-asst-line").map(lambda :hg_asst_line_parser(PyQuery(this))))
    
def peer_assignment_data_parser(S):
    return S(".hg-asst-list-item").map(lambda :hg_asst_list_item_parser(PyQuery(this)))

    
def assignment_item_deadline_parser(S):
    parsing_results = {}
    parsing_results["softdeadline"] = {}
    parsing_results["harddeadline"] = {}
    
    SS = S(".course-assignment-item-softdeadline")
    parsing_results["softdeadline"]["title"] = SS("time").attr("data-event-title")
    parsing_results["softdeadline"]["location"] = SS("time").attr("data-event-location")
    parsing_results["softdeadline"]["desc"] = SS("time").attr("data-event-description")
    parsing_results["softdeadline"]["times"] = SS("time").attr("data-event-times")
    parsing_results["softdeadline"]["time_str"] = SS("time").text()
    
    parsing_results["softdeadline"]["datetime"] = parser.parse(parsing_results["softdeadline"]["time_str"])
    

    HS = S(".course-assignment-item-harddeadline")
    parsing_results["harddeadline"]["title"] = HS("time").attr("data-event-title")
    parsing_results["harddeadline"]["location"] = HS("time").attr("data-event-location")
    parsing_results["harddeadline"]["desc"] = HS("time").attr("data-event-description")
    parsing_results["harddeadline"]["times"] = HS("time").attr("data-event-times")
    parsing_results["harddeadline"]["time_str"] = HS("time").text()

    parsing_results["harddeadline"]["datetime"] = parser.parse(parsing_results["harddeadline"]["time_str"])
    
    return parsing_results
    
    
def assignment_deadlines_parser(S):
    return S("ul.course-item-list-section-list li").map(lambda :assignment_item_deadline_parser(PyQuery(this)))
        

def quiz_item_deadline_parser(S):
    parsing_results = {}
    parsing_results["softdeadline"] = {}
    parsing_results["harddeadline"] = {}
    
    SS = S(".course-quiz-item-softdeadline")
    parsing_results["softdeadline"]["title"] = SS("time").attr("data-event-title")
    parsing_results["softdeadline"]["location"] = SS("time").attr("data-event-location")
    parsing_results["softdeadline"]["desc"] = SS("time").attr("data-event-description")
    parsing_results["softdeadline"]["times"] = SS("time").attr("data-event-times")
    parsing_results["softdeadline"]["time_str"] = SS("time").text()
    
    parsing_results["softdeadline"]["datetime"] = parser.parse(parsing_results["softdeadline"]["time_str"])
    
    HS = S(".course-quiz-item-harddeadline")
    parsing_results["harddeadline"]["title"] = HS("time").attr("data-event-title")
    parsing_results["harddeadline"]["location"] = HS("time").attr("data-event-location")
    parsing_results["harddeadline"]["desc"] = HS("time").attr("data-event-description")
    parsing_results["harddeadline"]["times"] = HS("time").attr("data-event-times")
    parsing_results["harddeadline"]["time_str"] = HS("time").text()
    
    parsing_results["harddeadline"]["datetime"] = parser.parse(parsing_results["harddeadline"]["time_str"])
    
    return parsing_results
    
    
def quiz_deadlines_parser(S):
    return S(".course-item-list li").map(lambda :quiz_item_deadline_parser(PyQuery(this)))
  
    
    
class CourseraCourseData(object):
    PAGE_URL_TEMPLATE = 'https://class.coursera.org/{class_session}{data_api}'
    DEADLINES_DATA_NAMES = ["quiz","exam","assignment","peer"]
    DEADLINES_DATA_APIS = ["/quiz","/quiz?quiz_type=exam","/assignment","/human_grading",]
    DEADLINES_DATA_PARSERS = [quiz_deadlines_parser,
                              quiz_deadlines_parser,
                              assignment_deadlines_parser,
                              peer_assignment_data_parser]
    
    
    def __init__(self, class_session="db", session_id=None):
        self.class_session = class_session
        self.session_id = session_id
    
    def get_deadlines_html_pages(self, session):
        urls = map(lambda xx:self.PAGE_URL_TEMPLATE.format(class_session=self.class_session,
                                                           data_api=xx),
                   self.DEADLINES_DATA_APIS)
        
        self.deadlines_html_page = map(lambda one_url:PyQuery(get_page(session,one_url)),urls)
    
    def parse_deadlines_data(self, session=None):
        assert ("deadlines_html_page" in self.__dict__) or isinstance(session,requests.Session)
        self.course_deadlines_data = {}
        
        if "deadlines_html_page" not in self.__dict__:
            self.get_deadlines_html_pages(session)
        
        pairing_parsers_apis = zip(self.DEADLINES_DATA_APIS,
                                   self.DEADLINES_DATA_PARSERS,
                                   self.deadlines_html_page,
                                   self.DEADLINES_DATA_NAMES)
        
        for xx in pairing_parsers_apis:
            temp_results = xx[1](xx[2])
            if len(temp_results) > 0:
                self.course_deadlines_data[xx[3]] = temp_results
        
    def update_deadlines_data_to_db(self, session=None, mdb_collection=coursera_deadlines):
        assert ("course_deadlines_data" in self.__dict__) or isinstance(session,requests.Session)
    
        if "course_deadlines_data" not in self.__dict__:
            self.parse_deadlines_data(session)
        
        update_data = {}
        update_data["session"] = self.class_session
        update_data["session_id"] = self.session_id
        update_data["deadlines"] = self.course_deadlines_data
        mdb_collection.insert(update_data)
        
        
    

