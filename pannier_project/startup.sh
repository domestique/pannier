#! /bin/bash
../wait_for_it.sh db:5432
sed -i "s@STATIC_PATH@$STATIC_PATH@g" /etc/nginx/sites-enabled/pannier.conf
python3 manage.py migrate --noinput
python3 manage.py collectstatic --noinput
# Symlink in Django admin path
if [ "$STATIC_PATH" == "/home/docker/pannier/pannier/pannier/static" ]; then
    ln -s /usr/local/lib/python3.5/dist-packages/django/contrib/admin/static/admin /home/docker/pannier/pannier/pannier/static/admin;
else
    # Just in case this snuck in via a build somewhere
    rm -f /home/docker/pannier/pannier/pannier/static/admin;
fi
uwsgi --ini /home/docker/pannier/configs/uwsgi/pannier_uwsgi.ini --daemonize /var/log/uwsgi/pannier.log 
nginx -g "daemon off;"
