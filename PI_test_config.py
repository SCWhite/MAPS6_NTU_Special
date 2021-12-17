import os

#for nbiot
def formatStrToInt(target):
    kit = ""
    for i in range(len(target)):
        temp=ord(target[i])
        temp=hex(temp)[2:]
        kit=kit+str(temp)+" "
        #print(temp,)
    return kit

#ID
DEVICE_ID = "MAPSV6_001"

#IP
DEVICE_IP = ""

#APP ID
APP_ID = "MAPS6"

#GPS
gps_lat = ""
gps_lon = ""

#key
SecureKey = "NoKey"

#mcu version
latest_mcu_version = 1000
ver_app            = "6.4.3-a"  # 6.x.x-a for NTU project(add dB sensor) / v6.4.3 increase upload frequency


#path
FS_SD = "./data"

# #If there is no "data" folder in path
# if not os.path.isdir(FS_SD):
#     os.mkdir(FS_SD)


#Enable 1:on / 0:off
POLL_TEMP  = 1
POLL_CO2   = 1
POLL_TVOC  = 1
POLL_LIGHT = 1
POLL_PMS   = 1
POLL_RTC   = 1

#url
Restful_URL = "https://data.lass-net.org/Upload/MAPS-secure.php?"
TimeURL = "https://pm25.lass-net.org/util/timestamp.php"

#setting
#GPS_LAT = ""
#GPS_LON = ""


mac = open('/sys/class/net/eth0/address').readline().upper().strip()
DEVICE_ID = mac.replace(':','')

#CONN/RL/PLEN/MQIsdp/LVL/FL/KA/CIDLEN/ABCDEF/ULEN/maps/PWLEN/iisnrl
#see more from "mqtt.xlsx"
connect_pack_pre = "10 28 00 06 4D 51 49 73 64 70 03 C2 00 3C 00 0C "
Client_ID = formatStrToInt(DEVICE_ID)
connect_pack_post = "00 04 6D 61 70 73 00 06 69 69 73 6E 72 6C "
connect_pack = connect_pack_pre + Client_ID + connect_pack_post

prifix = "MAPS/MAPS6/"+DEVICE_ID


#interval(in seconds)
show_interval       = 0.3
upload_interval     = 60
save_interval       = 1
nbiot_send_interval = 600
