from langchain_core.messages import HumanMessage
from langgraph_backend import chatbot, retreive_all_threads
import streamlit as st
import uuid

# ************************************** Utility functions ******************************

def generate_thread_id():
    """Generate a unique thread ID for each chat session"""
    return uuid.uuid4()

def reset_chat():
    """Reset chat and create a new conversation thread"""
    thread_id = generate_thread_id()
    st.session_state["thread_id"] = thread_id
    add_thread(st.session_state["thread_id"])
    st.session_state["messages_history"] = []

def add_thread(thread_id):
    """Add a thread ID to the session state if not already present"""
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)
        
def load_conversations(thread_id):
    """Load stored messages for a given thread"""
    state = chatbot.get_state(config={"configurable": {"thread_id": thread_id}})
    messages = state.values.get("messages", [])
    return messages

# ************************************** Session setup **********************************
if "messages_history" not in st.session_state:
    st.session_state["messages_history"] = [] 
    
if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()
    
if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = retreive_all_threads()
    
add_thread(st.session_state["thread_id"])

# **************************************** Sidebar UI ***********************************

st.sidebar.title("LangGraph Chatbot")

if st.sidebar.button("New Chat"):
    reset_chat()

st.sidebar.header("My Conversations")

for thread_id in st.session_state["chat_threads"][::-1]:
    if st.sidebar.button(str(thread_id)):
        st.session_state["thread_id"] = thread_id
        messages = load_conversations(thread_id)
        
        temp_messages = []
        for msg in messages:
            role = "user" if isinstance(msg, HumanMessage) else "assistant"
            temp_messages.append({"role": role, "content": msg.content})
            
        st.session_state["messages_history"] = temp_messages
        
# ****************************************** Main UI *************************************

# Display message history
for message in st.session_state["messages_history"]:
    with st.chat_message(message["role"]):
        st.text(message["content"])

# Chat input
user_input = st.chat_input("Type here...")

if user_input:
    # Display user input
    st.session_state["messages_history"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.text(user_input)
        
    # CONFIG = {"configurable": {"thread_id": st.session_state["thread_id"]}, "run_name": "obv1"}
    
    CONFIG = {
        "configurable": {"thread_id": st.session_state["thread_id"]},
        "metadata": {"thread_id": st.session_state["thread_id"]},
        "run_name": "chat_turn",
    }
    
    # ✅ Only one chatbot call (streaming mode)
    with st.chat_message("assistant"):
        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode="messages"
            )
        )
        
    # Save assistant response
    st.session_state["messages_history"].append({"role": "assistant", "content": ai_message})
