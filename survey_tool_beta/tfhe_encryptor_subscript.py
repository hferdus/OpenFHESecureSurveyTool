import random
from openfhe import *
import tempfile
import os
import glob
from math import log2
import struct

#datafolder = "/home/christopherjoseph/Downloads/client_server/demoData"



# Generate the cryptocontext
def gen_cc(datafolder): 

	print(" ")
	print("This program requires the subdirectory `" + datafolder + "' to exist, otherwise you will get an error writing serializations.")
	print(" ")
	
	batchSize = 16
	
	parameters = CCParamsBFVRNS()
	parameters.SetPlaintextModulus(65537)
	parameters.SetBatchSize(batchSize)
	parameters.SetMultiplicativeDepth
	
	## NOISE_FLOODING_MULTIPARTY adds extra noise to the ciphertext before decrypting and is most secure mode of threshold FHE for BFV and BGV.
    	
	parameters.SetMultipartyMode(NOISE_FLOODING_MULTIPARTY)
    	
	cc = GenCryptoContext(parameters)
	cc.Enable(PKE)
	cc.Enable(KEYSWITCH)
	cc.Enable(LEVELEDSHE)
	cc.Enable(ADVANCEDSHE)
	cc.Enable(MULTIPARTY)
    	
    	##########################################################
    	# Set-up of parameters
    	##########################################################
    	
    	# Output of the generated parameters 
	print(f"p = {cc.GetPlaintextModulus()}")
	print(f"n = {cc.GetCyclotomicOrder()/2}")
	print(f"lo2 q = {log2(cc.GetModulus())}")
    	
    	############################################################
    	# Perform Key Generation Operation
    	############################################################
    	
	print("\n Running key generation (used for source data) ...\n")
    	
    	## Round 1 (Party A)
    	
	kp1 = cc.KeyGen()
	
	# Generate evalsum key part for A
	
	cc.EvalSumKeyGen(kp1.secretKey)
	evalSumKeys = cc.GetEvalSumKeyMap(kp1.secretKey.GetKeyTag())
	
	## Round 2 (Party B)
	
	kp2 = cc.MultipartyKeyGen(kp1.publicKey)
	
	evalSumKeysB = cc.MultiEvalSumKeyGen(kp2.secretKey, evalSumKeys, kp2.publicKey.GetKeyTag())
	
	evalSumKeysJoin = cc.MultiAddEvalSumKeys(evalSumKeys, evalSumKeysB, kp2.publicKey.GetKeyTag())
	
	cc.InsertEvalSumKey(evalSumKeysJoin)
	
	print("\n Key generation has ended. \n")
	
	return cc,kp1,kp2
	
		
# Generate Plaintext
def gen_plaintext(num_questions,num_peple):
	
    	
	answer_choice = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
	answers = []
	answer_in_answer = []
	for j in range(num_peple):
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
def serialize(datafolder,cc,ciphertext,kp1sk,kp2pk,kp2sk):
	
	
	serType = BINARY
	
	if not SerializeToFile(datafolder + f"/cc.txt", cc, serType):
            raise Exception(f"Error writing serialization of cc.txt")
      	
	for i in range(len(ciphertext)):
		if not SerializeToFile(datafolder + f"/ciphertext_{i}.txt", ciphertext[i], serType):
			raise Exception(f"Error writing serialization of ciphertext.txt")
        
	if not SerializeToFile("/home/christopherjoseph/Downloads/survey_tool_beta_version/client_stor/keys/" + f"/sk1.txt", kp1sk, serType):
            raise Exception(f"Error writing serialization of sk1.txt")
        
	if not SerializeToFile(datafolder + f"/pk2.txt", kp2pk, serType):
		raise Exception(f"Error writing serialization of pk2.txt")
            
	if not SerializeToFile("/home/christopherjoseph/Downloads/survey_tool_beta_version/client_stor/keys/" + f"/sk2.txt", kp2sk, serType):
		raise Exception(f"Error writing serialization of sk2.txt")
# Main Action
def main_encryption():
	print("-------Program Start-------")
	
	datafolder = "/home/christopherjoseph/Downloads/survey_tool_beta_version/client_stor/initial/"
	
	# Deleting pre-existing files in the storage folder
	files = glob.glob(datafolder+"/*")
	for f in files:
    		os.remove(f)
	
	print(" ")
	
	# Validating user input as integers
	while True:
		try:
			num_questions = int(input("How many questions do you want to be simulated?: "))
			break
		except ValueError:
			print("Please input valid integers.")
			
	while True:
		try:
			num_peple = int(input("How many people do you want to respond to your question?: "))
			break
		except ValueError:
			print("Please input valid integers.")
	print(" ")
	
	
	cc,kp1,kp2 = gen_cc(datafolder)
	plaintext = gen_plaintext(num_questions,num_peple)
	
	print(" ")
	print(f"Generated answers are : {plaintext}")

	ciphertext = encrypt(plaintext,cc,kp2)

	serialize(datafolder,cc,ciphertext,kp1.secretKey,kp2.publicKey,kp2.secretKey)

	
	print(" ")
	print("-------Program End-------")
	
def partial_decrypt(no_resp):

	serType = BINARY
	
	sk1, res = DeserializePrivateKey("/home/christopherjoseph/Downloads/survey_tool_beta_version/client_stor/keys" + f"/sk1.txt", serType)
	if not res:
		raise Exception(f"Could not read the sk.txt")
		
	sk2, res = DeserializePrivateKey("/home/christopherjoseph/Downloads/survey_tool_beta_version/client_stor/keys" + f"/sk2.txt", serType)
	if not res:
		raise Exception(f"Could not read the sk.txt")
		
	cc, res = DeserializeCryptoContext("/home/christopherjoseph/Downloads/survey_tool_beta_version/client_stor/initial" + f"/cc.txt", serType)
	if not res:
        	raise Exception(f"Could not read the cc.txt")
            
	computed_ciphertext, res = DeserializeCiphertext("/home/christopherjoseph/Downloads/survey_tool_beta_version/client_stor/computed/" + f"computed_ciphertext.txt", serType)
	if not res:
        	raise Exception(f"Cound not read  the ciphertext.")
            
	ciphertextpartial1 = cc.MultipartyDecryptLead([computed_ciphertext],sk1)
	ciphertextpartial2 = cc.MultipartyDecryptMain([computed_ciphertext],sk2)
	
	partialCiphertextVec = [ciphertextpartial1[0],ciphertextpartial2[0]]	
	
	plaintext = cc.MultipartyDecryptFusion(partialCiphertextVec)
	
	plaintext = Plaintext.GetPackedValue(plaintext)
	
	plaintext = plaintext[0]

	no_resp = 1/(no_resp)
	
	avg = plaintext*(no_resp)
	
	avg = bytearray(struct.pack("f",avg))
	
	with open('/home/christopherjoseph/Downloads/survey_tool_beta_version/client_stor/final/partial.txt','wb') as f:
			f.write(avg)
	
	#if not SerializeToFile("/home/christopherjoseph/Downloads/survey_tool_beta_version/client_stor/partial/" + f"part.txt", partialCiphertextVec, serType):
		#raise Exception(f"Error writing serialization of ciphertext.txt")

 
def main():
    global datafolder
    with tempfile.TemporaryDirectory() as td:
        # datafolder = td + "/" + datafolder
        # os.mkdir(datafolder)
        main_action()
      
if __name__ == "__main__":
    main()