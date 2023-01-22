from json_to_discord_message import *

def interperet_data(cd, ct, lu, lt):
    import requests
    import datetime
    if not cd["success"]:
        print("epic fail")
        return
    
    player = requests.get("https://playerdb.co/api/player/minecraft/"+cd["uuid"]).json()["data"]["player"]["username"]

    if not (lu["session"]["online"] or cd["session"]["online"]):
        return [f"`{player}` is currently offline.", {}, 'ff0000']

    time_spent = (ct - lt).seconds
    h = (time_spent - time_spent % 3600) // 3600
    m = (time_spent - time_spent % 60 - h*3600) // 60
    s = (time_spent - h*3600 - m*60)

    if not cd["session"]['online']:
        return [f'`{player}` has left `{lu["session"]["gameType"]}`, `{lu["session"]["mode"]}` on `{ct.strftime("%B %d %Y`, `%H:%M:%S")}`', {
            "Previous game": lu["session"]["gameType"],
            "Previous mode": lu["session"]["mode"],
            "Current Time": ct.strftime("%B %d %Y`, `%H:%M:%S"),
            "Time spent": f"{str(h).zfill(2)}:{str(m).zfill(2)}:{str(s).zfill(2)}"
        }, 'ff0000']
    if not lu["session"]['online']:
        return [f'`{player}` has joined `{cd["session"]["gameType"]}` in `{cd["session"]["mode"]}` on `{ct.strftime("%B %d %Y`, `%H:%M:%S")}`', {
            "Current game": cd["session"]["gameType"],
            "Current mode": cd["session"]["mode"],
            "Current Time": ct.strftime("%B %d %Y`, `%H:%M:%S")
        }, '00ff00']

    return [f'`{player}` has moved to `{cd["session"]["mode"]}` in `{cd["session"]["gameType"]}` on `{ct.strftime("%B %d %Y`, `%H:%M:%S")}`', {
        "Current game": cd["session"]["gameType"],
        "Current mode": cd["session"]["mode"],
        "Current Time": ct.strftime("%B %d %Y`, `%H:%M:%S"),
        "Previous game": lu["session"]["gameType"],
        "Previous mode": lu["session"]["mode"],
        "Time spent": f"{str(h).zfill(2)}:{str(m).zfill(2)}:{str(s).zfill(2)}"
    }, '00ff00']

def on_change(cd, ct, lu, lt):
    info = interperet_data(cd, ct, lu, lt)
    send("Update!", info[0], info[1], kwargs['webhook_link'], info[2])


def main():
    import requests
    global kwargs
    from kwargs import kwargs
    if not kwargs['use']:
        kwargs['name'] = input("Playername to track:\n")
        kwargs['hypixel_api_key'] = input("API key:\n")
        kwargs['webhook_link'] = input("Webhook link:\n")

    uuid = requests.get("https://api.mojang.com/users/profiles/minecraft/"+kwargs['name']).json()['id']
    check_for_updates("https://api.hypixel.net/status", {"key": kwargs['hypixel_api_key'], "uuid": uuid}, on_change, 1)

if __name__ == '__main__':
    main()