#This is both the change listener and the create new asset listener. With timer to start again every hour may use Task manager eventually for it. ***Does not Download nor upload information relies on other
#Classes for that like SyncroData.py and GrabID.py
#THIS IS THE CLASS THAT WILL RULE OVER ALL!!!!! SO ROUGHLY ASSETWATCHER->SyncroData.PY ->GRABID.PY TO CONNECTWISEUPLOAD || ASSET WATCHER IS THE TRIGGER CLASS

from datetime import datetime
from pickle import APPEND, TRUE
import time
import shutil
from types import NoneType
import report as r 
import GrabID as grab
datetime
import SyncroData as sync
import json
import traceback
import ConnectWiseUpload as wise 
import guiSyncroSync as gui 

#potentially will run on this timer or will put it on task manager runner
report = {} 
def timer(): 
    total_mins = 5
    while(total_mins):
        mins , secs = divmod(total_mins,60)
        timer = '{:02d}:{:02d}'.format(mins,secs)
        print(timer,end='\r')
        time.sleep(1)
        total_mins-=1
        
    print("Timer Done")
    getAssetListSyncro()
#Gets all the assets from SyncroMSP with syncro name syncro asset id and syncro company name that the asset belongs too.. 

def findConfig(data , configName , request):
    configID = 0
    print("made it")
    x=""
    word = ""
    
    for i in range (len(data.json())): 

    
        print(data.json()[i].get("name") , "findconfig help" , configName)
        if data.json()[i].get("name") == configName: #if asset exists within in connectwise then get the CW ID 
            print("Bonjour")
            configID = data.json()[i].get("id")
            print(configID) 
            return configID
    print(configID)
    request = str(request)
    
    if(configID == 0): 
        print("brek")
        for i in request:
            if(i == '{' ):
                x = x+i+"\n"
            elif(i == '}'):
                x=x+"\n"+i
            elif(i==','):
                x=x+i+"\n"
            elif(i=="'"):
                x=x.strip("'")
                x=x+'"' 
            else:
                x=x+i
               

         

        print(x)
        
        x=x.replace("True" , "true")
        x = x.replace("asset : {" , "")
        print(x)
        # x  = json.loads(x)
        print(type(x) , x)
        x = x.strip('"\"')
        print("x before chaos" , x)
        # x = json.dumps(x , indent=4 ,ensure_ascii=False)
        
        # with open("C:/Users/RileyHall/OneDrive - Nexthop Solutions Inc/Documents/ConnectWiseSyncroLink/newPostReqCW.json" , "w") as write:
        #     for j in x:   
        #         write.write(j)
            # write.close()
            # write.write(x)
        
       
        # if(x.__contains__("DESKTOP-68LU045")):
        # wise.createNewConfig()
        
        print("HELLLLLLO")
        return 0
    

def getAssetListSyncro(): 
    print("HEEEEEEEE")
    assetDict = sync.getAssets()
    print(assetDict) 
    print(len(assetDict))
    # archiveNewAssets(assetDict)
    # archiveAssetList(assetDict)
    print("HEEEEEEEE")
    # archiveAssets()
    # archiveAssets(assetDict)
    #first method call
    checkForNewAssetsListener(assetDict)
    # getArchiveAssets()
    print("FULL LOOP COMPLETE")
    r.createReport(report)
    #If timer is recalled from here that is a full loop where assets are both checked for update and checked for new assets 
    # timer()
    gui.start()
    return assetDict


def archiveAssetList(assets): 
    try:
        #C:/Users/RileyHall/OneDrive - Nexthop Solutions Inc/Documents/ConnectWiseSyncroLink/assetData/
        with open("allclientAssetID.txt" , "w+") as w:
            for key in assets:
                
                w.write(str(assets.get(key).get("AssetID")))
                w.write("\n")
            w.close()
    except:
        print("Cant write asset id to txt file")
        print(traceback.format_exc())
    # checkForNewAssetsListener(assets)





