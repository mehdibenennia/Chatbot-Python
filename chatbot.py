import streamlit as st
from openai import OpenAI
from langchain.agents import AgentExecutor
from langchain.tools import DuckDuckGoSearchRun
from langchain.agents.openai_assistant import OpenAIAssistantRunnable

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

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input for a new message
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get response from OpenAI Assistant
    response = agent_executor.invoke({"content": prompt})['output']
    
    # Display assistant's response
    with st.chat_message("assistant"):
        st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
