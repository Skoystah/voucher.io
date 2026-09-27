FROM nginx:alpine-slim

# Copy the project into the image
COPY . /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
