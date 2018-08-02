# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
'''
/******************************************************************************
 * FileName 	: 	func_mod.py
 * Author	 	: 	Guo Yujie
 * CreateDate	:	2018.06.20
 * Revision		:	V1.0
 * Description	:	define the functinon used  
 * Copyright	:	Copyright (c) 2000-2020	FiberHome
 * OtherInfo	:
 * ModifyLog	:
******************************************************************************/
'''
from trie_cons import trie

#n is defined as the column length of tcama
# in this case 16 is the cut length of tcama in this patent
global n 
n = int(16/4)
#tcama contains ip_mask_n
tcama = []
#tcamb contains ip_mask
tcamb = []
#mema is the hashmap contains the trie or next hop
mem = {}
#mema is the hashmap contains the next hop
memb = {}
#table contains the key-value is ip&mask - next hop
table = {}
"""
ip_mask:128/n
ip_mask_n:ip_mask&mask[0:n]
split_ip_mask(ip_mask):ip&mask
split_ip_mask_n(ip_mask): ip&mask[0:n],ip&mask[n:len]
splited_ip_mask:ip_mask&mask

"""

global ip_dict

def split_ip(ip):
    """
    split ip to str  
    type ip: str
    return type: str
    """
    ip_arr = ip.split(":")
    #ip_arr = ['123','123'....]
    splited_ip = "".join(ip_arr)
    return splited_ip
    
        
def split_ip_mask(ip_mask):
    """
    split the ip in the ip table 
    return the result of ip&mask
    convert ip to binary, then get the first mask's length bit,then convert it to hex
    
    type ip_mask: str "128/mask"
    return str:splited_ip_mask
    """
    res = ''
    spl = ip_mask.split("/")
    ip = ''.join(spl[0])
    
    ip_list = ip.split(":")
    join_ip = ''.join(ip_list)
    join_ip_bin = bin(int(join_ip,16))
    
    len_0 = 130 - len(join_ip_bin)
    join_ip_bin = '0'*len_0 + join_ip_bin[2:]
    
    len_mask = int(spl[1])
    for i in range(len_mask):
        res += join_ip_bin[i]
    res = hex(int(res,2))
    res = res[2:]
    return res

def split_ip_mask_n(splited_ip_mask):
    """
    split the ip&mask to n and (ip&mask - n) and return the result
    store the n bit in tcama and build the trie /
    with the (ip&mask - n)
    
    type splited_ip_mask: str
    type n: int
    return type res:list[str(ip_n),str(ip_m)]
    """
    global n 
    ip_n = ''
    ip_m = ''
    res_n_m = []
    if len(splited_ip_mask) <= n:
        #res_n_m.append(splited_ip_mask).append('')
        return splited_ip_mask
    else:
        ip_n = splited_ip_mask[0:n]
        ip_m = splited_ip_mask[n:len(splited_ip_mask)]
        res_n_m.append(ip_n)
        res_n_m.append(ip_m)
        return res_n_m



def add_ip_tcama(splited_ip_mask):
    """
    this function is to add the spkited_ip_mask to tcama
    type splited_ip_mask: str, ip_mask&mask
    considerate the condition that tcama contains contains same prefix
    
    
    """
    global n 
    if len(splited_ip_mask) >= n:
        temp = split_ip_mask_n(splited_ip_mask)
        if(temp == splited_ip_mask):
            ip_n = temp
            ip_m = ''
        else:
            ip_n = temp[0]
            ip_m = temp[1]
        #solve the condition that tcama contains same n_length prefix
        if (ip_n in tcama):
            index_ip_n = tcama.index(ip_n)
            trie_ip_n = mem[index_ip_n]
            trie_ip_n.insert(ip_m)
        else:
            pos = add_ip_n_tcama(ip_n)
         
            
            trie_ = trie()
            #if(len(ip_m) > 0):
            trie_.insert(ip_m)
            mem[pos] = trie_
        
    else:
        if(splited_ip_mask in tcama):
            return
        pos = add_ip_n_tcama(splited_ip_mask)
        mem[pos] = table[splited_ip_mask]
    
    
  
    
    
def add_ip(ip_mask):
    """
    this function is to add ip_mask to tcam
    this can be devided to three conditions:
        tcama contain prefix ;
        tcama not contain, tcamb not contain;
        tcamb contain
    type: ip_mask is 128/mask
    
    """    
    global n 
    splited_ip_mask = split_ip_mask(ip_mask)
    
    if tcama_con_same_prefix(splited_ip_mask):
        add_ip_tcama(splited_ip_mask)
        if tcamb_con_same_prefix(ip_mask):
            ip_mask_b_list = remove_same_prefix_ip_tcamb(ip_mask)
            for i in ip_mask_b_list:
                add_ip_tcama(split_ip_mask(i))
       
    
    elif not tcamb_con_same_prefix(ip_mask):
        #add the full ip addr
        add_ip_tcamb(ip_mask)
   
    else:
        ip_mask_b_list = remove_same_prefix_ip_tcamb(ip_mask)
        for i in ip_mask_b_list:
            add_ip_tcama(split_ip_mask(i))
        splited_ip_mask = split_ip_mask(ip_mask)
