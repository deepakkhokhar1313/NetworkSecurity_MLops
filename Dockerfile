FROM python:3.13        
WORKDIR /app
COPY . /app

RUN apt update -y && snap install awscli -y

RUN apt-get update -y && pip install -r requirements.txt
CMD ["python3","app.py"]