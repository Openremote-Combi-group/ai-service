from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.chat_models import ChatOllama
from langchain_core.output_parsers import JsonOutputParser
from openremote_service import OpenRemoteService
from api.config import config


openremote_service = OpenRemoteService()


class AiService:
    def prompt_with_tools(self, prompt: str, model: str, temperature: float = 0.2):
        model = ChatOllama(
            base_url=config.ollama_host.encoded_string(),
            model=model,
            temperature=temperature,
        )

        parser = JsonOutputParser()

        template = ChatPromptTemplate.from_messages(
            [
                (
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