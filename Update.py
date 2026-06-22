import json
import re
from Overige import stats

def sort_key(x):
    m = re.match(r'^(\d+)(.*)', x['id'])
    if m:
        return (int(m.group(1)), m.group(2))
    return (float('inf'), x['id'])

print("start")

live = open('inzetten.json')
data_live = json.load(live)
complete = open('complete.json')
data_complete = json.load(complete)

for m in data_live:
    print(f"?? Checking mission {m['id']}")
    mc = next((x for x in data_complete if x["id"] == m["id"]), None)

    if(mc == None):
        print(f"++ {m['id']} doens't exist, will be added")
        index_live = data_live.index(m)
        mission_live_prev = data_live[index_live - 1]
        mission_complete_prev = next((x for x in data_complete if x["id"] == mission_live_prev["id"]))
        index_complete_prev = data_complete.index(mission_complete_prev)
        data_complete.insert(index_complete_prev + 1, m)
    else:
        print(f"+- Comparing mission {m['id']}")
        if (m != mc):
            print(f"--> Updating mission {m['id']}")
            for z in data_complete:
                if (z['id'] == m['id']):
                    index = data_complete.index(z)
                    data_complete[index] = m


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