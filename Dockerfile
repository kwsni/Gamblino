FROM python:3.10

LABEL org.opencontainers.image.source=https://github.com/kwsni/Gamblino
LABEL org.opencontainers.image.description="CS:GO/CS2 crate opening simulator as a Discord Bot"
LABEL org.opencontainers.image.licenses=MIT

WORKDIR /usr/src/gamblino-bot/

COPY gamblino/*.py ./gamblino/
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "gamblino/bot.py"]
