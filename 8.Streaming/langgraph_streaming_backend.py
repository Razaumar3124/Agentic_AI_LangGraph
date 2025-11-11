from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import BaseMessage, HumanMessage
from typing import TypedDict, Annotated
from dotenv import load_dotenv

load_dotenv()

model = ChatGroq(model="llama-3.1-8b-instant")

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    
def chat_node(state: ChatState) -> ChatState:
    messages = state['messages']
    response = model.invoke(messages)
    return {"messages": [response]}

graph = StateGraph(ChatState)

graph.add_node("chat_node", chat_node)

graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

checkpoint = InMemorySaver()

chatbot = graph.compile(checkpointer=checkpoint)

# for message_chunk, metadata in chatbot.stream(
#     {"messages": [HumanMessage(content="what is the recipe to make pasta")]},
#     config = {"configurable": {"thread_id": "thread-1"}},
#     stream_mode = "messages"
# ):
#     if message_chunk.content:
#         print(message_chunk.content, end=" ", flush=True)

