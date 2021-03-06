FROM alpine:3.6

RUN set -x ; \
  addgroup -g 82 -S www-data ; \
  adduser -u 82 -D -S -G www-data www-data && exit 0 ; exit 1

RUN apk --update add \
        php7 \
        php7-bcmath \
        php7-dom \
        php7-pear \
        php7-dev \
        php7-ctype \
        php7-curl \
        php7-fileinfo \
        php7-fpm \
        php7-gd \
        php7-iconv \
        php7-intl \
        php7-json \
        php7-mbstring \
        php7-mcrypt \
        php7-mysqlnd \
        php7-mysqli \
        php7-opcache \
        php7-openssl \
        php7-pdo \
        php7-pdo_mysql \
        php7-pdo_pgsql \
        php7-pdo_sqlite \
        php7-phar \
        php7-posix \
        php7-simplexml \
        php7-session \
        php7-soap \
        php7-tokenizer \
        php7-xml \
        php7-xsl \
        php7-xmlreader \
        php7-xmlwriter \
        php7-zip \
        build-base \
        libxml2-dev \
        glib-dev

    RUN apk add --no-cache \
    		$PHPIZE_DEPS \
    		openssl-dev

    RUN apk add --update --no-cache autoconf g++ make && \
      pecl install redis

    RUN mkdir -p /var/www/html/ \
       && chown -R www-data:www-data /var/www/html/

    RUN mkdir -p /root/.composer/
    COPY conf/auth.json /root/.composer/auth.json


    RUN cd /var/www/html/ \
       && php -r "copy('https://getcomposer.org/installer', '/var/www/html/composer-setup.php');" \
       && php composer-setup.php \
       && php -r "unlink('/var/www/html/composer-setup.php');"

COPY conf/php.ini /etc/php7/conf.d/50-setting.ini
COPY conf/php-fpm.conf /etc/php7/php-fpm.conf

WORKDIR /var/www/html

EXPOSE 9000

CMD ["php-fpm7", "-F"]
