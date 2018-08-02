# -*- coding: utf-8 -*-

'''
/******************************************************************************
 * FileName 	: 	main.py
 * Author	 	: 	Guo Yujie
 * CreateDate	:	2018.06.20
 * Revision		:	V1.0
 * Description	:	Main Function
 * Copyright	:	Copyright (c) 2000-2020	FiberHome
 * OtherInfo	:
 * ModifyLog	:
******************************************************************************/

'''
import test
import read_ip_table

if __name__ == "__main__":
    #read ip table to dict
    ip_dict = read_ip_table.read_ip_table() 
    #construct the key-value contains the next hop info 
    for key,value in ip_dict.items():
        key = test.split_ip_mask(key)
        test.table[key] = value
    #add the next hop table's info
    ip_mask_set = ip_dict.keys()
    for i in ip_mask_set:
        test.add_ip(i)
    #search the distict ip
    ip_search = 'FF60:0999:110F:2A90:FE00:0000:4CA2:9C5A'
    out = test.search_ip(ip_search.lower())
    print(out)
   # print(test.memb)