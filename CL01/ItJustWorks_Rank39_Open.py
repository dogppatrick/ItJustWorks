from datetime import timedelta,datetime
import glob
import os
import pandas as pd
import numpy as np

def count_in_hour(order_time):
    for i in range(len(order_time)-2):
        st = datetime.strptime(order_time[i], "%Y-%m-%d %H:%M:%S")
        count = 1
        for j in range(i+1,len(order_time)):
            et = datetime.strptime(order_time[j], "%Y-%m-%d %H:%M:%S")
            dt = et-st
            if dt >= timedelta(hours=1):
                break
            else:
                count+=1
                if count >=3:
                    return True
    return False

def count_in_hour_v2(order_time):
    i = 0
    while i < len(order_time)-2:
        st = datetime.strptime(order_time[i], "%Y-%m-%d %H:%M:%S")
        et = datetime.strptime(order_time[i+2], "%Y-%m-%d %H:%M:%S")
        if et-st >= timedelta(hours=1):
            pass
        else:
            return True
        i +=1
    return False

if __name__ == '__main__':
    data = pd.read_csv("./order_brush_order.csv", encoding="utf-8")
    arr = np.array(data)
    shop_s = list(set(arr[:,1]))
    result = []
    for shop in shop_s:
        d_shop = arr[arr[:,1]==shop,:]
        users = set(d_shop[:,2])
        b_user = "0"
        for user in users:
            order_time = d_shop[d_shop[:,2]==user,3]
            order_time = sorted(order_time)

            if len(order_time)>=3:
                if count_in_hour_v2(order_time):
                    if b_user =="0":
                        b_user = [(int(user),len(order_time))]
                    else:
                        b_user+= [(int(user),len(order_time))]
        if b_user == "0":
            result.append([shop,b_user])
        else:
            if len(b_user) >1:
                b_user  = sorted(b_user,key= lambda x:(-x[1],x[0]))
                if b_user[0][1]==b_user[1][1]:
                    result.append([shop,str(b_user[0][0])+"&"+str(b_user[1][0])])
                else:
                    result.append([shop,str(b_user[0][0])])
            else:
                result.append([shop,str(b_user[0][0])])

    df_result = pd.DataFrame(result,columns=['shopid','userid'])
    df_result.to_csv("tmp01.csv",index=False)