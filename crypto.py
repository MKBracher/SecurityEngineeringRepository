from cryptography.fernet import Fernet

#Creating the key
# key = Fernet.generate_key()

# print (key)

# file = open('key.key', 'wb')
# file.write(key) #the key is type bytes
# file.close()

file = open('key.key', 'rb')
key = file.read() #the key is type bytes
file.close()
print(key)