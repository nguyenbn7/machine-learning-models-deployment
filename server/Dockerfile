FROM python:3.11-slim as download_model

RUN python -m pip install kaggle --upgrade

WORKDIR /ml-models

RUN mkdir $HOME/.kaggle
RUN --mount=type=secret,id=kaggle_json,dst=/etc/secrets/kaggle.json cat /etc/secrets/kaggle.json > $HOME/.kaggle/kaggle.json

RUN kaggle kernels output nguyenbnguyen/dog-breed-classification-mobilenet -p ./dog-breeds
RUN rm -f ./dog-breeds/*.log ./dog-breeds/*.csv

# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.11-slim as final

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt
RUN python -m pip install gunicorn

WORKDIR /app
COPY . /app
COPY --from=download_model /ml-models/dog-breeds/custom-mobilenetv2-Adam.h5 /app/classification/
RUN --mount=type=secret,id=settings_json,dst=/etc/secrets/settings.json cat /etc/secrets/settings.json > /app/settings.json

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker", "main:app"]
