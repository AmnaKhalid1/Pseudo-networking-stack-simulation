#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A program for a communication channel with one end sending strings to the other.
In between the two sides, the data will move through some layers to be fragmented
into smaller packets and encrypted. The program will inclued the implemintaion
of all needed layers. (Layered Networking Implementation)

@author: Ibtisam Al-Hinai  
         Amna Al-Nadabi    
         Abrar Al-Hsani    

"""

#Import the needed libraries     
import math
import random
from sys import exit

'''
Class of sender app which send strings to another app through Layered Networking
attributes: input string
methods: getMsg--> get the the massage to be send
'''
class sender:
    def __init__(self):
        self.msg = input("Enter the massage to be send: ")
        
    def getMsg(self):
        return self.msg
    

'''
Class of receiver app which receive strings through Layered Networking
attributes: string massage
methods: getMsg--> get the the received massage
         display--> print the received massage
'''        
class receiver:
    def __init__(self, msg):
        self.msg = msg
        
    def getMsg(self):
        return self.msg   
    
    def display(self):
        print("Received massage ==> ", self.msg )

'''
Class of the encryption layer that use rot3 technique to encrypt the sent message
attributes: sended massage & encrypted massage
methods: encrypt--> encrypt the sended massage by using rot3 method
         decrypt--> decrypt the sended massage when it get to the other side 
         display--> print the encrypt massages
'''
class Encryption:
    
    #alphabet letters
    l_alphabet = 'abcdefghijklmnopqrstuvwxyz'
    u_alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    def __init__(self, msg):
        self.msg = msg
        self.encryptedMsg = ""
        
    def encrypt(self):
        
        for char in self.msg or []:
            self.encryptedMsg += self.__rot3(char)
        
        return self.encryptedMsg
    
    '''
    This method convert a letter to another letter that is 3 positions
    further from that letter in alphabetical order.
    '''
    def __rot3(self, char):
        
        if char.isalpha()and char.isupper():
            e_char = self.u_alphabet[(self.u_alphabet.index(char) + 3) % 26]
        elif char.isalpha()and char.islower():
            e_char = self.l_alphabet[(self.l_alphabet.index(char) + 3) % 26]
        else:
            e_char = char
        
        return e_char
    
    #The opposite of rot3 used to decrypt the string
    def __rot3_l(self, char):
        
        if char.isalpha()and char.isupper():
            e_char = self.u_alphabet[(self.u_alphabet.index(char) - 3) % 26]
        elif char.isalpha()and char.islower():
            e_char = self.l_alphabet[(self.l_alphabet.index(char) - 3) % 26]
        else:
            e_char = char
        
        return e_char
    
    def decrypt(self):
        for char in self.msg or []:
            self.encryptedMsg += self.__rot3_l(char)
        
        return self.encryptedMsg
    
    
    def display(self):
        print(self.encryptedMsg)
        print()
        
'''
Class of the fragmentation layer that used to split the string into packets.
attributes: sended massage & list of packets
methods: split--> split the sened string into packets, each one is 4 bytes long, with one packet reserved for the checksum.
         join--> join the packets together to form the original data on the receiving end.
         display--> print the content of each packet.
'''
class Fragmentation:
  
   def __init__(self,input_string):
       self.input_string = input_string
       self.all_packets = []
       
       
   def split(self):
       
        # encode strings to bytes
        encoded_string = self.input_string.encode('utf-8')
        
        input_string_size = len(encoded_string)#in bytes 
        
        #compute number of packets needed
        num_packet = math.ceil(input_string_size / 3) 
        
        #create bytearray from encoded string 
        byte_array = bytearray(encoded_string)
        l = list(byte_array)
        
        #based on the number of packets the data is divied into packets
        #then it will be added to the all_packets list 
        count = 3
        for i in range (num_packet):
            self.all_packets.append(l[count-3:count])
            count = count+3
            
        #until now no byte added for checksum 
        #so every packet is with length 3 at maximum and 1 at minimum
        #using the subtraction will know how many zero byte should be appended
        #checksum byte is initially zero
        for i in self.all_packets :
            if len(i) != 4 :
                for n in range (4-len(i)):
                    i.append(00000000)
        return self.all_packets
    
   def display(self):
       i = 1
       for p in self.all_packets:
           print("Packet ", i , ": " , p)
           i+=1
       print()
    
   def __joinPacket (self, packet):
       num_packets = len(self.input_string)
       full_data = ""
       
       if len(self.all_packets) != num_packets :
           
           #don't include last byte(the one for checksum)
           packet =bytearray(packet[:-1]) 
           
           #decode the arraybyte to string 
           packet_string = packet.decode()
           self.all_packets.append(packet_string)
    
    
       if len(self.all_packets) == num_packets :
           for packett in self.all_packets:
               full_data = full_data + packett
               return full_data
   
   def join(self, packets):
       full_data = ""
       for p in packets :
       
           #if checksum valid go and join 
           self.__joinPacket(p)
    
       for packet in self.all_packets:
           full_data = full_data + packet
           
       print(full_data)
       return full_data
    
'''
Class of the checksum layer that computed a sum value and placed it in the last byte of the packet.
attributes: data packet
methods: checkSum--> compute the sum value of first 3 bytes of the packet and place that value in the fourth byte in the packet.
         checkSumValue--> check the validity of the ckecksum byte.
         display--> print the content of the packet after add the checksum value
'''
class CheckSum :
    def __init__(self,packet):
        self.packet = packet
        
    def checkSum(self):
        #sum the first three bytes (elements in the list)

        summation = sum(self.packet[:-1])
        binary_sum = bin(summation)
        binary_sum = binary_sum[2:]
        
        #make sure that the summation is not more than one byte
        if len(binary_sum) > 8 :
            summ = binary_sum[len(binary_sum)-8 :]
            carry =binary_sum[:len(binary_sum)-8 ]
           
            final_sum = int('0b'+carry,2)+ int('0b'+summ,2)
            final_sum = bin (final_sum)
           
            binary_sum = final_sum[2:] 
            
       
        #get the complemnet 
        complement = ''
        for i in  binary_sum :
            if i =='0':
                complement =complement+'1'
            else :
                complement =complement+'0'
        
        self.packet[len(self.packet)-1] = int('0b'+complement,2)
        
        return self.packet
    
        
    def checkSumValue(self,recive_packet):
        
        #sum the first three bytes (elements in the list)
        summation = sum(self.packet[:-1])
        binary_sum = bin(summation)
        
        #get rid of 0b string
        binary_sum = binary_sum[2:]
        
        #if the summation result is more than one byte(8bits)
        #sum the carry again with the result (result without carry)
        if len(binary_sum) > 8 :
            summ = binary_sum[len(binary_sum)-8 :]
            carry =binary_sum[:len(binary_sum)-8 ]
           
            final_sum = int('0b'+carry,2)+ int('0b'+summ,2)
            final_sum = bin (final_sum)
           
            binary_sum = final_sum[2:] 
            
       
        #get the one complemnet of the summation result
        complement = ''
        for i in  binary_sum :
            if i =='0':
                complement =complement+'1'
            else :
                complement =complement+'0'
        
        return int('0b'+complement,2)
    
    def validateCheckSum (self , CheckSum_reciver ,CheckSum_sender ):
        if CheckSum_reciver == CheckSum_sender :
            print("- Valid checksum accept ")
            
        else :
            print("- Invalid checkSum reject")
            print("The program has been stopped due to an error...")
            exit()
            
        
    def display(self):
        print(self.packet)
    
'''
Class of the physical layer that simulates (random generation) possible bit errors in a packet with some probability p.
attributes: data packet
methods: error--> simulates errors with a certain probability
         display--> print the content of the packet after the modifications
'''
class Physical:
    def __init__(self,packet):
        self.packet = packet
        
    def error(self):
        p = 0.05 #certain probability
        r = random.uniform(0, 1) #random probability
        
        #if r<p then modify one char in the packet
        if r < p:
            pos = random.randint(0, 2) #random position of byte [1,2,3]
            
            #modify the char in position p to the next char (add 1 to its ASCII value) 
            if self.packet[pos]== 127:
                self.packet[pos] = 0
            else:
                self.packet[pos] += 1
                
            return self.packet
        
        #else the packet is sent without modifications
        else:
            return self.packet
        
    def display(self):
        print(self.packet)

'''
Network layer that deals with send and receives of packets from a layer to another layer.
'''        
def Network():
    #header
    print("Layered Implementation Network")
    print()
    print("=="* 30)
    
    
    #Application1
    print("************ Application 1 ****************")
    app1 = sender()
    print()
    print("--"* 30)
    
    
    #Encryption Layer
    print("************ Encryption Layer *************")
    encrypt_obj = Encryption(app1.getMsg())
    encrypt_msg = encrypt_obj.encrypt()
    print("Encrypted String ==> ", end="")
    encrypt_obj.display()
    
    print("--"* 30)
    
    #Fragmentation Layer
    print("************ Split Layer ******************")
    split_obj = Fragmentation(encrypt_msg)
    split_packets = split_obj.split()
    print("Contant of each packet after split the string:")
    split_obj.display()
    
    print("--"* 30)
    
    #Checksum layer
    print("************ Checksum layer ***************")
    print("Contant of each packet after add the checksum byte:")
    for p in split_packets:
        checksum_obj = CheckSum(p)
        checksum_packet = checksum_obj.checkSum()
        checksum_obj.display()
        
    print()
    print("--"* 30)   

    #Physical layer
    print("************ Physical layer ***************")
    print("Contant of each packet after errors random generation:")
    for p in split_packets:
        physical_obj = Physical(p)
        error_packet = physical_obj.error()
        physical_obj.display()
        
    print()   
    print("--"* 30)
    
    
    #Validate CheckSum layer
    print("************ Validate CheckSum layer ******")
    for p in split_packets:
        checksum_obj2 = CheckSum(p)
        checksum_packet2 = checksum_obj2.checkSumValue(p)
        check_result = checksum_obj2.validateCheckSum(checksum_packet2, p[-1])
        
    print()   
    print("--"* 30)
    
    #Join layer
    print("************ Join layer ******************")
    join_obj = Fragmentation(split_packets)
    print("Joined String ==> ", end="")
    join_msg = join_obj.join(split_packets)
    
    print()   
    print("--"* 30)
    
    #Decryption Layer
    print("************ Decryption layer ************")
    decrypt_obj = Encryption(join_msg)
    decrypt_msg = decrypt_obj.decrypt()
    print("Decrypted String ==> ", end="")
    decrypt_obj.display()
    
    print()   
    print("--"* 30)

    #Application2
    print("************ Application 2 ***************")
    app2 = receiver(decrypt_msg)
    app2.display()
    
    
Network() 
    
