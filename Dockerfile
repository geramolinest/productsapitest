FROM python:3.12.0-slim
LABEL authors="geramolina"

WORKDIR /productsapi

COPY requirements.txt .

RUN cat /etc/os-release

RUN apt-get -y update; apt-get -y install curl gnupg gnupg1 gnupg2

RUN curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg
RUN curl https://packages.microsoft.com/config/debian/12/prod.list | tee /etc/apt/sources.list.d/mssql-release.list

RUN apt-get update \
  && ACCEPT_EULA=Y apt-get install -y msodbcsql18


RUN apt-get update -y && apt-get update
RUN apt-get install -y --no-install-recommends curl gcc g++ gnupg unixodbc-dev

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

RUN apt-get -y clean

EXPOSE 8000

# Run the FastAPI application using uvicorn server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]