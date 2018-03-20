# hxAccountManager
用于清除环信和数据库中的用户信息

## 配置文件生成

在config_manager.py 中配置好环信信息和数据库信息，然后运行生成配置文件库


## 运行
将配置文件放入到与exe相同的目录下，即可使用该软件

## 备注
若想修改通信的密钥，需要修改config_manager.py中的key变量值，并重新生成配置文件（config.ini），并且修改hx.py文件中DATA_KEY的变量值，若要是在windows使用，可使用pyinstaller重新打包exe文件
