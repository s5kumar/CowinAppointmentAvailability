# -*- coding: utf-8 -*-
"""
Created on Wed May  4 13:31:21 2021

@author: anandkumars82@gmail.com
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor


"""
import json
import requests
import urllib.request
import urllib.parse
import winsound
import datetime
import os
import re
import time
#from twilio.rest import Client #uncomment when you need whatsapp msgs using TWILIO
from datetime import date
# Find these values at https://twilio.com/user/account

TWILIO_ACCOUNT_SID = 'ACXXXXXXXXXXXXXXXXX' # twilio account id
TWILIO_AUTH_TOKEN = '5fXXXXXXXXXXXXXXXXXXXX' # twilio auth token
TWILIO_FROM_NUMBER = 'whatsapp:+XXXXXXXX' # add your twilio number
TWILIO_TO_NUMBER = 'whatsapp:+91XXXXXXXXX' # add the whatsapp number...create session on Twilio..or use sms
OTP_MOBILE_NUMBER = '{"mobile":"XXXXXXXXX"}' # add the mobile number at XXX
MINAGE = 18 # change to 45 if you are looking for 45+
MINCOUNT = 0 # if you want to avoid single return slots, change to 1

NUMBER_OF_DAYS_SCOUT = 2

DISTRICT_LIST = [('BBMP',"district_id=294"), ('URBAN',"district_id=265"), ('RURAL',"district_id=276")]



def sendWhatsAppMsgwithTwilio(bodytxt):
    
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        from_=TWILIO_FROM_NUMBER,
        body=bodytxt,
        to=TWILIO_TO_NUMBER
        )

def sendOTPRequest():
    headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json',
            }
    
    data = OTP_MOBILE_NUMBER
    
    response = requests.post('https://cdn-api.co-vin.in/api/v2/auth/public/generateOTP', headers=headers, data=data)

        
loop_run = True # run infinite loop

while(loop_run):
   
    today1 = datetime.date.today() #start from today

    for i in range(NUMBER_OF_DAYS_SCOUT):
        if (loop_run == False):
            break
        today2 = today1+ datetime.timedelta(days=i)
        date = today2.strftime("%d-%m-%Y")
        str1="&date="
        date_append=str1+date
     
        
        for j in range(len(DISTRICT_LIST)):
            if (loop_run == False):
                    break
                
            district_append = DISTRICT_LIST[j][1]

            print (DISTRICT_LIST[j][0] + " " + date)
              
               
            http_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?" + district_append + date_append
    
            print (http_url)
            time.sleep(5)
            base_request_header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
            'Upgrade-Insecure-Requests' : '1'
            }
            
            g = requests.get(http_url, headers = base_request_header)
            
            
            cal_data = json.loads(g.text)

       
            for key,value in cal_data.items():
                
                if (loop_run == False):
                    break
                for i in value:
                    print(i['name'] + ' ' + str(i['min_age_limit']) + ' ' + str(i['available_capacity']))
                    if(i['min_age_limit'] == MINAGE and i['available_capacity'] > MINCOUNT):        
                        print("Name: " + i['name'])
                        print("Date: " + str(i['date']))
                        print("Available: " + str(i['available_capacity']))
                        print("Pincode: " + str(i['pincode']))
                        
                        duration = 2000  # Set Duration To 1000 ms == 1 second
                        frequency = 2500  # Set Frequency To 2500 Hertz
                        if(i['available_capacity'] > 1): # smaller beeps for lower count
                            duration = 10000;
                            loop_run = False # remove this if you want it to continue running after finding one
                        
                        winsound.Beep(frequency, duration)
                        
                        bodytxt=i['name'] + ' ' + i['date'] + ' ' + str(i['pincode'])
                        sendOTPRequest()
                        #uncomment below line when you want the whatsapp msg using Twilio
                        #sendWhatsAppMsgwithTwilio(bodytxt) 

                        break
   
   
     
          
            

    
   
   
               
          
           
            
        