# 选择基础镜像
FROM centos:latest

MAINTAINER opsa Team opsa:latest

# 按照系统环境
RUN yum -y install wget unzip sqlite-devel xz gcc automake make autoconf libtool zlib-devel openssl-devel epel-release\
    git openldap-devel

# 安装nginx
RUN wget https://nginx.org/download/nginx-1.14.0.tar.gz && tar zxvf nginx-1.14.0.tar.gz && cd nginx-1.14.0 \
    && groupadd www && useradd -g www www -M -s /sbin/nologin && ./configure --prefix=/usr/local/nginx --user=www \
    --group=www --with-http_ssl_module --with-http_gzip_static_module --with-http_stub_status_module --with-file-aio \
    --with-http_dav_module && make && make install

# 添加配置文件
ADD nginx.conf /usr/local/nginx/conf
RUN cp /usr/local/nginx/sbin/nginx /sbin/nginx

# 创建conf.d文件
RUN mkdir /usr/local/nginx/conf.d/
ADD crontab.conf /usr/local/nginx/conf.d/

# 5.开启端口
EXPOSE 80

# 6.运行
CMD nginx
