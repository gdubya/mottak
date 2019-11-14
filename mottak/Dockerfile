FROM php:7.2-apache
RUN mkdir -p /srv
WORKDIR /srv

EXPOSE 80

# Copy these dirs to the container
ADD app app
ADD public public

# Add composer for deps.
COPY composer.phar /srv/
COPY composer.json /srv/

RUN apt-get update && apt-get install -y \
    zip unzip \
    git \
    libpq-dev
RUN docker-php-ext-install pdo pdo_pgsql
RUN php composer.phar install

COPY vhost.conf /etc/apache2/sites-available/000-default.conf
RUN a2enmod rewrite
RUN chown -R www-data:www-data /srv/app/storage


COPY start.sh /srv/
CMD ["/srv/start.sh"]
