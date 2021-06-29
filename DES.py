from DES_assets import *

class crypt():
    def __init__(self):
        self.text = None
        self.keys = list()

    def xorrer(self, t1, t2):
        return [x^y for x,y in zip(t1,t2)]
        
    def getDES(self, text):
        self.text = text
        self.getKeys()

        text_blocks = [self.text[k:k+16] for k in range(0, len(self.text), 16)]
        result = list()
        for block in text_blocks:
            binary_string = ""
            for ch in block:
                binary_string += bin_dict[ch]

            block = [int(x) for x in binary_string]
            block = [block[x-1] for x in PI]
            g, d = [block[k:k+32] for k in range(0, len(block), 32)]
            tmp = None
            for i in range(16):
                subbox = [d[x-1] for x in E]
                tmp = self.xorrer(self.keys[i], subbox)
                tmp = self.substitute(tmp)
                tmp = [tmp[x-1] for x in P]
                tmp = self.xorrer(g, tmp)
                g = d
                d = tmp
            
            inverted = d+g
            result += [inverted[x-1] for x in PI_1]

        return result
    
    def substitute(self, subbox):
        subblocks = [subbox[k:k+6] for k in range(0, len(subbox), 6)]
        result = list()
        for i in range(len(subblocks)):
            block = subblocks[i]
            row = int(str(block[0])+str(block[5]),2)
            column = int(''.join([str(x) for x in block[1:][:-1]]),2)
            val = S_BOX[i][row][column]
            bin = int_dict[str(val)]
            result += [int(x) for x in bin]
        return result
    
    def getKeys(self):
        self.keys = []
        key = masterkey
        key = [key[x-1] for x in CP_1]
        g, d = [key[k:k+28] for k in range(0, len(key), 28)]
        for i in range(16):
            g, d = g[SHIFT[i]:] + g[:SHIFT[i]], d[SHIFT[i]:] + d[:SHIFT[i]]
            tmp = g + d
            self.keys.append([tmp[x-1] for x in CP_2])
    
def calculateDES(text):
    d = crypt()
    r = d.getDES(text)
    
    binary_result = ""
    for x in r:
        binary_result += str(x)

    binary_result_list = [binary_result[k:k+4] for k in range(0, len(binary_result), 4)]
    hex_result = ""
    for part in binary_result_list:
        hex_result += hex_dict[part]

    return hex_result