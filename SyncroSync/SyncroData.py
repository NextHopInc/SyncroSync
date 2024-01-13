#Interacts with Syncro grabs no uploading only downloading 

from io import BytesIO
import requests as req
import ssl
import json
import TimeoutErrorhandler as out


#gets all the Assets from Syncro, by iterating through the pages about 25 results per page. 
# https://nexthop.syncromsp.com.syncromsp.com/api/v1/customer_assets?api_key=Tae352eaf5afaf91df-dbbb9f96cca83f8d88317d8446688328

def getAssets(): 
   
    jcount = 0
    icount = 0
    assetList = []
    
    pageNum = req.get(url="https://nexthop.syncromsp.com/api/v1/customer_assets?api_key=Tae352eaf5afaf91df-dbbb9f96cca83f8d88317d8446688328" , verify=ssl.CERT_NONE)
    pages = pageNum.json().get("meta").get("total_pages")
   
    assetDict = {}
    for i in range(pages+1):#Changed for now Must change back to pages later I think it needs to be pages+1 to account for the last page 
        iplus = i+1
        iplus = str(iplus)
        
        data = req.get(url="https://nexthop.syncromsp.com/api/v1/customer_assets?api_key=Tae352eaf5afaf91df-dbbb9f96cca83f8d88317d8446688328&page="+iplus, verify=ssl.CERT_NONE) 
        print(data.url)
        dirtyData = data.json().get("assets")
       
     
        
        
        for j in range(len(dirtyData)):
            roughdata = dirtyData[j]
            jcount+=1

            asset = roughdata.get("name")

            companyName = roughdata.get("customer").get("business_name")
            assetID = roughdata.get("id")
           
            
            assetList.append(asset)
            x = {asset : { "CompanyName" : companyName , "AssetID" : assetID}}
            assetDict.update(x)
         
            
            

        icount+=1 

       

    return assetDict

# def getAssests():
#     finalVar = 0

#     ConnectWiseAPI = "http://cloud.na.myconnectwise.net/v4_6_development/apis/3.0"
#     Syncro_URL = "https://nexthop.syncromsp.com.syncromsp.com/api/v1"
#     Syncro_Api_Key="Tae352eaf5afaf91df-dbbb9f96cca83f8d88317d8446688328"
    
    
#     status = req.get( "https://nexthop.syncromsp.com.syncromsp.com/api/v1/customer_assets?api_key=Tae352eaf5afaf91df-dbbb9f96cca83f8d88317d8446688328&?" ,  verify=ssl.CERT_NONE)
#     print(status.status_code)
#     return cleanData(status.json())
    


    
    # print(dirty)
def getCompanyName(): 
    try:
        data = req.get("https://nexthop.syncromsp.com/api/v1/customer_assets/6799648?api_key=Tae352eaf5afaf91df-dbbb9f96cca83f8d88317d8446688328&?" , verify=ssl.CERT_NONE)
    except req.Timeout: 
        out.timeOutError() 
        getCompanyName()    
    dirty = data.json().get("asset")
    companyName = dirty.get("customer").get("business_name")
    
    return companyName
# getCompanyName()  


#Returns TYPE OF ASSET LAPTOP ETC
def getTypeOfAsset(assetID):
    
    assetID = str(assetID)
    try:
        data = req.get("https://nexthop.syncromsp.com/api/v1/customer_assets/"+assetID+"?api_key=Tae352eaf5afaf91df-dbbb9f96cca83f8d88317d8446688328&?" , verify=ssl.CERT_NONE)
        print(data.url)
        dirty = data.json().get("asset")
    
    
        typeOfAsset = dirty.get("properties").get("kabuto_information").get("general").get("form_factor")
    except req.Timeout: 
        out.timeOutError() 
        getTypeOfAsset() 
    except:

        try:
            typeOfAsset = dirty.get("properties").get("configuration").get("configuration_type_name")
        except: 
            print("Cant find type of asset")
            typeOfAsset = ""
    
        
   
    typeOfAsset = {"Type" : typeOfAsset , "Data" : data.json()}
    return typeOfAsset

#GETS MANUFACTURER LENOVO ETC
def getManufacture(data):
    try:
        manu = data.get("asset").get("properties").get("kabuto_information").get("general").get("manufacturer")
        if(manu==""): 
            return "Cant find manufacturer"
        else:
             
            return manu
    except: 
        return "Cant find manufacturer"

# #GETS THE NAME OF THE ASSET 
# def getAssetName(): 
#     data = req.get("https://nexthop.syncromsp.com.syncromsp.com/api/v1/customer_assets/6799648?api_key=Tae352eaf5afaf91df-dbbb9f96cca83f8d88317d8446688328&?" , verify=ssl.CERT_NONE)
#     dirty = data.json().get("asset")
#     compName = dirty.get("name")
#     print(compName)
#     return compName

#GETS THE IPV4 OF THE ASSET
def getIPaddress(assetID , data): 
    assetID = str(assetID)
    ip = ""
    # data = req.get(url="https://nexthop.syncromsp.com.syncromsp.com/api/v1/customer_assets/"+assetID+"?api_key=Tae352eaf5afaf91df-dbbb9f96cca83f8d88317d8446688328&?" , verify=ssl.CERT_NONE)
    # print(data.json())
    try:
        for i in range(len(data.get("asset").get("properties").get("kabuto_information").get("network_adapters"))):
            ip = data.get("asset").get("properties").get("kabuto_information").get("network_adapters")[i].get("ipv4")
            if(ip!=""):
                break
        return ip 
    except :
        return "Cant Find IP address"
    
    
    #Getting the default gateway for all data getting pulled from network_adapters must be put in a loop because it can either return ethernet,Wifi or other network cards. Function will wait until 
    #finds the first gateway != "" then will break the loop and return it, else it will return "Cant find default gateway" This occurs FOR ALL DATA COMING FROM NETWORK_ADAPTERS 
    #(GATEWAY, IPV4 ,IPV6)

