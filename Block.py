import time
import hashlib
from DES import *

class Block:
    previousHash = ""
    blockHash = ""
    timestamp = None
    curr_med_data = None
    nonce = 0

    def __init__(self, prev, data):
        self.previousHash = prev
        self.curr_med_data = data
        self.timestamp = time.time()
        self.blockHash = self.calculateHash()

    def calculateHash(self):
        hash_comp = str(self.previousHash) + str(self.nonce)
        calculatedHash = calculateDES(hashlib.sha256(hash_comp.encode()).hexdigest())
        return calculatedHash
        
    def mineBlock(self, difficulty):
        target = "0"*difficulty
        
        while(self.blockHash[:difficulty] != target):
            self.nonce += 1
            self.blockHash = self.calculateHash()
        print("Block mined!!! : " + self.blockHash)

    def getBlockHash(self):
        return self.blockHash

    def getPreviousHash(self):
        return self.previousHash

    def getbrokerName(self):
        return self.curr_med_data.broker
    
    def getclientName(self):
        return self.curr_med_data.client

    def printData(self):
        self.curr_med_data.printData()

    def setBlockHash(self, hash):
        self.blockHash = hash
    
    def setTimestamp(self, ts):
        self.timestamp = ts

    def setNonce(self, n):
        self.nonce = n