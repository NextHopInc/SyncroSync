#Interacts with the connectwise get functions from the REST API ******ONLY GRABS INFORMATION DOES NOT UPLOAD*******




import SyncroData as sync
import requests as req
import json
import TimeoutErrorhandler as out

#https://api-na.myconnectwise.net/v2022_1//apis/3.0/company/companies?fields=id,name,contact&conditions=name="Dunder Mifflin"
cwToken ="bmV4dGhvcCtCZnZWMFc1cWllNHYzZHI0OlFYbXh1Zmc0ZVVsMzIzOVI="
cwHeaders = {"Authorization" : "Basic " + cwToken, "clientID":"3040b6af-ac90-42e6-932d-9178fc76f128"  , "Content-Type":"application/json" }

codebase_data =req.get(url = "https://na.myconnectwise.net/login/companyinfo/nexthop" , headers=cwHeaders )

codebase = codebase_data.json().get("Codebase")


cwURL = "https://api-na.myconnectwise.net/"+codebase+"//apis/3.0/"
companyID = 0




def getManufacturer(idDict):
  name = sync.getManufacture(idDict.get("Data"))
  try: 
    if(name == "Cant find manufacturer"): 
      return idDict
    else:
      name = '"'+name+'"' 
      data = req.get(url=cwURL+"company/configurations?fields=manufacturer/id,manufacturer/name&conditions=manufacturer/name="+name , headers=cwHeaders)
    
      id = data.json()[0].get("manufacturer").get("id")
      if(id == None): 
        return idDict
      else: 
        x = {"ManufacturerName" : name , "ManufacturerID" : id}
        idDict.update(x)
        return idDict
  except req.Timeout: 
    out.timeOutError()
    getManufacturer(idDict)
  except: 
    return idDict

#GETS ALL THE CONFIGURATIONS FROM CONNECTWISE 
def getConfigurations(): 
  # url = "https://api-na.myconnectwise.net/v2022_2//apis/3.0/"
  try:
    numPages = req.get(url=cwURL+"/company/configurations/count" , headers=cwHeaders)
  except req.Timeout:
    out.timeOutError() 
    getConfigurations()  

  # print(numPages.json())
  numPages = numPages.json().get("count")
  pages = int(numPages/1000)

  connectWiseConfig = []
  for i in range(pages):
    iplus = i+1
    iplus = str(iplus)
    configs= req.get(url =cwURL + "/company/configurations?fields=name&pageSize=1000&page="+iplus , headers=cwHeaders)
    
    
    connectWiseConfig = configs.json()[0].get("name")
    
  return connectWiseConfig
  



#GET THE STATUS ID
def getStatusID(id,idDict): 
 
  id = str(id)
  try:
    r= req.get(url=cwURL+"/company/companies?fields=status/id&conditions=id="+id,headers=cwHeaders)
  
  
    statusId = r.json()[0].get("status").get("id")
    
    if(statusId != 1):
      statusId = 1 

    statusId = {"statusID":statusId}
    idDict.update(statusId)
  except req.Timeout:
    out.timeOutError()
    getStatusID(id,idDict)
  except: 
    print("Cant find anything")

  
  return idDict
#GET THE SITE ID
def getSiteID(id,idDict):
  x = {} 

  try:
    id=str(id)
    r=req.get(url=cwURL+"/company/companies?fields=site/id&conditions=id="+id,headers=cwHeaders)
 
    dirty = r.json()[0].get("site")
    siteID = dirty.get("id")
    x = {"SiteID":siteID}
  except req.Timeout: 
    out.timeOutError()
    getSiteID(id,idDict)
  except: 
    print("Cant find siteID")

 
  idDict.update(x)
  
  
  return idDict

#GET THE TYPE ID
def getTypeId (idDict): 
  assetID = idDict.get("AssetId")
  if(idDict.get("TypeName") == None):
    typeOfAsset = sync.getTypeOfAsset(assetID)
    assetType = typeOfAsset.get("Type")
  else: 
    typeOfAsset = sync.getTypeOfAsset(assetID)
    assetType = idDict.get("TypeName")
  
  try:
    assetType = '"'+assetType+'"'
 
    
    r = req.get(url=cwURL+"/company/configurations?fields=type/id&conditions=type/name="+assetType,headers=cwHeaders)
    
    typeID = r.json()[0].get("type").get("id")
  except req.Timeout: 
    out.timeOutError() 
    getTypeId(idDict)
  except :
    print("Cant get id for " , idDict.get("CompanyName") , " Asset Name " , idDict.get("ComputerName"))
    typeID = 0000 
  
  typeID = {"TypeID":typeID}
  idDict.update(typeID)
  x = {"TypeName" : assetType}
  idDict.update(x)
  x= {"Data" : typeOfAsset.get("Data") }
  idDict.update(x)
  
  return idDict
