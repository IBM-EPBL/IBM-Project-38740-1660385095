# importing required modules and libraries  
import datetime # to read present date  
import time # to suspend the execution for a specific time  
import requests # to retrieve COVID stats from web  
from plyer import notification # to get notification on the computer  
  
# initializing a variable with None (temporary)  
# indicating that there is no data available currently  
from app.py import predict
user = int(input("Enter 1 to send notification, enter 0 to not send a notification"))
demandpower = float(input("Enter demanded value"))
title = "Sorry, demanded power can't be generated for 2022 -11-19"
message = "Predicted value is {predict}  but,  Demanded value is {demandpower}"  
    # repeating the loop for multiple times  
while(user ==1):
    notification.notify(  
        # defining the title of the notification,  
        title = title,
        
        # defining the message of the notification  
        message = message,
        # creating icon for the notification  
        # we have to download a icon of ico file format  
        app_icon = "windmill.ico",  
        # the notification stays for 30 seconds  
        timeout  = 30,  
        
        )
    break