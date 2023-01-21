def send_message(webhook_link, embed): # function for uploading data 
    from discord_webhook import DiscordWebhook
    webhook = DiscordWebhook(url=webhook_link)
    webhook.add_embed(embed)
    webhook.execute() # send message on webhook

def generate_embed(session, name, now, old_session, old_now):
    from discord_webhook import DiscordEmbed
    from datetime import datetime as dt
    if session != "None":
        embed = DiscordEmbed(title="Update!", description=f'`{name}` has joined `{session["gameType"]}` in `{session["mode"]}` on {now}')
        embed.add_embed_field(name='Current game', value=f"`{session['gameType']}`")
        embed.add_embed_field(name='Current mode', value=f"`{session['mode']}`")
        embed.add_embed_field(name='Current time', value=now)
        if old_session['online']:
            embed.add_embed_field(name='Previous game', value=f"`{old_session['gameType']}`")
            embed.add_embed_field(name='Previous mode', value=f"`{old_session['mode']}`")
            time_spent = dt.strptime(now, '`%B %d %Y`, `%H:%M:%S`') - dt.strptime(old_now, '`%B %d %Y`, `%H:%M:%S`')
            time_spent = time_spent.seconds
            hours = (time_spent-time_spent%3600) // 3600
            time_spent -= hours * 3600
            mins = (time_spent-time_spent%60) // 60
            time_spent -= mins * 60
            embed.add_embed_field(name='Time spent', value=f'`{str(hours).zfill(2)}:{str(mins).zfill(2)}:{str(time_spent).zfill(2)}`')
        embed.set_color('0x00ff00')
    else:
        embed = DiscordEmbed(title="Update!", description=f'`{name}` has left `{old_session["gameType"]}`, `{old_session["mode"]}` on {now}')
        embed.add_embed_field(name='Previous game', value=f"`{old_session['gameType']}`")
        embed.add_embed_field(name='Previous mode', value=f"`{old_session['mode']}`")
        embed.add_embed_field(name='Current time', value=now)
        embed.set_color('0xff0000')
    
    return embed
def write_message(session, name, old_session, old_now): # function for formatting data
    import datetime as dt
    now = dt.datetime.now(dt.timezone(dt.timedelta(hours=+1))).strftime('`%B %d %Y`, `%H:%M:%S`')
    if session['online']:
        embed = generate_embed(session, name, now, old_session, old_now)
    else:
        embed = generate_embed("None", name, now, old_session, old_now)
    return [embed, now]

def main_loop(_, hypixel_api_key, webhook_link, name):
    import requests
    from time import sleep
    current_session = {"online": False}
    uuid = requests.get("https://api.mojang.com/users/profiles/minecraft/"+name).json()['id']
    old_now = None
    while True:
        df = requests.get(hypixel_api_key+uuid).json()
        if df['session'] != current_session:
            old_session = current_session
            current_session = df['session']
            embed, old_now = write_message(current_session, name, old_session, old_now)
            send_message(webhook_link, embed)
        sleep(1) # prevent ratelimiting

def main(): # checks if the code is ran as a file
  from kwargs import kwargs
  if kwargs['_']:
    kwargs['hypixel_api_key'] = 'https://api.hypixel.net/status?key='+kwargs['hypixel_api_key']+'&uuid='
    print("Using external settings.")
    main_loop(**kwargs)
  else:
    print("No external settings found.")
    main_loop(None, 'https://api.hypixel.net/status?key='+input("Enter Hypixel api key:\n")+'&uuid=', input("Enter discord webhook link:\n"), input("Enter player to track:\n"))
if __name__ == '__main__':
    main()