def getDefaultGateWay(assetID , data):
    assetID = str(assetID)
    gateway = ""
    # data = req.get(url="https://nexthop.syncromsp.com.syncromsp.com/api/v1/customer_assets/"+assetID+"?api_key=Tae352eaf5afaf91df-dbbb9f96cca83f8d88317d8446688328&?" , verify=ssl.CERT_NONE)
    # print("URL FOR IP" , data.url)
    try:
        for i in range(len(data.get("asset").get("properties").get("kabuto_information").get("network_adapters"))):
            gateway = data.get("asset").get("properties").get("kabuto_information").get("network_adapters")[i].get("gateway")
            if(gateway!=""):
                break

        if(gateway == ""): 
            gateway = "Cant Find Default Gateway"
    
        return gateway
    except : 
        return "Cant get gateway"

def getMacAddress(assetID , data):

    assetID = str(assetID)
    # data = req.get(url ="https://nexthop.syncromsp.com.syncromsp.com/api/v1/customer_assets/"+assetID+"?api_key=Tae352eaf5afaf91df-dbbb9f96cca83f8d88317d8446688328&?" , verify=ssl.CERT_NONE)
    try:
        mac = data.get("asset").get("properties").get("configuration").get("mac_address")
    
        return mac
    except : 
        return "Cant get Mac"

def getRAM(assetID , data):
    assetID = str(assetID)
    # data = req.get(url ="https://nexthop.syncromsp.com.syncromsp.com/api/v1/customer_assets/"+assetID+"?api_key=Tae352eaf5afaf91df-dbbb9f96cca83f8d88317d8446688328&?" , verify=ssl.CERT_NONE)
    try:
        ram = data.get("asset").get("properties").get("kabuto_information").get("ram_gb")
        return ram 
    except : 
        return "Cant get RAM"
def getIPV6(assetID, data):
    
    assetID = str(assetID)
    # data = req.get(url ="https://nexthop.syncromsp.com.syncromsp.com/api/v1/customer_assets/"+assetID+"?api_key=Tae352eaf5afaf91df-dbbb9f96cca83f8d88317d8446688328&?" , verify=ssl.CERT_NONE)
    # print(data.url)
    try:
        for i in range(len(data.get("asset").get("properties").get("kabuto_information").get("network_adapters"))):
            ipv6 = data.get("asset").get("properties").get("kabuto_information").get("network_adapters")[i].get("ipv6")
            if(ipv6!=""):
                break
        if(ipv6==""):
            return "Cant find ipv6"
        else: 
            
            return ipv6
    except :
        return "Cant Get ipv6"
def getOsName(assetID , data):
    try:
        assetID = str(assetID)
        # data = req.get(url ="https://nexthop.syncromsp.com.syncromsp.com/api/v1/customer_assets/"+assetID+"?api_key=Tae352eaf5afaf91df-dbbb9f96cca83f8d88317d8446688328&?" , verify=ssl.CERT_NONE)
        osname = data.get("asset").get("properties").get("kabuto_information").get("os").get("name")
        if(osname==""):
            return "cant find os"
        else:
            return osname
    except : 
        return "Cant Get os"
def getCPU(assetID , data):
    assetID = str(assetID)
    # data = req.get(url ="https://nexthop.syncromsp.com.syncromsp.com/api/v1/customer_assets/"+assetID+"?api_key=Tae352eaf5afaf91df-dbbb9f96cca83f8d88317d8446688328&?" , verify=ssl.CERT_NONE)
    try: 
        cpu = data.get("asset").get("properties").get("kabuto_information").get("cpu")[0].get("name")
    
        if(cpu==""):
            return "Cant find cpu"
        else: 
            return cpu
    except : 
        return "Cant Find CPU information"

def getInstallDate(assetID , data):
    assetID  = str(assetID)
    # data = req.get(url ="https://nexthop.syncromsp.com.syncromsp.com/api/v1/customer_assets/"+assetID+"?api_key=Tae352eaf5afaf91df-dbbb9f96cca83f8d88317d8446688328&?" , verify=ssl.CERT_NONE)
    try:
       
        date = data.get("asset").get("properties").get("kabuto_information").get("install_dates").get("system_volume")
        lastchar = date[-1]
        year = date[0:4]
        year = int(year)
        if(date == "" or lastchar != "Z" or year<1753): 
            return "1753-07-12T12:44:52Z"
        else: 
            return date
    except:
        return "1753-07-12T12:44:52Z"



def getModelNumber(data): 
    try: 
        model = data.get("asset").get("properties").get("model")
        if(model == ""): 
            return "Cant find model"
        else: 
            return model
    except: 
        return"Cant find model"

def getSerialNumber(data): 
    try: 
        serial = data.get("asset").get("properties").get("kabuto_information").get("general").get("serial_number")
        if(serial == ""): 
            return "Cant find serial number"
        else: 
            return serial 
    except: 
        return "Cant find serial"

def getLastLogin(data): 
    try: 
        login = data.get("asset").get("properties").get("kabuto_information").get("last_user")
        if(login == ""): 
            return "Cant find login"
        else: 
            return login
    except: 
        return "Cant find login"

def findServer(data): 
    try: 
        server = data.get("asset").get("properties").get("form_factor")
        if(server == ""): 
            return "Cant find"
        else: 
            if("Server" in server or "server" in server): 
                return "Server"
    except: 
        return "cant find server"


