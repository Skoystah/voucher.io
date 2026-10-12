FROM nginx:alpine-slim

# Copy the project into the image
COPY . /usr/share/nginx/html

# Copy and replace the default config
COPY ./nginx.conf /etc/nginx/conf.d/default.conf
# EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
