import requests
from pyquery import PyQuery
import pandas as pd
import uuid
import datetime


def filter_blanks_in_sessions(one_session_string):
    return " ".join([xx for xx in one_session_string.split(" ") if xx != ""])

def get_chapters_and_sessions(one_book_page_url, output_type="json"):
    """
    output_type in ["list_of_tuple", "json"]
    if output_type=="list_of_tuple" 
        return book_name, page_url, [(ch1_name, [session1_name, session2_name, ...]), (ch2_name, [session1_name, session2_name, ...]), ... ]
    
    if output_type=="json" 
        return {"book_name":book_name,
                "chapters":[{"chapter":ch1_name, "session":[session1_name, session2_name, ...]}, 
                {"chapter":ch2_name, "session":[session1_name, session2_name, ...]}, ... ]}

    """
    
    assert output_type in ["list_of_tuple", "json"]
    
    r = requests.get(one_book_page_url)
    S = PyQuery(r.text)
    book_name = S(".detailheader").text()
    chapters_and_sessions = S("#tab_02_2_content li.chapter").map(lambda ii,ee:(PyQuery(ee)("h3").text(),
                                                                                map(filter_blanks_in_sessions,PyQuery(ee)("h4").map(lambda i,e:PyQuery(e).text()))
                                                                                ))
    
    if output_type=="list_of_tuple" :
        return book_name, one_book_page_url, chapters_and_sessions
    elif output_type=="json":
        return {"book_name":book_name, 
                "page_url":one_book_page_url,
                "chapters":map(lambda xx:{"chapter":xx[0],"sessions":xx[1]},chapters_and_sessions)}
        

        
def insert_book_data_into_db(one_book_url, mongo_client, default_user_id = "pmHzynLotJqXLjTcz"):
    book_data = get_chapters_and_sessions(one_book_url)
    
    planId = "oreilly-" + book_data["page_url"].split("product/")[-1].split(".")[0]



    mongo_client.meteor.plans.remove({"_id":planId})
    planId = mongo_client.meteor.plans.insert({"planName":book_data["book_name"],
                                       "_id":planId,
                                       "planUrl":book_data["page_url"],
                                       "moduleIds" :[],
                                       "userId":default_user_id,
                                       "createAt":datetime.datetime.utcnow()})

    mongo_client.meteor.modules.remove({"planId":planId})
    mongo_client.meteor.tasks.remove({"planId":planId})
    
    module_ids_list = []
    
    
    for one_chapter_dict in book_data["chapters"]:
        print "~~~~~~~~~~~~~~~~~"
        
        module_id = planId + "-" + one_chapter_dict["chapter"] if one_chapter_dict["chapter"] != "" else planId + "-" + str(uuid.uuid1())  
        print "module_id = ",module_id
        
        module_id = mongo_client.meteor.modules.insert({"moduleName":one_chapter_dict["chapter"],
                                             "_id":module_id,
                                             "planId":planId,
                                             "taskIds" :[],
                                             "userId":default_user_id,
                                             "createAt":datetime.datetime.utcnow()})
        
        module_ids_list.append(module_id)
        
        if len(one_chapter_dict["sessions"]) == 0:
            one_chapter_dict["sessions"].append(one_chapter_dict["chapter"])
        
        
        task_ids_list = []
        
        for one_session in one_chapter_dict["sessions"]:
            print "one_session = ",one_session
            session_id = module_id + "--" + str(uuid.uuid1())
            session_id = mongo_client.meteor.tasks.insert({"taskName":one_session,
                                                   "_id":session_id,
                                                   "planId":planId,
                                                   "moduleId" :module_id,
                                                   "userId":default_user_id,
                                                   "createAt":datetime.datetime.utcnow()})
            task_ids_list.append(session_id)
            
        mongo_client.meteor.modules.update({"_id":module_id},{"$push":{"taskIds":{"$each":task_ids_list}}})
            
        
            
            
        
        
    
    mongo_client.meteor.plans.update({"_id":planId},{"$push":{"moduleIds":{"$each":module_ids_list}}})


    
    
    
    
    

