FROM php:7.2-apache
WORKDIR /srv

EXPOSE 80

# Copy these dirs to the container
COPY app /srv/app
COPY public /srv/public

# Add composer for deps.
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer
# COPY ./composer.phar /srv/composer.phar
COPY ./composer.json /srv/composer.json

RUN apt-get update && apt-get install -y \
    zip unzip \
    git \
    libpq-dev \
    && docker-php-ext-install pdo_pgsql \
    && composer install \
    && a2enmod rewrite \
    && chown -R www-data:www-data /srv/app/storage

COPY vhost.conf /etc/apache2/sites-available/000-default.conf

COPY start.sh /srv/
CMD ["/srv/start.sh"]
