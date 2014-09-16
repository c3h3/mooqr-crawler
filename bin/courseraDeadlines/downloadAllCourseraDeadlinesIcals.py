'''
Created on Jul 31, 2014

@author: c3h3
'''

from mooqr_crawler.db.mongodb import clients
import pandas as pd
import os,commands

import string
import random
from dateutil.parser import parse
import ujson
import re
import numpy as np
import traceback


def create_new_id(collection, check_list=None):
    random_str = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(17))
    
    if check_list == None:
        while (collection.find({"_id":random_str}).count() > 0):
            random_str = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(17))
    else:
        while (collection.find({"_id":random_str}).count() > 0) or (random_str in check_list):
            random_str = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(17))
        
    
    return random_str


def _create_new_id(collection, check_list=None, auto_append=True):
    random_str = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(17))
    
    if check_list == None:
        while (collection.find({"_id":random_str}).count() > 0):
            random_str = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(17))
    else:
        while (collection.find({"_id":random_str}).count() > 0) or (random_str in check_list):
            random_str = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(17))
        
        if auto_append:
            check_list.append(random_str)
        
    
    return random_str

CourseraDeadlinePath = "/home/c3h3/c3h3works/Hacking/mooqr-crawler/bin/courseraDeadlines/dataJsons/"
DownloadedCoursesList = os.listdir(CourseraDeadlinePath)

#################################################


# df = pd.DataFrame(list(clients.mooqr_sessions.find({},{'sessionLocalId':1, "courseId":1, "sid":1, "_id":0})))
#  
# def download_cli(cli_str):
#     print "[Executing] " + cli_str
#     cli_res = commands.getoutput(cli_str)
#     print "[Std Output] "
#     print cli_res
#     print "[Finished Executing] " + cli_str
#     return cli_res
#      
#  
#  
# cli_results = df["sessionLocalId"].map(lambda xx:"coffee getCourseraDeadlinesJSON.coffee %s %s" % (xx, CourseraDeadlinePath)).map(download_cli)

#################################################

# df = pd.DataFrame(list(clients.mooqr_sessions.find({},{"courseId":1,"sessionLocalId":1,"provider":1})))
# df["sessionId"] = df["_id"]
# df = df.drop("_id",axis=1)
# df = df.set_index("sessionLocalId")
# df["sessionLocalId"] = df.index
# 
# 
# def update_one_sessionLocalId(one_sessionLocalId, lookup_df = df):
#     print "[update_one_sessionLocalId] BEGIN ... "
#     print "[update_one_sessionLocalId] one_sessionLocalId = ",one_sessionLocalId
#     
#     with open(CourseraDeadlinePath + one_sessionLocalId,"r") as rf:
#         data = ujson.loads(rf.read())
#     
#     one_sessionLocalId_df = pd.DataFrame([data[key] for key in data if len(data[key].keys())>0])
#     one_sessionLocalId_meta = df.ix[one_sessionLocalId].to_dict()
#     
#     for key in one_sessionLocalId_meta.keys():
#         one_sessionLocalId_df[key] = one_sessionLocalId_meta[key]
#     
#     if "start" in one_sessionLocalId_df.columns:
#         one_sessionLocalId_df["startTime"] = one_sessionLocalId_df["start"].map(lambda xx:parse(xx))
#     
#     if "end" in one_sessionLocalId_df.columns:
#         one_sessionLocalId_df["endTime"] = one_sessionLocalId_df["end"].map(lambda xx:parse(xx))
#     
#     for one_event in one_sessionLocalId_df.to_dict(outtype="records"):
#         
#         if clients.mooqr_course_events.find({"sessionId":one_event["sessionId"], "uid":one_event["uid"]}).count() == 0:
#             new_id = create_new_id(clients.mooqr_course_events)
#             one_event["_id"] = new_id
#             
#             print "[update_one_sessionLocalId] UPDATING one_event ... ",
#             
#             clients.mooqr_course_events.insert(one_event)
#             
#             print "[update_one_sessionLocalId] FINISHED UPDATING one_event = ",one_event
#             
#         else:
#             print "[update_one_sessionLocalId] ALREADY EXISTS one_event = ",one_event
#             
#             
# map(update_one_sessionLocalId,DownloadedCoursesList)            

#################################################

df = pd.DataFrame(list(clients.mooqr_sessions.find({},{"courseId":1,"sessionLocalId":1,"provider":1})))
df["sessionId"] = df["_id"]
df = df.drop("_id",axis=1)
df = df.set_index("sessionLocalId")
df["sessionLocalId"] = df.index


