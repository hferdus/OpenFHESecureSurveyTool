import random
from openfhe import *
from math import log2
import os
import glob

def dec():

	serType = JSON

	cc, res = DeserializeCryptoContext("/home/christopherjoseph/Downloads/test/server_stor" + f"/cc.json", serType)
	if not res:
            raise Exception(f"Could not read the cc.txt")
            
	ciphertext, res = DeserializeCryptoContext("/home/christopherjoseph/Downloads/test/server_stor" + f"/ciphertext.json", serType)
	if not res:
            raise Exception(f"Could not read the cc.txt")
            
	sk1, res = DeserializeCryptoContext("/home/christopherjoseph/Downloads/test/server_stor" + f"/sk1.json", serType)
	if not res:
            raise Exception(f"Could not read the cc.txt")
            
	sk2, res = DeserializeCryptoContext("/home/christopherjoseph/Downloads/test/server_stor" + f"/sk2.json", serType)
	if not res:
            raise Exception(f"Could not read the cc.txt")
            
	
            
	ciphertextpartial1 = cc.MultipartyDecryptLead(ciphertext,sk1)
	ciphertextpartial2 = cc.MultipartyDecryptLead(ciphertext,sk2)
	
	partialCiphertextVec = [ciphertextpartial1[0],ciphertextpartial2[0]]
	
	plaintext = cc.MultipartyDecryptFusion(partialCiphertextVec)
	
	plaintext = Plaintext.GetPackedValue(plaintext)
	
	plaintext = plaintext[0]
	
	return plaintext
        

def enc(sam_num):
	batchSize = 16
	
	files = glob.glob('/home/christopherjoseph/Downloads/test/client_stor/*')
	for f in files:
		os.remove(f)
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
	
	plaintext = [sam_num]
	
	enc_plaintext = cc.MakePackedPlaintext(plaintext)
	
	ciphertext = cc.Encrypt(kp2.publicKey,enc_plaintext)
	
	serType = JSON
	
	if not SerializeToFile("/home/christopherjoseph/Downloads/test/client_stor" + f"/ciphertext.json", ciphertext, serType):
				raise Exception(f"Error writing serialization of ciphertext.txt")
	if not SerializeToFile("/home/christopherjoseph/Downloads/test/client_stor" + f"/cc.json", cc, serType):
				raise Exception(f"Error writing serialization of ciphertext.txt")
				
	if not SerializeToFile("/home/christopherjoseph/Downloads/test/client_stor" + f"/sk1.json", kp1.secretKey, serType):
				raise Exception(f"Error writing serialization of ciphertext.txt")
	if not SerializeToFile("/home/christopherjoseph/Downloads/test/client_stor" + f"/sk2.json", kp2.secretKey, serType):
				raise Exception(f"Error writing serialization of ciphertext.txt")





