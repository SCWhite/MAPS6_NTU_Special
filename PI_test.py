import os
import serial
import time
import libs.MAPS_mcu as mcu
import libs.MAPS_pi as pi
import libs.display as oled
from datetime import datetime

import requests
import threading

#import current file's config, by getting the script name with '.py' replace by '_confg'
#ex: import "maps_V6_general.py" > "maps_V6_general_config" as Conf
PATH_OF_CONFIG = str(os.path.basename(__file__)[:-3] + "_config")
Conf = __import__(PATH_OF_CONFIG)

#temperary value
do_condition = 1
loop = 0

#if there is no GPS module
#or don't use GPS / set to '0'
use_GPS = 0


#preset
TEMP        = 0
HUM         = 0
CO2         = 0
TVOC        = 0
Illuminance = 0
PM1_AE      = 0
PM25_AE     = 0
PM10_AE     = 0
connection_flag = ""


def show_task():
    while True:
        oled.display(Conf.DEVICE_ID,TEMP,HUM,PM25_AE,CO2,connection_flag,Conf.ver_app)
        time.sleep(Conf.show_interval) #0.3 seconds / use about 18% cpu on PI3

def upload_task():
    while True:
        time.sleep(Conf.upload_interval) #300 seconds
        pairs = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S").split(" ")
        #remove GPS if we're not using it
        if(use_GPS == 1):
            msg = "|gps_lat=" + str(Conf.gps_lat) + "|s_t0=" + str(TEMP) + "|app=" + str(Conf.APP_ID) + "|date=" + pairs[0] + "|s_d2=" + str(PM1_AE) + "|s_d0=" + str(PM25_AE) + "|s_d1=" + str(PM10_AE) + "|s_h0=" + str(HUM) + "|device_id=" + Conf.DEVICE_ID +"|s_g8=" + str(CO2) + "|s_gg=" + str(TVOC) + "|gps_lon="+ str(Conf.gps_lon) +"|ver_app=" + str(Conf.ver_app) + "|time=" + pairs[1] 
        else:
            msg = "|s_t0=" + str(TEMP) + "|app=" + str(Conf.APP_ID) + "|date=" + pairs[0] + "|s_d2=" + str(PM1_AE) + "|s_d0=" + str(PM25_AE) + "|s_d1=" + str(PM10_AE) + "|s_h0=" + str(HUM) + "|device_id=" + Conf.DEVICE_ID +"|s_g8=" + str(CO2) + "|s_gg=" + str(TVOC) + "|ver_app=" + str(Conf.ver_app) + "|time=" + pairs[1]
        print("message ready")
        restful_str = Conf.Restful_URL + "topic=" + Conf.APP_ID + "&device_id=" + Conf.DEVICE_ID + "&key=" + Conf.SecureKey + "&msg=" + msg
        try:
            r = requests.get(restful_str)
            print("send result")
            print(r)
            print("message sent!")
        except:
            print("internet err!!")
        #save after upload / makesure data will be synchronize
        format_data_list = [Conf.DEVICE_ID,pairs[0],pairs[1],TEMP,HUM,PM25_AE,PM1_AE,PM10_AE,Illuminance,CO2,TVOC]
        try:
            pi.save_data(path,format_data_list) #save to host
            pi.save_to_SD(format_data_list)     #save to SD card
            print("send message saved!")
        except:
            print("Fail to save sent message!")


def save_task():
    while True:
        time.sleep(Conf.save_interval) #60 seconds
        #format to ['device_id', 'date', 'time', 'Tmp',  'RH',   'PM2.5','PM10', 'PM1.0','Lux',  'CO2',  'TVOC']
        pairs = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S").split(" ")
        format_data_list = [Conf.DEVICE_ID,pairs[0],pairs[1],TEMP,HUM,PM25_AE,PM1_AE,PM10_AE,Illuminance,CO2,TVOC]
        try:
            pi.save_data(path,format_data_list) #save to host
            pi.save_to_SD(format_data_list)     #save to SD card
            print("message saved!")
        except:
            print("Fail to save message!")


def connection_task():
    while True:
        time.sleep(10)
        check_connection()


def check_connection():
    global connection_flag
    if(os.system('ping www.google.com -q -c 1  > /dev/null')):
        connection_flag = "X"
        #print("no internet")
        #return 0

    else:
        connection_flag = "@"
        #print("connect OK")
        #return 1

def get_rtc_server_time():
    try:
        command = "wget -O /tmp/time1 " + Conf.TimeURL + " >/dev/null 2>&1"
        os.system(command)
        fh = open("/tmp/time1","r")
        server_time = fh.read()
        server_time = datetime.strptime(server_time, "%Y-%m-%d %H:%M:%S")
        print("got sever time:" + str(server_time))
        return 1 , server_time
    except:
        host_time = datetime.utcnow()
        print("use host time:" + str(host_time))
        return 0 , host_time  #no internet, use system time


#start oled displaying
display_t = threading.Thread(target = show_task)
display_t.setDaemon(True)
#display_t.start()

#start upload routine
upload_t = threading.Thread(target = upload_task)
upload_t.setDaemon(True)
#upload_t.start()

#start save routine
save_t = threading.Thread(target = save_task)
save_t.setDaemon(True)
#save_t.start()

#start connection routine
connection_t = threading.Thread(target = connection_task)
connection_t.setDaemon(True)
#connection_t.start()

