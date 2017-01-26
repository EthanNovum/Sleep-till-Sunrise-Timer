import urllib
import json
from datetime import date
from datetime import datetime
import time

key = 'N84X8S87EZ51'

locationurl = 'http://maps.googleapis.com/maps/api/geocode/json?'
sunriseurl = 'http://api.sunrise-sunset.org/json?'
timezoneurl = 'http://api.timezonedb.com/v2/get-time-zone?'
timezoneconverturl = 'http://api.timezonedb.com/v2/convert-time-zone?'

while True:
    # User input
    address = raw_input('Enter location: ')
    if len(address) < 1 : break

    print '''(Sleep duration in "hhmm" format, e.g. 0630 for 6h30min)'''
    sleepduration = raw_input('Enter sleep duration: ')
    if len(sleepduration) != 4:
        print 'Invalid sleep duration!'
        break

    sleephour = sleepduration[:2]
    sleepmin = sleepduration[2:]

    # MODULE 1: LOCATION
    url1 = locationurl + urllib.urlencode({'sensor':'false', 'address': address})
    # print 'Retrieving', url1
    uh = urllib.urlopen(url1)
    data = uh.read()
    # print 'Retrieved',len(data),'characters'

    try: js = json.loads(str(data))
    except: js = None
    if 'status' not in js or js['status'] != 'OK':
        print '==== Failure To Retrieve Location===='
        print data
        continue

    lat = js['results'][0]['geometry']['location']['lat']
    lng = js['results'][0]['geometry']['location']['lng']

    # MODULE 2: SUNRISE

    url2 = sunriseurl + urllib.urlencode({'lat':lat, 'lng':lng, 'formatted':'0'})
    # print 'Retrieving', url2
    uh2 = urllib.urlopen(url2)
    data2 = uh2.read()
    # print 'Retrived', len(data2), 'characters'

    try: js2 = json.loads(str(data2))
    except: js2 = None
    if 'status' not in js2 or js2['status'] != 'OK':
        print '==== Failure To Retrieve Sunrise===='
        print data2
        continue

    sunrise = js2['results']['sunrise']
    # 2017-01-25T22:45:01+00:00 unicode

    #MODULE 3 GLOBAL TIME ZONE
    url3 = timezoneurl + urllib.urlencode({'key':key, 'format':'json', 'by':'position', 'lat':lat, 'lng':lng})
    # print 'Retrieving', url3
    uh3 = urllib.urlopen(url3)
    data3 = uh3.read()
    # print 'Retrived', len(data3), 'characters'
    try: js3 = json.loads(str(data3))
    except: js3 = None
    if 'status' not in js3 or js3['status'] != 'OK':
        print '==== Failure To Retrieve TimeZone===='
        print data3
        continue
    timezone = js3['zoneName']
    # Asia/Shanghai str

    url4 = timezoneconverturl + urllib.urlencode({'key':key, 'format':'json', 'from': 'Africa/Accra' , 'to': timezone})
    # print 'Retrieving', url4
    uh4 = urllib.urlopen(url4)
    data4 = uh4.read()
    # print 'Retrievd', len(data4), 'characters'

    try: js4 = json.loads(str(data4))
    except: js4 = None
    if 'status' not in js4 or js4['status'] != 'OK':
        print '==== Failure To Convert TimeZone===='
        print data4
        continue

    offset = js4['offset'] / 3600
    hh = int(str(sunrise)[11:13]) + offset
    if hh >= 24: hh -= 24
    hhstr = str(hh)
    if len(hhstr) < 2: hhstr = '0' + hhstr
    localsunrise = hhstr + str(sunrise)[13:19]

    # Optional MODULE: LOCAL TIME ZONE
    '''
    tz = - time.timezone / 3600
    ini = int(sunrise[11:13]) + tz
    if ini >= 24: ini -= 24
    sunrise = str(ini) + sunrise[13:19]
    '''

    # MODULE 5 Sleep time

    print 'lat:', lat, 'lng', lng
    print 'Sunrise in local time:', localsunrise

    sunrisehour = localsunrise[:2]
    sunrisemin = localsunrise[3:5]
    durationhour = int(sunrisehour) - int(sleephour)
    durationmin = int(sunrisemin) - int(sleepmin)
    if durationmin < 0:
        durationmin += 60
        durationhour -= 1
    if durationhour <0:
        durationhour += 24
    durationhourstr = str(durationhour)
    if len(durationhourstr) < 2: durationhourstr = '0' + durationhourstr
    durationminstr = str(durationmin)
    if len(durationminstr) < 2: durationminstr = '0' + durationminstr
    sleeptime = durationhourstr + ':' + durationminstr + ':' + localsunrise[len(localsunrise) - 2:]
    print 'Suggested sleep time:', sleeptime