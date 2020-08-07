import os
import PI_test_config as Conf
from datetime import datetime

#This function is dasable for MVP version

def GET_STORAGE_PATH():

    # try:
    #     if len(os.listdir("/media/pi")):
    #         path = "/media/pi/" + os.listdir("/media/pi")[0]

    #         return path

    # except:
    #     path = Conf.FS_SD

    #     return path

    #only use
    path = Conf.FS_SD
    return path

def save_data(path,data_list):

    #CSV_items  =  ['device_id', 'date', 'time', 's_t0', 's_h0', 's_d0', 's_d1', 's_d2', 's_lr', 's_lg', 's_lb', 's_lc', 's_l0', 's_gh', 's_gg']
    CSV_msg = ""

    pairs = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S").split(" ")
    #values["date"] = pairs[0]
    #values["time"] = pairs[1]

    for i in range(len(data_list)):
        CSV_msg = CSV_msg + str(data_list[i]) + ','

    CSV_msg= CSV_msg[:-1] #to get rid  of ',' from last data

    # #no you can't do this / please fix, consider USB drive and native SD slot
    # if not os.path.isdir(path):
    #     os.mkdir(path)

    with open(path + "/" + pairs[0] + ".csv", "a") as f:
       f.write(CSV_msg + "\n")


def save_to_SD(data_list):
    #use fixed path "/mnt/SD"
    path = "/mnt/SD"

    #check is SD card is on the board
    if os.path.exists("/dev/mmcblk2p1"):
        #print("SD exists")

        #check if path is mountpoint (mounted or not)
        if(not(os.path.ismount("/mnt/SD"))):
            #print("Is NOT mounted!")
            try:
                os.system("mount -v -t auto /dev/mmcblk2p1 /mnt/SD")
            except:
                print("SD error / can't be mounted !!")

        else:
            #print("Is mounted")
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

#there is device problum / sda1 sdb1 sdc1... don't use for now
#def save_to_USB(data_list):
#    #use fixed path "/mnt/USB"
#    path = "/mnt/USB"

#    #check is SD card is on the board
#    if os.path.exists("/dev/sda1"):
#        #print("SD exists")

#        #check if path is mountpoint (mounted or not)
#        if(not(os.path.ismount("/mnt/USB"))):
#            #print("Is NOT mounted!")
#            try:
#                os.system("mount -v -t auto /dev/sda1 /mnt/USB")
#            except:
#                print("SD error / can't be mounted !!")

#        else:
#            print("Is mounted")
#            #CSV_items  =  ['device_id', 'date', 'time', 's_t0', 's_h0', 's_d0', 's_d1', 's_d2', 's_lr', 's_lg', 's_lb', 's_lc', 's_l0', 's_gh', 's_gg']
#            CSV_msg = ""

#            pairs = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S").split(" ")

#            for i in range(len(data_list)):
#                CSV_msg = CSV_msg + str(data_list[i]) + ','

#            CSV_msg= CSV_msg[:-1] #to get rid  of ',' from last data

#            try:
#                with open(path + "/" + pairs[0] + ".csv", "a") as f:
#                    f.write(CSV_msg + "\n")
#            except:
#                print("other error / try to mount again")
#                os.system("mount -v -t auto /dev/sda1 /mnt/USB")

#    else:
#        print("NO USB drive")


# def storage():

#     #This function is dasable for MVP version
#     #doesn't support USB drive hot-plugging

#     # if len(os.listdir("/media/pi")):
#     #     path = "/media/pi/" + os.listdir("/media/pi")[0]

#     # else:
#     #     path = Conf.FS_SD

#     #only use
#     path = Conf.FS_SD

#     #CSV_items =  ['device_id', 'date', 'time', 'Tmp',  'RH',   'PM2.5','PM10', 'PM1.0','RGB_R','RGB_G','RGB_B','RGB_C','Lux',  'CO2',  'TVOC']
#     #CSV_type  =  ['string',    'date', 'time', 'float','float','int',  'int',  'int',  'int',  'int'  ,'int',  'int',  'int',  'int',  'int' ]
#     CSV_items  =  ['device_id', 'date', 'time', 's_t0', 's_h0', 's_d0', 's_d1', 's_d2', 's_lr', 's_lg', 's_lb', 's_lc', 's_l0', 's_gh', 's_gg']
#     CSV_msg = ""

#     pairs = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S").split(" ")
#     values["date"] = pairs[0]
#     values["time"] = pairs[1]

#     for item in CSV_items:
#         if item in values:
#             CSV_msg = CSV_msg + str(values[item]) + ','
#         else:
#             CSV_msg = CSV_msg + "N/A" + ','
#     CSV_msg= CSV_msg[:-1] #to get rid  of ',' from last data

#     #color.print_p("CSV_MSG:")
#     #print(CSV_msg)

#     with open(path + "/" + values["date"] + ".csv", "a") as f:
#         f.write(CSV_msg + "\n")


def upload():
    restful_str = "wget -O /tmp/last_upload.log \"" + Conf.Restful_URL + "topic=" + Conf.APP_ID + "&device_id=" + Conf.DEVICE_ID + "&key=" + Conf.SecureKey + "&msg=" + msg + "\""

    color.print_p("restful_str:")
    print(restful_str)

    os.system(restful_str)