try:
    print("START")
    print("========================")

    #add welcome image?
    #TODO

    print("open port & init mcu")
    #mcu.ser=serial.Serial("COM57",115200,timeout=1)
    mcu.ser=serial.Serial("/dev/ttyS0",115200,timeout=1) #for PI (not ttyAMA0)(use /dev/ttyS0)
    time.sleep(5)
    print("mcu ok\n")
    print("------------------------")

    print("CHECK")
    print("========================")
    print("CHECK INTERNET")
    # if(check_connection()):

    #     print("-----with internet------")
    #     print("CHECK TIME")
    #     current_mcu_time = mcu.GET_RTC_DATE_TIME()
    #     print("MCU RTC time:")
    #     print(current_mcu_time)

    #     time_status, server_time =  get_rtc_server_time()
    #     if(time_status):
    #         host_time = datetime.utcnow()
    #         delta_time = host_time - server_time
    #         print("delta_time:" + str(delta_time))

    #         if abs(delta_time.seconds) > 30:
    #             print("!!!SET TO severtime!!!")
    #             print("server time:")
    #             print(server_time)
    #             print("host time")
    #             print(host_time)
    #             #to do
    #             #set system time
    #             #set mcu RTC time
    #         else:
    #             print("!!!use host time is ok!!!")
    #             print("server time:")
    #             print(server_time)
    #             print("host time")
    #             print(host_time)
    #             #to do
    #             #set mcu RTC time


    # else:
    #     print("-----no internet------")
    #     print("-----pass time check------")
    #     current_mcu_time = mcu.GET_RTC_DATE_TIME()
    #     print("MCU RTC time:")
    #     print(current_mcu_time)
    #     #set system time to mcu RTC clock time

    print("------------------------")
    print("CHECK PI VERSION")
    #TODO

    print("CHECK MCU VERSION")

    current_mcu_version = mcu.GET_INFO_VERSION()
    print(current_mcu_version)
    if (current_mcu_version < Conf.latest_mcu_version):
        #need update
        print("please update mcu")
    else:
        print("newest version")

    print("------------------------")
    print("SET SENSOR")

    mcu.SET_POLLING_SENSOR(Conf.POLL_TEMP,Conf.POLL_CO2,Conf.POLL_TVOC,Conf.POLL_LIGHT,Conf.POLL_PMS,Conf.POLL_RTC)

    print("CHECK SENSOR")
    print(mcu.GET_INFO_SENSOR_POR())


    print("------------------------")
    print("CHECK STORAGE")
    #In MPV version, only use "./data"
    path = pi.GET_STORAGE_PATH()
    print(path)

    print("CHECK read/write")
    #TODO

    print("------------------------")
    print("set upload")
    #if need to do
    print("------------------------")
    print("CHECK NB-IOT")

    print("CHECK GPS")
    #check if there is GPS module
    #and if we want to use GPS, set "use_GPS" to 1

    print("------------------------")

    #start routine job
    display_t.start()
    upload_t.start()
    save_t.start()
    connection_t.start()


    #close the fan
    #mcu.SET_PIN_FAN_ALL(0)

    while (do_condition):
        print("START GET DATA (loop:" + str(loop) + ")")
        print("========================")

        print("GET ALL DATA")
        data_list = mcu.GET_SENSOR_ALL()

        TEMP        = data_list[0]
        HUM         = data_list[1]
        CO2         = data_list[2]
        TVOC        = data_list[4]
        Illuminance = data_list[10]
        PM1_AE      = data_list[16]
        PM25_AE     = data_list[17]
        PM10_AE     = data_list[18]

        print("TEMP:" +str(TEMP))
        print("HUM:" +str(HUM))
        print("CO2:" +str(CO2))
        print("TVOC:" +str(TVOC))
        print("Illuminance:" +str(Illuminance))
        print("PM1_AE:" +str(PM1_AE))
        print("PM25_AE:" +str(PM25_AE))
        print("PM10_AE:" +str(PM10_AE))
        print("------------------------")

        #print("storage data") #change to another thread
        #format to ['device_id', 'date', 'time', 'Tmp',  'RH',   'PM2.5','PM10', 'PM1.0','Lux',  'CO2',  'TVOC']
        #pairs = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S").split(" ")
        #format_data_list = [Conf.DEVICE_ID,pairs[0],pairs[1],TEMP,HUM,PM25_AE,PM1_AE,PM10_AE,Illuminance,CO2,TVOC]
        #pi.save_data(path,format_data_list)

        #print("------------------------")
        #print("upload data") #change to another thread
        #url = Conf.Restful_URL +
        #msg = "|gps_lat=25.1933|s_t0=" + str(TEMP) + "|app=MAPS6|date=" + pairs[0] + "|s_d2=" + str(PM1_AE) + "|s_d0=" + str(PM25_AE) + "|s_d1=" + str(PM10_AE) + "|s_h0=" + str(HUM) + "|device_id=" + Conf.DEVICE_ID +"|s_g8=" + str(CO2) + "|gps_lon=121.787|ver_app=0.0.1|time=" + pairs[1]
        #print(msg)
        #restful_str = Conf.Restful_URL + "topic=" + Conf.APP_ID + "&device_id=" + Conf.DEVICE_ID + "&key=" + Conf.SecureKey + "&msg=" + msg
        #r = requests.get(restful_str)
        #print("------------------------")

        loop = loop + 1
        time.sleep(5)
        print("========================")

except KeyboardInterrupt:
    mcu.ser.close()
    print("ERROR!!")
    pass


##mcu.SET_PIN_FAN_ALL(0)
##time.sleep(3)
##
##mcu.SET_PIN_FAN_ALL(1)
##time.sleep(3)
##
##mcu.SET_PIN_FAN_ALL(0)
##time.sleep(3)

mcu.ser.close()

print("exit OK")
