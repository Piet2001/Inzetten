import json
import re
from Overige import discord, stats

def sort_key(x):
    raw_id = str(x.get('id', ''))
    m = re.match(r'^(\d+)(.*)', raw_id)
    if m:
        return (int(m.group(1)), m.group(2))
    return (float('inf'), raw_id)

print("start")

live = open('inzetten.json')
data_live = json.load(live)
complete = open('complete.json')
data_complete = json.load(complete)


def id_sort_key(raw_id):
    value = str(raw_id)
    m = re.match(r'^(\d+)(.*)', value)
    if m:
        return (int(m.group(1)), m.group(2))
    return (float('inf'), value)


added_missions = []
removed_missions = []

live_by_id = {
    str(mission.get('id')): mission
    for mission in data_live
    if isinstance(mission, dict) and mission.get('id') is not None
}
complete_by_id = {
    str(mission.get('id')): mission
    for mission in data_complete
    if isinstance(mission, dict) and mission.get('id') is not None
}

live_ids = set(live_by_id.keys())
complete_ids = set(complete_by_id.keys())

added_ids = sorted(live_ids - complete_ids, key=id_sort_key)
removed_ids = sorted(complete_ids - live_ids, key=id_sort_key)

for m in data_live:
    print(f"?? Checking mission {m['id']}")
    mission_id = str(m['id'])
    mc = complete_by_id.get(mission_id)

    if(mc == None):
        print(f"++ {m['id']} doens't exist, will be added")
        complete_by_id[mission_id] = m
        if mission_id in added_ids:
            added_missions.append(mission_id)
    else:
        print(f"+- Comparing mission {m['id']}")
        if (m != mc):
            print(f"--> Updating mission {m['id']}")
        complete_by_id[mission_id] = m

for removed_id in removed_ids:
    print(f"-- {removed_id} no longer exists in inzetten.json, removing")
    complete_by_id.pop(removed_id, None)
    removed_missions.append(removed_id)

data_complete = list(complete_by_id.values())

if removed_missions:
    change_lines = [f"Removed ({len(removed_missions)}): {', '.join(removed_missions)}"]
    discord.webhook(
        "MKS Mission List Update",
        "\n".join(change_lines),
        color="16711680",
    )


data_complete.sort(key=sort_key)
with open('complete.json', 'w', encoding='utf-8') as outfile:
    json.dump(data_complete, outfile, indent=2, ensure_ascii=False)


live.close()
complete.close()
stats.stats()

print("finished")

# --- EVENTS SECTION ---
try:
    events_live = open('events.json')
    data_events_live = json.load(events_live)
except Exception as e:
    print(f"Error opening events.json: {e}")
    data_events_live = []

try:
    events_complete = open('events_complete.json')
    data_events_complete = json.load(events_complete)
except Exception:
    data_events_complete = []

for e in data_events_live:
    print(f"?? Checking event {e['id']}")
    ec = next((x for x in data_events_complete if x["id"] == e["id"]), None)
    if(ec == None):
        print(f"++ {e['id']} doesn't exist, will be added")
        index_live = data_events_live.index(e)
        event_live_prev = data_events_live[index_live - 1] if index_live > 0 else None
        if event_live_prev:
            event_complete_prev = next((x for x in data_events_complete if x["id"] == event_live_prev["id"]), None)
            if event_complete_prev:
                index_complete_prev = data_events_complete.index(event_complete_prev)
                data_events_complete.insert(index_complete_prev + 1, e)
            else:
                data_events_complete.append(e)
        else:
            data_events_complete.insert(0, e)
    else:
        print(f"+- Comparing event {e['id']}")
        if (e != ec):
            print(f"--> Updating event {e['id']}")
            for z in data_events_complete:
                if (z['id'] == e['id']):
                    index = data_events_complete.index(z)
                    data_events_complete[index] = e

data_events_complete.sort(key=sort_key)
with open('events_complete.json', 'w', encoding='utf-8') as outfile:
    json.dump(data_events_complete, outfile, indent=2, ensure_ascii=False)

try:
    events_live.close()
except Exception:
    pass
try:
    events_complete.close()
except Exception:
    pass