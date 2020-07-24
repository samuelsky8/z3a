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
UART_REQ_NODE_IC_SN = 'cc032a'
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

def kick_out_a_node_type_1(mac_addr):
    if(type(mac_addr) == str and len(mac_addr) == 16):
        print(mac_addr)
        rev_mac_addr = mac_addr[14:16] + mac_addr[12:14] + \
               mac_addr[10:12] + mac_addr[8:10]  + \
               mac_addr[6:8]   + mac_addr[4:6]   + \
               mac_addr[2:4]   + mac_addr[0:2]   
    data = UART_KICK_OUT_A_NODE_TYPE_1 + rev_mac_addr
    print(data)
    return data
               

def kick_out_a_node_type_2(srt_addr):
    if(type(srt_addr) == str and len(srt_addr) == 4):
        print(srt_addr)
        rev_srt_addr = srt_addr[2:4] + srt_addr[0:2]
    data = UART_KICK_OUT_A_NODE_TYPE_2 + rev_srt_addr
    print(data)
    return data

def analyze_white_list(list_s, s_len):
    s_dict = {}
    for i in range(s_len):
        key = str(list_s[(16+(i*34)):(18+(i*34))] + list_s[(14+(i*34)):(16+(i*34))])
        value = str(list_s[(32+(i*34)):(34+(i*34))] + list_s[(30+(i*34)):(32+(i*34))] + \
                list_s[(28+(i*34)):(30+(i*34))] + list_s[(26+(i*34)):(28+(i*34))] + \
                list_s[(24+(i*34)):(26+(i*34))] + list_s[(22+(i*34)):(24+(i*34))] + \
                list_s[(20+(i*34)):(22+(i*34))] + list_s[(18+(i*34)):(20+(i*34))])
        s_dict[key] = value
    return s_dict

def add_a_node(mac_addr):
    rev_mac_addr = mac_addr[14:16] + mac_addr[12:14] + \
                   mac_addr[10:12] + mac_addr[8:10]  + \
                   mac_addr[6:8]   + mac_addr[4:6]   + \
                   mac_addr[2:4]   + mac_addr[0:2]
    data = UART_ADD_A_NODE + rev_mac_addr
    print(data)
    return data

def req_node_fw_ver(srt_addr):
    data = UART_REQ_NODE_FW_VER + srt_addr[2:] + srt_addr[0:2]
    print(data)
    return(data)            

def req_node_ic_sn(srt_addr):
    data = UART_REQ_NODE_IC_SN + srt_addr[2:] + srt_addr[0:2]
    print(data)
    return(data) 

def req_node_net_info(srt_addr):
    data = UART_REQ_NODE_NET_INFO + srt_addr[2:] + srt_addr[0:2]
    print(data)
    return(data)

def analyze_node_net_info(data):
    net_info_dict = {}
    srt_addr = data[8:10] + data[6:8]
    mac_addr = data[24:26] + data[22:24] + \
               data[20:22] + data[18:20] + \
               data[16:18] + data[14:16] + \
               data[12:14] + data[10:12]
    rf_ch = data[26:28]
    panid = data[30:32] + data[28:30]
    net_info_dict['srt_addr'] = srt_addr
    net_info_dict['mac_addr'] = mac_addr
    net_info_dict['rf_ch'] = rf_ch
    net_info_dict['panid'] = panid
    print(net_info_dict)
 
if __name__ == '__main__':

    ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.5)
    print(ser.name)
    print(bytes.fromhex(UART_REQ_NODE_NET_INFO))
    ser.write(bytes.fromhex(UART_REQ_NODE_NET_INFO))    
    time.sleep(0.3)
    count = ser.inWaiting()
    print(count)
    s = ser.read(count)
    print(s.hex())
    
    
    ser.write(bytes.fromhex(UART_REQ_WHITE_LIST))
    time.sleep(0.3)
    count = ser.inWaiting()
    print(count)	
    s = ser.read(count)
    #print(s.hex())
    s_list = s.hex()
    s_len = s_list[12:14] + s_list[10:12]
    #print(s_len)
    s_dict = analyze_white_list(s_list, int(s_len, 16))
    print(s_dict)
    print(type(s_dict))
    
    ser.write(bytes.fromhex(req_node_fw_ver('0000')))
    time.sleep(0.3)
    count = ser.inWaiting()
    print(count)
    s = ser.read(count)
    print(s)
    ver = s[5:].decode()
    print(ver)

    #ser.write(bytes.fromhex(req_node_ic_sn('0000')))
    #time.sleep(0.3)
    #count = ser.inWaiting()
    #print(count)
    #s = ser.read(count)
    #print(s)
    
    ser.write(bytes.fromhex(req_node_net_info('4a03')))
    time.sleep(0.3)
    count = ser.inWaiting()
    print(count)
    s = ser.read(count)
    print(s.hex())

    analyze_node_net_info(s.hex())
 
    #for i in range(1,60):
    #    data = '7a624e528822' + hex(int('4a03', 16) + i)[2:]
    #    print(data)
    #    ser.write(bytes.fromhex(add_a_node(data)))
    #    time.sleep(0.3)
    #    count = ser.inWaiting()
    #    print(count)
    #    s = ser.read(count)
    #    print(s.hex())
    ser.close()     
    
    
