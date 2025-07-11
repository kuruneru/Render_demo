FROM mysql:8.0

EXPOSE 3306

# 初期化SQLを読み込ませる場合
# COPY ./init.sql /docker-entrypoint-initdb.d/


ENV MYSQL_DATABASE=sampledb \
    MYSQL_USER=sampleuser \
    MYSQL_PASSWORD=samplepass \
    MYSQL_ROOT_PASSWORD=rootpass