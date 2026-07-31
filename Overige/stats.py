import json
from Overige import discord

UP_COLOR = "8388352"
DOWN_COLOR = "16711680"

def stats():
    missions = json.load(open(f"inzetten.json"))
    old = json.load(open(f"Overige/stats.json"))
    output = {}
    normal_missions = []
    alliance_missions = []
    planned_missions = []
    mission_types = []
    
    for mission in missions:
            if "only_alliance_mission" in mission.get('additional'):
                alliance_missions.append(mission)
            elif "guard_mission" in mission.get('additional'):
                planned_missions.append(mission)
            else:
                normal_missions.append(mission)

            for type in mission.get("mission_categories", []):
                if type not in mission_types:
                    mission_types.append(type)


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

    mission_types.sort()

    for type in mission_types:
        type_missions = [v for item in normal_missions if type in item.get("mission_categories", []) and (v := item.get("average_credits")) is not None and isinstance(v, (int, float))]
        if not "generation" in output:
            output["generation"] = {}
        if not type in output["generation"]:
            output["generation"][type] = {}
        output["generation"][type]["mission_amount"] = len(type_missions)
        output["generation"][type]["average_credits"] = round((sum(type_missions) / len(type_missions)),2)

    change_message = ""
    old_generation = old.get("generation", {})
    new_generation = output.get("generation", {})
    up_category_changes = []
    down_category_changes = []

    if output["mission_amount"] != old["mission_amount"]:
        change_message += f"Mission amount changed from {old['mission_amount']} to {output['mission_amount']} ({round(abs(old['mission_amount'] - output['mission_amount']),2)})\n"
    if output["average_credits"] != old["average_credits"]:
        change_message += f"Average credits changed from {old['average_credits']} to {output['average_credits']} ({round(abs(old['average_credits'] - output['average_credits']),2)})\n"

    for category in sorted(new_generation):
        old_category = old_generation.get(category)
        if not old_category:
            new_value = new_generation[category].get("average_credits")
            up_category_changes.append(
                f"Category: {category}\n"
                f"A new category was added with average credits of {new_value}\n"
                f"Mission amount: {new_generation[category].get('mission_amount')}"
            )
            continue

        old_value = old_category.get("average_credits")
        new_value = new_generation[category].get("average_credits")

        if old_value == new_value:
            continue

        difference = round(new_value - old_value, 2)
        direction = "increased" if difference > 0 else "decreased"
        category_message = (
            f"Category: {category}\n"
            f"Average credits {direction} from {old_value} to {new_value}\n"
            f"Change: {difference:+.2f}"
        )
        if difference > 0:
            up_category_changes.append(category_message)
        else:
            down_category_changes.append(category_message)

    for category in sorted(old_generation):
        if category in new_generation:
            continue

        old_value = old_generation[category].get("average_credits")
        down_category_changes.append(
            f"Category: {category}\n"
            f"This category was removed\n"
            f"Previous average credits: {old_value}"
        )

    if up_category_changes:
        discord.webhook("MKS Category Update", "\n\n".join(up_category_changes), color=UP_COLOR)

    if down_category_changes:
        discord.webhook("MKS Category Update", "\n\n".join(down_category_changes), color=DOWN_COLOR)

    if change_message != "":
        print("Changes detected:")
        print(change_message)

        if output["average_credits"] > old["average_credits"]:
            discord.webhook("MKS Stats Update", change_message, color=UP_COLOR)
        else:
            discord.webhook("MKS Stats Update", change_message, color=DOWN_COLOR)

    print("save output")
    with open("./Overige/stats.json", "w+") as outfile:
        json.dump(output, outfile, indent=4)




stats()
