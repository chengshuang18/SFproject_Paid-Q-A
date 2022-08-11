FROM mysql:5.7
 
#设置免密登录
ENV MYSQL_ALLOW_EMPTY_PASSWORD yes
ENV MySQL=/home/mysql
WORKDIR $MySQL
#将所需文件放到容器中
COPY setup.sh $MySQL/setup.sh
COPY schema.sql $MySQL/schema.sql
COPY privileges.sql $MySQL/privileges.sql
 
#设置容器启动时执行的命令
CMD ["/bin/sh", "setup.sh"]
