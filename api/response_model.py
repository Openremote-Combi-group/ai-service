from typing import Literal

from pydantic import BaseModel, Field


class Asset(BaseModel):
    id: str
    attributeName: str


class NodePosition(BaseModel):
    x: int
    y: int


class NodeAssetPicker(BaseModel):
    assetId: str = Field(description="Id of the Asset")
    attributeName: str = Field(description="Name of the Asset attribute to be used.")


class Picker(BaseModel):
    type: Literal["ASSET_ATTRIBUTE"]

class NodeInternal(BaseModel):
    name: str
    picker: Picker
    value: NodeAssetPicker


class NodeSocket(BaseModel):
    id: str = Field(description="Random generated id", min_length=10, max_length=10)
    name: str
    nodeId: str = Field(description="Id of the node this socket belongs to.", min_length=10, max_length=10)
    type: Literal["NUMBER"]


class Node(BaseModel):
    id: str = Field(description="Random generated id", min_length=10, max_length=10)
    name: Literal["READ_ATTRIBUTE", "ADD_OPERATOR", "WRITE_ATTRIBUTE"]
    type: Literal["INPUT", "OUTPUT", "PROCESSOR"]
    position: NodePosition
    internals: list[NodeInternal] = Field(description="List of internals that reference an asset")
    outputs: list[NodeSocket] = Field("Output sockets that Input sockets can connect to. INPUT & PROCESSOR always has 1 & OUTPUT has none.")
    inputs: list[NodeSocket] = Field("Input sockets that Output sockets can connect to. INPUT has none, PROCESSOR always has 2 & OUTPUT always has 1.")


class NodeConnection(BaseModel):
    nodeSocketId1: str = Field(description="1st id of the node socket to connect to.", min_length=10, max_length=10)
    nodeSocketId2: str = Field(description="2nd id of the node socket to connect to.", min_length=10, max_length=10)


class NodeOutput(BaseModel):
    nodes: list[Node] = Field(description="List of nodes inside the rules.")
    connections: list[NodeConnection] = Field(description="List of node connection that determine how nodes socket should connect.")
