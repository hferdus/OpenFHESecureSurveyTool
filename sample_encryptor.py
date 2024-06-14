import random
from openfhe import *
import tempfile
import os


datafolder = "/home/christopherjoseph/Downloads/client_server/demoData"

# Generate the cryptocontext
def gen_cc(): 

	print(" ")
	print("This program requires the subdirectory `" + datafolder + "' to exist, otherwise you will get an error writing serializations.")
	print(" ")
	
	parameters = CCParamsBFVRNS()
	parameters.SetPlaintextModulus(65537)
	parameters.SetMultiplicativeDepth(2)
	
	cc = GenCryptoContext(parameters)
	
	cc.Enable(PKESchemeFeature.PKE)
	cc.Enable(PKESchemeFeature.KEYSWITCH)
	cc.Enable(PKESchemeFeature.LEVELEDSHE)
	
	key_pair = cc.KeyGen()
	
	cc.EvalMultKeyGen(key_pair.secretKey)
	
	return cc,key_pair
		
# Generate Plaintext
def gen_plaintext():
	
	num_questions = 10
	num_clients = 1
    	
	answer_choice = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
	answers = []
	answer_in_answer = []
	for i in range(num_questions):
		answer_in_answer.append(random.choice(answer_choice))
		answers.append(answer_in_answer)
		answer_in_answer = []
	return answers
	
# Encrypt the plain text
def encrypt(plaintext,cc,key_pair):
	ct_list = []
	for i in plaintext:
		enc_plaintext = cc.MakePackedPlaintext(i)
		ct_list.append(cc.Encrypt(key_pair.publicKey,enc_plaintext))
	return ct_list
	
# Serialize the ciphertext    
def serialize(datafolder,cc,ciphertext,pk,sk):
	
	serType = BINARY
	
	if not SerializeToFile(datafolder + f"/cc.txt", cc, serType):
            raise Exception(f"Error writing serialization of cc.txt")
      	
	for i in range(len(ciphertext)):
			if not SerializeToFile(datafolder + f"/ciphertext_{i}.txt", ciphertext[i], serType):
				raise Exception(f"Error writing serialization of ciphertext.txt")
        
	if not SerializeToFile(datafolder + f"/pk.txt", pk, serType):
            raise Exception(f"Error writing serialization of pk.txt")
        
	if not SerializeToFile(datafolder + f"/sk.txt", sk, serType):
            raise Exception(f"Error writing serialization of sk.txt")
        
# Main Action
def main_action():
	print("-------Program Start-------")
	
	
	
	cc,key_pair = gen_cc()
	plaintext = gen_plaintext()
	
	print(" ")
	print(f"Generated answers are : {plaintext}")

	ciphertext = encrypt(plaintext,cc,key_pair)

	serialize(datafolder,cc,ciphertext,key_pair.publicKey,key_pair.secretKey)
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
    
    
    
