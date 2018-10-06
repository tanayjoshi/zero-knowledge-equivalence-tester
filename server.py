'''
    Simple socket server using threads
'''
 
import socket
import sys
from thread import *
#from paillier.paillier import *
import Crypto
from Crypto.PublicKey import RSA
from random import randint

#protocol using Crypto
#cipher = RSAencrypt(se)
#Server send two nonces non_a and non_b to Alice and Bob
#Server has it's own public/private key pair
#Alice sends Server Enc(non_a * hash(Sa))
#Bob sends Server Enc(non_b * hash(Sb))
#Server calculates non_b * non_a * hash(Sa)
#Server calculates non_a * non_b * hash(Sb)
#Server checks if they are equal

HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

#generate RSA keypair
key = RSA.generate(2048)
#generate a separate public key for others to use
pub = key.publickey()

#export this public key to a file for others to use
f = open('mykey.pem','w')
f.write(pub.exportKey('PEM'))
f.close()



#create two nonces to send to the two clients
non_a = (randint(0,9))
non_b = (randint(0,9))

#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
 
#Start listening on socket
s.listen(10)
print 'Socket now listening'
 
 
#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    #send the random nonce to client A
    conn.send(str(non_a))
    #receive data from client A
    d = conn.recv(1024)
    data = ((d))
    f = open('cl1key.pem','r')
    cl1key = RSA.importKey(f.read())
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    #decrypt the data
    b = key.decrypt(data)
    
    #repeat the same for client B
    conn2, addr2 = s.accept()
    conn2.send(str(non_b))
    d2 = conn2.recv(1024)
    data2 = ((d2))
    f = open('cl1key.pem','r')
    cl1key = RSA.importKey(f.read())
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    c = key.decrypt(data2)

    #multiply decrypted values with opposite nonces
    a1= b*non_b
    a2= c*non_a
    #print a1
    #print a2

    #if the final values are equal, output same else not same
    if (a1==a2):
        print "same"
        conn.send((cl1key.encrypt("same",1))[0])
        conn2.send("same")  
    else:
        print "not same"
        conn.send((cl1key.encrypt("not same",1))[0])
        conn2.send("not same")
    print "end"
    
s.close()


#Dishonesty by Bob: Not possible. When message sent by clients, its encypted with nonce. When replying, data displayed directly by server [encrypted as well, using clients' public keys.]
#Prone to attacks: 
#Privacy preserving:
#Information leakage: No leakage except for whether they are equal or not. All computations done on the server and messages sent by the clients encrypted and hashed, so no MITM, and no possible to read the message, just equate hash values.