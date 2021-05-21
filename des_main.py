# coding=UTF-8

import AllTable as at

# ======================== 編碼轉換 =============================
def ascii_to_binary(ascii):
    temp = [bin(ord(x))[2:].zfill(8) for x in ascii]
    ans = ''
    for i in temp:
        ans += i[:8]
    return ans

def binary_to_ascii(binary):
    temp = []
    for i in range(8):
        temp.append(binary[i*8:i*8+8])
    ans = ''.join([chr(int(x, 2)) for x in temp])
    return ans

def binary_to_hex(binary):
    ans = hex(int(binary, 2))[2:].zfill(16)
    return ans

def hex_to_binary(hexnum):
    temp = []
    for x in hexnum:
        x = bin(int(x, 16)).split('b')[1].zfill(4)
        temp.append(x)
    ans = ''.join(str(x) for x in temp)
    return ans

def ascii_to_hex(ascii):
    temp = ascii_to_binary(ascii)
    ans = binary_to_hex(temp)
    return ans

def hex_to_ascii(hexnum):
    temp = hex_to_binary(hexnum)
    ans = binary_to_ascii(temp)
    return ans
    
# =================================================================

# ======================== 常用函數 ===============================
#代換
def substitution(source, table):
    source_trans = []
    for x in table:
        source_trans.append(source[x-1])
    return source_trans

#左移
def left_shift(key, i): # i（第幾輪）
    st = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1] #shift_table
    temp = []
    temp = key[:st[i]]
    key = key[st[i]:]
    for x in temp:
        key.append(x)
    return key

#XOR
def xor(a, b):
    for i in range(len(a)):
        a[i] = int(a[i]) ^ int(b[i])
    return a
# =================================================================

# ======================== 主函式 =================================
def DES_func(ascii_key, ascii_text, E_or_D):

    # ------------ 對字串做轉碼處理 -------------
    key = hex_to_binary(ascii_key)
    text = hex_to_binary(ascii_text)
    # -------------------------------------------

    # ------------ 以下開始準備subkey -----------
    #pc1置換    
    key = substitution(key, at.pc1)
    #左右切割
    c = key[:28]
    d = key[28:]
    subkey_list = []
    for i in range(16):
        #向左平移
        c = left_shift(c, i)
        d = left_shift(d, i)
        subkey = c + d
        subkey = substitution(subkey, at.pc2)
        subkey_list.append(subkey)
    # ------------------------------------------

    # ------------ 以下開始加密  ---------------
    #ip轉換
    text = substitution(text, at.ip)
    #左右拆分
    l = text[:32]
    r = text[32:]
    for x in range(16):
        tempR = r
        #EBOX轉換
        r = substitution(r, at.E)
        #XOR Key
        if(E_or_D == 'enc'):
            r = xor(r, subkey_list[x])
        elif(E_or_D == 'dec'):
            r = xor(r, subkey_list[15-x])
        #SBOX轉換
        for i in range(8):
            temp = r[i*6:i*6+6]
            row = temp[0]*2 + temp[5]
            colum = temp[1]*8 + temp[2]*4 + temp[3]*2 + temp[4]
            if(i == 0): ans1 = bin(at.S1[row][colum]).split('b')[1].zfill(4)
            elif(i == 1): ans2 = bin(at.S2[row][colum]).split('b')[1].zfill(4)
            elif(i == 2): ans3 = bin(at.S3[row][colum]).split('b')[1].zfill(4)
            elif(i == 3): ans4 = bin(at.S4[row][colum]).split('b')[1].zfill(4)
            elif(i == 4): ans5 = bin(at.S5[row][colum]).split('b')[1].zfill(4)
            elif(i == 5): ans6 = bin(at.S6[row][colum]).split('b')[1].zfill(4)
            elif(i == 6): ans7 = bin(at.S7[row][colum]).split('b')[1].zfill(4)
            elif(i == 7): ans8 = bin(at.S8[row][colum]).split('b')[1].zfill(4) 
        r = ans1 + ans2 + ans3 + ans4 + ans5 + ans6 + ans7 + ans8
        #PBOX轉換
        r = substitution(r, at.P)
        #XOR l
        r = xor(r, l)
        for i in range(32):
            l[i] = int(tempR[i])
    l, r = r, l
    text = l + r

    #ip-1轉換
    text = substitution(text, at.ipRe)
    final_text = ''.join(str(x) for x in text)
    
    returnText = binary_to_hex(final_text)
    return(returnText)