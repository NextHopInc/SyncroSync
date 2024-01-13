#Creates report of what changed each iteration. Maybe will email it probably not 
import base64
from functools import partial
import re
import time
import datetime
import json
import smtplib as smtp
import win32com.client as win32
#Dictionary must come as CompanyName : {AssetName : {Change Occured : change} 
def emailChange(): 
    pass


def createReport(changes): #Creates the report by adding date and time and just prininting out the change logs 
    print(changes)
    print("Report")

    perCompany = {}
    today = datetime.date.today() 
    t = time.localtime()
    currentTime = time.strftime("%H:%M:%S" , t)
    x = str(today.strftime('%B-%d-%Y'))
    currentTime = str(currentTime)
    #C:/Users/RileyHall/OneDrive - Nexthop Solutions Inc/Documents/ConnectWiseSyncroLink
    with open("report.txt" , "w+" ) as f:
        f.write( x + " " + currentTime ) 
        f.write("\n")
        if(len(changes) == 0): 
            f.write("Nothing Occurred")
    #C:/Users/RileyHall/OneDrive - Nexthop Solutions Inc/Documents/ConnectWiseSyncroLink/
    with open("report.txt" , "a" ) as f: 
        f.write("________________________________________________________________")
        f.write("\n")
        name = json.dumps(changes , indent=4 ,ensure_ascii=False)
        f.write(name)
        f.write("\n")
        f.write("________________________________________________________________")
        f.write("\n")
        f.close() 
    email() 


def email(): #Sends report to email 
    try:
        rec = "thalladsadasdad@nexthop.ca"
        
        outlook = win32.Dispatch('outlook.application')
        mail = outlook.CreateItem(0)

        mail.To = rec 
        mail.Subject = 'Syncro Sync Update'
        mail.Body = 'Syncro Sync update see attached'

        #C:/Users/RileyHall/OneDrive - Nexthop Solutions Inc/Documents/ConnectWiseSyncroLink/
        path = "report.txt"

        mail.Attachments.Add(path)

        mail.send
    
    except: 
        return 0
                    
    