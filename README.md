# Gamblino

CS:GO/CS2 case opening simulator as a Discord Bot.

Feel the rush of opening cases in Counter-Strike 2 without risking any real world currency with this Discord bot that *simulates* opening cases from CS2. Keep track of your *imaginary* inventory with a web interface that shows you all of the *fictional* skins you acquired from simulating opening cases with the bot.

Note: This bot is ***NOT*** tied in any way to CS2/Steams's inventory system or the Steam Community Market. This is a Discord bot *strictly* to be used for fun in your own Discord guild/server.

## Bot Commands
/open [case_name] - Open a case

## Setup
### Docker
Use the provided docker compose file below, ensuring that all environment variables are filled out.

```
# compose.yaml

services:
  gamblino-bot:
    image: ghcr.io/gamblino-bot
    container_name: gamblino-bot-1
    restart: unless-stopped
    environment:
      - DISCORD_TOKEN=      # from Discord application
      - APP_ID=             # from Discord application
      - PUBLIC_KEY=         # from Discord application
      - CLIENT_SECRET=      # from Discord application
      - API_URL=
  gamblino-web:
    image: ghcr.io/gamblino-web
    container_name: gamblino-web-1
    restart: unless-stopped
    environment:
      - DISCORD_TOKEN=      # from Discord application
      - APP_ID=             # from Discord application
      - PUBLIC_KEY=         # from Discord application
      - CLIENT_SECRET=      # from Discord application
      - DJANGO_SECRET_KEY=
      - DATABASE_NAME=
      - DATABASE_USER=
      - DATABASE_PASSWORD=
      - DATABASE_HOST=
      - DATABASE_PORT=
      - ALLOWED_HOSTS=
      - ADMINS=
      - EMAIL_HOST=
      - EMAIL_PORT=
      - EMAIL_HOST_USER=
      - EMAIL_HOST_PASSWORD=
      - EMAIL_USE_TLS=
      - STORAGE_HOST=
      - STORAGE_MEDIA_ROOT=
      - STORAGE_STATIC_ROOT=
      - STORAGE_SSH_KEY_PATH=
```
Then run the following command:
```
docker compose up -d
```