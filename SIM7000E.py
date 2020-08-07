import serial
import libs.MAPS_mcu as mcu
import time
from datetime import datetime

mcu.debug = 1

#print([hex(x) for x in a_list])


DEVICE_ID = "NBIOT-TEST01"
gps_lat   = "25.1933"
gps_lon   = "121.787"
app       = "MAPS6"
ver_app   = "6.1.0" #NBIOT test




def known_length(TX_DATA,RX_LENGTH):
    print("------------------------")

    print("send with known recive length")

    RESULT,RX_DATA = mcu.PROTOCOL_UART_TX_RX(0,TX_DATA,RX_LENGTH)

    print("RESULT:" + str(RESULT))
    print("RX_DATA:")
    #print([hex(x).upper() for x in RX_DATA])
    print("".join("0x%02x " % i for i in RX_DATA).upper())

    time.sleep(3)

    print("------------------------")


def unknown_length(TX_DATA):
    print("------------------------")

    print("send with unknown recive length")

    RESULT,RX_DATA = mcu.PROTOCOL_UART_TXRX_EX(0,TX_DATA,250,3000)
    print("RESULT:" + str(RESULT))
    print("RX_DATA:")
    print(RX_DATA)
    #print([hex(x).upper() for x in RX_DATA])
    #print("".join("0x%02x " % i for i in RX_DATA))


    time.sleep(3)
    print("------------------------")



try:
    print("START")
    print("========================")

    print("open port & init mcu")
    #mcu.ser=serial.Serial("COM57",115200,timeout=1)
    mcu.ser=serial.Serial("/dev/ttyS0",115200,timeout=3) #for PI (not ttyAMA0)(use /dev/ttyS0)
    time.sleep(5)
    print("mcu ok\n")
    print("------------------------")

    print("check I/O and device busy")

    #mcu.GET_INFO_VERSION()
    print(mcu.GET_INFO_SENSOR_POR())

    print("open uart\n")

    mcu.PROTOCOL_UART_BEGIN(0,4)


    time.sleep(1)

    mcu.CLEAR_INPUT()

    time.sleep(1)


    #TX_DATA = AT +CR (0x41 0x54 0x0D)
    #TX_DATA = [0x41,0x54,0x0D]
    TX_DATA = "AT\r".encode()
    #TX_DATA = bytearray()
    #RX_LENGTH = 9 byte for "OK" / 12 byte for "error"
    RX_LENGTH = 9

    print("start!!")

    while(1):

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

        pairs = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S").split(" ")

        #NBIOT_MQTT_pack(DEVICE_ID,gps_lat,gps_lon,app,ver_app,date,time,s_t0,s_h0,s_d0,s_d1,s_d2,s_lc,s_g8,s_gg)
        connect_pack,message_package = mcu.NBIOT_MQTT_pack(DEVICE_ID,gps_lat,gps_lon,app,ver_app,pairs[0],pairs[1],TEMP,HUM,PM25_AE,PM10_AE,PM1_AE,Illuminance,CO2,TVOC)

        print("!!!!!")
        print(connect_pack)
        print(message_package)
        print("!!!!!")

        print("".join("0x%02x " % i for i in connect_pack).upper())
        print("".join("0x%02x " % i for i in message_package[0]).upper())
        print("".join("0x%02x " % i for i in message_package[1]).upper())
        print("".join("0x%02x " % i for i in message_package[2]).upper())

        print("!!!!!")

        mcu.CLEAR_INPUT()
        #func1()
        #print(mcu.GET_INFO_SENSOR_POR())

        print("TEST AT")
        unknown_length("AT\r".encode())
        time.sleep(1)

        print("CPIN?")
        unknown_length("AT+CPIN?\r".encode())
        time.sleep(1)

        print("CSQ")
        unknown_length("AT+CSQ\r".encode())
        time.sleep(1)

        print("CIPCLOSE")
        unknown_length("AT+CIPCLOSE\r".encode())
        time.sleep(1)

        print("send hex")
        unknown_length("AT+CIPSENDHEX=1\r".encode())
        time.sleep(1)

        print("CSTT")
        unknown_length("AT+CSTT=\"nbiot\"\r".encode())
        time.sleep(1)

        print("CIICR")
        unknown_length("AT+CIICR\r".encode())
        time.sleep(1)

        print("CIFSR")
        unknown_length("AT+CIFSR\r".encode())
        time.sleep(1)

        print("CIPSTART")
        unknown_length("AT+CIPSTART=\"TCP\",\"35.162.236.171\",\"8883\"\r".encode())
        time.sleep(1)

        print("SEND COMMAND")
        unknown_length("AT+CIPSEND\r".encode())
        time.sleep(1)


        print("PACKAGE---connect")
        unknown_length(connect_pack)
        time.sleep(3)

        mcu.CLEAR_INPUT()
        mcu.ser.reset_output_buffer()

###
#        for i in range(len(message_package)):
#            print("PACKAGE---message")
#            unknown_length(message_package[i])
#            time.sleep(1)
###

#        print("PACKAGE---message")
#        unknown_length([0x30,0xdd,0x01,0x00,0x1d,0x4d,0x41,0x50,0x53,0x2f,0x4d,0x41,0x50,0x53,0x36,0x2f,0x4e,0x42,0x49,0x4f,0x54,0x2f,0x4e,0x42,0x49,0x4f,0x54,0x2d,0x54,0x45,0x53,0x54,0x30,0x31,0x7c,0x67,0x70,0x73,0x5f,0x6c,0x61,0x74,0x3d,0x32,0x35,0x2e,0x31,0x39,0x33,0x33,0x7c,0x73,0x5f,0x74,0x30,0x3d,0x32,0x37,0x2e,0x39,0x36,0x7c,0x61,0x70,0x70,0x3d,0x4d,0x41,0x50,0x53,0x36,0x7c,0x64,0x61,0x74,0x65,0x3d,0x32,0x30,0x32,0x30,0x2d,0x30,0x33,0x2d,0x32,0x37,0x7c,0x73,0x5f,0x64,0x32,0x3d,0x36,0x35,0x35,0x33,0x35,0x7c,0x73])
#        time.sleep(1)

        unknown_length(message_package[0])
        time.sleep(1)

        unknown_length(message_package[1])
        time.sleep(1)

        unknown_length(message_package[2])
        time.sleep(1)


        print("CIPCLOSE")
        unknown_length("AT+CIPCLOSE\r".encode())
        time.sleep(30)

        print("========================")





except KeyboardInterrupt:
    mcu.ser.close()
    print("ERROR!!")
    pass

mcu.ser.close()

print("exit OK")
