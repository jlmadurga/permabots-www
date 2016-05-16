web: gunicorn config.wsgi:application
worker: newrelic-admin run-program celery worker --app=permabots_www.taskapp --loglevel=info --without-gossip --without-mingle --without-heartbeat
