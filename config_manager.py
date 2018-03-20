#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
Created on 2018-3-16

@author: wise
'''

#配置文件解析库
import configparser
import json
import WWAES

HX_SOFT_CONFIG_FILE = 'config.ini'

data = {
	'hx_app_key' : '环信app_key',
	'hx_client_id' : '环信的client_id',
	'hx_client_secret' : '环信的client_secret',
	#环信用户名前缀，major_key为’id‘, hx_prefix为’test‘, 则对应环信用户为'test'+(id的值)
	'hx_prefix' : 'test',

	'sql_host' : '127.0.0.1',
	'sql_port' : 3306,
	'sql_user' : 'test',
	'sql_passwd' : 'test_password',
	'sql_db' : 'testdb',
	'sql_query': 'SELECT id,name,mobile FROM member',
	#删除数据的主键
	'major_key' : 'id',
	'sql_delete' : [
		#major_key为’id‘,则该条sql表示删除id = 对应选择的数据
		'DELETE FROM member WHERE ',
	]
}

key = b'modataMODATA6789'



cf = configparser.ConfigParser()
#cf.read(HX_SOFT_CONFIG_FILE)

#判断是否存在
if not cf.has_section('info'):
    cf.add_section("info")
    pass


cf.set('info', 'data', WWAES.aes128_encrypt(key, json.dumps(data)))

'''
#环信配置信息
cf.set("info", "hx_app_key", hx_app_key)
cf.set("info", "hx_client_id", hx_client_id)
cf.set("info", "hx_client_secret", hx_client_secret)


#数据库
cf.set("info", "sql_host", sql_host)
cf.set("info", "sql_port", sql_port)
cf.set("info", "sql_user", sql_user)
cf.set("info", "sql_passwd", sql_passwd)
cf.set("info", "sql_db", sql_db)
'''

with open(HX_SOFT_CONFIG_FILE,"w+") as f:
    cf.write(f)



