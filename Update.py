import json
import time

print("start")

live = open('inzetten.json')
data_live = json.load(live)
complete = open('complete.json')
data_complete = json.load(complete)

for m in data_live:
    print(f"Checking mission {m['id']}")
    mc = next((x for x in data_complete if x["id"] == m["id"]), None)

    if(mc == None):
        print(f"{m['id']} doens't exist, will be added")
        data_complete.append(m)
    else:
        print(f"Comparing mission {m['id']}")
        if (m != mc):
            print(f"Updating mission {m['id']}")
            for z in data_complete:
                if (z['id'] == m['id']):
                    index = data_complete.index(z)
                    print(index)
                    data_complete[index] = m


with open('complete.json', 'w') as outfile:
    json.dump(data_complete, outfile)


live.close()
complete.close()

print("finished")