#//////////////////////////////////////////////////////////////////////////////////////
#Archives all asstets 
def archiveNewAssets(assets , nonSimilar):
    count = 0
    print("******************************************************************************")
    #C:/Users/RileyHall/OneDrive - Nexthop Solutions Inc/Documents/ConnectWiseSyncroLink/assetData/
    with open("allNewclientAssetInformation.json"  , "w+") as d:
        d.seek(0)
        d.truncate()
        d.write("[")
        d.write("\n")
        d.close()
    if(len(assets)>0):
        for key in assets:
            try:
                print(assets.get(key).get("AssetID"))
                print(assets.get(key).get("ComapnyName") , key , assets.get(key).get("AssetID"))
                jsonFile = grab.getConnectWiseClientID(assets.get(key).get("ComapnyName") , key , assets.get(key).get("AssetID"))
                #C:/Users/RileyHall/OneDrive - Nexthop Solutions Inc/Documents/ConnectWiseSyncroLink/
                with open("newPostReqCW.json" , 'r') as r:
                    jsonFile = json.load(r)

                jsonFile = json.dumps(jsonFile , indent=4 ,ensure_ascii=False)
                #C:/Users/RileyHall/OneDrive - Nexthop Solutions Inc/Documents/ConnectWiseSyncroLink/assetData/
        
                with open('allNewclientAssetInformation.json' , 'a' , encoding='utf-8' )as f:
                    f.write(jsonFile)
                    f.write(",")
                    f.write("\n")
                    count = count+31
                    f.close()
                print("success")
        

            except:
                print("json file cant be composed")
                print(traceback.print_exc())
                continue

                # C:/Users/RileyHall/OneDrive - Nexthop Solutions Inc/Documents/ConnectWiseSyncroLink/assetData/
        with open('allNewclientAssetInformation.json' , 'r+' , encoding='utf-8' )as f:
            current_position = previous_position = f.tell()
            while f.readline():
                previous_position = current_position
                current_position = f.tell()
            f.truncate(previous_position-2)
            f.close()
            #Got rid of the , at the end then adds the } and ] to complete JSON array
            #C:/Users/RileyHall/OneDrive - Nexthop Solutions Inc/Documents/ConnectWiseSyncroLink/assetData/
        with open('allNewclientAssetInformation.json' , 'a' , encoding='utf-8' )as f:
            f.write("}\n")
            f.write("]")
            f.close()
    #makes call to compare all similar assets checks for any updates. after return writes in the non similar and then will transfer the data to the other json file 
   
        getArchiveAssets()
#C:/Users/RileyHall/OneDrive - Nexthop Solutions Inc/Documents/ConnectWiseSyncroLink/assetData/
    with open('allNewclientAssetInformation.json' , 'r+' , encoding='utf-8' )as f:
        current_position = previous_position = f.tell()
        while f.readline():
            previous_position = current_position
            current_position = f.tell()
        f.truncate(previous_position)
        #C:/Users/RileyHall/OneDrive - Nexthop Solutions Inc/Documents/ConnectWiseSyncroLink/assetData/
        f.close()
    with open('allNewclientAssetInformation.json' , 'a' , encoding='utf-8' )as f:
        if(len(assets)>0):
            f.write(",")
        else: 
            f.write("[")
        f.write("\n")
        f.close()
    for keys in nonSimilar:
        try: 
            print(nonSimilar.get(keys).get("AssetID"))
            print(nonSimilar.get(keys).get("ComapnyName") , keys , nonSimilar.get(keys).get("AssetID"))
            
            print("NON SIMILAR")
            jsonFile = grab.getConnectWiseClientID(nonSimilar.get(keys).get("ComapnyName") , keys , nonSimilar.get(keys).get("AssetID"))
            #C:/Users/RileyHall/OneDrive - Nexthop Solutions Inc/Documents/ConnectWiseSyncroLink/
            with open("newPostReqCW.json" , 'r') as r:
                jsonFile = json.load(r)

            jsonFile = json.dumps(jsonFile , indent=4 ,ensure_ascii=False)
            print(jsonFile)
