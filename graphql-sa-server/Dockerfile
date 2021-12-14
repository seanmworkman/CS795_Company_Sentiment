############################################################
# Dockerfile to run SA-Server Container
############################################################

# Pull the node image from the local registry
FROM registry.access.redhat.com/ubi8/nodejs-12

USER root

MAINTAINER swork002@odu.edu

WORKDIR /usr/src/app

COPY ./ /usr/src/app/

RUN npm i

EXPOSE 80

# Start the service
CMD ["npm", "start"]
