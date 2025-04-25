from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import JsonOutputParser
from openremote_service import OpenRemoteService
from models import FlowRule
from api.config import config


openremote_service = OpenRemoteService()


class AiService:
    def generate_json_llm_chain(self, prompt: str, model: str, temperature: float = 0.2) -> ChatOllama:
        model = ChatOllama(
            base_url=config.ollama_url.encoded_string(),
            model=model,
            temperature=temperature,
        )

        parser = JsonOutputParser(pydantic_object=FlowRule)

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