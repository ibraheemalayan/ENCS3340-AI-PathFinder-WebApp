import multiprocessing

workers = multiprocessing.cpu_count() * 2 + 1
bind = 'unix:route_finder_gunicorn_socket.sock'
umask = 0o007
reload = False

#logging
accesslog = 'logs/access.log'
errorlog = 'logs/error.log'