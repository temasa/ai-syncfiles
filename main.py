from typing import Tuple, List
from google.oauth2 import service_account
import google.auth.transport.requests
import os

def listLocalDirectory(path: str) -> Tuple[List[str], List]:
    """Return list of directories and files as tuple in the specified local path"""
    
    folders = []
    files = []
    for entry in os.listdir(path):
        if os.path.isdir(os.path.join(path, entry)):
            folders.append(os.path.join(path, entry))
        else:
            files.append(os.path.join(path, entry))

    return (folders, files)



def getOllamaAPIKey() -> str:
    key_path = "./key.json"
    # OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")
    base_url = "https://ollama-gemma-644138903664.us-central1.run.app"
    credentials = service_account.IDTokenCredentials.from_service_account_file(
        key_path, target_audience=base_url
    )
    credentials.refresh(google.auth.transport.requests.Request())
    id_token_value = credentials.token

    return id_token_value

def main():
    # token = getOllamaAPIKey()
    # print(f'token:\n{token}')

    subfolders, filenames = listLocalDirectory("/home/yosalfa/my_stuffs/software_sources")


if __name__ == "__main__":
    main()
