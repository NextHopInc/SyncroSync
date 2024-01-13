#This class will deal with both editiing and deleting the Configurations in ConnectWise 



import GrabID as grab
import requests as req 
import ssl
import SyncroData as sync
import json
import pickle

#Public Key: BfvV0W5qie4v3dr4
#Private Key: QXmxufg4eUl3239R
#memberID syncrsync

cwToken ="bmV4dGhvcCtCZnZWMFc1cWllNHYzZHI0OlFYbXh1Zmc0ZVVsMzIzOVI="
cwHeaders = {"Authorization" : "Basic " + cwToken, "clientID":"3040b6af-ac90-42e6-932d-9178fc76f128"  , "Content-Type":"application/json; charset=utf-8"  , "Accept" : "application/vnd.connectwise.com+json; version=2022.1"
}
codebase_data =req.get(url = "https://na.myconnectwise.net/login/companyinfo/nexthop" , headers=cwHeaders )

codebase = codebase_data.json().get("Codebase")
cwURL = "https://api-na.myconnectwise.net/"+codebase+"//apis/3.0/"
#https://na.myconnectwise.net


#CREATES NEW ASSET IN CONNECT WISE single id 201 == good
def createNewConfig(): 
    # grab.getConnectWiseClientID()
    # C:/Users/RileyHall/OneDrive - Nexthop Solutions Inc/Documents/ConnectWiseSyncroLink/
    with open('newPostReqCW.json' , "r")as f:
        file = json.load(f)

    #     lines = f.readlines() 
    # with open('C:/Users/RileyHall/OneDrive - Nexthop Solutions Inc/Documents/ConnectWiseSyncroLink/newPostReqCW.json' , "w+")as write:
    #     current_position = previous_position = write.tell()

    #     for line in lines: 
    #         if(line.strip("\n") != lines.__contains__("asset")):
    #             write.write(line) 
    #         previous_position = current_position
    #         current_position = write.tell()
    #     write.truncate(previous_position-2)
    #     # file = json.load(write)
    #     file = lines
    #     write.close()
    


        
    
    print( "We are sending it" , file)
   


    requests = req.post(url=cwURL+"company/configurations",json=file , headers=cwHeaders)
    print("Content= " , requests.content , "\n")
    print(requests.url)
    print("JSON RETURN= " ,requests.json(),"\n")
    print("Status= ",requests.status_code)
    if(requests.status_code !=201): 
        return requests.json()
    else:
        return requests.status_code




# createNewConfig() 

#Is called when we need to update a company instead of adding one 
def updateCompany(path , identify , element , id): 

    print( path,identify , element , "ELEMENT")
    if(path == "company"):
        x = [{"op" : "replace" , "path" : path , "value" : {identify : element}}]
    else: 
        x = [{"op" : "replace" , "path" : path , "value" : element}] 
    id = str(id)

    requests = req.patch(url=cwURL+"company/configurations/"+id,json=x , headers=cwHeaders)
    print(x)
    # print("Content= " , requests.content , "\n")
    print(requests.url)
    print("Status= " ,requests.status_code,"\n")
    print(requests.json())
    # print("Status= ",requests.status_code)

    if(requests.status_code != 200): 
        return requests.json() 
    else: 
        return requests.status_code

def pullCompany(): 
    r = req.get(cwURL+"company/companies" , headers=cwHeaders , data =grab.buildJsonFile())
    print(r.json())

def getConfigData(): 
    r = req.get(url=cwURL+"/company/configurations" , headers=cwHeaders)
    print("\n")
    print("Id of 4980VPN01",r.json())
    r = req.get(url=cwURL+"/company/configurations?conditions=name='AC2'" , headers=cwHeaders)
    print("id of ACC-SVR", r.json())


# getConfigData()

# print(len("169.254.179.143|fe80::18c2:f33b:3ff2:b38f%14"))
