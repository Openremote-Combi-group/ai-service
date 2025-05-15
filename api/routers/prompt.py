from fastapi import APIRouter
import ollama
from starlette.responses import HTMLResponse
from starlette.websockets import WebSocket

from api.service import OpenRemoteService

router = APIRouter(prefix="/prompt", tags=["Prompt"])

openremote_service = OpenRemoteService()


available_tools = {
    "fetch_all_assets": openremote_service.fetch_all_assets,
}


@router.get("/query")
async def test():
    ollama_client = ollama.AsyncClient()

    messages = [
        {'role': 'system', 'content': f"""You\'re an AI assistant that helps OpenRemote users. You are able to use the
OpenRemote tools to gather more context the user needs."""},
        {'role': 'user', 'content': f"Can you query all the assets available? Filter out any asset that doesn't have a attribute with the 'rule_state' meta. do this yourself the tool has no parameters you can use."}
    ]

    response = await ollama_client.chat(
        model='llama3.2:latest',
        messages=messages,
        tools=available_tools.values()
    )

    if response.message.tool_calls:
        for tool in response.message.tool_calls:
            # Ensure the function is available, and then call it
            if function_to_call := available_tools.get(tool.function.name):
                print('Calling function:', tool.function.name)
                print('Arguments:', tool.function.arguments)
                output = await function_to_call(**tool.function.arguments)
                print('Function output:', output)
            else:
                print('Function', tool.function.name, 'not found')

        messages.append(response.message)
        messages.append({'role': 'tool', 'content': str(output), 'name': tool.function.name})
        print(messages)

        final_response = await ollama_client.chat('llama3.2:latest', messages=messages)
        print('Final response:', final_response.message.content)
        return final_response.message.content
    else:
        print('No tool calls found in response')

    print(response)
