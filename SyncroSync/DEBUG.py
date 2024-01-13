import requests as req
import ssl
def getAssetID(): 
    id = []
    for i in range (32): 
        iplus = i+1
        iplus = str(iplus)
        data = req.get("https://nexthop.syncromsp.com.syncromsp.com/api/v1/customer_assets?api_key=Tae352eaf5afaf91df-dbbb9f96cca83f8d88317d8446688328&page="+iplus , verify=ssl.CERT_NONE )
        print(data.url)
        dirty = data.json().get("assets")
        for j in range(len(dirty)): 
            id.append(dirty[j].get("id"))
            

    print(id)
    print(len(id))
    compare(id)

def compare(id):
    archive = []
    different =[]   
    with open("C:/Users/RileyHall/OneDrive - Nexthop Solutions Inc/Documents/backup/ConnectWiseSyncroLink/assetData/allclientAssetID.txt" , "r+")as read: 
        for line in read:
            archive.append(line.strip("\n"))
    print(len(archive))
    for i in range(len(id)): 
        flag = True
        for j in range(len(archive)): 
            
            if(id[i] == int(archive[j])): 
                flag = False
                break
        if(flag): 
            print("Checked")
            different.append(id[i])
    print("DIFFERENET", different)
getAssetID()
# compare(1) 