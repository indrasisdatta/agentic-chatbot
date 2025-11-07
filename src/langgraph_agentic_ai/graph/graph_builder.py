from langgraph.graph import StateGraph, START, END
from src.langgraph_agentic_ai.nodes.ai_news_node import AINewsNode
from src.langgraph_agentic_ai.nodes.basic_chatbot import BasicChatbotNode
from src.langgraph_agentic_ai.nodes.chatbot_with_tool_node import ChatbotWithToolNode
from src.langgraph_agentic_ai.state.state import State
from src.langgraph_agentic_ai.tools.search_tool import create_tool_node, get_tools
from langgraph.prebuilt import ToolNode, tools_condition

class GraphBuilder:
    def __init__(self, model):
        self.llm = model 
        self.graph_builder = StateGraph(State)

    def basic_chatbot_build_graph(self):
        """
        Builds a basic chatbot graph using LangGraph.
        This method initializes a chatbot node using the `BasicChatbotNode` class and integrates it into the graph. The chatbot node is set as both the entry and exit point of the graph.
        """

        self.basic_chatbot_node = BasicChatbotNode(self.llm)

        self.graph_builder.add_node("chatbot", self.basic_chatbot_node.process)    
        self.graph_builder.add_edge(START, "chatbot") 
        self.graph_builder.add_edge("chatbot", END) 

    def chatbot_with_tools_build_graph(self):
        """
        Builds an advanced chatbot graph with tool integration using LangGraph.
        This method creates a chatbot graph that includes both a chatbot node and a tool node. It defines tools, initializes the chatbot with tool capabilities and sets up conditional and direct edges between nodes. The chatbot node is set as the entry point.
        """
        # Define the tool and ToolNode 
        tools = get_tools()
        tool_node = create_tool_node(tools)

        # Define the LLM
        llm = self.llm 

        # Define the chatbot node 
        chatbot_node = ChatbotWithToolNode(llm).create_chatbot(tools)

        # Add nodes 
        self.graph_builder.add_node("chatbot", chatbot_node)
        self.graph_builder.add_node("tools", tool_node)

        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_conditional_edges("chatbot", tools_condition)
        self.graph_builder.add_edge("tools", "chatbot")
        self.graph_builder.add_edge("chatbot", END)

    def ai_news_builder_graph(self):
        ai_news_node = AINewsNode(self.llm)
        # Add nodes
        self.graph_builder.add_node("fetch_news", ai_news_node.fetch_news)
        self.graph_builder.add_node("summarize_news", ai_news_node.summarize_news)
        self.graph_builder.add_node("save_result", ai_news_node.save_result)

        # Add edges
        self.graph_builder.add_edge(START, "fetch_news")
        self.graph_builder.add_edge("fetch_news", "summarize_news")
        self.graph_builder.add_edge("summarize_news", "save_result")
        self.graph_builder.add_edge("save_result", END)

        
    def setup_graph(self, usecase: str):
        """
        Sets up the graph for the selected use case.
        """
        if usecase == "Basic Chatbot":
            self.basic_chatbot_build_graph()
        elif usecase == "Chatbot with Web":
            self.chatbot_with_tools_build_graph()
        elif usecase == "AI News":
            self.ai_news_builder_graph()

        return self.graph_builder.compile()
    
     