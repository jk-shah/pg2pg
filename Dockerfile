FROM python:2.7
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -y && apt-get install -y  locales  apt-utils
RUN dpkg-reconfigure locales &&  locale-gen en_US.UTF-8  

RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ jessie-pgdg main" > /etc/apt/sources.list.d/pgdg.list
RUN curl https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -

ENV PGVERSION 9.5
RUN apt-get update -y && apt-get install postgresql-${PGVERSION} -y


ENV VDMASK_HOME /root/vdatamask
ADD . ${VDMASK_HOME}
WORKDIR ${VDMASK_HOME}

RUN pip install fake-factory psycopg2 flask && \
    chmod +x entrypoint.sh

CMD ["./entrypoint.sh"]