def get_one_event_tasks_data(one_event_local_id, events_df_lookup, one_sessionLocalId_df_lookup):
    print "[in get_one_event_tasks_data] Starting ... "
    print "[in get_one_event_tasks_data] one_event_local_id = ", one_event_local_id
    
    tasks_df = one_sessionLocalId_df_lookup.ix[one_event_local_id]
    tasks_df["penalty"] = tasks_df["description"]
    
    print '''events_df_lookup.ix[one_event_local_id]["singleTaskEvent"] = ''', events_df_lookup.ix[one_event_local_id]["singleTaskEvent"]
    
    try:
        singleTaskEvent = bool(events_df_lookup.ix[one_event_local_id]["singleTaskEvent"])
    except:
        singleTaskEvent = events_df_lookup.ix[one_event_local_id]["singleTaskEvent"]

    if singleTaskEvent:
    
        _final_data = events_df_lookup.ix[one_event_local_id].to_dict()
        _final_data["evetId"] = _final_data["_id"]
        
        del _final_data["_id"]
        
        try:
            _final_data["deadlines"] = tasks_df[["startTime","endTime","penalty","deadlineType"]].to_dict(outtype="records")
        except:
            _final_data["deadlines"] = tasks_df[["startTime","endTime","penalty","deadlineType"]].to_dict()
            
        _final_data["taskId"] = _create_new_id(clients.mooqr_db.courseTasks)
        _final_data["singleTaskEvent"] = bool(_final_data["singleTaskEvent"])
        final_data = [_final_data]
    
    else:
        try:
            tasks_df["deadlines"] = map(lambda xx:[xx],tasks_df[["startTime","endTime","penalty"]].to_dict(outtype="records"))
        except:
            tasks_df["deadlines"] = map(lambda xx:[xx],tasks_df[["startTime","endTime","penalty"]].to_dict())
        
        
        tasks_df["taskTitle"] = tasks_df["deadlineType"]
        tasks_df["taskType"] = tasks_df["deadlineType"]
    
        merged_tasks_df = pd.merge(tasks_df[["taskTitle","taskType","deadlines"]].reset_index(),events_df_lookup.reset_index(), left_on="eventLocalId", right_on="eventLocalId", how="inner")
        merged_tasks_df["eventId"] = merged_tasks_df["_id"]
        merged_tasks_df = merged_tasks_df.drop("_id",1)
        
        
        tasks_id_list = []
        [ _create_new_id(clients.mooqr_db.courseTasks,tasks_id_list) for nn in range(merged_tasks_df.shape[0])]
    
        merged_tasks_df["taskId"] = tasks_id_list
        final_data = merged_tasks_df.to_dict(outtype="records")
    
    print "[in get_one_event_tasks_data] Finished ... "
    
    return final_data

def update_session_events(one_sessionLocalId):
    print "[In update_session_events] Starting ... "
    print "[In update_session_events] one_sessionLocalId = ",one_sessionLocalId

    
    with open(CourseraDeadlinePath + one_sessionLocalId,"r") as rf:
        data = ujson.loads(rf.read())
        
    one_sessionLocalId_df = pd.DataFrame([data[key] for key in data if len(data[key].keys())>0])
    one_sessionLocalId_meta = df.ix[one_sessionLocalId].to_dict()
    for key in one_sessionLocalId_meta.keys():
        one_sessionLocalId_df[key] = one_sessionLocalId_meta[key]
    
    for yy in ["params","transparency","type"]:
        try:
            one_sessionLocalId_df = one_sessionLocalId_df.drop(yy, axis=1)
        except:
            pass

    summary_decode = one_sessionLocalId_df["summary"].map(lambda xx:  re.match("(?P<eventTitle>[^(]*)\((?P<eventSubTitle>[^)]*)\)",xx).groupdict())
    one_sessionLocalId_df["eventTitle"] = summary_decode.map(lambda xx:xx["eventTitle"])
    one_sessionLocalId_df["eventSubTitle"] = summary_decode.map(lambda xx:xx["eventSubTitle"])
    
    one_sessionLocalId_df["eventLocalId"] = one_sessionLocalId_df["uid"].map(lambda xx:"|".join(xx.split("|")[:3]))
    one_sessionLocalId_df["deadlineType"] = one_sessionLocalId_df["uid"].map(lambda xx:xx.split("|")[3])
    one_sessionLocalId_df["eventType"] = one_sessionLocalId_df["uid"].map(lambda xx:xx.split("|")[1])
    one_sessionLocalId_df["startTime"] = one_sessionLocalId_df["start"].map(lambda xx:parse(xx))
    one_sessionLocalId_df["endTime"] = one_sessionLocalId_df["end"].map(lambda xx:parse(xx))
    one_sessionLocalId_df["url"] = one_sessionLocalId_df["location"]
    
    group_by_list = ["provider","courseId","sessionId","eventLocalId","eventType","eventTitle","url"]
    grouped = one_sessionLocalId_df.groupby(group_by_list)
    
    etype = grouped.apply(lambda xx: "hard" in xx["deadlineType"].tolist())
    events_df = etype.reset_index()
    events_df.columns = group_by_list + ["singleTaskEvent"]
    events_df["singleTaskEvent"] = events_df["singleTaskEvent"].map(bool)
    
    
    update_eids = [ xx['eventLocalId'] for xx in events_df[["provider","courseId","sessionId","eventLocalId"]].to_dict(outtype="records") if clients.mooqr_course_events.find(xx).count() == 0 ]
    events_df = events_df[np.in1d(events_df["eventLocalId"],update_eids) ]
    
    
    if events_df.shape[0] > 0 :
        
        events_id_list = []
        
        [ _create_new_id(clients.mooqr_course_events,events_id_list) for nn in range(events_df.shape[0])]
        
        events_df["_id"] = events_id_list
        events_df_lookup = events_df.set_index("eventLocalId")
        one_sessionLocalId_df_lookup = one_sessionLocalId_df.set_index("eventLocalId")
        
        
        update_events_data = events_df.to_dict(outtype="records")
        for xx in update_events_data:
            xx["tasks"] = get_one_event_tasks_data(one_event_local_id = xx["eventLocalId"], events_df_lookup = events_df_lookup, one_sessionLocalId_df_lookup = one_sessionLocalId_df_lookup)


        clients.mooqr_course_events.insert(update_events_data)
    
    print "[In update_session_events] Finished ... "
    

def skip_update_session_events(one_sessionLocalId):
    try:
        update_session_events(one_sessionLocalId)
    except Exception as e:
        print "[Exception ... ]"
        print e
        print "[Traceback ... ]"
        print traceback.format_exc()

map(skip_update_session_events, DownloadedCoursesList)            





