FROM php:7.2-cli
RUN mkdir -p /srv
WORKDIR /srv

# Copy these dirs to the container
ADD app app
ADD public public
ADD vendor public
# Add composer for deps.
COPY composer.phar /srv/
COPY composer.json /srv/

RUN apt-get update && apt-get install -y \
    zip unzip \
    git \
    postgresql-client
RUN php composer.phar install

COPY start.sh /srv/
CMD ["start.sh"]
