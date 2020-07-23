FROM python:3.7-slim
COPY / /app
WORKDIR /app
RUN pip3 install -r requirements.txt
#RUN apt update && apt install -y python3-opencv
COPY start.sh /usr/bin/start.sh
RUN chmod +x /usr/bin/start.sh
CMD ["python", "/app/app.py"]

