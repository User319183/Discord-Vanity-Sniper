"""
@Author: github.com/user319183
@Date: 3/3/2024
"""

from tls_client   import Session
from time         import sleep
from random       import choice
from veilcord import VeilCord
from base64       import b64decode
from toml         import load
from modules.console import ConsoleX, LogLevel

console = ConsoleX()
veilcord_instance = VeilCord()
xsup = veilcord_instance.generateXProp()
console.log(f"Fetched latest x-super-properties | {xsup}", LogLevel.INFO)
try:
    config = load('config.toml')
except Exception as e:
    console.log(f"Failed to load config.toml | {e}", LogLevel.ERROR)
    config = None


class Sniper:
    def __init__(
        self, 
        invite: str, 
        proxies: list = None, 
        xcontext = None
    ) -> None:
        self.invite = invite
        self.proxies = proxies
        self.xcontext = xcontext
    def newSession(self):
        self.client = Session(
            client_identifier="discord_1_0_9015",
            random_tls_extension_order=True
        )
        self.client.proxies = (
            f"http://{choice(self.proxies).strip()}"
            if self.proxies != None and len(self.proxies) != 0
            else None
        )
        self.client.headers = {
            "authority": "discord.com",
            "accept": "*/*",
            "accept-language": "en-US",
            "connection": "keep-alive",
            "content-type": "application/json",
            "origin": "https://discord.com",
            "referer": "https://discord.com/channels/@me",
            "sec-ch-ua": '"Not?A_Brand";v="8", "Chromium";v="108"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9015 Chrome/108.0.5359.215 Electron/22.3.2 Safari/537.36",
            "x-debug-options": "bugReporterEnabled",
            "x-discord-locale": "en-US",
            "x-discord-timezone": "America/New_York",
            "x-super-properties": xsup
        }
        if self.xcontext is not None:
            self.client.headers["x-context-properties"] = self.xcontext
            
        self.veilcord = VeilCord(self.client, "app", user_agent=self.client.headers.get("user-agent"), build_num=glbuildnum)
        self.fingerp, self.client.cookies = self.veilcord.getFingerprint(self.client.headers.get("x-super-properties"))
        
        return self.client

    def getUserID(self, token):
        return b64decode(token.split(".")[0]).decode()
    
        
    def snipe(self, token, guild_id, new_vanity_url, delay):
        
        # Validate inputs
        if not token or not guild_id or not new_vanity_url:
            return console.log(f"Invalid token, guild ID, or vanity URL.", LogLevel.ERROR)
        
        self.newSession()
        
        # Console.printf(f"(~) Connecting token [{token[:25]}]... to gateway...")
            
        session = self.veilcord.openSession()
        session_id = self.veilcord.getSession(token, session)

        if session_id is None:
            return console.log(f"Failed to connect token [{token[:25]}]... to gateway due to invalid session ID.", LogLevel.ERROR)

       
        if session_id is None:
            return console.log(f"Failed to connect token [{token[:25]}]... to gateway due to invalid session ID.", LogLevel.ERROR)
        
        try:
            self.client.headers["authorization"] = token

            r = self.client.patch(
                f"https://discord.com/api/v9/guilds/{guild_id}/vanity-url",
                json = {"code": new_vanity_url}
            )
            sleep(delay)

            match r.status_code:
                case 200:
                    console.log(f"Successfully sniped vanity URL [{new_vanity_url}] for guild [{guild_id}] with token [{token[:25]}]... - [{r.status_code}]", LogLevel.SUCCESS)
                case 400:
                    error_code = r.json().get('code')
                    if error_code == 50020:
                        console.log(f"Vanity URL [{new_vanity_url}] is either invalid or taken for guild [{guild_id}] with token [{token[:25]}]... - [{r.status_code}]", LogLevel.ERROR)
                        sleep(delay)
                    else:
                        console.log(f"Unknown error with the token [{token[:25]}]...| [{r.status_code}] | {r.text}", LogLevel.ERROR)
                        sleep(delay)
                case 429:
                    console.log(f"Rate limited with the token [{token[:25]}]...| [{r.status_code}] | {r.text}", LogLevel.ERROR)
                    sleep(delay) 
                case 403:
                    console.log(f"Permission Denied. The token [{token[:25]}] does not have the 'Manage Server' permission in the guild {guild_id}.", LogLevel.ERROR)
                    sleep(delay)
                case 401:
                    console.log(f"Invalid token [{token[:25]}]...| [{r.status_code}] | {r.text}", LogLevel.ERROR)
                    sleep(delay)
                case _:
                    console.log(f"Unknown error with the token [{token[:25]}]...| [{r.status_code}] | {r.text}", LogLevel.ERROR)
                    sleep(delay)
        except Exception as e:
            console.log(f"Failed to snipe vanity URL for guild [{guild_id}] with token [{token[:25]}]... | {e}", LogLevel.ERROR)
            sleep(delay)
            
                    
def start():
    console.clear()
    console.print(
        """
    ╦ ╦┌─┐┌─┐┬─┐
    ║ ║└─┐├┤ ├┬┘
    ╚═╝└─┘└─┘┴└─
                                                                                
    ╔══════════════════════════════════════════════════════════════════════════════╗
    ║ Discord vanity sniper - Developed by User319183                              ║
    ║ discord.gg/p3xxVhyb65                                                        ║
    ╚══════════════════════════════════════════════════════════════════════════════╝
    """,
        fg="pink",
        style="bright",
    )

    while True:

        with open("tokens.txt", "r") as f:
            tokens = [x.strip() for x in f.readlines()]

        proxies = (open("./proxies.txt", "r").readlines())
        proxy = (
            proxies
            if proxies != None and len(proxies) != 0 
            else None
        )

        if len(tokens) > 100 and not proxy:
            console.alert(
                "(?) You have more than 100 tokens without proxies. This will most likely result in a rate limit. Do you want to continue? (y/n) > ",
                style="question",
            )
            if not console.confirm("Continue? (y/n) > "):
                console.log("Exiting...", LogLevel.INFO)
                exit()

        # Load configurations
        config = load("config.toml").get("opts")
        delay = config.get("delay")
        guild_id = config.get("guild_id")
        new_vanity_url = config.get("new_vanity_url")

        # Initiate the Sniper class and start the sniping process
        for token in tokens:
            sniper = Sniper(proxies)
            sniper.snipe(token, guild_id, new_vanity_url, delay)

if __name__ == "__main__":
    glbuildnum = VeilCord.getBuildNum()

start()
