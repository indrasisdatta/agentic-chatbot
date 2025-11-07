import streamlit as st 
from src.langgraph_agentic_ai.LLMS.groq_llm import GroqLLM
from src.langgraph_agentic_ai.UI.streamlit_ui.display_result import DisplayResultsStreamlit
from src.langgraph_agentic_ai.UI.streamlit_ui.load_ui import LoadStreamlitUI
from src.langgraph_agentic_ai.graph.graph_builder import GraphBuilder

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
    
    if st.session_state.fetch_ai_btn_clicked:
        user_message = st.session_state.time_frame
    else:    
        user_message = st.chat_input("Enter your message")

    if user_message:
        try:
            # Configure the LLMs
            obj_llm_config = GroqLLM(user_controls_input=user_input)
            model = obj_llm_config.get_llm_model()

            if not model:
                st.error("LLM model couldn't be initialized")
                return 
            
            # Initialize and set up graph based on input 
            usecase = user_input.get("selected_usecase")

            if not usecase:
                st.error("Error: No use case selected")
                return 
            
            # Graph builder
            graph_builder = GraphBuilder(model)
            try:
                graph = graph_builder.setup_graph(usecase)
                print('Graph --> ', graph)
                DisplayResultsStreamlit(usecase, graph, user_message).display_results_on_ui()
            except Exception as e:
                st.error(f'Error: graph setup failed {e}')

        except Exception as e:
            raise ValueError(f"Error occurred with exception: {e}")
