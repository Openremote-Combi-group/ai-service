from typing import Literal

from fastapi import APIRouter
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_core.output_parsers import JsonOutputParser, PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from starlette.responses import HTMLResponse
from starlette.websockets import WebSocket

from api import config
from api.response_model import NodeOutput
from api.service import OpenRemoteService

router = APIRouter(prefix="/chat", tags=["chat"])

openremote_service = OpenRemoteService()


available_tools = {
    "fetch_all_assets": openremote_service.fetch_all_assets,
}


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off" value="Create a flow rule that calculates the total area of a city using all the buildings"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/api/v1/chat/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""



@router.get("/ws-debug")
async def get():
    return HTMLResponse(html)

@router.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    # model = ChatOllama(
    #     base_url=config.ollama_host.encoded_string(),
    #     model='llama3.2:3b',
    #     temperature=0.2,
    #     verbose=True
    # )
    model = ChatOpenAI(
        api_key=config.openai_api_key,
        model='gpt-4o',
        temperature=0.2,
    )

    template = ChatPromptTemplate(
        [("system", """You\'re an AI assistant that helps OpenRemote users. {format_instructions}""")]
    )

    while True:
        message = await websocket.receive_text()

        or_service = OpenRemoteService()

        template.append(HumanMessage(f"""{await or_service.fetch_all_assets()}"""))
        template.append(HumanMessage(message))

        parser = JsonOutputParser(pydantic_object=NodeOutput)

        formatted_template = template.format_prompt(
            format_instructions=parser.get_format_instructions()
        )

        print(formatted_template)

        chain = model | parser

        # response = await chain.ainvoke(formatted_template)

        # await websocket.send_json(response)

        async for token in chain.astream(formatted_template):
            await websocket.send_json(token)


@router.post("/test")
async def test(prompt: str):
    # model = ChatOllama(
    #     base_url=config.ollama_host.encoded_string(),
    #     model='llama3.2:3b',
    #     temperature=0.2,
    #     verbose=True
    # )
    model = ChatOpenAI(
        api_key=config.openai_api_key,
        model='gpt-4o',
        temperature=0.2,
    )

    template = ChatPromptTemplate(
        [("system", """You\'re an AI assistant that helps OpenRemote users. {format_instructions}""")]
    )

    or_service = OpenRemoteService()

    template.append(HumanMessage(f"""{await or_service.fetch_all_assets()}"""))
    template.append(HumanMessage(prompt))

    parser = JsonOutputParser(pydantic_object=NodeOutput)

    formatted_template = template.format_prompt(
        format_instructions=parser.get_format_instructions()
    )

    print(formatted_template)

    chain = model | parser

    response = await chain.ainvoke(formatted_template)

    return response

        # await websocket.send_json(response)

    async for token in chain.astream(formatted_template):
        await websocket.send_json(token)
