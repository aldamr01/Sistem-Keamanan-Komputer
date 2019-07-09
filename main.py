import os, sys, time
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random


def Main():
    choice = input("Would you like to (E)ncrypt or (D)ecrypt?: ")
    if choice is 'E' or choice is 'e':
        filename = input("File to encrypt: ")
        password = input("Password: ")
        encrypt(getKey(password), filename)
        print("Done.")
    elif choice is 'D' or choice is 'd':
        filename = input("File to decrypt: ")
        password = input("Password: ")
        decrypt(getKey(password), filename)
        print("Done.")
    elif choice is 'C' or choice is 'c':
        print("Have a Nice Day.....")
        for i in range(1,4):
            print("."*i)
            time.sleep(1)
        sys.exit()

    else:
        print("No Option selected, closing…")
        Main()


#Encryption of files
def encrypt(key, filename):
    chunksize =64 * 1024
    outputFile = "ENC_" + filename
    filesize = str(os.path.getsize(filename)).zfill(16)
    IV = Random.new().read(16)
    encryptor = AES.new(key, AES.MODE_CBC, IV)

    with open(filename, 'rb') as infile:
        with open(outputFile, 'wb') as outfile:
            outfile.write(filesize.encode('utf-8'))
            outfile.write(IV)

            while True:
                chunk = infile.read(chunksize)

                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk +=b' ' * (16 - (len(chunk) % 16))
                    outfile.write(encryptor.encrypt(chunk))


#Decryption of files
def decrypt(key, filename):
    chunksize =64 * 1024
    outputFile = "DEC_" + filename

    with open(filename, 'rb') as infile:
        filesize = int(infile.read(16))
        IV = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, IV)

        with open(outputFile, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)

                if len(chunk) == 0:
                    break

                outfile.write(decryptor.decrypt(chunk))
                outfile.truncate(filesize)


def getKey(password):
    hasher = SHA256.new(password.encode('utf-8'))
    return hasher.digest()



if __name__ == '__main__':
    Main()