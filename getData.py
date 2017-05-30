import json
import pprint
import requests
import datetime
from bs4 import BeautifulSoup
import xlsxwriter

def convetTime(uinxTime):
    if(int(uinxTime) > 0):
        return datetime.datetime.fromtimestamp(int(uinxTime)).strftime('%d-%m-%Y %H:%M:%S')
    else:
        return uinxTime

def fetch_data():
    url = "http://wotlabs.net/sea/clan/ina"
    soup = BeautifulSoup(requests.get(url).text,"html.parser")
    writeExcel((getNames(soup)))
    #Test data to be commented out
    #tempPlayerDetails = [{2005083140: 'm_y765'}]
    #pprint.pprint(getSats(tempPlayerDetails))

def getNames(soup):
    playerURL = "https://api.worldoftanks.asia/wot/account/list/?application_id=28429e4b12e6a40008897255aab38e00&language=en&type=exact&fields=account_id&search="
    names = [ { json.loads(requests.get(playerURL + text.contents[0]).text)["data"][0].get("account_id") :
              text.contents[0] } for text in soup.tbody.find_all('a') 
            if text.contents[0] != "Toggle tank list"]
        
    return getSats(names)

def getSats(playerDetails):
    statsURL = """https://api.worldoftanks.asia/wot/account/info/?application_id=28429e4b12e6a40008897255aab38e00&fields=created_at%2Clast_battle_time%2Cstatistics.all.battles%2Cglobal_rating%2Cstatistics.all.hits_percents%2Cstatistics.stronghold_skirmish.battles&language=en&account_id="""
    playerStats = []
    for tempDic in playerDetails: 
        tempPlayer = str(list(tempDic.keys())[0])
        temp = json.loads(requests.get(statsURL + str(tempPlayer)).text)["data"]        
        playerStat = { "PlayerId" : tempPlayer , "PlayerName" : tempDic.get(int(tempPlayer)) ,
                        "CreatedDate" : convetTime(temp[tempPlayer]["created_at"])}
        playerStat["LastBattle"] = convetTime(temp[tempPlayer]["last_battle_time"])
        playerStat["TotalBattles"] = temp[tempPlayer]["statistics"]["all"]["battles"]
        playerStat["Rating"] = temp[tempPlayer]["global_rating"]
        playerStat["HitRatio"] = temp[tempPlayer]["statistics"]["all"]["hits_percents"]
        playerStat["SH_Battles"] = temp[tempPlayer]["statistics"]["stronghold_skirmish"]["battles"]
        playerStat["Vehicles"] = getVehicles(tempPlayer)
        playerStats.append(playerStat)
    return playerStats

def getVehicles(playerID):
    stantardVeh = { "Cromwell":1105, "Cromwell_Berlin":55889, "T-34-85":2561 ,"T34_85_Rudy":59393,
                    "T34_85M":58113, "T37":16673, "Type64":64817, "59_16":4913, "O-I":5473, "HT-NO6":52321}
    vehURL = """https://api.worldoftanks.asia/wot/tanks/stats/?application_id=28429e4b12e6a40008897255aab38e00&tank_id=1105%2C55889%2C64817%2C2561%2C59393%2C58113%2C16673%2C4913%2C5473%2C52321%2C&language=en&fields=tank_id%2Call.battles%2Call.damage_dealt%2Call.hits_percents&account_id="""
    tempVS = json.loads(requests.get(vehURL + playerID).text)["data"][playerID]
    if tempVS:
        return [{item["tank_id"] : item["all"] } for item in tempVS ]
    else:
        return 'null'

def writeExcel(dataToWrite):
    tempdata1 = [{'CreatedDate': '18-04-2011 16:26:36',
              'HitRatio': 46,
              'LastBattle': '24-05-2017 17:24:58',
              'PlayerId': '2000575131',
              'PlayerName': 'Enforcer_aiyush',
              'Rating': 2198,
              'SH_Battles': 26,
              'TotalBattles': 4058,
              'Vehicles': 'null'}]
    tempdata2 = [{'CreatedDate': '10-01-2013 04:12:10',
              'HitRatio': 61,
              'LastBattle': '19-05-2017 21:42:42',
              'PlayerId': '2001444796',
              'PlayerName': 'big0012',
              'Rating': 4663,
              'SH_Battles': 1856,
              'TotalBattles': 31990,
              'Vehicles': [{52321: {'battles': 414,
                                    'damage_dealt': 260701,
                                    'hits_percents': 66}},
                           {64817: {'battles': 3788,
                                    'damage_dealt': 1531457,
                                    'hits_percents': 70}}]}]

    columnTemplate = {0:'PlayerName', 1:'CreatedDate', 2 : 'LastBattle',
                      3:'TotalBattles',4:'Rating',5:'HitRatio',6:'SH_Battles' }

    vehicleTemplate = {1105:{7:'battles' , 8:'hits_percents'},55889:{9:'battles', 10:'hits_percents'},
                       2561:{11:'battles', 12:'hits_percents'},16673:{13:'battles', 14:'hits_percents'},
                       64817:{15:'battles', 16:'hits_percents'},5473:{17:'battles', 18:'hits_percents'},
                       59393:{19:'battles', 20:'hits_percents'},58113:{21:'battles', 22:'hits_percents'},
                       52321:{23:'battles', 24:'hits_percents'},4913:{25:'battles', 26:'hits_percents'}}
    workbook = xlsxwriter.Workbook('Expenses01.xlsx')
    worksheet = workbook.add_worksheet()
    row = 0
    for item in dataToWrite:
        writeCell(row,worksheet,item,columnTemplate)        
        if(item['Vehicles'] != 'null'):
            for veh in item['Vehicles']:
                key = list(veh.keys())[0]
                writeCell(row, worksheet,veh[key],vehicleTemplate[key])
        row = row +1
    workbook.close()

def writeCell(rowNum,worksheet, rowData, columnTemplate):
    for colNum, dicKey in columnTemplate.items():
        if(rowData[dicKey]):
            worksheet.write(rowNum,colNum,rowData[dicKey])
        else:
            worksheet.write(rowNum,colNum,0)      
    
    
    
if __name__=="__main__":
    fetch_data()
    
