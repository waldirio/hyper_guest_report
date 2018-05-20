import re
import requests
import json

userName="admin"
passWord="redhat"
serverAddr="wallsat6.usersys.redhat.com"
satApi="http://"+ serverAddr +"/apidoc"
allHosts="http://"+ serverAddr +"/api/v2/hosts/"
onlyHost="http://"+ serverAddr +"/api/v2/hosts/"

def printResult(aux):
    theJSON = json.loads(aux)

    if "name" in theJSON:
        print(theJSON["name"])


def processGuests(hyperHostname, idHyper):
    #print("Params: " + hyperHostname + "," + str(idHyper))
    webUrl = requests.get(onlyHost+idHyper,auth=(userName,passWord), verify=False)
    data = webUrl.text
    jsonHyper = json.loads(data)
    print(str(jsonHyper))


def listAllHypevisors():

    webUrl = requests.get(allHosts,auth=(userName,passWord), verify=False)
    # Status code of this page
    #print(webUrl.status_code)
    data = webUrl.text

    # didn't working / calling
    #printResult(data)
    theJSON = json.loads(data)

    totalNumber = theJSON["total"]

    for count in range(0,totalNumber):
        if "name" in theJSON["results"][count]:
            hostname = theJSON["results"][count]["name"]
            if re.search("virt-who",hostname):
                idHyper = theJSON["results"][count]["id"]
                subStatus = theJSON["results"][count]["subscription_status_label"]
                #print(hostname,idHyper)
                
                # didn't working / call
                #processGuests(hostname,idHyper)

                webUrlHyper = requests.get(onlyHost+str(idHyper),auth=(userName,passWord), verify=False)
                dataHyper = webUrlHyper.text
                jsonHyper = json.loads(dataHyper)
                #print(str(jsonHyper))

                countGuests = len(jsonHyper["subscription_facet_attributes"]["virtual_guests"])
                # Just showing the # of guests on each hypervisor
                #print("Guest # on hypervisor " + hostname + ": " + str(countGuests))

                if countGuests > 0:
                    # If found the guest, we will process just to generate the report
                    #print("Let's process !!!")
                    for b in range(0,countGuests):
                        guestName=jsonHyper["subscription_facet_attributes"]["virtual_guests"][b]["name"]
                        print(subStatus + "," + hostname + "," + guestName)
    



def testConn():
    webUrl = requests.get(satApi)
    #print(webUrl.status_code)
    if webUrl.status_code != 200:
        print("Ërror accessing Satellite Server. Exiting ...")
        exit()
    

def main():
    print("Starting the job")
    testConn()
    listAllHypevisors()


if __name__ == "__main__":
    main()