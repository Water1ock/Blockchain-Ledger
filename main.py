from User import *
from Record import *
from DES import *
from Block import *
import random as rand

# Inits
blockchain = []
records = []
brokers = []
users = []

difficulty = 2 # Here difficulty is based on a 64 bit hex hash
p = 11
g = 2
prevH = None # Init after loading files in main

def addRecordToBlock(previousHash, data):
    print("Mining Block. Please Wait.")

    block = Block(previousHash, data)

    block.mineBlock(difficulty)
    if (verifyChain(block)):
        blockchain.append(block)

        f = open("blockchain.txt", "a")
        data = str(block.previousHash) + " " + str(block.blockHash) + " " + str(block.timestamp) + " " + str(len(records)-1) + " " + str(block.nonce) + "\n"
        f.write(data)
        f.close()
    else:
        print("Could not verify block. Block not appended")
    
    return block.getBlockHash()

def verifyChain(block):
    for i in range(len(blockchain)):
        if i == 0:
            continue
        else:
            if(blockchain[i].getPreviousHash() !=  blockchain[i-1].getBlockHash()):
                return False
    return True

def exp(a, b, c):
    ans = 1
    for i in range(b):
        ans = ((ans % c) * (a % c)) % c
    
    return ans
    
def ZKP(y1):
    y1 = exp(2, y1, 11)
    print("--------------------------------------")
    print("Zero Knowledge Proof -- Verify Yourself")
    print("--------------------------------------")
    h = int(input("Choose a random r [0-9] and computer [2^r mod 11]: "))
    b = rand.randint(0, 1)
    print("Random bit assigned is " + str(b))
    if b==0:
        print("Please compute [r]: ", end='')
    else:
        print("Please compute [(x+r) mod 10]: ", end='')
    s = int(input())

    if b==0:
        val1 = exp(2, s, 11)
        if (val1==h):
            print("ZKP passed. Verified User")
            print("--------------------------------------")
            return True
        else:
            print("ZKP failed. Please try again")
            print("--------------------------------------")
            return False
    else:
        val1 = exp(2, s, 11)
        val2 = (h*y1)%11
        if (val1 == val2):
            print("ZKP passed. Verified User")
            print("--------------------------------------")
            return True
        else:
            print("ZKP failed. Please try again")
            print("--------------------------------------")
            return False

def loadBrokers():
    f = open("brokers.txt", "r").read().split("\n")

    for doc in f:
        dat = doc.split()
        if len(dat) == 2:
            brokers.append(User(dat[0], dat[1]))

def loadUsers():
    f = open("users.txt", "r").read().split("\n")

    for usr in f:
        dat = usr.split()
        if len(dat) == 2:
            users.append(User(dat[0], dat[1]))

def loadRecords():
    f = open("records.txt", "r").read().split("\n")
    i = 0
    while i < len(f)-1:
        dat = f[i].split()
        if len(dat) == 3:
            doc = dat[0]
            pat = dat[1]
            med_dat = []
            
            for k in range(int(dat[2])):
                i += 1
                med_dat.append(f[i])
            i += 1
            tmp = Record(doc, pat)
            tmp.setData(med_dat)
            records.append(tmp)

def loadBlockchain():
    f = open("blockchain.txt", "r").read().split("\n")

    for block in f:
        dat = block.split()
        if len(dat) == 5:
            phash = dat[0]
            bhash = dat[1]
            tstamp = dat[2]
            mdata = records[int(dat[3])]
            nonce = dat[4]

            tmp = Block(phash, mdata)
            tmp.setBlockHash(bhash)
            tmp.setTimestamp(tstamp)
            tmp.setNonce(nonce)
            blockchain.append(tmp)

