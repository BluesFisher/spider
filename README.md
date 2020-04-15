#### 环境说明
- 开发环境：python 2.7.16

#### MySQLdb安装
- fatal error: 'my_config.h' file not found解决方案
    1、brew install mysql
    2、brew unlink mysql
    3、brew install mysql-connector-c
    4、sed -i -e 's/libs="$libs -l "/libs="$libs -lmysqlclient -lssl -lcrypto"/g' /usr/local/Cellar/mysql/8.0.13/bin/mysql_config //后面的路径就是你 mysql 的安装路径，这个尤为重要，就是路径问题报错的
    5、pip install MySQL-python
    6、brew unlink mysql-connector-c
    7、brew link --overwrite mysql