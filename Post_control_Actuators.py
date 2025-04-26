import requests 
i = 0.9
payload = {"Analog_input":{"PA0":"analog","PA1":"analog","PA2":"analog","PA3":"analog","PA4":"analog","PA5":"analog","PA6":"analog","PA7":"analog"},"pwm_control":{"PB3":i,"PB4":i,"PB5":i,"PB9":i},"servo_control":{"PB14":0,"PB15":0}}
reqdat = requests.post("http://0.0.0.0:4832/receive_payload_data",json=payload).json()
print("Output control data: ",reqdat)
get_sensors = requests.get("http://0.0.0.0:4832/all_sensors_data").json() 
print("Get sensors payload: ",get_sensors)
