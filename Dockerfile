FROM python:3.10

WORKDIR /usr/src/gamblino-bot/

COPY gamblino/*.py ./
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./gamblino/bot.py"]
