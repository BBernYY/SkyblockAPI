def send_message(webhook_link, content): # function for uploading data 
    from discord_webhook import DiscordWebhook
    webhook = DiscordWebhook(url=webhook_link, content=content)
    webhook.execute() # send message on webhook
def write_message(session, name): # function for formatting data
    import datetime as dt
    now = dt.datetime.now(dt.timezone(dt.timedelta(hours=+2))).strftime('`%B %d %Y` at `%H:%M:%S`')
    if session['online']:
        message = f"`{name}` has joined `{session['mode']}` in `{session['gameType']}` on {now}"
    else:
        message = f"`{name}` has left hypixel on {now}"
    print(message)
    return message

def main_loop(_, hypixel_api_key, webhook_link, name):
    import requests
    from time import sleep
    current_session = {"online": False}
    uuid = requests.get("https://api.mojang.com/users/profiles/minecraft/"+name).json()['id']
    while True:
        df = requests.get('https://api.hypixel.net/status?key='+hypixel_api_key+'&uuid='+uuid).json()
        if df['session'] != current_session:
            current_session = df['session']
            send_message(webhook_link, write_message(current_session, name))
        sleep(1) # prevent ratelimiting

if __name__ == '__main__': # checks if the code is ran as a file
  from kwargs import kwargs
  if kwargs['_']:
    print("Using external settings.")
    main_loop(**kwargs)
  else:
    print("No external settings found.")
    main_loop(None, 'https://api.hypixel.net/status?key='+input("Enter Hypixel api key:\n")+'&uuid=', input("Enter discord webhook link:\n"), input("Enter player to track:\n"))
