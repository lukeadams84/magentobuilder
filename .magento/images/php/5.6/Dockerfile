FROM alpine:3.5

RUN set -x ; \
  addgroup -g 82 -S www-data ; \
  adduser -u 82 -D -S -G www-data www-data && exit 0 ; exit 1

RUN apk --update add \
        php5 \
        php5-pear \
        php5-common \
        php5-bcmath \
        php5-dom \
        php5-ctype \
        php5-curl \
        php5-fpm \
        php5-gd \
        php5-iconv \
        php5-intl \
        php5-json \
        php5-mcrypt \
        php5-opcache \
        php5-openssl \
        php5-pdo \
        php5-pdo_mysql \
        php5-pdo_pgsql \
        php5-pdo_sqlite \
        php5-phar \
        php5-posix \
        php5-soap \
        php5-xml \
        php5-zlib \
        git \
    && rm -rf /var/cache/apk/*

RUN printf '* *\t* * *\twww-data\t%s/usr/local/bin/php /var/www/html/cron.php\n#\n' >> /etc/crontab

RUN apk add --no-cache \
    $PHPIZE_DEPS \
    openssl-dev


  RUN mkdir -p /var/www/html/ \
     && chown -R www-data:www-data /var/www/html/


COPY conf/php.ini /etc/php5/conf.d/50-setting.ini
COPY conf/php-fpm.conf /etc/php5/php-fpm.conf

WORKDIR /var/www/html
EXPOSE 9000

CMD ["php-fpm", "-F"]
