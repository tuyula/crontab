#!/bin/bash


cd /opt/crontab && python3 crontab start celery -d && python3 crontab start beat -d && python3 crontab start gunicorn