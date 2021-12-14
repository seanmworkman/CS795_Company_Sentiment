#!/bin/sh

if [ -z "${DEVELOP}" ]; then
    echo "DEVELOP MODE disabled!"
    rm -f /etc/nginx/conf.d/develop.conf
else
    cp -f /develop.conf /etc/nginx/conf.d/
    echo "!!!!!!!!!!!!!!!!!!! DEVELOP MODE enabled !!!!!!!!!!!!!!!!!!!!!!!!!"
fi

exec "$@"