import sqlite3
import math
import re
conn = sqlite3.connect('F:/Users/18210/Documents/Prepar3D v4 Add-ons/FSLabs/NavData/CHN2014001.rom')
c = conn.cursor()
def getDegree(latA, lonA, latB, lonB): 
    radLatA = math.radians(latA) 
    radLonA = math.radians(lonA) 
    radLatB = math.radians(latB) 
    radLonB = math.radians(lonB) 
    dLon = radLonB - radLonA 
    y = math.sin(dLon) * math.cos(radLatB) 
    x = math.cos(radLatA) * math.sin(radLatB) - math.sin(radLatA) * math.cos(radLatB) * math.cos(dLon) 
    brng = math.degrees(math.atan2(y, x)) 
    brng = (brng + 360) % 360 
    return brng
def getlatlonbyraddis(lat,lon,deg,dis):
    r = 6371393
    radlat = math.radians(lat)
    radlon = math.radians(lon)
    deg = math.radians(deg)
    lat2 = math.asin(math.sin(radlat)*math.cos(dis/r)+math.cos(radlat)*math.sin(dis/r)*math.cos(deg))
    lon2 = radlon+math.atan2(math.sin(deg)*math.sin(dis/r)*math.cos(radlat),math.cos(dis/r)-math.sin(radlat)*math.sin(lat2))
    #lon2 = radlon + (dis * math.sin(deg* Math.PI / 180)) / (111 * Math.cos($lat * Math.PI / 180));
    resl = []
    resl.append(math.degrees(lat2))
    resl.append(math.degrees(lon2))
    return resl
def searchwaypoint(name,icao_code,sect_code,airport):
    conn = sqlite3.connect('F:/Users/18210/Documents/Prepar3D v4 Add-ons/FSLabs/NavData/CHN2014001.rom')
    c = conn.cursor()
    resw = c.execute("SELECT * FROM WAYPOINT where WAYPOINT_IDENT='"+name+"' AND SECT_CODE='"+sect_code+"' AND WAYPOINT_ICAO_CODE='"+icao_code+"' AND REGION_CODE='"+airport+"'")
    for roww in resw:
        return roww
    resw=c.execute("SELECT * FROM VHF_NAVAID where VOR_IDENT='"+name+"' AND SECT_CODE='"+sect_code+"' AND VHF_ICAO_CODE='"+icao_code+"'")
    for roww in resw:
        roww = list(roww)
        roww[13] = roww[12]
        roww[12] = roww[11]
        return roww
    resw = c.execute("SELECT * FROM WAYPOINT where WAYPOINT_IDENT='"+name+"' AND SECT_CODE='"+sect_code+"' AND WAYPOINT_ICAO_CODE='"+icao_code+"'")
    for roww in resw:
        return roww
    conn.close()
def printpath(res):
    prewaypoint = ""
    h = 0
    for row in res:
        #print(row)
        if row[18]=="IF" or row[18]=="TF":
            ifp = searchwaypoint(row[10],row[11],row[12],airport)
            try:
                print(str(ifp[13])+","+str(ifp[12])+","+str(h)+" ", end='')
            except:
                print(row)
        elif row[18]=="RF":
            prejw = searchwaypoint(prewaypoint[10],prewaypoint[11],prewaypoint[12],airport)
            cjw = searchwaypoint(row[36],row[38],row[39],airport)
            jw = searchwaypoint(row[10],row[11],row[12],airport)
            deg2 = getDegree(cjw[12],cjw[13],jw[12],jw[13])
            deg1 = getDegree(cjw[12],cjw[13],prejw[12],prejw[13])
            '''if(row[10]=="RK684"):
                print(prejw)
                print(cjw)
                print(jw)
                print(deg1)
                print(deg2)'''
            if row[16]=="L":
                angle = math.floor(deg1)
                cnt = 0
                while cnt<=360:
                    if angle==math.ceil(deg2):
                        break
                    elif (math.ceil(deg2)==360 or math.ceil(deg2)==0) and angle==0:
                        break
                    rflatlon=getlatlonbyraddis(cjw[12],cjw[13],angle,(row[22]/1000)*1852)
                    print(str(rflatlon[1])+","+str(rflatlon[0])+","+str(h)+" ", end='')
                    angle = angle-1
                    if(angle<=0):
                        angle = 360+angle
                    cnt=cnt+1
            else:
                angle = math.ceil(deg1)
                cnt = 0
                while cnt<=360:
                    if angle==math.floor(deg2):
                        break
                    elif (math.floor(deg2)==360 or math.floor(deg2)==0) and angle==0:
                        break
                    rflatlon=getlatlonbyraddis(cjw[12],cjw[13],angle,(row[22]/1000)*1852)
                    print(str(rflatlon[1])+","+str(rflatlon[0])+","+str(h)+" ", end='')
                    angle = angle+1
                    if(angle==360):
                        angle = 0
                    cnt = cnt+1
            ifp = searchwaypoint(row[10],row[11],row[12],airport)
            print(str(ifp[13])+","+str(ifp[12])+","+str(h)+" ", end='')
        prewaypoint = row
        if re.match("[\s\S]Y[\s\S]M",row[15]):
            print("")
            print("")
            print("")
            h=0
            ifp = searchwaypoint(prewaypoint[10],prewaypoint[11],prewaypoint[12],airport)
            print(str(ifp[13])+","+str(ifp[12])+","+str(h)+" ", end='')





airport="ZLYS"
#res = c.execute("SELECT * FROM AIRPORT_PROCEDURE WHERE ARPT_IDENT='"+airport+"' AND ROUTE_TYPE=5 AND PROC_IDENT='R15' ORDER BY SEQ_NR")# AND TRANSITION_IDENT='RW09'
#res = c.execute("SELECT * FROM AIRPORT_PROCEDURE WHERE ARPT_IDENT='"+airport+"' AND ROUTE_TYPE=5 AND PROC_IDENT='DOB6JA' ORDER BY SEQ_NR")
#res = c.execute("SELECT * FROM AIRPORT_PROCEDURE WHERE ARPT_IDENT='"+airport+"' AND ROUTE_TYPE='A' AND PROC_IDENT='R33' AND TRANSITION_IDENT='LXA' ORDER BY SEQ_NR")
res = c.execute("SELECT * FROM AIRPORT_PROCEDURE WHERE ARPT_IDENT='"+airport+"' AND ROUTE_TYPE='R' AND PROC_IDENT='R10';")
printpath(res)
conn.commit()
conn.close()