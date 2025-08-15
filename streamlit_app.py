import streamlit as st
from crewai import Agent, Task, Crew, LLM
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize LLM and tools
llm = LLM(model="gpt-3.5-turbo")
search_tool = SerperDevTool(n=10)

# Define Agents
senior_research_analyst = Agent(
    role="Senior Research Analyst",
    goal="Research and analyze comprehensive information on a given topic.",
    backstory="Expert in web research, analysis, and fact-checking.",
    allow_delegation=False,
    verbose=True,
    tools=[search_tool],
    llms=[llm]
)

content_writer = Agent(
    role="Content Writer",
    goal="Transform research findings into an engaging blog post.",
    backstory="Skilled in content writing with a balance of accuracy and readability.",
    allow_delegation=False,
    verbose=True,
    llms=[llm]
)

# Streamlit UI
st.title("AI-Powered Blog Generator")
st.write("Enter a topic to generate a research-based blog post.")

# User input
topic = st.text_input("Enter a topic:", "Technology")

if st.button("Generate Blog Post"):
    with st.spinner("Generating..."):
        # Define Tasks
        research_tasks = Task(
            description=f"""
                1. Conduct research on {topic}
                2. Evaluate credibility and fact-check information
                3. Organize findings into a structured report
            """,
            expected_output="A detailed research report with citations.",
            agent=senior_research_analyst
        )

        writing_task = Task(
            description="""
                Create an engaging blog post based on the research.
            """,
            expected_output="A well-structured blog post in markdown format.",
            agent=content_writer
        )

        # Run CrewAI
        crew = Crew(
            agents=[senior_research_analyst, content_writer],
            tasks=[research_tasks, writing_task],
            verbose=True
        )

        # Get the crew result
        result = crew.kickoff(inputs={"topic": topic})
        result_text = str(result)
        
        # Display result
        st.markdown(result_text)
