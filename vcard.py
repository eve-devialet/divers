# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 13:10:01 2017

@author: eveaporee
"""
import csv
import vobject

with open("/Users/eveaporee/Desktop/repertoire.txt", "r") as myfile:
    mycsv = csv.reader(myfile, delimiter=';')
       
    for line in mycsv:
        print(line)
        prenom = line[0]
        nom = line[1]
        num = line[2]
        card = vobject.vCard()
        
        card.add('n')
        card.n.value = vobject.vcard.Name( family=nom, given=prenom )
        card.add('fn')
        
        card.fn.value = prenom + ' ' + nom
        #card.add('email')
        
        #card.email.value = 'jeffrey@osafoundation.org'
        #card.email.type_param = 'INTERNET'
        
        card.add('TEL')
        card.tel.value= num
        card.tel.type_param="cell"
        
        card.prettyPrint()
        #TEL;TYPE=cell:(123) 555-5832
        
        with open("/Users/eveaporee/Desktop/cards/%s%s.VCF"%(prenom, nom), "w") as myfile:
            myfile.writelines(card.serialize())