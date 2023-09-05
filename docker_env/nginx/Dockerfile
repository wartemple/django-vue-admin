FROM nginx:1.19.10

RUN rm /etc/nginx/conf.d/default.conf &&\
    mkdir -p /usr/share/nginx/ssl

ADD ./nginx.conf /etc/nginx/conf.d/

CMD ["nginx", "-g", "daemon off;"]