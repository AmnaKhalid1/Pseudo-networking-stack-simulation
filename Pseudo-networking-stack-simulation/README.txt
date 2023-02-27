The main body of the program takes in a string, passesthrough the layers, across the network, and then reassembles (Join) the string to print it out:

Split: this should split the string into packets. Remember that packets are 4 bytes long, with one packet
reserved for the checksum. If a string does not fill a packet completely, the packet should be padded
with zeros. On the receiving end, packets are joined together to form the original data


Checksum: a value is computed and placed in the last byte of the packet. On sending you calculate
the byte based on the 4 data bytes. A very simple method that you can use is to add the data bytes
modulo 256, and place the result in the checksum byte. On the receiving end, you should calculate the
checksum again and compare it with the value in the packet. If they are different, you should print out
a warning error message and stop.


Encryption: The encryption layer will initially use a simple technique called rot3- rot3 simply rotates
alphabetic characters by 3 places in the alphabet. Applying rot 3 a second time returns the cyphertext to
the plaintext. Code is supplied to perform rot3 using C below.


Network: This layer deals with send and receives of one packet at a time.
Physical: This layer simulates (random generation) possible bit errors in a packet with some
probability p.