import os
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from tools.tools import web_search_tool, scrape_url_tool
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")

model = init_chat_model(
    model="gemini-3.1-flash-light",
    model_provider="google_genai",
)

def build_search_agent():
    return create_agent(
        model=model,
        tool=[web_search_tool]
        )


def build_reader_agent():
    return create_agent(
        model=model,
        tool=[scrape_url_tool]
        )

# writer chain
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research paper writer. You will be given a topic and you will write a research paper on that topic. You will use the information provided to you to write the research paper. You will not make up any information. You will only use the information provided to you."),
    ("human", """
    Write a research paper on the topic: {topic}. Use the following information to write the research paper: {information}.
    Structure the paper as follows:
    1. Introduction
    2. Literature Review
    3. Methodology
    4. Results
    5. Discussion
    6. Conclusion
    """)
])

writer_chain = writer_prompt | model | StrOutputParser()

# critic chain
critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an sharp expert research paper critic. Be brutally honest and specific in your feedback."),
    ("human", """
    Critique the following research paper: {research_paper}. Provide specific feedback on the following aspects:
    1. Clarity and coherence of the writing
    2. Depth and breadth of the literature review
    3. Appropriateness of the methodology
    4. Validity and reliability of the results
    5. Strength and relevance of the discussion
    6. Overall quality and contribution of the research paper
    """)
])

critic_chain = critic_prompt | model | StrOutputParser()