#C:/Users/RileyHall/OneDrive - Nexthop Solutions Inc/Documents/ConnectWiseSyncroLink/assetData/
    
            with open('allNewclientAssetInformation.json' , 'a' , encoding='utf-8' )as f:
                f.write(jsonFile)
                f.write(",")
                f.write("\n")
                count = count+31
                f.close()
            print("success")   
        except: 
            print("JSON FILE NOT LOADED")
            print(traceback.format_exc())

#C:/Users/RileyHall/OneDrive - Nexthop Solutions Inc/Documents/ConnectWiseSyncroLink/assetData/
    with open('allNewclientAssetInformation.json' , 'r+' , encoding='utf-8' )as f:
        current_position = previous_position = f.tell()
        while f.readline():
            previous_position = current_position
            current_position = f.tell()
        f.truncate(previous_position)
        f.close()
        #Got rid of the , at the end then adds the } and ] to complete JSON array
        #C:/Users/RileyHall/OneDrive - Nexthop Solutions Inc/Documents/ConnectWiseSyncroLink/assetData/
    with open('allNewclientAssetInformation.json' , 'a' , encoding='utf-8' )as f:
        f.write("\n")
        if(len(nonSimilar)>0):
            f.write("}")
        f.write("\n")
        f.write("]")
        f.close()
    
    archiveAssets()

#////////////////////////////////////////////////////////////////////////////
#Saves all assets to a JSON file to be read later for changes. needs Dict with asset id in syncro asset name in syncro and company name in syncro 
def archiveAssets(): 
    #C:/Users/RileyHall/OneDrive - Nexthop Solutions Inc/Documents/ConnectWiseSyncroLink/assetData/
    #C:/Users/RileyHall/OneDrive - Nexthop Solutions Inc/Documents/ConnectWiseSyncroLink/assetData/
    shutil.copyfile("allNewclientAssetInformation.json" , 
    "allclientAssetInformation.json" )
    print("finish copying")



def getArchiveAssets():
    try: #IT will error if there are no values in the folders or if corruption occured and not right format so set to empty if exception is thrown
        #C:/Users/RileyHall/OneDrive - Nexthop Solutions Inc/Documents/ConnectWiseSyncroLink/assetData/
        with open("allclientAssetInformation.json"  , "r") as read: 
            jsonFile = json.load(read)
            read.close()
        oldAsset = json.dumps(jsonFile , indent=4 ,ensure_ascii=False)
    except: 
        oldAsset = {} 
    try:
        #C:/Users/RileyHall/OneDrive - Nexthop Solutions Inc/Documents/ConnectWiseSyncroLink/assetData/
        with open("allNewclientAssetInformation.json" ,"r") as read: 
            jsonFile = json.load(read)
            read.close()
        newAsset = json.dumps(jsonFile , indent=4 ,ensure_ascii=False) 
    except:
        newAsset = {}
    if(len(oldAsset)>0):
        checkForUpdate(oldAsset,newAsset)
    else: 
        print("Uncomplete Loop")
        r.createReport(report)
        archiveAssets()
        # timer()
        gui.start()

def sortJsonFiles(): 
    pass

