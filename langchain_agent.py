from langchain.tools import tool
from langchain.agents import initialize_agent
from langchain_openai import AzureChatOpenAI
import os
from fraud_detection import detect_fraud


# ✅ Tool wrapper
@tool
def fraud_tool():
    """Runs fraud detection on transaction data"""
    data = detect_fraud()
    return data.to_string()


# ✅ LLM setup
llm = AzureChatOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    deployment_name="gpt-4o",
    api_version="2024-02-15-preview"
)


# ✅ Create agent
agent = initialize_agent(
    tools=[fraud_tool],
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True
)


def run_agent(query):
    return agent.run(query)
