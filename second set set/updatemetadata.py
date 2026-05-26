from collections import OrderedDict
import os,json

rootdir = 'results/'
usertag = "spreadsheet-row41"
key_order = ["run-type", "simulation-type", "simulation-subtype", "user-defined-tag", "sampling-freq-mega-hz", "configured-e-min", "configured-pitch-min", "configured-x-min", "configured-y-min", "configured-z-min"]

for root, dirs, files in os.walk(rootdir):
    for name in files:
        full_path = os.path.join(root, name)
        if (name.endswith(("LocustEventProperties.json")) and (os.path.getsize(full_path)) > 0):
            with open(full_path) as json_file:
                json_data = json.load(json_file)
                json_data_header = json_data["run-parameters"]
                ordered_data = OrderedDict()
                for key in key_order:
                    if key in json_data_header:                        
                        ordered_data[key] = json_data_header[key]
                        if (key == "user-defined-tag"):
                            ordered_data[key] = usertag
                    else:
                        if (key == "user-defined-tag"):
                            ordered_data[key] = usertag

                json_data["run-parameters"] = ordered_data
                with open(full_path, 'w', encoding='utf-8') as json_file:
                    json.dump(json_data, json_file, indent=4, ensure_ascii=False)
#                print(json.dumps(ordered_data))
#                print(json.dumps(json_data))