#Checks for NEW ASSETS...........
def checkForNewAssetsListener(assets):
    archive = []
    print('made it to asset id') 
    fileReport = {}
    #All similar DATA TO PULL FROM SYNCRO
    assetDict= {}
    addNewAsset = []
    #NON SIMILAR DATA PULL FROM SYNCRO LATER
    nonSimlarData = {}
    x = {}
    flag = True
    #C:/Users/RileyHall/OneDrive - Nexthop Solutions Inc/Documents/ConnectWiseSyncroLink/assetData/
    with open("allclientAssetID.txt" , "r+")as read:
        for line in read:
            archive.append(line.strip("\n"))
            
    #PUTS previous ids in list 
    for key in assets:
        flag =True
        #Searching for new IDS 
        for k in range(len(archive)):
            if(assets.get(key).get("AssetID")==int(archive[k])):
                flag = False
                print("Checked")
                x = {key : {"ComapnyName" : assets.get(key).get("CompanyName") , "AssetID" : assets.get(key).get("AssetID") }}
                assetDict.update(x)
                break
            else:
                flag = True
        print(flag)
        if(flag == True):
            print("FLAGGED")
            
            #ALL NEW CODE 
            grab.getConnectWiseClientID(assets.get(key).get("CompanyName") , key , assets.get(key).get("AssetID"))
            #C:/Users/RileyHall/OneDrive - Nexthop Solutions Inc/Documents/ConnectWiseSyncroLink/
            with open("newPostReqCW.json" , "r") as read: 
                file = json.load(read)
                read.close()
            compID = file.get("company").get("id")
            compID = grab.getConfigID(compID)
            name = file.get("name")
            id = findConfig(compID , name , file)
            if(id==0):
                grab.getConnectWiseClientID(file.get("company").get("name") , file.get("name") , assets.get(key).get("AssetID"))
                status = wise.createNewConfig()
                #IF config created add to list 
                if(status ==201): 
                    addNewAsset.append(assets.get(key).get("AssetID"))
                    fileReport = { file.get("name") : "Asset Created"}
                else: 
                    #else dont add to list 
                    with open ("newPostReqCW.json" , "r")as read: 
                        attempt = json.load(read)
                    fileReport = {file.get("name") : "Asset Could not be created" , "requset"  : attempt , "Status" : status}
            else:  
                status = wise.updateCompany("tagNumber" , "tagNumber" , "zz" , id)
                nonSimlarData.update(x)
                if(status == 200): 
                    addNewAsset.append(assets.get(key).get("AssetID"))
                else: 
                    with open("newPostReqCW.json" , "r")as read: 
                        attempt = json.load(read)
                    fileReport = {file.get("name") : "Asset Could not be updated" , "requset"  : attempt , "Status" : status}
            #TOO HERE IF IT DOESNT WORK ITS PROBABLY WRONG SOMEWHERE HERE
            print("COmpanyNAmeasdfasdfsafdsafasf" , assets.get(key).get("CompanyName"))
            x = {key : {"ComapnyName" : assets.get(key).get("CompanyName") , "AssetID" : assets.get(key).get("AssetID") }}
            
            
            report.update(fileReport)
            print(addNewAsset)
    print(assetDict , nonSimlarData)
    archiveAssetList(assets)
    archiveNewAssets(assetDict , nonSimlarData)



