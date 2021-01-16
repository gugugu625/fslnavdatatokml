import sqlite3
import math
import re
conn = sqlite3.connect('F:/Users/18210/Documents/Prepar3D v4 Add-ons/FSLabs/NavData/CHN2014001.rom')
c = conn.cursor()
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

airport="ZURK"
#res = c.execute("SELECT * FROM AIRPORT_PROCEDURE WHERE ARPT_IDENT='"+airport+"' AND ROUTE_TYPE=4 AND PROC_IDENT='SQH1' AND TRANSITION_IDENT='RW27' ORDER BY SEQ_NR")#
#res = c.execute("SELECT * FROM AIRPORT_PROCEDURE WHERE ARPT_IDENT='"+airport+"' AND ROUTE_TYPE=5 AND PROC_IDENT='DOB6JA' ORDER BY SEQ_NR")
res = c.execute("SELECT * FROM AIRPORT_PROCEDURE WHERE ARPT_IDENT='"+airport+"' AND ROUTE_TYPE='A' AND PROC_IDENT='R09' AND TRANSITION_IDENT='SQH' ORDER BY SEQ_NR")
#res = c.execute("SELECT * FROM AIRPORT_PROCEDURE WHERE ARPT_IDENT='"+airport+"' AND ROUTE_TYPE='R' AND PROC_IDENT='R27';")
for row in res:
    wp = searchwaypoint(row[10],row[11],row[12],airport)
    print("<Placemark>")
    print("<name>"+wp[7]+"</name>")
    print("<styleUrl>#std</styleUrl>")
    print("<Point>")
    print("<extrude>1</extrude>")
    print("<altitudeMode>clampToGround</altitudeMode>")
    print("<coordinates>"+str(wp[13])+","+str(wp[12])+",0</coordinates>")
    print("</Point>")
    print("</Placemark>")
    
conn.commit()
conn.close()