# getTypeId(0 ,  {"AssetId" : 6799648})
#Getting Contact ID 
#We try to get the approvers if there are no approvers then we move on to the champions if there are neither champion or approver we just grab the first
#contact that comes up maybe rewrite with recursion. 
def getContactID(id,dict):
 
  id=str(id)
  try:
    r = req.get(url=cwURL+"/company/contacts?fields=firstname,lastname,id&conditions=company/id="+id + "&childconditions=types/name='Approver'", headers=cwHeaders)
    if(r.json()!=None): 
      print("GET CONTACT ID   ",  r.json())
      dirty = r.json()[0].get("id")
      fullname = r.json()[0].get("firstName")
      fullname=fullname+" "+r.json()[0].get("lastName")

    else: 
      r = req.get(url=cwURL+"/company/contacts?fields=firstname,lastname,id&conditions=company/id="+id + "&childconditions=types/name='Champion'", headers=cwHeaders)

      if(r.json()!=None):
        dirty = r.json()[0].get("id")
        fullname = r.json()[0].get("firstName")
        fullname=fullname+" "+r.json()[0].get("lastName")

      else: 
        r = req.get(url=cwURL+"/company/contacts?fields=firstname,lastname,id&conditions=company/id="+id , headers=cwHeaders)
        dirty = r.json()[0].get("id")
        fullname = r.json()[0].get("firstName")
        fullname=fullname+" "+r.json()[0].get("lastName")

  except req.Timeout: 
    out.timeOutError()
    getContactID(id,dict)

  except: 
    return dict
  
  #Cleaning Contact ID now 
  
  print("GETTTING ID")

    # dirty = ""

  contactID = {"ContactID" : dirty , "ContactName" : fullname}
  dict.update(contactID)



  return dict
#getting Company ID 
#passing the contact type we want we can recurse instead of writting a extremely long function if the request pulls no data we recurse through the method with new data
#then it will request from connectwise with new data until we find the right data
def getKeycontact(id,dict,i):
  contactype = ["Approver" , "Champion" , ""]
  if(contactype[i]==""): 
    r = req.get(url=cwURL+"/company/contacts?fields=firstname,lastname,id&conditions=company/id="+id , headers=cwHeaders)
  else:
    r = req.get(url=cwURL+"/company/contacts?fields=firstname,lastname,id&conditions=company/id="+id + "&childconditions=types/name="+'"'+contactype[i]+"'", headers=cwHeaders)
  try:
    if(r.json()!=None): 
     
      dirty = r.json()[0].get("id")
      fullname = r.json()[0].get("firstName")
      fullname=fullname+" "+r.json()[0].get("lastName")
      
  
    else: 
      i = i +1
      getKeycontact( id , dict, i)

      if(dict.get("ContactName")!=None): 
        return dict

  except: 
      contactID = {"ContactID" : dirty , "ContactName" : fullname}
      dict.update(contactID)
      return dict 
  #Update dict 
  contactID = {"ContactID" : dirty , "ContactName" : fullname}
  dict.update(contactID)
  return dict 

def getConnectWiseClientID(companyName , assetName , assetID):
  idDict = {}
  idDict.clear()

   
  
  companyName = str(companyName)
  #Checking to see if Company Name has & in it if so then replace with %26 Trying to trouble shoot company name errors if there is a + 
  try:
    if("&" in companyName):
    
      companyNameChecked = companyName.replace("&","%26")
      companyNameChecked = '"'+companyNameChecked+'"'
      companyID = req.get(url=cwURL+"company/companies?fields=id,contact&conditions=name=" +companyNameChecked , headers=cwHeaders)
    elif("+" in companyName):
      k = companyName.replace("+" , "%2b")
      k = '"'+k+'"'
      companyID = req.get(url=cwURL+"company/companies?fields=id,contact&conditions=name="+k, headers=cwHeaders)
    elif(companyName == "Oval Village Law"): 
      k = companyName+" Corporation"
      k = '"'+k+'"'
      companyID = req.get(url=cwURL+"company/companies?fields=id,contact&conditions=name="+k, headers=cwHeaders)
    else:
      companyName = '"'+companyName+'"'
      companyID = req.get(url=cwURL+"company/companies?fields=id,contact&conditions=name=" +companyName , headers=cwHeaders)
  
  except req.Timeout: 
    out.timeOutError() 
    getConnectWiseClientID(companyName,assetName,assetID)
  
  print(companyID.url)
  

  
  idDict = {"CompanyName" : companyName}

  x = {"ComputerName" : assetName}
  idDict.update(x)
  x = {"AssetId" : assetID}
  idDict.update(x)
  
  cleanID(companyID , idDict)

