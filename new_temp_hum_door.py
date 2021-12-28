# -*- coding: utf-8 -*-
from new_relay_control import relay
from time import sleep
import json

#温湿度获取
def temp_hum_sensor_get():
    temp_hum = relay()
    temp_hum.all_relay = 3
    temp_hum.relay_all_on_order = ['01 04 00 00 00 02 71 CB']
    return_str = temp_hum.ALL_ON()
    return return_str

#门磁状态获取
def door_sensor_get():
    door_sensor = relay()
    door_sensor.all_relay = 3 
    door_sensor.relay_all_on_order = ['FE 01 00 00 00 02 A9 C4']
    return_str = door_sensor.ALL_ON()
    return return_str

id_value = 2
time = 1

while True:
    try:
        #读文件（读平台下发的指令）
        fp = open('/tmp/from_platform.txt', 'r')
        str_read = fp.read()
        # {"inputParams":{"relay_action":true},"actionCode":"relay"}
        recv_json = json.loads(str_read)
        relay_action = recv_json['inputParams']['action']
        action_code = recv_json['actionCode']
        print(relay_action)
        print(action_code)
        print("read from platform: %s " % str_read)
        print("data type: %s" % (type(str_read)))

        if action_code == "relay":
            relay_open = relay()
            if relay_action == True:
                return_str = relay_open.ALL_ON()
            else:
                return_str = relay_open.ALL_OFF()

            relay_str = return_str[8:12]
            upload_to_platform = 0
            print(relay_str)
            if relay_str != "0000":
                upload_to_platform = 1

            string = "{\"actionCode\": \"relay\", \"actionTime\": 1626197189630,\"outputParams\": {\"relaystate\":0}}"
            new_json = json.loads(string)
            new_json['outputParams']['relaystate'] = upload_to_platform
            final_str3 = json.dumps(new_json)
            print(final_str3)

            f = open('/tmp/1.txt', 'w')
            f.write(final_str3)
            f.close()

    except FileNotFoundError:
            print ("File is not found")

    if id_value == 2:

        return_str = temp_hum_sensor_get()
        print(return_str)

        get_str1 = return_str[6:10]
        get_str2 = return_str[10:14]

        try:
            # temp_value = (int(get_str1, 16))/10
            temp_value = int(get_str1, 16)
            # hum_value = (int(get_str2, 16)) / 10
            hum_value = int(get_str2, 16)
        except ValueError:
            pass

        print(temp_value)
        print(hum_value)
        print(get_str1)
        print(get_str2)

        string1 = "{\"temp\":{\"value\":\"temp_value\",\"time\":1631708204231},\"hum\":{\"value\":\"hum_value\",\"time\":1631708204231}}"
        new_json1 = json.loads(string1)
        new_json1['temp']['value'] = temp_value
        new_json1['hum']['value'] = hum_value
        final_str4 = json.dumps(new_json1)
        print(final_str4)

        f = open('/tmp/2.txt', 'w')
        f.write(final_str4)
        f.close()


    #if id_value == 3:
        return_str = door_sensor_get()
        get_str3 = return_str[6:8]
        door_upload_to_platform = 0
        if get_str3 == "00":
           door_upload_to_platform = 0
        else:
           door_upload_to_platform = 1

        string2 = "{\"eventCode\":\"door\",\"eventTime\":1626197189630,\"outputParams\":{\"doorsate\":0}}"
        new_json2 = json.loads(string2)
        new_json2['outputParams']['doorsate'] = door_upload_to_platform
        final_str5 = json.dumps(new_json2)
        print(get_str3)
        print(final_str5)
        f = open('/tmp/3.txt', 'w')
        f.write(final_str5)
        f.close()
    sleep(time)

