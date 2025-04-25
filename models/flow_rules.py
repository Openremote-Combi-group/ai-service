from typing import Literal
from pydantic import BaseModel, Field


class Inputs(BaseModel):
    assetId: str = Field(description="Id of the asset to be used for the rule")
    attributeName: str = Field(description="Name of the attribute to be used for the rule")


class Processors(BaseModel):
    operator: Literal["add", "subtract", "multiply", "divide"] = Field(description="Processors to be used for the rule")
    inputs: list[Inputs] = Field("List of the inputs that this operator uses.")


class Output(BaseModel):
    assetId: str = Field(description="Id of the asset to be used for the rule")
    attributeName: str = Field(description="Name of the attribute to be used for the rule")
    input: Processors = Field("Processors that is used to calculate the output.")


class FlowRule(BaseModel):
    output: Output = Field(description="The final output where all the input should go into")