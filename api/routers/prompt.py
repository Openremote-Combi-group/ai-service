import httpx
from fastapi import APIRouter
import ollama

from api.service import OpenRemoteService

router = APIRouter(prefix="/prompt", tags=["Prompt"])

openremote_service = OpenRemoteService()


available_tools = {
    "send_request": openremote_service.send_request,
}


@router.get("/query")
async def test():
    ollama_client = ollama.AsyncClient()

    messages = [
        {'role': 'system', 'content': f"""You\'re an AI assistant that helps OpenRemote users, You are able to call every endpoint of the OpenRemote REST API, using the 'send_request' tool.
Here are the OpenAPI specs: {await openremote_service.fetch_openapi_specs()}

Use this to determine the path to call, Make sure the path provides is exactly the same as the one specified in the OpenAPI specs."""},
        {'role': 'user', 'content': f"Can you query all the assets available?"}
    ]

    response = await ollama_client.chat(
        model='llama3.2:3b',
        messages=messages,
        tools=list(available_tools.values())
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

        final_response = await ollama_client.chat('qwen3:14b', messages=messages)
        print('Final response:', final_response.message.content)

    else:
        print('No tool calls found in response')

    print(response)