#        splited_ip_mask_b = split_ip_mask(ip_mask_b)
        
#        add_ip_tcama(splited_ip_mask_b)
        add_ip_tcama(splited_ip_mask)

    
def tcama_con_same_prefix(splited_ip_mask):
    """
    this fuction is to judge whethe tcama contains same prefix as splited_ip_mask
    type splited_ip_mask: str
    return type: bool
    """
    res = False
    if(len(tcama) == 0):
        return res
    
    for i in tcama:
        res = contains(i,splited_ip_mask)
        if res:
            break
    return res

def contains(str1, str2):
    """
    judge whethe str1 contains str2 or str2 contains str1
    return True if contain,return False otherwise
    type str1,str2: str
    type res: bool
    """
    res = False
    j=0
    min_len = min(len(str1),len(str2))
    for i in range(min_len):
        if str1[i] == str2[i]:
            j = j+1
        else:
            break
    if j == min_len:
        res = True
    else:
        res = False
    return res
    
    

def tcamb_con_same_prefix(ip_mask): 
    """
    judge whethe the tcamb contains same prefix as splited_ip_mask
    type splited_ip_mask: str (ip&mask)
    return type: bool
    """
    res = False
    splited_ip_mask = split_ip_mask(ip_mask)
    if len(tcamb) == 0:
        return res
    for i in tcamb:
        splited_ip_mask_b = split_ip_mask(i)
        
        if contains(splited_ip_mask,splited_ip_mask_b) :
            res = True
            break
    return res
        

    
def add_ip_n_tcama(ip_mask_n):
    """
     
    this func is to insert the ip_mask_n to tcama
    
    return type: the index of the input item
    """
    
    
    '''
    we need to know every item's positon after sort ,so that we can arrange the mem/
    construct a hashmap to matain the positon relationship
    '''   
    tcama.append(ip_mask_n)

    index_ = tcama.index(ip_mask_n)
    return index_
    

def add_ip_tcamb(ip_mask):
    """
    tcamb contains ip_mask:128/mask
    add ip_mask to tcamb
    """
    tcamb.append(ip_mask)
    index_b = tcamb.index(ip_mask)
    splited = split_ip_mask(ip_mask)
    memb[index_b] = table[splited]
    
 
def remove_same_prefix_ip_tcamb(ip_mask):
    """
    remove the item has same prefix as ip_mask from tcamb
    return value: the item with same prefix as ip_mask,
    """
    result = []
    #rem_list = []
    splited_ip_mask = split_ip_mask(ip_mask)
    for i in range(len(tcamb)):
        splited_ip_mask_b = split_ip_mask(tcamb[i])
        if contains(splited_ip_mask,splited_ip_mask_b) :
            result.append(tcamb[i])
            tcamb[i] = '0000:0000:0000:0000:0000:0000:0000:0000/128'
    
    
#    for i in range(len(tcamb)-1,-1,-1):
#        
#        if(tcamb[i] == '0000:0000:0000:0000:0000:0000:0000:0000/128'):
#            del tcamb[i]
#            memb.pop(i)
#  
#    tcamb_copy = tcamb.copy()
#    for j in range(len(tcamb)):
#        if j == tcamb_copy.index(tcamb[j]):
#            continue
#        else:
#            memb.pop(tcamb_copy.index(tcamb[j]))
#            memb[j] = table[split_ip_mask(tcamb[j])]
#        
        
        
            
    return result 



    

def search_ip(ip):
    '''
    this function is to search_ip in the tcam
    first look up in the tcmab,if not match ,then lookup in tcama
    type ip: input ip
    return typr: the next hop 
    '''
    link_ip = split_ip(ip)

    for i in tcamb:
        
        
        item = split_ip_mask(i)
        len_item = len(item)
        if item == link_ip[:len_item].lower():
            index_match = tcamb.index(i)
            return memb[index_match]
    
    max_len = 0
    max_item = tcama[0]
    for j in tcama:
        len_match = len(j)
        if j == link_ip[:len_match].lower():
            if(len(j) > max_len):
                max_len = len(j)
                max_item = j
    index_match_tcama = tcama.index(max_item)
    if(max_len == n):
        trie_node = mem[index_match_tcama]
        trie_res = trie_node.search(link_ip[len_match:])
        if(len(trie_res) == 0):
            return table[max_item]
        else:
            longer_match = max_item + trie_res
            return table[longer_match]
        
    else:
        return mem[index_match_tcama]

 
    


   
        
    

    
    
    