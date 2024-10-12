from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_community.tools.tavily_search import TavilySearchResults
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from typing import Annotated

app = Flask(__name__)

# 環境設定
load_dotenv()
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
TAVILY_API_KEY = os.getenv('TAVILY_API_KEY')

# モデルとツールの設定
tool = TavilySearchResults(max_results=2)
tools = [tool]
llm = ChatAnthropic(model="claude-3-5-sonnet-20240620")
llm_with_tools = llm.bind_tools(tools)

# グラフの定義
class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)

def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

graph_builder.add_node("chatbot", chatbot)

tool_node = ToolNode(tools=[tool])
graph_builder.add_node("tools", tool_node)

graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)
graph_builder.add_edge("tools", "chatbot")
graph_builder.set_entry_point("chatbot")
graph = graph_builder.compile()

# ルートページ
@app.route('/')
def index():
    return render_template('index.html')

# チャットエンドポイント
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['message']
    response = ""
    for event in graph.stream({"messages": [("user", user_input)]}):
        for value in event.values():
            response = value["messages"][-1].content
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)