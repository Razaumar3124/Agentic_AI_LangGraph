from langchain_core.messages import HumanMessage
from langgraph_streaming_backend import chatbot
import streamlit as st

CONFIG = {"configurable": {"thread_id": "thread-1"}}

if "messages_history" not in st.session_state:
    st.session_state["messages_history"] = []
    
for message in st.session_state["messages_history"]:
    with st.chat_message(message["role"]):
        st.text(message["content"])
        
user_input = st.chat_input("Type here")

if user_input:
    st.session_state["messages_history"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.text(user_input)
        
    response = chatbot.invoke({"messages": [HumanMessage(content=user_input)]}, config=CONFIG)
    
    # st.session_state["messages_history"].append({"role": "assistant", "content": ai_response})
    with st.chat_message("assistant"):
        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config = CONFIG,
                stream_mode = "messages"
            )
        )
    
    st.session_state["messages_history"].append({"role": "assistant", "content": ai_message})