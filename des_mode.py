# coding=UTF-8
from des_main import *

#XOR
def xor(a, b):

    for i in range(len(a)):
        a[i] = int(a[i]) ^ int(b[i])
    return a

# ==================== ECB_mode ===========================
def ECB_mode(file, E_or_D):
    f = open('key.txt', 'r', encoding='utf-8')
    key = f.read()
    key = ascii_to_hex(key)
    if E_or_D == 'enc':
        d = open("./result/Cipher_output.txt", "w", encoding='utf-8')
        d.write('')
        with open(file, 'r', encoding='utf-8') as f:
            for text in iter(lambda: f.read(8), ''):
                text = ascii_to_hex(text.ljust(8,' '))
                cipherText = DES_func(key, text, 'enc')  
                d = open("./result/Cipher_output.txt", "a", encoding='utf-8')
                d.write(cipherText)
            d.close()
    elif E_or_D == 'dec':
        d = open("./result/Decrypt_output.txt", "w", encoding='utf-8')
        d.write('')
        with open(file, 'r', encoding='utf-8') as f:
            for text in iter(lambda: f.read(16), ''):
                plainText = DES_func(key, text, 'dec')
                plainText = hex_to_ascii(plainText)
                d = open("./result/Decrypt_output.txt", "a", encoding='utf-8')
                d.write(plainText)
        d.close()
# =========================================================

# ==================== CBC_mode ===========================
def CBC_mode(file, E_or_D):
    f = open('key.txt', 'r', encoding='utf-8')
    key = f.read()
    key = ascii_to_hex(key)
    IV = '0101010010101011101010000110110111010111110000101011010101000110'
    if E_or_D == 'enc':
        d = open("./result/Cipher_output.txt", "w", encoding='utf-8')
        d.write('')
        with open(file, 'r', encoding='utf-8') as f:
            temp = IV
            for text in iter(lambda: f.read(8), ''):
                iv_temp = temp
                text_temp = ascii_to_binary(text.ljust(8,' '))
                n_List = xor(list(text_temp), list(iv_temp))
                n = ''.join(str(x) for x in n_List) 
                text = binary_to_hex(n)
                cipherText = DES_func(key, text, 'enc')
                temp = hex_to_binary(cipherText)
                d = open("./result/Cipher_output.txt", "a", encoding='utf-8')
                d.write(cipherText)
        d.close()
    elif E_or_D == 'dec':
        temp = IV
        d = open("./result/Decrypt_output.txt", "w", encoding='utf-8')
        d.write('')
        with open(file, 'r', encoding='utf-8') as f:
            for text in iter(lambda: f.read(16), ''):
                n = DES_func(key, text, 'dec')
                n_temp = hex_to_binary(n)
                iv_temp = temp
                plainList = xor(list(iv_temp), list(n_temp))
                plainText = ''.join(str(x) for x in plainList) 
                plainText = binary_to_ascii(plainText)
                temp = hex_to_binary(text)
                d = open("./result/Decrypt_output.txt", "a", encoding='utf-8')
                d.write(plainText)
        d.close()
# =========================================================

# ==================== CFB_mode ===========================
def CFB_mode(file, E_or_D):
    f = open('key.txt', 'r', encoding='utf-8')
    key = f.read()
    key = ascii_to_hex(key)
    IV = '0101010010101011101010000110110111010111110000101011010101000110'
    if E_or_D == 'enc':
        d = open("./result/Cipher_output.txt", "w", encoding='utf-8')
        d.write('')
        with open(file, 'r', encoding='utf-8') as f:
            iv_enc = binary_to_hex(IV)
            for text in iter(lambda: f.read(8), ''):
                iv_enc = DES_func(key, iv_enc, 'enc')
                iv_temp = hex_to_binary(iv_enc)
                text_temp = ascii_to_binary(text.ljust(8,' '))
                cipherList = xor(list(text_temp), list(iv_temp))
                cipherText = ''.join(str(x) for x in cipherList) 
                cipherText = binary_to_hex(cipherText)
                iv_enc = cipherText
                d = open("./result/Cipher_output.txt", "a", encoding='utf-8')
                d.write(cipherText)
        d.close()
    elif E_or_D == 'dec':
        d = open("./result/Decrypt_output.txt", "w", encoding='utf-8')
        d.write('')
        with open(file, 'r', encoding='utf-8') as f:
            iv_enc = binary_to_hex(IV)
            for text in iter(lambda: f.read(16), ''):
                iv_enc = DES_func(key, iv_enc, 'enc')
                iv_temp = hex_to_binary(iv_enc)
                text_temp = hex_to_binary(text)
                plainList = xor(list(text_temp), list(iv_temp))
                plainText = ''.join(str(x) for x in plainList) 
                plainText = binary_to_ascii(plainText)
                iv_enc = text
                d = open("./result/Decrypt_output.txt", "a", encoding='utf-8')
                d.write(plainText)
        d.close()
