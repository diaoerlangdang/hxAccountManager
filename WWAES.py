#AES加解密
"""
    @author: wise

    @file: WWAES.py

    @time: 2018/03/19

    @desc: AES加解密
"""


from Cryptodome.Cipher import AES
import base64
import json

'''
    将二进制数据转换为16进制显示的字符串
    bins  类型（bytes） 二进制数据
'''
def byte2hex( bins ):

    return ''.join( [ "%02X" % x for x in bins ] ).strip()


'''
    将16进制显示的字符串转换为二进制数据
    hexStr  类型（str） 16进制显示的字符串
'''
def hex2byte( hexStr ):

    return bytes.fromhex(hexStr)


'''
    PKCS7 补齐方式  
    text  类型（bytes）  二进制数据（bytes）
    block_len 类型（int）数据块长度
'''
def pad_pkcs7(text,block_len=16):   

    count=len(text) 

    mod_num=count%block_len

    add_num=block_len-mod_num

    return text+(chr(add_num)*add_num).encode('utf-8')    

'''
    PKCS7 去除补齐方式
    text  类型（bytes）  二进制数据（bytes）
    block_len 类型（int）数据块长度
'''
def unpad_pkcs7(text,block_len=16):

    lastLen = text[-1]
    #lastChar=text[-1] 
    #lastLen=ord(lastChar)

    return text[:-lastLen]



'''
    aes 128 加密 ECB模式
    key 类型（bytes） 要求长度为16
    plain_text 字符串 明文数据

    return 密文数据 16进制字符串
'''
def aes128_encrypt(key, plain_text):

    #明文数据或者密钥为空
    if not plain_text or len(key) != 16 :
        return b''
        pass

    #进行加密算法，模式ECB模式，把叠加完16位的秘钥传进来
    aes = AES.new(key, AES.MODE_ECB)

    #加密内容,此处需要将字符串转为字节
    text = plain_text.encode(encoding="utf-8")

    #进行内容拼接16位字符后传入加密类中，结果为字节类型
    encrypted_text = aes.encrypt(pad_pkcs7(text))

    #return byte2hex(encrypted_text)

    return str(base64.b64encode(encrypted_text), encoding='utf-8')

    pass

'''
    aes 128 加密 ECB模式
    key 类型（bytes） 要求长度为16
    encrypted_text 字符串 密文数据（16进制字符串）
'''
def aes128_decrypt(key, encrypted_text):
    #密文数据或者密钥为空
    if not encrypted_text or len(key) != 16 :
        return b''
        pass

    #进行加密算法，模式ECB模式，把叠加完16位的秘钥传进来
    aes = AES.new(key, AES.MODE_ECB)

    text = unpad_pkcs7(aes.decrypt(base64.b64decode(encrypted_text.encode('utf-8'))))

    return str(text, encoding='utf-8')
    pass




