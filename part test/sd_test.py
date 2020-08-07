import os
import time
from datetime import datetime

data_list = ["111111","22222","33333","44444","55555"]

def save_to_SD(data_list):
    #use fixed path "/mnt/SD"
    path = "/mnt/SD"

    #check is SD card is on the board
    if os.path.exists("/dev/mmcblk2p1"):
        print("SD exists")

        #check if path is mountpoint (mounted or not)
        if(not(os.path.ismount("/mnt/SD"))):
            print("Is NOT mounted!")
            try:
                os.system("mount -v -t auto /dev/mmcblk2p1 /mnt/SD")
            except:
                print("SD error / can't be mounted !!")

        else:
            print("Is mounted")
            #CSV_items  =  ['device_id', 'date', 'time', 's_t0', 's_h0', 's_d0', 's_d1', 's_d2', 's_lr', 's_lg', 's_lb', 's_lc', 's_l0', 's_gh', 's_gg']
            CSV_msg = ""

            pairs = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S").split(" ")

            for i in range(len(data_list)):
                CSV_msg = CSV_msg + str(data_list[i]) + ','

            CSV_msg= CSV_msg[:-1] #to get rid  of ',' from last data

            try:
                with open(path + "/" + pairs[0] + ".csv", "a") as f:
                    f.write(CSV_msg + "\n")
            except:
                print("other error / try to mount again")
                os.system("mount -v -t auto /dev/mmcblk2p1 /mnt/SD")

    else:
        print("NO SD card")


print("OK")

while(1):
    print("---------start----------")
    save_to_SD(data_list)
    print("---------stop----------")
    time.sleep(10)
