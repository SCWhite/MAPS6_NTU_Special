import os

#ID
DEVICE_ID = "MAPSV6_001"

#IP
DEVICE_IP = ""

#APP ID
APP_ID = "MAPS6"

#GPS
gps_lat = "25.1933"
gps_lon = "121.787"

#key
SecureKey = "NoKey"

#mcu version
latest_mcu_version = 980
ver_app            = "6.1.1-a"  #change to 6.x.x version for MAPS6 / 6.1.1-a for NTU project


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
GPS_LAT = 25.1933
GPS_LON = 121.7870


mac = open('/sys/class/net/eth0/address').readline().upper().strip()
DEVICE_ID = mac.replace(':','')

#interval(seconds)
show_interval   = 0.3
upload_interval = 300
save_interval   = 60
