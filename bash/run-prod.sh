#!/usr/bin/env bash
yes yes | python3 manage.py migrate && python3 manage.py collectstatic --noinput && gunicorn va_checker.wsgi -b 0.0.0.0:8000 --log-file -