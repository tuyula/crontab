import os
import uuid
from django.db import models


# Create your models here.
def upload_notice_script(instance, filename):
    """
    因为通知脚本中可能会存在一些私密信息，如账号密码等，所以重命名文件，避免可以直接下载此文件
    :param instance:
    :param filename:
    :return:
    """
    upload_to = 'crontab_script'
    ext = filename.split('.')[-1]
    if ext not in ('py', 'sh'):
        raise Exception('只支持python或者bash脚本')
    filename = '{}.{}'.format(uuid.uuid1(), ext)
    return os.path.join(upload_to, filename)


class CustomScript(models.Model):
    """
    自定义循环脚本
    """
    name = models.CharField('名称', max_length=50)
    description = models.CharField('描述', max_length=100, null=True, blank=True)
    script = models.FileField('自定义脚本', upload_to=upload_notice_script, null=True, blank=True)
    type = models.IntegerField('脚本类型', default=0, blank=True, help_text='1,表示为bash脚本。2表示为python脚本')
    creator = models.CharField('创建人', max_length=50)
    gmt_created = models.DateTimeField(u'创建时间', auto_now_add=True)
    gmt_modified = models.DateTimeField(u'修改时间', auto_now=True)
    is_deleted = models.BooleanField(u'已删除', default=False)

    class Meta:
        verbose_name = '自定义脚本'
        verbose_name_plural = '自定义脚本'
