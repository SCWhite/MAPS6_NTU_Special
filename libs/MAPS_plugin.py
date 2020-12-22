# -*- coding: UTF-8 -*-

import math
import time
import serial
import threading
import traceback
from datetime import datetime
from collections import deque
from statistics import median

MIC_COM_PORT = '/dev/ttyACM0'
BAUD_RATES = 115200

#pairs = datetime.now().strftime("%Y-%m-%d %H-%M").split(" ")

time_slot_string = ""
slot_count = 0
slot_energy = 0
Leq = 0
Leq_Max = 0
Leq_Min = 0
Leq_Median = 0

eq_slot_count = 0
eq_slot_energy = 0
min_leq = 0

#all_slot_energy = 0
#all_slot_count  = 0
#all_leq         = 0

#notice: we use a sliding windows to calculate Max/Min/Mid
# one goes in, one come out
dba_windows = deque(maxlen=60)


"""
# explan how Leq worked

 - first we have a lot of data in 1 second
    ex: dB(A)_t0 = 50 db ~ dB(A)_tn = 60 db

 - second, do  "pow(10,(x/5))" to get energy of t0

 - next, "sum up pow_t0 ~ pow_tn" and cacluate "pow_AVG" (depends on how long we want)

 - do a "sqrt(pow_AVG)" to get energy of this time period

 - last, caculate  "log10(energy_of__t0~tn) * 10" to get Leq of this time period (dB(A))

"""

#notice: change Leq to every minute, instead of every second.


def transfer_to_eng(x):
    Lf = math.pow(10,(x/5))
    return Lf

def get_dba_data():

    global slot_count, slot_energy, Leq, time_slot_string
    global Leq_Max, Leq_Min, Leq_Median, dba_windows
    global eq_slot_count, eq_slot_energy, min_leq
    #global all_slot_energy, all_slot_count, all_leq

    while True:
        #ser = serial.Serial(MIC_COM_PORT, BAUD_RATES)
        try:
            ser = serial.Serial(MIC_COM_PORT, BAUD_RATES)

            last_time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S").split(" ")[1]
            #add a time stamp for minute_eq
            last_time_stamp_for_minute_eq = datetime.now().strftime("%Y-%m-%d %H:%M").split(" ")[1]

            while True:
                time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S").split(" ")[1]
                #add a time stamp for minute_eq
                time_stamp_for_minute_eq = datetime.now().strftime("%Y-%m-%d %H:%M").split(" ")[1]

                if(time_stamp == last_time_stamp):
                    while ser.in_waiting:

                        data_raw = ser.readline()
                        data = data_raw.decode()

                        data_set = data.strip().split(" ")

                        #caculate dba to energy
                        slot_energy =  slot_energy + transfer_to_eng(float(data_set[1]))

                        #print(time_stamp +": "+data_set[1])

                        #time_slot_string = time_slot_string + str(data_set[1]) + ","
                        slot_count = slot_count + 1
                        #all_slot_count = all_slot_count + 1

                else:
                    #transfer back to dba / Leq in 1 seconds
                    Leq = math.log10(math.sqrt(slot_energy / slot_count)) * 10

                    #check eng
                    #all_slot_energy = all_slot_energy + slot_energy

                    #limited to 2 places
                    Leq = round(Leq,2)
                    dba_windows.append(Leq)

                    #this part is for calculate minute Leq
                    if(time_stamp_for_minute_eq == last_time_stamp_for_minute_eq):
                        eq_slot_energy = eq_slot_energy + transfer_to_eng(Leq)
                        eq_slot_count  = eq_slot_count + 1
                        #print("min_count:" + str(eq_slot_count) + "\n")
                    else:
                        min_leq = math.log10(math.sqrt(eq_slot_energy / eq_slot_count)) * 10
                        min_leq = round(min_leq,2)

                        #to verify min_leq / compare to every entry in one minite
                        #all_leq = math.log10(math.sqrt(all_slot_energy / all_slot_count)) * 10
                        #all_leq = round(all_leq,2)

                        #print("eq_slot_energy   :" + str(eq_slot_energy) + "\n")
                        #print("check_slot_energy:" + str(all_slot_energy) + "\n")

                        #print("eq_slot_count   :" + str(eq_slot_count) + "\n")
                        #print("check_slot_count:" + str(all_slot_count) + "\n")

                        #print("eq_DB   :" + str(min_leq) + "\n")
                        #print("all_DB  :" + str(all_leq) + "\n")

                        eq_slot_energy = 0
                        eq_slot_count  = 0
                        #all_slot_energy = 0
                        #all_slot_count  = 0

                        last_time_stamp_for_minute_eq = time_stamp_for_minute_eq

                    Leq_Max = max(dba_windows)
                    Leq_Min = min(dba_windows)
                    Leq_Median = round(median(dba_windows),2)

                    #print("Leq: " + str(Leq) + "\n")
                    #print("------------------")
                    #print("Leq: " + str(Leq) + "\n")
                    #print("Leq_Max: " + str(Leq_Max) + "\n")
                    #print("Leq_Min: " + str(Leq_Min) + "\n")
                    #print("Leq_Median: " + str(Leq_Median) + "\n")
                    #print("min_leq: " + str(min_leq) + "\n")
                    #print("------------------")

                    time_slot_string = ""
                    slot_energy = 0
                    slot_count  = 0
                    last_time_stamp = time_stamp

                    #eq_slot_energy = 0
                    #eq_slot_count  = 0
                    #last_time_stamp_for_minute_eq = time_stamp_for_minute_eq

        except:
            ser.close()

            #clear remain data
            dba_windows.clear()
            Leq = 0
            Leq_Max = 0
            Leq_Min = 0
            Leq_Median = 0
            min_leq = 0

            time.sleep(5)
            print('no MIC or port error!\n')
            traceback.print_exc()


#start MIC sensing
get_dba_data_t = threading.Thread(target = get_dba_data)
get_dba_data_t.setDaemon(True)
get_dba_data_t.start()

#use for testing
#while 1:
#    print("OK start")
#    get_dba_data()
