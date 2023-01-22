import old as mn
def generate_embed(title, description, json, color=None):
    from discord_webhook import DiscordEmbed
    embed = DiscordEmbed(title=title, description=description)
    for name, value in json.items():
        embed.add_embed_field(name=str(name), value=f"`{str(value)}`")
    if color:
        embed.set_color(color)
    return embed



def send(title, description, json, webhook_link, color=None):
    from discord_webhook import DiscordWebhook
    webhook = DiscordWebhook(url=webhook_link)
    webhook.add_embed(generate_embed(title, description, json, color=color))
    webhook.execute()

def check_for_updates(api_url, params, detection_function, interval_seconds):
    import requests
    import time, datetime
    api_url += "?"
    for k, v in params.items():
        api_url += f"{str(k)}={str(v)}&"
    run = True
    previous_data = None
    last_update = {"session": {"online": False}}
    last_update_time = datetime.datetime(year=1970, month=1, day=1, hour=0, minute=0, second=0)
    while run:
        time.sleep(interval_seconds)
        current_data = requests.get(api_url).json()
        if (current_data != previous_data) or (previous_data == None):
            detection_function(current_data, datetime.datetime.now(), last_update, last_update_time)
            last_update = current_data
            last_update_time = datetime.datetime.now()
        previous_data = current_data