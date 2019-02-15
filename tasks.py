# from __future__ import absolute_import, unicode_literals
import contextlib
import os
import sys
import traceback
import logging
from celery import Celery


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.dev')
import django
django.setup()

app = Celery('loonflow')
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


from apps.script.models import CustomScript


try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

logger = logging.getLogger('django')



@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

@app.task
def test_task(a, b):
    print('a:', a)
    print('b:', b)
    print(a+b)


@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        try:
            # for python2
            stdout = StringIO.StringIO()
        except Exception:
            stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old


@app.task
def cron_custom_script(script_id):
    """
    自定义计划任务，通过上传的脚本+django-beat可以方便的自定义计划任务
    :param script_id: 获取Script的id
    :return:
    """
    # 获取对应的脚本
    # 根据python,bash判断不同类型，执行脚本
    script_obj = CustomScript.objects.filter(id=script_id, is_deleted=0).first()
    if not script_obj:
        return False, 'Custom script object doesn`t exist or has been delete'
    script_type = script_obj.type
    script_file = 'media/' + str(script_obj.script)
    globals = {}

    if not script_file:
        return False, 'Custom script object doesn`t have file'
    if script_type == 1:
        # 执行bash脚本
        pass
    elif script_type == 2:
        # 执行python脚本
        try:
            with stdoutIO() as s:
                print(script_file)
                exec(open(script_file).read(), globals)
            script_result = True
            script_result_msg = ''.join(s.getvalue())
            logger.info('cron script for script_id: {}'.format(script_id))
        except Exception as e:
            logger.error(traceback.format_exc())
            script_result = False
            script_result_msg = e.__str__()
        return script_result, script_result_msg
    else:
        return False, 'Custom script type must be 1(bash) or 2(python)'