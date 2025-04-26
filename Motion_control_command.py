import requests 
from itertools import count
i = 40
for ri in count(0):
       #Post non publish data here
       get_res = requests.get("http://0.0.0.0:4832/get_rec_payload").json() 
       print("GPIO control payload: ",get_res) #Get the response payload data 
       #Get the request data 
       Analog_Input = get_res.get('Analog_input')
       PWM_control = get_res.get('pwm_control')
       Servo_control = get_res.get('servo_control')
       #Use this default when no published data detected in the list
       #Get the publish status request 
       state_publish = requests.get('http://0.0.0.0:4832/status_publish').json() 
       if state_publish['status'] == 'non_published': 
          print("Default status")
          payload = {"Analog_input":{"PA0":"analog","PA1":"analog","PA2":"analog","PA3":"analog","PA4":"analog","PA5":"analog","PA6":"analog","PA7":"analog"},"pwm_control":{"PB3":i,"PB4":i,"PB5":i,"PB9":i},"servo_control":{"PB14":30,"PB15":30}}       
          #Checkig the existing payload GPIOs is existing in the list of the created GPIO after updated or not 
          reqdat = requests.post("http://0.0.0.0:4832/control_payload_data",json=payload).json() 
          print(reqdat)
       if state_publish['status'] == 'published':
           print("Activated published")
           payload = {"Analog_input":Analog_Input,"pwm_control":PWM_control,"servo_control":Servo_control}     
           reqdat = requests.post("http://0.0.0.0:4832/control_payload_data",json=payload).json() 
           print(reqdat)
 
