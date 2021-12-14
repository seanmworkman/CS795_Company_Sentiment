############################################################
# Dockerfile to run SA-Server Container
# Please reflect any changes in Dockerfile.cloud
############################################################

FROM docker.io/nginx:latest

USER 0

MAINTAINER swork002@odu.edu

COPY proxy.conf /etc/nginx/conf.d/
COPY nginx.conf /etc/nginx/nginx.conf
COPY default.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD [ "nginx", "-g", "daemon off;" ]
