# python image with with version 3.11.3
FROM python:3.11 as flaskapp

# Set the working directory in the container
WORKDIR /

ENV PYTHONUNBUFFERED 1
ENV POSTGRES_PASSWORD="database-password"
ENV POSTGRES_DB="postgres"
ENV DATABASE_URL=postgresql://postgres:database-password@localhost:5432/postgres?host=/absolute/path/to/project/data


# Copy the requirements file into the container
COPY requirements.txt .

# Install the python dependencies listed in the requirements.txt file
RUN pip install --no-cache-dir -r requirements.txt

# Make the shell script executable
LABEL 'tag'='value'

# Copy the source code into the Docker container
COPY . .



# Expose the Flask port
EXPOSE 8080

# ENTRYPOINT ["docker-entrypoint.sh"]

CMD [ "python", "script.py"]


RUN set -e
#RUN flask postgres upgrade
#RUN gunicorn -c gunicorn.config.py wsgi:app








# FROM postgres:latest as postgres 



# #RUN su -u postgres pg_ctl -D /var/lib/postgresql/data -l logfile start

# FROM postgres as final

# COPY --from=postgres /var/lib/postgresql/data /var/lib/postgresql/data

# CMD ["postgres", "-c", "config_file=../database/postgresql.conf"] && ["flaskapp"]