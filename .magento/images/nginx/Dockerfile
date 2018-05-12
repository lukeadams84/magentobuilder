FROM alpine:3.6
RUN apk add --update nginx && rm -rf /var/cache/apk/*
RUN mkdir -p /tmp/nginx/client-body

RUN set -x ; \
  addgroup -g 82 -S www-data ; \
  adduser -u 82 -D -S -G www-data www-data && exit 0 ; exit 1

RUN touch /var/run/nginx.pid


RUN mkdir -p /var/www/html/ \
 && mkdir -p /var/cache/nginx/ \
 && chown -R www-data:www-data /var/www/html/ \
 && chown -R www-data:www-data /var/lib/nginx/ \
 && chown -R www-data:www-data /var/tmp/nginx/ \
 && chown -R www-data:www-data /var/log/nginx/ \
 && chown -R www-data:www-data /var/cache/nginx/ /var/run/nginx.pid

USER www-data:www-data

VOLUME /var/www

WORKDIR /var/www/html

EXPOSE 8000

CMD ["nginx", "-g", "daemon off;"]
