import random
from openfhe import *
import tempfile
import os


#datafolder = "/home/christopherjoseph/Downloads/client_server/demoData"


	
# Deserialize the crypto-context, ciphertext, pk,sk
def deserialize(datafolder,responses):

	serType = BINARY

	cc, res = DeserializeCryptoContext(datafolder + f"/cc.txt", serType)
	if not res:
            raise Exception(f"Could not read the cc.txt")
        
	ct = []
	for i in range(responses):  
		holder, res = DeserializeCiphertext(datafolder + f"/ciphertext_{i}.txt", serType)
		ct.append(holder)
		if not res:
			raise Exception(f"Could not read the ciphertext.txt")
            
	pk, res = DeserializePublicKey(datafolder + f"/pk.txt", serType)
	if not res:
		raise Exception(f"Could not read the pk.txt")

	sk, res = DeserializePrivateKey(datafolder + f"/sk.txt", serType)
	if not res:
		raise Exception(f"Could not read the sk.txt")
                
	return cc,ct,pk,sk
	
# Compute
def computes(cc,ct,pk):
	
	sum_r = cc.MakePackedPlaintext([0])
	sum_r = cc.Encrypt(pk,sum_r)
	for i in range(len(ct)):
		sum_r = cc.EvalAdd(sum_r,ct[i])
		
	div_avg = 1/len(ct)
	
	return sum_r,div_avg
	
# Decrypt
def decrypt(cc,sk,computed_ciphertext):
	
	plaintext = cc.Decrypt(sk,computed_ciphertext)
	
	plaintext = Plaintext.GetPackedValue(plaintext)
	
	plaintext = plaintext[0]
		
	return plaintext

# Main Action
def main_action():
	
	print("-------Program Start-------")
	
	print(" ")
	datafolder = input("Please enter the path of your desired storage folder: ")
	print(" ")
	
	print(" ")
	responses = int(input("How many user responses are to be averaged? : "))
	print(" ")
	
	cc,ct,pk,sk = deserialize(datafolder,responses)
	
	computed_ciphertext,div_avg = computes(cc,ct,pk)
	
	plaintext = decrypt(cc,sk,computed_ciphertext)
	
	avg = plaintext*div_avg
	
	print(f"The average user response is {avg}.")
	
	print(" ")
	
	print("-------Program End-------")
	
def main():
    global datafolder
    with tempfile.TemporaryDirectory() as td:
        # datafolder = td + "/" + datafolder
        # os.mkdir(datafolder)
        main_action()

if __name__ == "__main__":
    main()
    
