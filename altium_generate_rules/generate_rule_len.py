# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 18:27:58 2017

@author: eveaporee
"""

import numpy as np
import csv

def export_rule(nets):
    i = 0
    lines = list()
    for net in nets:
        if net['type'] == 0:
            pass
        else:
            if i >= 26**2:
                raise NotImplementedError('Up to 26*26')
            msb = i / 26
            lsb = i%26
            msb = chr(ord('A') + msb)
            lsb = chr(ord('A') + lsb)
            uniqueid = "LENRUL%s%s"%(msb, lsb)
            i = i+1           
            #uniqueid = "KHDVUPHW"
            line = ("SELECTION=FALSE|LAYER=UNKNOWN|LOCKED=FALSE|POLYGONOUTLINE=FALSE|USERROUTED=TRUE|UNIONINDEX=0|RULEKIND=Length|NETSCOPE=AnyNet|LAYERKIND=SameLayer|SCOPE1EXPRESSION=InNet('%s')|SCOPE2EXPRESSION=All|NAME=Len_%s|ENABLED=TRUE|PRIORITY=%i|COMMENT= |UNIQUEID=%s|DEFINEDBYLOGICALDOCUMENT=FALSE|MAXLIMIT=%.1fmil|MINLIMIT=%.1fmil"%
                   (net['net'], net['net'], i, uniqueid, net['pcb_max_len']/0.0254, net['pcb_min_len']/0.0254))
            lines.append(line)
    filecontent = '\xb6\r\n'.join(lines)
    # Don't forget EOL at the end of file
    filecontent = filecontent + '\xb6\r\n'
    
    with open('ddr_rules.RUL', 'w') as myfile:
        myfile.write(filecontent)

def create_nets():
      # Create ndarray
    num = np.zeros(52)

    nets = np.array(num, dtype=[('net', 'S30'), ('ball', 'S5'), ('type', 'i4'),
                       ('sip_len', 'f'), 
                       ('tot_nom_len', 'f'), 
                       ('pcb_nom_len', 'f'),
                       ('margin', 'f'), 
                       ('pcb_min_len', 'f'),
                       ('pcb_max_len', 'f')])
    nets['type'].fill(0)
    return(nets)

def import_csv(nets):
    '''
    Import the SIP net length list from CSV.
    Lengths are in um.
    Types:
    * 1 : address and control signals
    * 2 : DQ and DM signals
    * 3 : DQS pairs
    * 4 : CLK
    * 0 : no length matching on those signals
    '''
    with open("net_len.csv", 'r') as myfile:
        csvr = csv.reader(myfile)
        for idx, row in enumerate(csvr):
            nets['net'][idx] = row[0]
            nets['ball'][idx] = row[1]
            nets['sip_len'][idx] = float(row[2]) * 1e-3
            nets['type'][idx] = int(row[3])

def create_nom_values(nets, clk_ref, dqs_ref = 0):
    '''
    Create nominal len values from a DQS ref and a CLK ref len value (PCB
    track length)
    '''
    clk_ref_tot = clk_ref + nets[nets['net'] == 'DDR_CK_P']['sip_len'][0]
    if dqs_ref != 0:
        dqs_ref_tot = dqs_ref + nets[nets['net'] == 'DDR_DQS0_P']['sip_len'][0]
        if abs(dqs_ref_tot - clk_ref_tot + 32) > 44.5:
            raise Exception("DQS = (CLK - 32 mm) +- 44.5mm")
    else:
        dqs_ref_tot = clk_ref_tot - 32
    
    for net in nets:
        typenet = net['type']
        if typenet == 1:
            # Address and control len
            net['tot_nom_len'] = clk_ref_tot + 5
            net['margin'] = 10
        elif typenet == 2:
            # Data DQ and DM len
            net['tot_nom_len'] = dqs_ref_tot
            net['margin'] = 8
        elif typenet == 3:
            # DQS pairs len
            net['tot_nom_len'] = dqs_ref_tot
            net['margin'] = 0.127
        elif typenet == 4:
            # Clock len
            net['tot_nom_len'] = clk_ref_tot
            net['margin'] = 0.127
    
    # Taking SIP len into account
    nets['pcb_nom_len'] = nets['tot_nom_len'] - nets['sip_len']
    # Calculating min and max
    nets['pcb_min_len'] = nets['pcb_nom_len'] - nets['margin']
    nets['pcb_max_len'] = nets['pcb_nom_len'] + nets['margin'] 

nets = create_nets()

import_csv(nets)

create_nom_values(nets, 100)
export_rule(nets)