if __name__ == "__main__":

    loadBrokers()
    loadUsers()
    loadRecords()
    loadBlockchain()

    if(len(blockchain) > 0):
        prevH = blockchain[-1].getBlockHash()
    else:
        prevH = 0

    # Main Loop
    user_choice = "Yes"

    while(user_choice == "Yes" or user_choice == "yes"):
        try:
            print("--------------------------------------")
            print("1. View Client Details")
            print("2. Add Trading Record for Client")
            print("3. Register A New Client")
            print("--------------------------------------")

            user_option = input()
            
            if (user_option == "3"):
                new_name = input("Enter Name: ")
                new_pass = int(input("Enter Password: "))
                new_user = User(new_name, new_pass)
                users.append(new_user)

                f = open("users.txt", "a")
                data = new_name + " " + str(new_pass) + "\n"
                f.write(data)
                f.close()

            elif(user_option == "2"):
                doc_name = input("Enter Broker Name: ")
                doc_pass = int(input("Enter your Password: "))
                pat_name = input("Enter your Client's Name: ")

                y = 0
                for usr in users:
                    if usr.getName() == pat_name:
                        y = int(usr.getPass())
                        break
                    
                if(not ZKP(y)):
                    continue

                for doc in brokers:
                    if doc.getName() == doc_name and int(doc.getPass()) == int(doc_pass):
                        for usr in users:
                            if usr.getName() == pat_name:
                                rec = Record(doc_name, pat_name)

                                if(len(rec.data) != 0):
                                    rec.data = []

                                while True:
                                    med_data = input("Enter Trade Details:")
                                    rec.addData(med_data)

                                    choice = input("Enter Additional Data? (Y/N): ")

                                    if(choice == "N" or choice == "n"):
                                        records.append(rec)

                                        f = open("records.txt", "a")
                                        data = rec.broker + " " + rec.client + " " + str(len(rec.data))
                                        f.write(data + "\n")
                                        for s in rec.data:
                                            f.write(s + "\n")
                                        f.close()

                                        prevH = addRecordToBlock(prevH, rec)
                                        break
            elif (user_option == "1"):
                print("--------------------------------------")
                print("1. Broker")
                print("2. Client")
                value = int(input())
                print("--------------------------------------")
                
                if (value == 1):
                    broker = input("Enter your name: ")
                    password = input("Enter your password:")
                    flag1 = 0
                    for i in range(len(brokers)):
                        if (brokers[i].getName() == broker and brokers[i].getPass() == password):
                            for j in range(len(blockchain)):
                                if (blockchain[j].getbrokerName() == broker):
                                    print("--------------------------------------")
                                    print("Time:" + str(blockchain[j].timestamp))
                                    print("Broker: " + broker)
                                    print("Client:" + blockchain[j].getclientName())
                                    print("Trading Data:")
                                    blockchain[j].printData()
                                    print("--------------------------------------")
                                    flag1 = 1
                            if (flag1 == 1):
                                break
                    if (flag1 == 0):
                        print("Broker not found")

                elif (value == 2):
                    client = input("Enter your name: ")
                    y = 0
                    for j in range(len(users)):
                        if users[j].getName() == client:
                            y = int(users[j].getPass())
                    
                    if (not ZKP(y)):
                        continue

                    flag2 = 0
                    for i in range(len(users)):
                        if (users[i].getName() == client):
                            for k in range(len(blockchain)):
                                if (blockchain[k].getclientName() == client):
                                    print("--------------------------------------")
                                    print("Time:" + str(blockchain[k].timestamp))
                                    print("Broker: " + blockchain[k].getbrokerName())
                                    print("Client: " + blockchain[k].getclientName())
                                    print("Client's Trading Data: ")
                                    blockchain[k].printData()
                                    print("--------------------------------------")
                                    flag2 = 1
                            if (flag2 == 1):
                                break
                    if (flag2 == 0):
                        print("No record for Client found")

                else:
                    print("Invalid")
            user_choice = input("Do you want to continue? [Yes/No]: ")
        except KeyboardInterrupt:
            quit()
        except:
            print("An error occurred. Please try again.")