#This watches for updates on the json files if we find one that needs to be updated then we can send that json file over too connectwise
def checkForUpdate(oldAsset, newAsset):
    changeFlag = False
    path = ""
    identify = ""
    element = ""
    print(type(oldAsset))
    oldAsset = json.loads(oldAsset)
    newAsset = json.loads(newAsset)
    count = 0
    for i in range(len(newAsset)): 
        changeFlag = False
        for j in range(len(oldAsset)):
            
            
            if(newAsset[i].get("name") == oldAsset[j].get("name")):
                print("First if statement")
                print(newAsset[i])
                for key in newAsset[i]:
                   
                    # if (type(newAsset[i].get("asset").get(key)) == dict): 
                    #     print("Second if statement")
                        
                    #     for keys in newAsset[i].get("asset").get(key):
                    #         print(newAsset[i].get("asset").get(key).get(keys))
                    #         if(newAsset[i].get("asset").get(key).get(keys)!=oldAsset[j].get("asset").get(key).get(keys)):
                    #             changeFlag = True
                    #             print(oldAsset[j].get("asset").get(key).get(keys))
                    #             print("////////////////")
                    #             print(newAsset[i].get("asset").get(key).get(keys))
                     
                    if(newAsset[i].get(key) != oldAsset[j].get(key)):
                        
                        print(newAsset[i].get(key))
                        # print("assets that change" , newAsset[i].get(key).get(kys))
                        #this gets the path of what needs to be changed 
                        path = list(newAsset[i].keys())[list (newAsset[i].values()).index(newAsset[i].get(key))]
                        #IF data type is dict then we know we have to iterate through the keys with in that dict as well so we need to enter into more for loops
                        if(type(newAsset[i].get(key)) == dict):#IF dictionary we need to iterate through those values as well 
                            print("dict")
                            for k in newAsset[i].get(key):
                                print(newAsset[i].get(key).get(k))
                                try:
                                    if(newAsset[i].get(key).get(k) != oldAsset[j].get(key).get(k)):
                                        print("found")
                                        #This is getting the identifyer for the patch request probably a simpler way to do it but too lazy to find it 
                                        identify = list(newAsset[i].get(key).keys())[list (newAsset[i].get(key).values()).index(newAsset[i].get(key).get(k))] 
                                        element = newAsset[i].get(key).get(k)
                                        print("FINDED",path , identify , element)
                                        compID = newAsset[i].get(key).get("company").get("id")
                                        print("BROTHER" , compID)
                                        configid = grab.getConfigID(compID)
                                        print(newAsset[i].get(key).get("name"), "NAME help")
                                        id = findConfig(configid , newAsset[i].get("name") , newAsset[i].get(key)) 
                                        if(id!=0):
                                            print("Hello My brother" , element , identify , path)
                                            wise.updateCompany(path,identify,element , id) 
                                            fileReport = {newAsset[i].get("name") : element}
                                            report.update(fileReport)

                                except AttributeError:#This means the whole field didnt exist ex.... type{id:8 , name:server} etc
                                        identify = list(newAsset[i].get(key).keys())[list (newAsset[i].get(key).values()).index(newAsset[i].get(key).get(k))] 
                                        element = newAsset[i].get(key)
                                        print("FINDED",path , identify , element)
                                        compID = newAsset[i].get("company").get("id")
                                        print("BROTHER" , compID)
                                        configid = grab.getConfigID(compID)
                                        print(newAsset[i].get(key).get("name"), "NAME help")
                                        id = findConfig(configid , newAsset[i].get("name") , newAsset[i].get(key)) 
                                        if(id!=0):
                                            print("Hello My brother" , element , identify , path)
                                            wise.updateCompany(path,identify,element , id) 
                                            fileReport = {newAsset[i].get("name") : element , "Reason" : "Field Does not exist"}
                                            report.update(fileReport)

                                

                                    #id = config id , configid = to all configurations for given company and newAsset[i].get("name") is the name of the configuration 
                                    #need this to check if asset is in connectwise or not if not then we need a POST request if yes then we need PATCH request might need to create 

                        else: #if key doesnt point to dictionary
                            if(newAsset[i].get(key)!= oldAsset[j].get(key)):
                                print("found")
                                path = list(newAsset[i].keys())[list (newAsset[i].values()).index(newAsset[i].get(key))]
                                
                                print(newAsset[i].get(key))
                            
                                print("found")
                                #This is getting the identifyer for the patch request probably a simpler way to do it but too lazy to find it 
                                identify = list(newAsset[i].keys())[list (newAsset[i].values()).index(newAsset[i].get(key))] 
                                element = newAsset[i].get(key)
                                print("FINDED",path , identify , element)
                                compID = newAsset[i].get("company").get("id")
                                print("BROTHER" , compID)
                                configid = grab.getConfigID(compID )
                                id = findConfig(configid , newAsset[i].get("name") , newAsset[i].get(key))
                                if(id!=0):
                                    print("Hello my brothers" , element , path , identify)
                                    wise.updateCompany(path,identify,element , id)                                    
                                    fileReport = {newAsset[i].get("name") : element}
                                    report.update(fileReport)   
                                                
                                    
                            #Trying to get the key to send to connectwise to patch the existing configuration

                    

    # if(newAsset != oldAsset):
    #     for key in newAsset: 

    #         if(newAsset.get(key) == list): 
    #             for i in range(len(newAsset.get(key))): 
    #                 if(newAsset.get(key)[i] != oldAsset.get(key)[i]): 
    #                     changeFlag = True     
    #         else: 
    #             if(newAsset.get(key) != oldAsset.get(key)): 
    #                 changeFlag = True
    #         if(newAsset.get(key) == "cpuSpeed"): 
    #             pass
    #             if(changeFlag): 
    #                 pass
    #                 #Send to upload the past couple lines to connectWise
    #             else: 
    #                 continue


# getArchiveAssets()
# getAssets()
# newAssetListener()
# timer()



# getAssetListSyncro()
