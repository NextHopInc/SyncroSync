

import os
from tkinter import *
import tkinter as tk
import tkinter
from tkinter import font
from turtle import back 
import AssetWatcher as asset
import time 
import threading as thread 


try: 
    
    def timer(i , label , r):
        print("timer")
        if (i>0): 
            i-=1
            i = str(i)
            label.set("Time until next sync \n"+i +"\nClick to sync now \n" )
            i = int(i)
            r.after(1000,lambda:timer(i,label , r))
        else:
            close(r)
    def close(r):
        r.destroy()
        asset.getAssetListSyncro()
        
        
    def start():    

        r= tk.Tk()
        r.configure(background='#00ccff')
        counter = 14400
        r.title('Syncro Sync')
        r.geometry('700x500')
        buttonlbl = tk.StringVar() 
        buttonlbl.set(counter)


        # txtbx = tk.Text(r,height = 5 , width=5)
            
        # txtbx.pack() 

        tk.Button(r, textvariable=buttonlbl, width=75 ,height=50 ,  command=lambda: close(r) , background='#0099cc').pack()
        timer(counter , buttonlbl , r)

        

        r.mainloop()
 
     

    def checkForFile(): #Checks to see if files exist if they do then dont create them if they dont create the file then call itself again 
        count = 0
        print(os.listdir())
        files = os.listdir() 
        place = os.getcwd()
        
 
        if(os.path.exists('allclientAssetID.txt') == True):
            print("1")
            count+=1
            
        else: 
            with open("allclientAssetID.txt" , "w") as fp: 
                fp.write("")

        if(os.path.exists('allNewclientAssetInformation.json')==True): 
                print("2")
                count+=1
                
        else: 
            with open("allNewclientAssetInformation.json" , "w") as fp: 
                fp.write("")

        if(os.path.exists("allclientAssetInformation.json")==True): 
            print("3")
            count+=1
        else: 
            with open("allclientAssetInformation.json" , "w") as fp: 
                fp.write("")
                

        if(os.path.exists("newPostReqCW.json")==True): 
            print("4")
            count+=1

        else: 
            with open("newPostReqCW.json" , "w") as fp: 
                fp.write("")

        if(os.path.exists("report.txt") == True): 
            print("5")
            count+=1
            if(count==5):
                start() 
        else: 
            with open("report.txt", 'w')as fp:
                fp.write("")
                checkForFile()


except: 
    print("Error Was thrown") 
checkForFile()


    #send to check for new
