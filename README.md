# osu!UW Bot Platform

`auth` - proxy HTTP server used to link your osu! account to your Discord account

`bot` - the actual bot

## Setup
1. Create a new app in the [Discord developer portal](https://discord.com/developers/applications), and invite it to your server with <insert_permissions_here>
2. Create a new OAuth application in [osu!](https://osu.ppy.sh/home/account/edit#oauth) 
3. Create a `.env` file under both the `auth` and `bot` directories
    ```.env
    # auth/.env
    CLIENT_ID=XXXX
    CLIENT_SECRET=XXXX
    REDIRECT_URI=XXXX
    ```
    ```.env
    # bot/.env
    DISCORD_TOKEN=XXXX
    ALLOWED_SERVERS=XXXX # comma-delimited list of Discord guild IDs 

    GOOGLE_API_KEY=XXXX
    GOOGLE_SHEET_ID=16sRHUiVHC46V43YSBhUNG3JZ7QoOWsyJTfJsy9JYsi4
    GOOGLE_SHEET_NAME=Users
    GOOGLE_SHEET_CELL_RANGE=B:AC

    # these should match the entries in `auth/.env`
    OSU_CLIENT_ID=XXXX
    OSU_CLIENT_SECRET=XXXX
    REDIRECT_URI=XXXX
    ```
    When testing locally, you may need to create a public tunnel to `localhost:8000` using something like [ngrok](https://ngrok.com/), because otherwise the osu! servers will not be able to communicate with the proxy authentication server.
4. Run the following commands to build and deploy the application
    ```console
    $ docker compose build
    $ docker compose up
    ```