# =========================================================

# ==================== OFB_mode ===========================        
def OFB_mode(file, E_or_D):
    f = open('key.txt', 'r', encoding='utf-8')
    key = f.read()
    key = ascii_to_hex(key)
    IV = '0101010010101011101010000110110111010111110000101011010101000110'
    if E_or_D == 'enc':
        d = open("./result/Cipher_output.txt", "w", encoding='utf-8')
        d.write('')
        with open(file, 'r', encoding='utf-8') as f:
            iv_enc = binary_to_hex(IV)
            for text in iter(lambda: f.read(8), ''):
                iv_enc = DES_func(key, iv_enc, 'enc')
                iv_temp = hex_to_binary(iv_enc)
                text_temp = ascii_to_binary(text.ljust(8,' '))
                cipherList = xor(list(text_temp), list(iv_temp))
                cipherText = ''.join(str(x) for x in cipherList) 
                cipherText = binary_to_hex(cipherText)
                d = open("./result/Cipher_output.txt", "a", encoding='utf-8')
                d.write(cipherText)
        d.close()
    elif E_or_D == 'dec':
        d = open("./result/Decrypt_output.txt", "w", encoding='utf-8')
        d.write('')
        with open(file, 'r', encoding='utf-8') as f:
            iv_enc = binary_to_hex(IV)
            for text in iter(lambda: f.read(16), ''):
                iv_enc = DES_func(key, iv_enc, 'enc')
                iv_temp = hex_to_binary(iv_enc)
                text_temp = hex_to_binary(text)
                plainList = xor(list(text_temp), list(iv_temp))
                plainText = ''.join(str(x) for x in plainList) 
                plainText = binary_to_ascii(plainText)
                d = open("./result/Decrypt_output.txt", "a", encoding='utf-8')
                d.write(plainText)
        d.close()
# =========================================================

# ==================== CTR_mode ===========================        
def CTR_mode(file, E_or_D):
    f = open('key.txt', 'r', encoding='utf-8')
    key = f.read()
    key = ascii_to_hex(key)
    if E_or_D == 'enc':
        counter = '0000000000000000'
        d = open("./result/Cipher_output.txt", "w", encoding='utf-8')
        d.write('')
        with open(file, 'r', encoding='utf-8') as f:
            for text in iter(lambda: f.read(8), ''):
                temp = DES_func(key, counter, 'enc')
                counter = int(counter, 16) + 1
                counter = hex(counter)[2:].zfill(16)
                n_temp = hex_to_binary(temp)
                text_temp = ascii_to_binary(text.ljust(8,' '))
                cipherList = xor(list(n_temp), list(text_temp))
                cipherText = ''.join(str(x) for x in cipherList) 
                cipherText = binary_to_hex(cipherText)
                d = open("./result/Cipher_output.txt", "a", encoding='utf-8')
                d.write(cipherText)
        d.close()
    elif E_or_D == 'dec':
        counter = '0000000000000000'
        d = open("./result/Decrypt_outputs.txt", "w", encoding='utf-8')
        d.write('')
        with open(file, 'r', encoding='utf-8') as f:
            for text in iter(lambda: f.read(16), ''):
                temp = DES_func(key, counter, 'enc')
                counter = int(counter, 16) + 1
                counter = hex(counter)[2:].zfill(16)
                n_temp = hex_to_binary(temp)
                text_temp = hex_to_binary(text)
                plainList = xor(list(n_temp), list(text_temp))
                plainText = ''.join(str(x) for x in plainList) 
                plainText = binary_to_hex(plainText)
                d = open("./result/Decrypt_output.txt", "a", encoding='utf-8')
                d.write(plainText)
        d.close()
# =========================================================

# ==================== mode選擇導向器 ======================
def DES(file, E_or_D,mode):
    if mode == 'ECB':
        ECB_mode(file, E_or_D)
    elif mode == 'CBC':
        CBC_mode(file, E_or_D)
    elif mode == 'CFB':
        CFB_mode(file, E_or_D)
    elif mode == 'OFB':
        OFB_mode(file, E_or_D)
    elif mode == 'CTR':
        CTR_mode(file, E_or_D)
    else:
        print('請輸入一個正確的MODE')
# =========================================================