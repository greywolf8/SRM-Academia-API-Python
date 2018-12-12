from pyquery import PyQuery as pq
import json
import requests
import base64


TimeTable = {}

Slots = []


def getCookieFromToken(token):
    try:
        token = token.replace('\\n', '\n')
        token = base64.decodestring(str.encode(token))
        cookie = json.loads(token)
        return cookie
    except:
        return "error"






def get_timetable(index, element):
    DayName = "Day-" + str(index + 1)
    timetable_eachDay = {}

    for index, value in enumerate(pq(element).find('td:nth-child(n + 2)')):
        timetable_eachDay[Slots[index]] = pq(value).text()

    TimeTable[DayName] = timetable_eachDay




url = "https://academia.srmuniv.ac.in/liveViewHeader.do"


def getTimeTable(token, batch):
    batch = str(batch)

    if(batch == "1"):
        viewLinkName = "Common_Time_Table_Batch_1"
    elif(batch == "2"):
        viewLinkName = "Common_Time_Table_Batch_2"
    else:
        json_o = {"status":"error", "msg":"Error in batch name."}
        json_o = json.dumps(json_o)
        return json_o

    Cookies = getCookieFromToken(token)
    if (Cookies == "error"):
        json_o = {"status": "error", "msg": "Error in token"}
        json_o = json.dumps(json_o)
        return json_o
    else:

        headers = {'Origin': 'https://academia.srmuniv.ac.in',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'
                   }
        data = {"sharedBy": "srm_university",
                "appLinkName": "academia-academic-services",
                "viewLinkName": viewLinkName,
                "urlParams": {},
                "isPageLoad": "true"}

        dom = requests.post(url, data=data, headers=headers,cookies=Cookies).text

        s1 = '$("#zc-viewcontainer_' + viewLinkName + '").prepend(pageSanitizer.sanitize('
        s2 = '});</script>'

        a, b = dom.find(s1), dom.find(s2)
        dom = pq(dom[a + 56 + len(viewLinkName):b - 5])




        for value in dom('table[width="400"]').find('tr').eq(0).find('td:nth-child(n + 2)'):
            Slots.append(pq(value).text().replace("	", ""))

        dom('table[width="400"]').find('tr:nth-child(n + 5)').each(get_timetable)


        if len(TimeTable) > 3:
            json_o = {"status": "success", "data": TimeTable}
            json_o = json.dumps(json_o)
            return json_o
        else:
            json_o = {"status": "error", "msg": "Error occured"}
            json_o = json.dumps(json_o)
            return json_o






