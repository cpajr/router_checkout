#!/usr/bin/env python

from pprint import pprint
import re

#====================================
#           Functions               =
#====================================

def int_check(input):
    '''
    This function is to review the output of 
    'show router interfaces'.  It will then review
    each interface and review its current status.   
    '''
    
    for line in input.splitlines():
        
        if not re.search(r'to-.*mplse1', line):
            continue

        split_list = line.split()

        if split_list[1] != "Up":
            print ("ERROR: Interface '{}' is Admin Down".format(split_list[0]))
        elif split_list[2] != "Up/Down":
            print ("ERROR: Interface '{}' is Operationally Down".format(split_list[0]))

def isis_check(input):
    
    #Counter
    adj_counter = 0

    for line in input.splitlines():

        if not re.search(r'^[a-z]*mplse1', line):
            continue
        
        split_list = line.split()
        if split_list[2] != "Up":
            print ("ERROR: Isis adjacency on {} is not 'Up'".format(split_list[4]))

        

        adj_counter += 1

    if adj_counter != 2:
        print("ERROR: Unexpected number of adjacencies -- found {}, expecting 2".format(adj_counter))


#====================================
#           Main Routine            =
#====================================

#with open("router_interfaces.txt") as a:
#    a_output = a.read()

with open("isis_adj.txt") as b:
    b_output = b.read()
 
#int_check(a_output)
isis_check(b_output)