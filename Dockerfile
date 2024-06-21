FROM dockercodata.pb.gov.br/ci-base-images/python:3.11

USER root
RUN apk add weasyprint
RUN apk --no-cache add msttcorefonts-installer fontconfig && \
    update-ms-fonts && \
    fc-cache -f
RUN apk --no-cache add binutils geos-dev proj-dev gdal-dev
    # ln -s $(find /usr/lib -iname libgdal.so.* -type f) /usr/lib/libgdal.so && \
    # ln -s $(find /usr/lib -iname libproj.so.* -type f) /usr/lib/libproj.so && \
    # ln -s $(find /usr/lib -iname libgeos_c.so.* -type f) /usr/lib/libgeos_c.so
USER default

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# COPY docker-entrypoint.sh /docker-entrypoint.sh

# COPY --chown=default:default docker-entrypoint.sh /docker-entrypoint.sh

# RUN chmod 755 /docker-entrypoint.sh

CMD ["gunicorn", "app:app" ,"--bind=0.0.0.0:8080"]
