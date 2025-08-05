from cryptography.fernet import Fernet
import os

# key=Fernet.generate_key()
# with open('key.key','wb') as key_file:
#     key_file.write(key)
def load_key():
    file=open('key.key','rb')
    key_=file.read()
    file.close()
    return key_


key=load_key()
fer=Fernet(key)
data=os.getcwd()+'/db'.encode()
enc=fer.encrypt(data)
print(enc)
