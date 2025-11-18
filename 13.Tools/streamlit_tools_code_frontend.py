import streamlit as st
import uuid
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langGraph_tool_backend import chatbot, retreive_all_threads

# ---------------------------------------------------
# Utility Functions
# ---------------------------------------------------

def generate_thread_id():
    return uuid.uuid4()

def add_thread(thread_id):
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state["thread_id"] = thread_id
    add_thread(thread_id)
    st.session_state["messages_history"] = []

def load_conversations(thread_id):
    state = chatbot.get_state(config={"configurable": {"thread_id": thread_id}})
    messages = state.values.get("messages", [])

    # Convert LC messages → Streamlit format
    formatted = []
    for msg in messages:
        if isinstance(msg, HumanMessage):
            formatted.append({"role": "user", "content": msg.content})
        elif isinstance(msg, AIMessage):
            formatted.append({"role": "assistant", "content": msg.content})

    return formatted


# ---------------------------------------------------
# Streamlit Session Setup
# ---------------------------------------------------

st.set_page_config(page_title="LangGraph Chatbot", layout="wide")

if "messages_history" not in st.session_state:
    st.session_state["messages_history"] = []

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()

if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = retreive_all_threads()

add_thread(st.session_state["thread_id"])

# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------

st.sidebar.title("💬 LangGraph Chatbot")
st.sidebar.markdown("---")

if st.sidebar.button("🆕 New Chat"):
    reset_chat()

st.sidebar.subheader("📁 My Conversations")

# Scrollable area
with st.sidebar.container():
    for thread_id in st.session_state["chat_threads"][::-1]:

        is_active = (thread_id == st.session_state["thread_id"])
        button_label = f"🟢 {thread_id}" if is_active else f"⚪ {thread_id}"

        if st.sidebar.button(button_label):
            st.session_state["thread_id"] = thread_id
            st.session_state["messages_history"] = load_conversations(thread_id)


# ---------------------------------------------------
# Main Chat UI
# ---------------------------------------------------

st.title("🤖 LangGraph Chatbot")

# Chat bubble style
def chat_bubble(role, text):
    if role == "user":
        st.markdown(f"""
        <div style="
            background:#DCF8C6;
            padding:12px;
            border-radius:10px;
            margin-bottom:8px;
            max-width:85%;
            float:right;
            clear:both;">
            {text}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="
            background:#F1F0F0;
            padding:12px;
            border-radius:10px;
            margin-bottom:8px;
            max-width:85%;
            float:left;
            clear:both;">
            {text}
        </div>
        """, unsafe_allow_html=True)


# Display messages
for msg in st.session_state["messages_history"]:
    chat_bubble(msg["role"], msg["content"])

st.markdown("<br><br>", unsafe_allow_html=True)

# ---------------------------------------------------
# Chat Input
# ---------------------------------------------------

user_input = st.chat_input("Type your message...")

if user_input:
    # Add user message
    st.session_state["messages_history"].append({"role": "user", "content": user_input})
    chat_bubble("user", user_input)

    CONFIG = {
        "configurable": {"thread_id": st.session_state["thread_id"]},
        "metadata": {"thread_id": st.session_state["thread_id"]},
        "run_name": "chat_turn"
    }

    with st.chat_message("assistant"):
        status_holder = {"box": None}

        def generate_stream():
            """Streaming response from LangGraph"""
            for chunk, meta in chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode="messages"
            ):

                if isinstance(chunk, ToolMessage):
                    tool_name = getattr(chunk, "name", "Tool")

                    if status_holder["box"] is None:
                        status_holder["box"] = st.status(
                            f"🛠 Running tool `{tool_name}`...", expanded=True
                        )
                    else:
                        status_holder["box"].update(
                            label=f"🛠 Running tool `{tool_name}`...",
                            state="running"
                        )

                elif isinstance(chunk, AIMessage):
                    yield chunk.content

        ai_response = st.write_stream(generate_stream())

        if status_holder["box"] is not None:
            status_holder["box"].update(
                label="✅ Tool execution completed",
                state="complete"
            )

    # Save assistant message
    if ai_response:
        st.session_state["messages_history"].append(
            {"role": "assistant", "content": ai_response}
        )
