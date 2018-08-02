# -*- coding: utf-8 -*-
"""

/******************************************************************************
 * FileName 	: 	read_ip_table.py
 * Author	 	: 	Guo Yujie
 * CreateDate	:	2018.06.20
 * Revision		:	V1.0
 * Description	:	read the next hop table to dict
 * Copyright	:	Copyright (c) 2000-2020	FiberHome
 * OtherInfo	:
 * ModifyLog	:
******************************************************************************/

"""
import csv

def read_ip_table():
    """
    this function is to read the (ip_mask + next_hop) data to a dict
    type output table: dict 
    """
    dict_ip={}
    with open('ip.csv')as f:
        reader=csv.reader(f,delimiter=',')
        for row in reader:
            dict_ip[row[0]]=row[1]
    return dict_ip
    
    

