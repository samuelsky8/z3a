#!/usr/bin/python3

import serial
from queue import Queue
import time
from threading import Thread
import threading


UART_CHANGE_RF_CHANNEL = 'cc022f'
UART_REQ_WHITE_LIST = 'cc0105'
UART_REQ_CHILDREN_TABLE = 'cc0123'
UART_PERMIT_NODES_JOIN = 'cc030d'
UART_KICK_OUT_A_NODE_TYPE_1 = 'cc0903'
UART_KICK_OUT_A_NODE_TYPE_2 = 'cc0303'
UART_REQ_NODE_EXIST = 'cc0320'
UART_ADD_A_NODE = 'cc0906'
UART_REQ_NODE_FW_VER = 'cc032c'
UART_REQ_NODE_IC_SN = 'cc0324'
UART_REQ_NODE_NET_INFO = 'cc032d'
UART_REQ_NODE_RSSI = 'cc0321'
UART_REQ_NODE_NODE_VOLTAGE = 'cc0322'
UART_SET_NODE_NET_INFO_TYPE_1 = 'cc052b'
UART_SET_NODE_NET_INFO_TYPE_2 = 'cc0B2b'
UART_SET_NODE_NET_INFO_TYPE_3 = 'cc0d2b'
UART_REQ_NODE_NET_INFO = 'cc032d0000'
UART_RESET_NET_CONNECTION = 'cc0108'
UART_REQ_MANUFACTURE_SN = 'cc047E'

def change_rf_channel(number):
    if(type(number) == int):
        nu = "%02x" % number
    if(type(number) == str):
        nu = "%02x" % int(number)
    
    data = UART_CHANGE_RF_CHANNEL + nu
    return data

def permit_nodes_join(number):
    if(type(number) == int):
        nu = "%04x" % number
    if(type(number) == str):
        nu = "%04x" % int(number)

    data = UART_PERMIT_NODES_JOIN + nu[2:] + nu[:2]
    return data

def kick_out_a_node_type_1(mac_nu):
    if(type(mac_nu) == str and len(mac_nu) == 16):
        print(mac_nu)
        rev_mac_nu = mac_nu[14:16] + mac_nu[12:14] + \
               mac_nu[10:12] + mac_nu[8:10]  + \
               mac_nu[6:8]   + mac_nu[4:6]   + \
               mac_nu[2:4]   + mac_nu[0:2]   
    data = UART_KICK_OUT_A_NODE_TYPE_1 + rev_mac_nu
    print(data)
    return data

def kick_out_a_node_type_2(srt_addr):
    if(type(srt_addr) == str and len(srt_addr) == 4):
        print(srt_addr)
        rev_srt_addr = srt_addr[2:] + srt_addr[0:2]
    data = UART_KICK_OUT_A_NODE_TYPE_2 + rev_srt_addr
    print(data)    
               


def analyz_req_white_list(s_list, list_len,):
    
    return
    
if __name__ == '__main__':

    ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.5)
    print(ser.name)
    print(bytes.fromhex(UART_REQ_NODE_NET_INFO))
    ser.write(bytes.fromhex(UART_REQ_NODE_NET_INFO))    
    time.sleep(2)
    count = ser.inWaiting()
    print(count)
    s = ser.read(count)
    print(s.hex())
    
    rfchannel = '26'
    change_rf_channel(rfchannel)
    print(bytes.fromhex(change_rf_channel(rfchannel)))
    ser.write(bytes.fromhex(change_rf_channel(rfchannel)))
    time.sleep(2)
    count = ser.inWaiting()
    s = ser.read(count)
    print(s.hex())

    print(bytes.fromhex(UART_REQ_NODE_NET_INFO))
    ser.write(bytes.fromhex(UART_REQ_NODE_NET_INFO))    
    time.sleep(2)
    count = ser.inWaiting()
    print(count)
    s = ser.read(count)
    print(s.hex())
 
    
    ser.write(bytes.fromhex(UART_REQ_WHITE_LIST))
    time.sleep(2)
    count = ser.inWaiting()
    print(count)
    s = ser.read(count)
    s_list = s.hex()
    print(s_list, len(s_list))
    
     
