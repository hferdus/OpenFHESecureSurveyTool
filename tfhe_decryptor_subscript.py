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
            

	sk1, res = DeserializePrivateKey(datafolder + f"/sk1.txt", serType)
	if not res:
		raise Exception(f"Could not read the sk.txt")

	pk2, res = DeserializePublicKey(datafolder + f"/pk2.txt", serType)
	if not res:
		raise Exception(f"Could not read the pk.txt")
		
	sk2, res = DeserializePrivateKey(datafolder + f"/sk2.txt", serType)
	if not res:
		raise Exception(f"Could not read the sk.txt")            
	
	return cc,ct,sk1,pk2,sk2
	
# Compute
def computes(cc,ct,pk):
	
	sum_r = cc.MakePackedPlaintext([0])
	sum_r = cc.Encrypt(pk,sum_r)
	for i in range(len(ct)):
		sum_r = cc.EvalAdd(sum_r,ct[i])
		
	div_avg = 1/len(ct)
	
	return sum_r,div_avg
	
# Decrypt
def decrypt(cc,sk1,sk2,computed_ciphertext):
	
	ciphertextpartial1 = cc.MultipartyDecryptLead([computed_ciphertext],sk1)
	ciphertextpartial2 = cc.MultipartyDecryptMain([computed_ciphertext],sk2)
	
	partialCiphertextVec = [ciphertextpartial1[0],ciphertextpartial2[0]]
	
	plaintext = cc.MultipartyDecryptFusion(partialCiphertextVec)
	
	plaintext = Plaintext.GetPackedValue(plaintext)
	
	plaintext = plaintext[0]
		
	return plaintext

# Main Action
def tfhe_decryptor_subscript():
	
	print("-------Program Start-------")
	print(" ")
	while True:
		try:
			responses = int(input("How many user responses are to be averaged? : "))
			break
		except ValueError:
			print("Please enter a valid integer.")
	print(" ")
	
	cc,ct,sk1,pk2,sk2 = deserialize('/home/christopherjoseph/Downloads/epsilon_version/serv_stor/',responses)
	
	computed_ciphertext,div_avg = computes(cc,ct,pk2)
	
	plaintext = decrypt(cc,sk1,sk2,computed_ciphertext)
	
	avg = plaintext*div_avg
	
	print(f"The average user response is {avg}.")
	
	print(" ")
	
	print("-------Program End-------")
	
def main():
    global datafolder
    with tempfile.TemporaryDirectory() as td:
        # datafolder = td + "/" + datafolder
        # os.mkdir(datafolder)
        tfhe_decryptor_subscript()
if __name__ == "__main__":
    main()
