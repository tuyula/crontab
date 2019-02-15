# 选择基础镜像
FROM centos:latest

MAINTAINER opsa Team opsa:latest

# 按照系统环境
RUN yum -y install wget unzip sqlite-devel xz gcc automake make autoconf libtool zlib-devel openssl-devel epel-release git openldap-devel mysql-devel bzip2-devel

# 按照python3.6环境
RUN wget https://www.python.org/ftp/python/3.6.1/Python-3.6.1.tar.xz && tar xvf Python-3.6.1.tar.xz && cd Python-3.6.1 && ./configure && make && make install


# 安装pip依赖
COPY ./requirements/common.txt /tmp/common.txt
COPY ./requirements/crontab.txt /tmp/crontab.txt
RUN pip3 install -i https://mirrors.aliyun.com/pypi/simple --upgrade pip && pip install -i https://mirrors.aliyun.com/pypi/simple --upgrade setuptools && pip install -i https://mirrors.aliyun.com/pypi/simple -r /tmp/crontab.txt

# 切换目录
WORKDIR /opt/crontab

# 将文件放入dokcer里
COPY . /opt/crontab

EXPOSE 80
RUN chmod +x ./entrypoint.sh ./crontab
# run celery deamon
# RUN

CMD ["bash", "entrypoint.sh"]
