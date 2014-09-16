

from pyquery import PyQuery
from dateutil import parser

def parse_one_courseware_page(res, flatten=True):
    #course_code = res.url.split("/")[-5]
    
    course_info_list = res.url.split("courseware")[0].split("/")[-4:-1]
    institutionId = course_info_list[0]
    courseLocalId = "/".join(course_info_list[:2])
    sessionLocalId = "/".join(course_info_list)

    
    
    S = PyQuery(res.text)
    course_deadline_data = S(".chapter").filter(lambda iii,eee:len(PyQuery(eee)("li.graded")) > 0).map(lambda i, el:(PyQuery(el)("h3").text(),
                                                                                                                     PyQuery(el)("li.graded").map(lambda ii,ee: (PyQuery(ee)("p:not(.subtitle)").text(),
                                                                                                                                                                 PyQuery(ee)("p.subtitle").text(),
                                                                                                                                                                 PyQuery(ee)("a").attr("href")
                                                                                                                                                                 ))))
    
    
    course_deadline_data_list = []

    for xx in course_deadline_data:
        for yy in xx[1]:
            try:
                due_time = parser.parse(yy[1].split("due")[-1].strip())
                if flatten:
                    course_deadline_data_list.append({"topic":xx[0],
                                                  "subTopic":yy[0],
                                                  "dueStr":yy[1],
                                                  "url":yy[2],
                                                  "dueTime":due_time,
                                                  #"CourseCode":course_code
                                                  "institutionId":institutionId,
                                                  "courseLocalId":courseLocalId,
                                                  "sessionLocalId":sessionLocalId,
                                                  
                                                  })
                else:
                    course_deadline_data_list.append({"topic":xx[0],
                                                  "subTopic":yy[0],
                                                  "dueStr":yy[1],
                                                  "url":yy[2],
                                                  "dueTime":due_time,
                                                  })
            except:
                pass
            
    if flatten:
        return course_deadline_data_list
    else:
        return {#"CourseCode":course_code, 
                "deadlines": course_deadline_data_list,
                "institutionId":institutionId,
                "courseLocalId":courseLocalId,
                "sessionLocalId":sessionLocalId,}
    

def get_deadline_data(edx_url, login_session):
    r = login_session.get(edx_url.dashboard)
    S = PyQuery(r.text)
    courses_info_page_urls = map(lambda xx: edx_url.base + xx,S("article.course").map(lambda :PyQuery(this)("a.cover").attr("href")))
    courses_courseware_page_urls = map(lambda xx:xx.replace("info","courseware"),courses_info_page_urls)
    
    courses_courseware_pages = map(login_session.get,courses_courseware_page_urls)
    all_course_deadlines = map(parse_one_courseware_page, courses_courseware_pages)
    return all_course_deadlines
    
    
    