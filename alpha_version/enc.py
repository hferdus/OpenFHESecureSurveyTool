import random
from openfhe import *
from math import log2
import os
import glob




def gen_plaintext(num_questions,num_people):
	
    	
	answer_choice = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
	answers = []
	for j in range(num_people):
		for i in range(num_questions):
			answer_in_answer = random.choice(answer_choice)
			answers.append(answer_in_answer)
	return answers

def partial_dec():

	serType = BINARY

	cc, res = DeserializeCryptoContext("/home/christopherjoseph/Downloads/alpha_version/client_stor/initial" + f"/cc.txt", serType)
	if not res:
            raise Exception(f"Could not read the crypto-context.")
            
	ciphertext, res = DeserializeCryptoContext("/home/christopherjoseph/Downloads/alpha_version/client_stor/computed" + f"/computed_ciphertext.txt", serType)
	if not res:
            raise Exception(f"Could not read the computed ciphertext.")
            
	sk1, res = DeserializeCryptoContext("/home/christopherjoseph/Downloads/alpha_version/client_stor/keys" + f"/sk1.txt", serType)
	if not res:
            raise Exception(f"Could not read the secret key 1.")
            
	sk2, res = DeserializeCryptoContext("/home/christopherjoseph/Downloads/alpha_version/client_stor/keys" + f"/sk2.txt", serType)
	if not res:
            raise Exception(f"Could not read the secret key 2.")
            
	
            
	ciphertextpartial1 = cc.MultipartyDecryptLead(ciphertext,sk1)
	ciphertextpartial2 = cc.MultipartyDecryptLead(ciphertext,sk2)
	
	partialCiphertextVec = [ciphertextpartial1[0],ciphertextpartial2[0]]
	
	plaintext = cc.MultipartyDecryptFusion(partialCiphertextVec)
	
	plaintext = Plaintext.GetPackedValue(plaintext)
	
	plaintext = plaintext[0]
		
	return plaintext
def gen_cc():

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
	
	return cc,kp1,kp2

def gen_plaintext(num_peple,num_questions):

	answer_choice = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
	answers = []
	answer_in_answer = []
	for j in range(num_peple):
		for i in range(num_questions):
			answer_in_answer.append(random.choice(answer_choice))
			answers.append(answer_in_answer)
			answer_in_answer = []
	return answers
	
def encrypt(plaintext,cc,key_pair):

	ct_list = []
	for i in plaintext:
		enc_plaintext = cc.MakePackedPlaintext(i)
		ct_list.append(cc.Encrypt(key_pair.publicKey,enc_plaintext))
	return ct_list
	
def serialize(cc,ciphertext,kp1sk,kp2pk,kp2sk):
	
	serType = BINARY
	
	datafolder = '/home/christopherjoseph/Downloads/alpha_version/client_stor/initial/'
	
	if not SerializeToFile(datafolder + f"/cc.txt", cc, serType):
            raise Exception(f"Error writing serialization of cc.txt")
      	
	for i in range(len(ciphertext)):
			if not SerializeToFile(datafolder + f"/ciphertext_{i}.txt", ciphertext[i], serType):
				raise Exception(f"Error writing serialization of ciphertext.txt")
				
	if not SerializeToFile(datafolder + f"/pk2.txt", kp2pk, serType):
		raise Exception(f"Error writing serialization of pk2.txt")
				
	datafolder = '/home/christopherjoseph/Downloads/alpha_version/client_stor/initial/'
        
	if not SerializeToFile(datafolder + f"/sk1.txt", kp1sk, serType):
            raise Exception(f"Error writing serialization of sk1.txt")
        
	if not SerializeToFile(datafolder + f"/sk2.txt", kp2sk, serType):
		raise Exception(f"Error writing serialization of sk2.txt")

def enc_action(num_people,num_questions):

	datafolder = ['/home/christopherjoseph/Downloads/alpha_version/client_stor/initial','/home/christopherjoseph/Downloads/alpha_version/client_stor/keys','/home/christopherjoseph/Downloads/alpha_version/client_stor/computed','/home/christopherjoseph/Downloads/alpha_version/client_stor/partial']
	
	for folder in datafolder:
		files = glob.glob(folder+"/*")
		for f in files:
    			os.remove(f)

	cc,kp1,kp2 = gen_cc()
	
	plaintext = gen_plaintext(num_people,num_questions)
	
	ciphertext = encrypt(plaintext,cc,kp2)
	
	serialize(cc,ciphertext,kp1.secretKey,kp2.publicKey,kp2.secretKey)

	

