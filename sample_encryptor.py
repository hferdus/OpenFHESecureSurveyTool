from openfhe import *

import requests
import json
import pandas as pd

# Assuming we use an Excel file or an online json file to store user data
url = "url"

user_data = requests.get(url).text

data_json = json.loads(user_data)

user_df = pd.read_json(data_json)

rows = len(df.axes[0])
cols = len(df.axes[1])

# Setting Cryptocontext

parameters = CCParamsBFVRNS()
parameters.SetPlaintextModulus(65537)
parameters.SetMultiplicativeDepth(2)
crypto_context = GenCryptoContext(parameters)

# Enabling Features

crypto_context.Enable(PKESchemeFeature.PKE)
crypto_context.Enable(PKESchemeFeature.KEYSWITCH)
crypto_context.Enable(PKESchemeFeature.LEVELEDSHE)

# Generating key pair

key_pair = crypto_context.KeyGen()

# Generating Relinearization Key

crypto_context.EvalMultKeyGen(key_pair.secretKey)

# Obtaining Input

user_list = df.tolist()
		

# Encoding payload

plaintext1 = crypto_context.MakePackedPlaintext(user_list)


# Encryption

ciphertext1 = crypto_context.Encrypt(key_pair.publicKey,plaintext1)






