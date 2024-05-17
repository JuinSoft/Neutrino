FROM nginx:latest

COPY cloned_repo /usr/share/nginx/html

CMD ["nginx", "-g", "daemon off;"]