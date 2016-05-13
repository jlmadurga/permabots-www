web: gunicorn config.wsgi:application
worker: newrelic-admin run-program celery worker --app=permabots.taskapp --loglevel=info --without-gossip --without-mingle --without-heartbeat
