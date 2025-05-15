import ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.utils.pydantic import TBaseModel
from langchain_ollama.chat_models import ChatOllama
from langchain_core.output_parsers import JsonOutputParser

from api.schemas import Model
from openremote_service import OpenRemoteService
from api.config import config


openremote_service = OpenRemoteService()


class AiService:
    @staticmethod
    async def list_available_models() -> list[Model]:
        ollama_client = ollama.AsyncClient()

        available_models: list[Model] = []

        ollama_models = await ollama_client.list()
        for model in ollama_models.models:
            available_models.append(Model(name=model.name, provider="Ollama"))

        return available_models

    @classmethod
    async def get_model_factory(cls, model: str) -> ChatOllama:
        # if model not in await self.list_available_models():
        #     pass

        return ChatOllama(
            base_url=config.ollama_url.encoded_string(),
            model=model,
        )

    def prompt_with_tools(self, prompt: str, model: str, temperature: float = 0.2, response_object: type[TBaseModel] | None = None):
        model = ChatOllama(
            base_url=config.ollama_host.encoded_string(),
            model=model,
        )
        model.temperature = temperature

        parser = JsonOutputParser()

        template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a system that generates OpenRemote automation rules, {format_instructions}"
                ),
                ("user", "{prompt}"),
            ]
        )

        formatted_template = template.format_prompt(
            format_instructions=parser.get_format_instructions(),
            prompt=prompt,
        )

        chain = model | parser


    def generate_json_llm_chain(self, prompt: str, model: str, temperature: float = 0.2) -> ChatOllama:
        model = ChatOllama(
            base_url=config.ollama_url.encoded_string(),
            model=model,
            temperature=temperature,
        )

        parser = JsonOutputParser()

        template = ChatPromptTemplate.from_messages(
            [
                (
                    "You are a system that generates OpenRemote automation rules, {format_instructions}"
                ),
                ("user", "{prompt}, Here are the available assets: {assets}"),
            ]
        )

        formatted_template = template.format_prompt(
            assets=openremote_service.fetch_assets(),
            format_instructions=parser.get_format_instructions(),
            prompt=prompt
        )

        chain = model | parser

        result = None

        for text in chain.stream(formatted_template):
            print(text)
            result = text

        return result