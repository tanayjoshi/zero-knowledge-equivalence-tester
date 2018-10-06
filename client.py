
import socket   #for sockets
import sys  #for exit
#from paillier.paillier import *
import json
import Crypto
from Crypto.PublicKey import RSA
from Crypto.Hash import MD5

#create an INET, STREAMing socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()
     
print 'Socket Created'
 
host = 'localhost';
port = 8888;

#import the public key of the server
f = open('mykey.pem','r')
key = RSA.importKey(f.read())

#generate RSA keypair
mykey = RSA.generate(2048)
#generate a separate public key for others to use
pub = mykey.publickey()

#export this public key to a file for others to use
f = open('cl1key.pem','w')
f.write(pub.exportKey('PEM'))
f.close()

try:
    remote_ip = socket.gethostbyname( host )
 
except socket.gaierror:
    #could not resolve
    print 'Hostname could not be resolved. Exiting'
    sys.exit()
 
#Connect to remote server
s.connect((remote_ip , port))
 
print 'Socket Connected to ' + host + ' on ip ' + remote_ip
 
#receive the nonce from server
d = s.recv(4096)
e = long(d)

#create a new hash and update it to your own value (here, 5)
h = MD5.new()
h.update(b'5')
#get the digest of the hash
g = h.digest()
#encrypt the product of digest and nonce
x = key.encrypt(((g*e)), 1)

y = (x[0])
try :
    #Set the ciphertext
    s.sendall((y))
except socket.error:
    #Send failed
    print 'Send failed'
    sys.exit()
 
print 'Message send successfully'
 
#Now receive data
reply = s.recv(4096)
#print reply
print (reply)
