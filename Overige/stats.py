import json
from Overige import discord

def stats():
    missions = json.load(open(f"Inzetten.json"))
    old = json.load(open(f"Overige/stats.json"))
    output = {}
    normal_missions = []
    alliance_missions = []
    planned_missions = []
    
    for mission in missions:
            if "only_alliance_mission" in mission.get('additional'):
                alliance_missions.append(mission)
            elif "guard_mission" in mission.get('additional'):
                planned_missions.append(mission)
            else:
                normal_missions.append(mission)


    normal = [v for item in normal_missions if (v := item.get("average_credits")) is not None and isinstance(v, (int, float))]
    alliance = [v for item in alliance_missions if (v := item.get("average_credits")) is not None and isinstance(v, (int, float))]
    planned = [v for item in planned_missions if (v := item.get("average_credits")) is not None and isinstance(v, (int, float))]

    output["mission_amount"] = len(normal_missions)
    output["average_credits"] = round((sum(normal) / len(normal)),2)
    output["min_credits"] = min(normal)
    output["max_credits"] = max(normal)
    output["alliance_mission_amount"] = len(alliance_missions)
    output["alliance_Average_credits"] = round((sum(alliance) / len(alliance)))
    output["planned_mission_amount"] = len(planned_missions)
    output["planned_Average_credits"] = round((sum(planned) / len(planned)))

    change_message = ""

    if output["mission_amount"] != old["mission_amount"]:
        change_message += f"Mission amount changed from {old['mission_amount']} to {output['mission_amount']}\n"
    if output["average_credits"] != old["average_credits"]:
        change_message += f"Average credits changed from {old['average_credits']} to {output['average_credits']}\n"

    if change_message != "":
        print("Changes detected:")
        print(change_message)
        discord.webhook("MKS Stats Update", change_message)

    print("save output")
    with open("./Overige/stats.json", "w+") as outfile:
        json.dump(output, outfile, indent=4)




stats()