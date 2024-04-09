FROM python:3.10-bullseye

RUN pip3 install dailyai[daily,openai,silero]
RUN pip3 install flask flask-cors gunicorn requests python-dotenv

RUN mkdir /app
RUN mkdir /app/assets
COPY *.py /app/
copy assets/* /app/assets/

EXPOSE 8000

CMD ["python3", "/app/server.py"]