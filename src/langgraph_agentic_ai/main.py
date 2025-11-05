import streamlit as st 
from src.langgraph_agentic_ai.UI.streamlit_ui.load_ui import LoadStreamlitUI

def load_langgraph_agentic_ai_app():
    """
    Loads and runs LangGraph Agentic AI application with Streamlit UI.
    This function initializes the UI, handles user input, configures the LLM Model, sets up the graph based on the selected use case and displays the output while exception handling for robustness.
    """ 

    print("Load langgraph")

    # Load UI 
    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()

    print("user_input", user_input)

    if not user_input:
        st.error('Error! Failed to load user input from the UI.')
        return 
    
    user_message = st.chat_input("Enter your message")

    if user_message:
        st.write("Hello")