from openfhe import *



def deserialize(datafolder):

	serType = BINARY

	cc, res = DeserializeCryptoContext(datafolder + f"/cc.txt", serType)
	if not res:
            raise Exception(f"Could not read the cc.txt")
        
	ct = []
	for i in range(10):  
		holder, res = DeserializeCiphertext(datafolder + f"/ciphertext_{i}.txt", serType)
		ct.append(holder)
		if not res:
			raise Exception(f"Could not read the ciphertext.txt")
	
	pk2, res = DeserializePublicKey(datafolder + f"/pk2.txt", serType)
	if not res:
		raise Exception(f"Could not read the pk.txt")
		
	return cc,ct,pk2

def computes(cc,ct,pk):
	
	sum_r = cc.MakePackedPlaintext([0])
	sum_r = cc.Encrypt(pk,sum_r)
	for i in range(len(ct)):
		sum_r = cc.EvalAdd(sum_r,ct[i])
		
	div_avg = 1/len(ct)
	
	return sum_r,div_avg
	
def serialize(ct):

	datafolder = '/home/christopherjoseph/Downloads/alpha_version/server_stor/computed'
	
	serType = BINARY
	if not SerializeToFile(datafolder + f"/computed_ciphertext.txt", ct, serType):
            raise Exception(f"Error writing serialization of cc.txt")
	

def comp_action(datafolder):

	cc,ct,pk2 = deserialize(datafolder)
	
	sum_r,div_avg = computes(cc,ct,pk2)
	
	serialize(sum_r)
	
	return div_avg
	
	
	

