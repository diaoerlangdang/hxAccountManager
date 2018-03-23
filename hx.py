#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import json
import pymysql
from time import time, strftime, localtime
import os
from easemob_server_python import *
#配置文件解析库
import configparser
import WWAES


HX_SOFT_CONFIG_FILE = 'config.ini'

DATA_KEY = b'modataMODATA6789'

TEST_DEBUG = False

class ConfigInfo(object):
	"""docstring for ConfigInfo"""
	def __init__(self):
		super(ConfigInfo, self).__init__()
		self.hx_app_key 		=	 	''#1136170607178782#liangjianbingcheng55'
		self.hx_client_id 		= 		''#'YXA6SbKVwPdZEeeYd8v269dtMw'
		self.hx_client_secret 	= 		''#'YXA6ywaN8wmbreIDMfJWimy_f0dgONQ'
		self.hx_prefix			=		'' #环信用户前缀

		self.sql_host 			= 		''#'10.0.1.107'
		self.sql_port			=		3306
		self.sql_user 			=		''#'mododata'
		self.sql_passwd			=		''#'Modb@666'
		self.sql_db				=		''#'modoshop'
		self.hx_org_name		=		''
		self.hx_app_name 		= 		''
		self.major_key			= 		'id'
		self.sql_query 			=  		''
		self.sql_delete 		=		[]



	def init_config(self):
		cf = configparser.ConfigParser()
		cf.read(HX_SOFT_CONFIG_FILE)
		#判断是否存在
		if not cf.has_section('info'):
			return False

		json_dict = {}

		if not cf.has_option('info','data'):
			return False
		else :
			json_dict = json.loads(WWAES.aes128_decrypt(DATA_KEY, cf.get('info', 'data')))
			#json_dict = json.loads('{}')

		#环信数据
		if('hx_app_key' in json_dict.keys()):
			self.hx_app_key = json_dict['hx_app_key']
		else :
			return False

		if('hx_client_id' in json_dict.keys()):
			self.hx_client_id = json_dict['hx_client_id']
		else :
			return False

		if('hx_client_secret' in json_dict.keys()):
			self.hx_client_secret = json_dict['hx_client_secret']
		else :
			return False

		if('hx_prefix' in json_dict.keys()):
			self.hx_prefix = json_dict['hx_prefix']
		else :
			return False


		#数据库
		if('sql_host' in json_dict.keys()):
			self.sql_host = json_dict['sql_host']
		else :
			return False

		if('sql_port' in json_dict.keys()):
			self.sql_port = json_dict['sql_port']
		else :
			return False

		if('sql_user' in json_dict.keys()):
			self.sql_user = json_dict['sql_user']
		else :
			return False

		if('sql_passwd' in json_dict.keys()):
			self.sql_passwd = json_dict['sql_passwd']
		else :
			return False

		if('sql_db' in json_dict.keys()):
			self.sql_db = json_dict['sql_db']
		else :
			return False

		if('major_key' in json_dict.keys()):
			self.major_key = json_dict['major_key']
		else :
			return False

		if('sql_query' in json_dict.keys()):
			self.sql_query = json_dict['sql_query']
		else :
			return False

		if('sql_delete' in json_dict.keys()):
			self.sql_delete = json_dict['sql_delete']
		else :
			return False

		self.hx_org_name, self.hx_app_name = parse_appkey(self.hx_app_key)

		return True

		pass


configInfo = ConfigInfo()


#打印日志
def print_log(data):

	#print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
	if TEST_DEBUG:
		print(data)
	else :
		if not os.path.exists('log') : 
			os.makedirs('log')
		currentTime = strftime("%Y-%m-%d %H:%M:%S")
		with open('log\log.txt','a+') as fw:
			fw.write('['+currentTime+']  '+data+'\r\n')
	pass


