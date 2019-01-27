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
    
    #begin function output
    print()
    print("{}".format("="*30))
    print("{:^30}".format("Router Interface Check"))
    print("{}".format("="*30))

    for line in input.splitlines():
        
        if not re.search(r'to-.*mplse1', line):
            continue

        split_list = line.split()

        if split_list[1] != "Up":
            print ("ERROR: Interface '{}' is Admin Down".format(split_list[0]))
        elif split_list[2] != "Up/Down":
            print ("ERROR: Interface '{}' is Operationally Down".format(split_list[0]))

def isis_check(input):
    
    '''
    This is to verify the ISIS adjacency status.  It is checking on three things:
      1) Verifying that the ISIS adjacency is 'Up'
      2) Verifying that the advertised router name matches that of the router 
         interface name
      3) Verifying the expected count of 2 adjacencies
    '''

    #Variables Instantiation
    adj_counter = 0

    #begin function output
    print()
    print("{}".format("="*30))
    print("{:^30}".format("ISIS Adjacency Check"))
    print("{}".format("="*30))

    for line in input.splitlines():

        #Ignore potential case where it picks up on the command line name
        if not re.search(r'^[a-z]*mplse1', line):
            continue
        
        split_list = line.split()
        if split_list[2] != "Up":
            print ("ERROR: Isis adjacency on {} is not 'Up'".format(split_list[4]))

        rtr_int_name = re.search(r'to-(.*mplse1)', split_list[4]).group(1)
        rtr_name = split_list[0]

        if rtr_name != rtr_int_name:
            print("ERROR: Adjacent router name does not match Router Interface name ({} -- {})".format(rtr_name, rtr_int_name))

        adj_counter += 1

    if adj_counter != 2:
        print("ERROR: Unexpected number of adjacencies -- found {}, expecting 2".format(adj_counter))

def rsvp_check(input):
    '''
    This does a check against the RSVP neighbors and their
    current status.  It will check on the following:
     1) Verify that the neighbor is in an "up" state
     2) Verify the expected RSVP flags are seen
     3) Verify the expected two neighbors
    '''

    #Variables
    nei_counter = 0

    #begin function output
    print()
    print("{}".format("="*30))
    print("{:^30}".format("RSVP Neighbor Check"))
    print("{}".format("="*30))

    for line in input.splitlines():

        if not re.search(r'to-.*mplse1', line):
            continue

        split_list = line.split()
        if split_list[2] != "Up":
            print ("ERROR: RSVP Neighbor on {} is not 'Up'".format(split_list[1]))

        if (split_list[5] != "LR") or (split_list[6] != "RR") or (split_list[7] != "RM"):
            print("ERROR: Unexpected RSVP flags on {}".format(split_list[1]))

        nei_counter += 1

    if nei_counter != 2:
        print("ERROR: Unexpected number of neighbors -- found {}, expecting 2".format(nei_counter))

#====================================
#           Main Routine            =
#====================================

with open("router_interfaces.txt") as a:
    a_output = a.read()

with open("isis_adj.txt") as b:
    b_output = b.read()

with open("rsvp_neighbors.txt") as c:
    c_output = c.read()
 
int_check(a_output)
isis_check(b_output)
rsvp_check(c_output)