ARG PYTHON_VERSION=3.13-slim

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create working directory
RUN mkdir -p /code
WORKDIR /code

# Install dependencies
COPY requirements.txt /tmp/requirements.txt
RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /root/.cache/

# Copy project files
COPY . /code
RUN chmod +x /code/startup.sh


# Use environment variable for SECRET_KEY
ENV DJANGO_SETTINGS_MODULE=dndRestAPI.settings

# Command to run the app
CMD ["./startup.sh"]
