FROM alpine:3.6

# add our user and group first to make sure their IDs get assigned consistently, regardless of whatever dependencies get added
RUN addgroup -S redis && adduser -S -G redis redis

# grab su-exec for easy step-down from root
RUN apk add --no-cache 'su-exec>=0.2'

RUN mkdir -p /usr/src/redis;
COPY redis.tar.gz /usr/src/

# for redis-sentinel see: http://redis.io/topics/sentinel
RUN set -ex; \
	apk add --no-cache --virtual .build-deps \
		coreutils \
		gcc \
		linux-headers \
		make \
		musl-dev \
	; \
	tar -xzf /usr/src/redis.tar.gz -C /usr/src/redis --strip-components=1; \
	rm /usr/src/redis.tar.gz; \
	grep -q '^#define CONFIG_DEFAULT_PROTECTED_MODE 1$' /usr/src/redis/src/server.h; \
	sed -ri 's!^(#define CONFIG_DEFAULT_PROTECTED_MODE) 1$!\1 0!' /usr/src/redis/src/server.h; \
	grep -q '^#define CONFIG_DEFAULT_PROTECTED_MODE 0$' /usr/src/redis/src/server.h; \
	make -C /usr/src/redis -j "$(nproc)"; \
	make -C /usr/src/redis install; \
	rm -r /usr/src/redis; \
	apk del .build-deps

COPY redis.conf /usr/local/etc/redis/redis.conf
RUN mkdir /data && chown redis:redis /data
VOLUME /data
WORKDIR /data

EXPOSE 6379
CMD ["redis-server", "/usr/local/etc/redis/redis.conf"]
