import os
import json 
import serial
import requests
from multiprocessing import Process
import uvicorn
from typing import Union
from fastapi import FastAPI,File,UploadFile,Request,Form
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from itertools import count

app = FastAPI()
payload_store = {} #Get the store payload data to control actuators and function logic of actuators 
state_publish = {} 
rec_payload = {} #Get the receive payload data 
try:
     hardware_comm_ttyUSB0 = serial.Serial('/dev/ttyUSB0',115200)
except:
     print('Error accessing serial hardeware device')
        
@app.get("/all_sensors_data")
def get_sensor_data():
            
     return payload_store #Get the output positioon store   
       
@app.get('/status_publish')
def status_publish():
    if state_publish == {}:
         state_publish['status'] = 'non_published'  
         return state_publish 
    if state_publish != {}:
         return state_publish 
@app.get('/get_rec_payload')
def getrec_payloadat():
     if rec_payload != {}:
        return rec_payload['Sensors_payload']
     if rec_payload  == {}:
        #Get the full GPIO port input to get the analog data 
        payload_ref = {"Analog_input":{"PA0":"analog","PA1":"analog","PA2":"analog","PA3":"analog","PA4":"analog","PA5":"analog","PA6":"analog","PA7":"analog"},"pwm_control":{"PB3":0,"PB4":0,"PB5":0,"PB9":0},"servo_control":{"PB14":0,"PB15":0}}
        return payload_ref       
@app.post('/receive_payload_data')
async def receive_payload_data(request:Request): #Receive the payload data of the control 
     print("Receive the payload data") 
     reqrec = await request.json() #Receive the JSON payload
     print("Payload struct: ",reqrec) #Display payload struct 
     rec_payload['Sensors_payload'] = reqrec  #Store the current command payload data 
     state_publish['status'] = 'published' 
     return reqrec    
@app.post('/control_payload_data')
async def control_payload_data(request:Request): #Get the control payload data 
     print("Control logic data")
     reqdat = await request.json() #get the payload request data 
     print("Request data: ",reqdat)
     #Send the request data to the serial port
     #payload_store['control'] = reqdat #Get the payload store data
     try:
       hardware_comm_ttyUSB0.close() #Close the serial first to start writing  
       hardware_comm_ttyUSB0.open()
       hardware_comm_ttyUSB0.write((json.dumps(reqdat)+"\n").encode()) #Sending the control payload data to the hardware 
       sensors_response = hardware_comm_ttyUSB0.readline().decode().strip()
       print("Sensors response: ",sensors_response)
       sensor_payloadres = {"Sensors":{'STM32F103C8T6':{'mcus_sensor':sensors_response}}} #Setting the sensor payload response  
       #Post request sensor payload data 
       payload_store['Sensors'] = sensor_payloadres['Sensors'] 
       reqsensor = requests.post("http://0.0.0.0:8967/sense_postprocessing",json=sensor_payloadres) #Post the sensor response data 
       print("Request sensor: ",reqsensor.json()) #Get the payload JSON output   
     except:
         print("Error serial handeling")
     return reqsensor.json()  #reqdat #Get the returning data of control serial port actuators and sensors 
#USE PC13 pin of the mcus on to activate request of the Analog data and sensor data requests 

def function_control_payload(): 
        uvicorn.run("mcus_controller_server:app",host="0.0.0.0",port=4832) #Actuator control port and sensor data request 


actuator_control_thread = Process(target=function_control_payload)
actuator_control_thread.start()
actuator_control_thread.join()

