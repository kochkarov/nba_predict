import multiprocessing as mp

workers = mp.cpu_count() * 2 + 1
command = '/home/admin/web/venv/bin/gunicorn'
pythonpath = '/home/admin/web/nba_predict/'
bind = '0.0.0.0:8001'
user = 'admin'
limit_request_fields = 32000
limit_request_field_size = 0
raw_env = 'DJANGO_SETTINGS_MODULE=nba_predict.settings'
