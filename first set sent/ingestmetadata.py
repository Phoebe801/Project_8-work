#  module load Globus-CLI/3.18.0-GCCcore-12.2.0
#  python ./ingestmetadata.py > meta_test.json
#  globus search ingest 2707914f-bdeb-49ee-a4b8-54e645b3d885 meta_test.json

#import sqlite3
#from globus_sdk import SearchClient
#from globus_sdk import AuthClient
#from globus_sdk import ConfidentialAppAuthClient
import subprocess
from subprocess import Popen, PIPE, STDOUT
import os,json

rootdir = "./"

#CLIENT_ID = '632b533f-4a24-4018-a209-33d23d1d7bfd'       # Your Globus client ID
entries = []
index_id = "2707914f-bdeb-49ee-a4b8-54e645b3d885"
#CLIENT_SECRET = os.environ.get("GLOBUS_CLIENT_SECRET")
# Now use the retrieved client_secret to initialize the ConfidentialAppAuthClient
#confidential_client = ConfidentialAppAuthClient(CLIENT_ID,CLIENT_SECRET)
#search_client = SearchClient(authorizer=confidential_client)


    

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
                                    "path": "/spreadsheetData/SpreadsheetRow39_Trap_CCA_long_trap_44/Trap_CCA_long_trap_44/results/",
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
#                    ingest_result = search_client.ingest(index_id, compiledmetadata)
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
                        
#                    os.system("globus search ingest 2707914f-bdeb-49ee-a4b8-54e645b3d885 data.json")
#                    print(json.dumps(compiledmetadata))
#                    task_id = ingest_result["task_id"]
#                    print(f"Ingest task submitted with task ID: {task_id}")


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