#Cleaning Company Data 

def cleanID(dirty , idDict):
  id = 0  
  print('Dirty' , dirty.json())
  try:
    dirty = dirty.json()
    
    id = dirty[0].get("id")
    print(dirty[0].values())
  except:
    print("Cant find company ID")
    return 0
   
  
    
  x = {"companyID" : id}
  idDict.update(x)
  idDict = getContactID(id,idDict)
  idDict = getTypeId(idDict)
  idDict = getSiteID(id,idDict)
  
  idDict = getStatusID(id,idDict)
  idDict = getManufacturer(idDict)
  # getManufactureID(idDict)

  buildJsonFile(id , idDict)


def buildJsonFile(id , idDict):

  #The formatting class this formats the request to connectwise 
  stat = ""
  false = False
  server = sync.findServer(idDict.get("Data"))
  if(server == "Server"):
    idDict.pop("TypeName")
    x = {"TypeName" : "server"}
    idDict.update(x)
    print("SERVER")
    print(idDict)

    getTypeId( idDict)
  if(idDict.get("statusID")==1):
    stat ="Active"
  else:
    stat = "Inactive"
  ip = str(sync.getIPaddress(idDict.get("AssetId") , idDict.get("Data")))
  mac = str(sync.getMacAddress(idDict.get("AssetId"), idDict.get("Data")))
  gate = str(sync.getDefaultGateWay(idDict.get("AssetId"), idDict.get("Data")))
  
  ip6 = sync.getIPV6(idDict.get("AssetId"), idDict.get("Data"))
  ram = sync.getRAM(idDict.get("AssetId")  , idDict.get("Data"))
  os = sync.getOsName(idDict.get("AssetId"), idDict.get("Data"))
  cpu = sync.getCPU(idDict.get("AssetId"), idDict.get("Data"))
  serial = sync.getSerialNumber(idDict.get("Data"))
  model = sync.getModelNumber(idDict.get("Data"))
  user = sync.getLastLogin(idDict.get("Data"))


  typeName = idDict.get("TypeName")
  if(typeName!=None):
    typeName = typeName.strip('"\"')
  companyName = idDict.get("CompanyName")
  if(companyName!=None): 
    companyName = companyName.strip('"\"')
  manu = idDict.get("ManufacturerID")

  manuName = idDict.get("ManufacturerName")
  if(manuName!=None):
    manuName = manuName.strip('"\"')
  
  date = sync.getInstallDate(idDict.get("AssetId"), idDict.get("Data"))




  true = True


  jsonFile ={
  
  "id": 0,
  "name":idDict.get("ComputerName") ,
  "type": {
    "id": idDict.get("TypeID"),
    "name": typeName,
  },
  "status": {
    "id": idDict.get("statusID"),
    "name": stat,
  },
  "company": {
    "id": id,
    "identifier": companyName,
    "name": companyName,
  },
  "contact": {
    "id": idDict.get("ContactID"),
    "name": idDict.get("ContactName"),
  },
  "site": {
    "id": idDict.get("SiteID"),
    "name": "main",
  },
    "manufacturer": {
    "id": manu,
    "name": manuName,

    },

  "installationDate" : date,
  "billFlag": true,
  "ipAddress":ip,
  "macAddress": mac,
  "defaultGateway": gate,
  "ram": ram,
  "osType": os,
  "cpuSpeed":cpu ,
  "tagNumber": "zz",
  "serialNumber": serial,
  "modelNumber": model,
  "lastLoginName": user,

  
  }

    
  jsonFile = json.dumps(jsonFile , indent=4 ,ensure_ascii=False)

  print("Success")
  # C:/Users/RileyHall/OneDrive - Nexthop Solutions Inc/Documents/ConnectWiseSyncroLink/
  with open('newPostReqCW.json' , 'w' , encoding='utf-8' )as f:
    f.write(jsonFile)
  print("RETURING JSON FILE")
  idDict.clear()

   
# getConnectWiseClientID()


def getConfigID(compId): 
  compId = str(compId)
  a = '"Active"'
  data = req.get(url="https://api-na.myconnectwise.net/v2022_2//apis/3.0/company/configurations?fields=name,id&conditions=company/id="+compId+"%20and%20status/name="+a+"&pageSize=1000" , headers=cwHeaders)
  # print(data.json())
  print(data.url)
  return data