#注册
def hx_register_user(username, password):

	global app_client_auth
	if app_client_auth is None:
		app_client_auth = AppClientAuth(configInfo.hx_org_name, configInfo.hx_app_name,configInfo. hx_client_id, configInfo.hx_client_secret)
		pass

	username = 'test'+username
	success, result = register_new_user(configInfo.hx_org_name, configInfo.hx_app_name, app_client_auth, username, password)
	if success:
		print_log("注册成功用户： %s 密钥：[%s]" % (username, configInfo.hx_app_key))
	else:
		print_log("注册新用户失败 %s 密钥：[%s]" % (username, configInfo.hx_app_key))
		pass

	return success

#删除
def hx_delete_user(username):

	global app_client_auth
	if app_client_auth is None:
		app_client_auth = AppClientAuth(configInfo.hx_org_name, configInfo.hx_app_name,configInfo. hx_client_id, configInfo.hx_client_secret)
		pass

	username = configInfo.hx_prefix+username
	success, result = delete_user(configInfo.hx_org_name, configInfo.hx_app_name, app_client_auth, username)
	if success:
		print_log("从 appkey[%s] 删除用户[%s] 成功" % (configInfo.hx_app_key, username))
	else:
		print_log("从 appkey[%s] 删除用户[%s] 失败" % (configInfo.hx_app_key, username))
	
	return success


#查询成员
def sql_query_member():

	db = None
	sql = configInfo.sql_query #"SELECT id,name,mobile FROM modoshop.member"
	data = None

	try: 

		# 打开数据库连接
		db = pymysql.Connect(
			host=configInfo.sql_host,
			port=configInfo.sql_port,
			user=configInfo.sql_user,
			passwd=configInfo.sql_passwd,
			db=configInfo.sql_db,
			charset='utf8',
			cursorclass = pymysql.cursors.DictCursor #查询返回数据为字典
			)

		# 使用 cursor() 方法创建一个游标对象 cursor
		cursor = db.cursor()

		# 使用 execute()  方法执行 SQL 查询
		cursor.execute(sql)

		# 使用 fetchone() 方法获取单条数据.
		data = cursor.fetchall()
		# name,nickName,headerImgUrl,phone = data
		# print(list(data))
	except Exception as e: #方法一：捕获所有异常 
		print_log('查询数据库异常： ' + repr(e))
		pass
	finally:
		if not db is None:
			# 关闭数据库连接
			db.close()

	if data is None:
		return None
		pass
	else :
		return data
	pass


def sql_delete_user(userid):

	#sql = "DELETE FROM modoshop.member WHERE id="+userid

	success = False
	data = None

	try: 

		# 打开数据库连接
		db = pymysql.Connect(
			host=configInfo.sql_host,
			port=configInfo.sql_port,
			user=configInfo.sql_user,
			passwd=configInfo.sql_passwd,
			db=configInfo.sql_db,
			charset='utf8'
			)

		# 使用 cursor() 方法创建一个游标对象 cursor
		cursor = db.cursor()

		for sql in configInfo.sql_delete :
			sql = sql + ' ' + configInfo.major_key + '=' + userid
			# 使用 execute()  方法执行 SQL 删除
			cursor.execute(sql)
			pass

		print_log("从 数据库[%s] 删除用户%s为[%s] 成功" % (configInfo.sql_db, configInfo.major_key, userid))

		if not hx_delete_user(userid):
			db.rollback()
			print_log('环信删除失败回滚数据 数据库[%s] 用户%s[%s] ' % (configInfo.sql_db, configInfo.major_key, userid))
			pass
		else :
			success = True
			db.commit()

	except Exception as e: #方法一：捕获所有异常 
		print_log('删除数据异常： ' + repr(e))
		#错误回滚  
		db.rollback()
		print_log('删除数据异常回滚数据 数据库[%s] 用户%s[%s] ' % (configInfo.sql_db, configInfo.major_key, userid))
		pass
	finally:
		print_log('===================================================================')
		if not db is None:
			# 关闭数据库连接
			db.close()

	return success

	pass


# 通过client id和secret来获取app管理员的token
app_client_auth = None
# print_log('Token数据: '+ app_client_auth.get_token())

# test_username = 'wuruizhi'
# test_password = '123456'

# hx_register_user(test_username,test_password);
# hx_delete_user(test_username)

# query_member()

















