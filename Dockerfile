############################################################################################################
# BUILD
############################################################################################################
FROM python:3.12.6 AS build

# Install dependencies
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY ./config.yml .
COPY ./generate_nginx_config.py .
RUN python generate_nginx_config.py > nginx.conf

############################################################################################################
# RELEASE
############################################################################################################
FROM nginx:1.27.3 AS release

# Path: /etc/nginx/nginx.conf
COPY --from=build nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
