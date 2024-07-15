import random
from openfhe import *
import tempfile
import os


# Main Action
def tfhe_computer():


	print("-------Program Start-------")
	print(" ")
	while True:
		try:
			responses = int(input("How many user responses are to be averaged? : "))
			break
		except ValueError:
			print("Please enter a valid integer.")
	print(" ")
	
	datafolder = "/home/christopherjoseph/Downloads/survey_tool_beta_version/server_stor/generated/"
	
	serType = BINARY

	cc, res = DeserializeCryptoContext(datafolder + f"cc.txt", serType)
	if not res:
            raise Exception(f"Could not read the cc.txt")
        
	ct = []
	for i in range(responses):  
		holder, res = DeserializeCiphertext(datafolder + f"/ciphertext_{i}.txt", serType)
		ct.append(holder)
		if not res:
			raise Exception(f"Could not read the ciphertext.txt")
            
	pk2, res = DeserializePublicKey(datafolder + f"/pk2.txt", serType)
	if not res:
		raise Exception(f"Could not read the pk.txt")
	
	sum_r = cc.MakePackedPlaintext([0])
	sum_r = cc.Encrypt(pk2,sum_r)
	for i in range(len(ct)):
		sum_r = cc.EvalAdd(sum_r,ct[i])
	
	
	if not SerializeToFile("/home/christopherjoseph/Downloads/survey_tool_beta_version/server_stor/computed/" + f"computed_ciphertext.txt", sum_r, serType):
		raise Exception(f"Error writing serialization of computed ciphertext ciphertext.txt")	
		
	
	
	
def tfhe_decryptor(div_avg):

	serType = BINARY

	partial_ciphertext, res = DeserializeCiphertext("/home/christopherjoseph/Downloads/survey_tool_beta_version/server_stor/final/" + f"part.txt", serType)
	if not res:
        	raise Exception(f"Cound not read  the ciphertext.")

	cc, res = DeserializeCryptoContext("/home/christopherjoseph/Downloads/survey_tool_beta_version/server_stor/generated" + f"cc.txt", serType)
	if not res:
            raise Exception(f"Could not read the cc.txt")	
	
	
	plaintext = cc.MultipartyDecryptFusion(partial_ciphertext)
	
	plaintext = Plaintext.GetPackedValue(plaintext)
	
	plaintext = plaintext[0]
	
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
