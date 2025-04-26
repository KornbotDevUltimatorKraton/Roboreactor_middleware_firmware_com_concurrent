import os
import signal 
import json 
import jwt 
import imaplib
import requests
import time 
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        #FastAPI 
import uvicorn
from typing import Union 
from fastapi import FastAPI,File,UploadFile,Request,Form
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
from itertools import count 
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
   #Generate the code from uploaded structure 
app = FastAPI()
struct_sense = {} #Get the structure of the sensor payload input 
store_piddata = {} #Get the PID data store  
@app.get("/payload_struct")
def get_payloadstruct():

      return struct_sense 
@app.get("/get_stored_pid")
def get_store_pid_process():

     return store_piddata 
@app.post("/store_pid_process")
async def store_pid_process(request:Request):
        req_pid = await request.json() #Get the request json 
        print("Get pid request: ",req_pid) #Get the pid request 
        category = req_pid.get('components') 
        pid_number = req_pid.get('PID') 
        store_piddata[category] = pid_number #Get the PID  
        return store_piddata #Get the response of the pid data 
@app.post("/kill_pid_process")
async def kill_pid_process(request:Request):
        req_pidkill = await request.json() #Get the request kill pid 
        print("Get pid kill ",req_pidkill) #Get the pid kill data 
        category = req_pidkill.get('components')
        os.kill(store_piddata[category],signal.SIGTERM)
        del store_piddata[category] #Delete the PID data  
        return store_piddata
@app.post("/sense_postprocessing")
async def post_senseprocessing(request:Request):
        ressense = await request.json() #Get the request json data 
        print("Response sense: ",ressense)  
        category = list(ressense)[0]   #Get the category data 
        component_name = list(ressense.get(category))[0] #Get the component name
        payload = ressense.get(category).get(component_name) #Get the payload 
        object_name = list(payload)[0]
        print("Get_payload object detection: ",payload)
        list_non_append = ['Audio_system'] #Get the non append type data 
        if category not in list(struct_sense):
               print("Category is not existing in the list")
               struct_sense[category] = {component_name:payload} #Get the payload data 
        if category in list(struct_sense):
               print("Category is existing in the list")
               if component_name not in list(struct_sense[category]):
                       print("Component not existing in the list")
                       if category not in list_non_append:
                             struct_sense[category][component_name] = payload 
                       if category in list_non_append:
                             struct_sense[category] = {component_name:payload}                           
               if component_name in list(struct_sense[category]):
                       print("component name is existing in the list")
                       if category not in list_non_append:
                            struct_sense[category][component_name][object_name] = payload[object_name] 
                       if category in list_non_append:
                            struct_sense[category] = {component_name:payload}
                            
        print("Structure payload sensor: ",struct_sense) 
        return struct_sense
if __name__ == "__main__":

        uvicorn.run("internal_servercom:app",host="0.0.0.0",port=8967)



