from typing import Tuple, List
from google.oauth2 import service_account
import google.auth.transport.requests
import os
from langchain_core.tools import tool, Tool
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, ToolMessage
from dotenv import load_dotenv

load_dotenv()

a_base_folder = '/home/yosalfa/my_stuffs/tmp/a'
b_base_folder = '/home/yosalfa/my_stuffs/tmp/b'
# a_files = [ a_base_folder + '/' + file for file in ['a', 'b', 'c', 'd']]
a_files = ['a', 'b', 'c', 'd']
# b_files = [ b_base_folder + '/' + file for file in ['c', 'd', 'e', 'f']]
b_files = ['c', 'd', 'e', 'f']

@tool
def listLocalDirectory(path: str) -> Tuple[List[str], List]:
    """Return list of directories and files as tuple in the specified local path"""
    
    folders = []
    files = []
    # for entry in os.listdir(path):
    #     if os.path.isdir(os.path.join(path, entry)):
    #         folders.append(os.path.join(path, entry))
    #     else:
    #         files.append(os.path.join(path, entry))

    if (path == "/home/yosalfa/my_stuffs/tmp/a"):
        files = a_files

    if (path == "/home/yosalfa/my_stuffs/tmp/b"):
        files = b_files

    return (folders, files)

@tool
def copyFiles(files: List[str], dest_folder: str):
    """Copy files or folder to destination folder"""
    if (dest_folder == '/home/yosalfa/my_stuffs/tmp/a'):
        for file in files:
            a_files.append(file)

    if (dest_folder == '/home/yosalfa/my_stuffs/tmp/b'):
        for file in files:
            b_files.append(file)




base_url = "https://ollama-gemma-644138903664.us-central1.run.app"

def getOllamaAPIKey() -> str:
    key_path = "./key.json"
    # OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")
    credentials = service_account.IDTokenCredentials.from_service_account_file(
        key_path, target_audience=base_url
    )
    credentials.refresh(google.auth.transport.requests.Request())
    id_token_value = credentials.token

    return id_token_value

def find_tool_by_name(tools: List[Tool], tool_name: str) -> Tool:
    for tool in tools:
        if tool.name == tool_name:
            return tool

def createOllamaLLM():
    llm = ChatOllama(
        temperature=0,
        model="mistral-nemo:latest",
        client_kwargs={
            "headers": {
                "Authorization": f"Bearer {getOllamaAPIKey()}"
            }
        },
        base_url=base_url
    )

    return llm


def createChatOpenAILLM():
    llm = ChatOpenAI(
        temperature=0
    )

    return llm


def main():
    tools = [listLocalDirectory, copyFiles]

    # base_url = "https://ollama-gemma-644138903664.us-central1.run.app"
    # llm = ChatOllama(
    #     temperature=0,
    #     model="mistral-nemo:latest",
    #     client_kwargs={
    #         "headers": {
    #             "Authorization": f"Bearer {getOllamaAPIKey()}"
    #         }
    #     },
    #     base_url=base_url
    # )
    #llm = createChatOpenAILLM()
    llm = createOllamaLLM()
    llm_with_tools = llm.bind_tools(tools)

    messages = [HumanMessage(
        # content="Compare the content of folder /home/yosalfa/my_stuffs/tmp/a and "
        #         "folder /home/yosalfa/my_stuffs/tmp/b. Then provide list of same files by name"
        #         "in both directory and list of different files by name in both directory"
        content="First I need you to provide list of files/folders need to be copied "
        "to make content of the following directories: /home/yosalfa/my_stuffs/tmp/a and "
        "/home/yosalfa/my_stuffs/tmp/b equal. Do not include in the list files/folders that exist "
        "in both directories." 
        "Second I need you to copy the differences files to appropriate folder to make both folder same"
    )]

    while True:
        ai_message = llm_with_tools.invoke(messages)
        tool_calls = getattr(ai_message, "tool_calls", None) or []

        if len(tool_calls) > 0:
            messages.append(ai_message)
            for tool_call in tool_calls:
                tool_name = tool_call.get("name")
                tool_args = tool_call.get("args", {})
                tool_call_id = tool_call.get("id")

                tool_to_use = find_tool_by_name(tools, tool_name)
                observation = tool_to_use.invoke(tool_args)

                messages.append(
                    ToolMessage(content=str(observation), tool_call_id=tool_call_id)
                )

            continue
        print(ai_message.content)
        break

    print(f"folder a:\n{a_files}")
    print(f"folder b:\n{b_files}")

if __name__ == "__main__":
    main()
