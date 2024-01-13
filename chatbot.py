import streamlit as st
from openai import OpenAI
from langchain.agents import AgentExecutor
from langchain.tools import DuckDuckGoSearchRun
from langchain.agents.openai_assistant import OpenAIAssistantRunnable
import datetime
import time  # for adding a delay

# Set Streamlit title
st.title("Datawise Bot")

# Initialize OpenAI client with your API key
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Initialize OpenAI Assistant
assistant_id = st.secrets["ASSISTANT_ID"]
tools = [DuckDuckGoSearchRun()]
agent = OpenAIAssistantRunnable(assistant_id="asst_X6RcOFD2WgbBuJoUFM7y2JpU", as_agent=True)
agent_executor = AgentExecutor(agent=agent, tools=tools)

# Initialize messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize a flag for typing indicator
is_typing = False

# Function to simulate typing indicator
def simulate_typing():
    global is_typing
    is_typing = True
    st.session_state.messages.append({"role": "Assistant", "content": "Assistant is typing...", "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
    st.session.sync()
    time.sleep(2)  # Simulate typing for 2 seconds
    is_typing = False
    st.session_state.messages.pop()  # Remove the typing indicator
    st.session.sync()

# Display chat messages
for message in st.session_state.messages:
    role = message["role"]
    content = message["content"]
    timestamp = message["timestamp"]

    # Add timestamps to messages
    with st.container():
        st.write(f"{role} ({timestamp}):")
        with st.chat_message(role):
            st.markdown(content)

# Input for a new message
if prompt := st.text_input("You:", "Type your message here..."):
    # Add user message with timestamp
    user_message = {"role": "User", "content": prompt, "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    st.session_state.messages.append(user_message)
    
    # Display typing indicator
    simulate_typing()
    
    # Get response from OpenAI Assistant
    response = agent_executor.invoke({"content": prompt})['output']
    
    # Add assistant message with timestamp
    assistant_message = {"role": "Assistant", "content": response, "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    st.session_state.messages.append(assistant_message)
