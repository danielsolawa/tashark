FROM alpine:3.10
RUN apk add --update sqlite
RUN mkdir /db
WORKDIR /db

RUN mkdir /opt/sqlite3
ADD init.sql /opt/sqlite3
ENTRYPOINT ["sqlite3"]
CMD ["tashark.db < /opt/sqlite3/init.sql"]



