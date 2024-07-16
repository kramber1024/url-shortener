FROM debian:stable-slim

RUN apt-get update && \
    apt-get install --no-install-recommends --no-install-suggests -y gnupg1 ca-certificates nginx && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /etc/nginx/conf.d/* && \
    rm -rf /etc/nginx/sites-enabled/* && \
    rm -rf /etc/nginx/sites-available/* && \
    rm -rf /etc/nginx/nginx.conf && \
    rm -rf /var/www/html/*

COPY ./nginx.conf /etc/nginx/nginx.conf

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]
