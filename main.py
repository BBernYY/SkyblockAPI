def send_message(content):
    from discord_webhook import DiscordWebhook
    webhook = DiscordWebhook(url='https://discord.com/api/webhooks/944608376048975962/TJv1zug9QpXpt4lLJw5oFAIyg6UT8a6s8ifRkVBAO4b7C6pZEaI779aKWmeJAW9xDEGk', content=content)
    webhook.execute()
def write_message(session, name):
    from datetime import datetime
    now = datetime.now().strftime('`%B %d %Y` at `%H:%M:%S`')
    if session['online']:
        message = f"`{name}` has joined `{session['mode']}` in `{session['gameType']}` on {now}"
    else:
        message = f"`{name}` has left hypixel on {now}"
    print(message)
    return message

def main_loop(name):
    import requests
    from time import sleep
    current_session = None
    uuid = requests.get("https://api.mojang.com/users/profiles/minecraft/"+name).json()['id']
    while True:
        df = requests.get(open("api.env", "r").read()+uuid).json()
        if df['session'] != current_session:
            current_session = df['session']
            send_message(write_message(current_session, name))
        sleep(1)




if __name__ == '__main__': # checks if the code is ran as a file
    main_loop("BBernYY") # starts the main function
