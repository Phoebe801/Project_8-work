#  module load Globus-CLI/3.18.0-GCCcore-12.2.0
#  python ./ingestmetadata.py

import subprocess
from subprocess import Popen, PIPE, STDOUT
import os,json

rootdir = "./"

entries = []
index_id = "2707914f-bdeb-49ee-a4b8-54e645b3d885"

counter = 1

for root, dirs, files in os.walk(rootdir):
    for name in files:
        full_path = os.path.join(root, name)
        if (name.endswith(("LocustEventProperties.json")) and (os.path.getsize(full_path)) > 0):
            counter += 1;
            with open(full_path) as json_file:
                metadata = json.load(json_file)
                subject = metadata['run-id']
                name = metadata['run-id']
                entries.append(
                    {
                        "subject": subject,
                        "visible_to": ["public"],
                        "content": {
                            "name": name,
                            "raw_metadata" : json.dumps(metadata),
                            "globus": {
                                "transfer": {
                                    "collection": "0f2a4dce-dc3d-468a-86e7-d057c70aacba",
                                    "path": "/spreadsheetData/SpreadsheetRow41_Trap_CCA_V44_TE012/Trap_CCA_long_trap_44_TE012/results/",
                                    "type": "directory"
                                }
                            }
                        }

                    },
                )
                                
                compiledmetadata = {
                    "ingest_type": "GMetaList",
                    "ingest_data": {
                        "gmeta": entries,
                    }
                }

                if (counter%1000==0):
                    with open('data.json', 'w') as file:
                        json.dump(compiledmetadata, file, indent=4) # indent=4 for pretty printing
                        file.close()
                        entries = []
                        process = subprocess.Popen(['globus', 'search', 'ingest', '2707914f-bdeb-49ee-a4b8-54e645b3d885', 'data.json'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        stdout, stderr = process.communicate()
                        # Print the output
                        print(stdout.decode('utf-8'))
                        # Print any errors
                        if stderr:
                            print(stderr.decode('utf-8'))
                        # Check the return code
                        print("Return Code:", process.returncode)



with open('data.json', 'w') as file:
    json.dump(compiledmetadata, file, indent=4) # indent=4 for pretty printing
    file.close()
    entries = []
    process = subprocess.Popen(['globus', 'search', 'ingest', '2707914f-bdeb-49ee-a4b8-54e645b3d885', 'data.json'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    # Print the output
    print(stdout.decode('utf-8'))
    # Print any errors
    if stderr:
        print(stderr.decode('utf-8'))
    # Check the return code
    print("Return Code on final ingest:", process.returncode)



#print(json.dumps(compiledmetadata))

