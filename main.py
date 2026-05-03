import os
import json
import re
import smtplib

from email.mime.text import MIMEText

from pydantic import BaseModel, Field
from typing import List, Optional

# from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

from dotenv import load_dotenv
load_dotenv()



# Agent State Definition

class JobDetails(BaseModel):
    role: str = Field(default=None, description='Hiring Role')
    company: Optional[str] = Field(default=None, description='Company Name')
    skills: Optional[list[str]] = Field(default=None, description='Required Skills')

class AgentState(BaseModel):
    post: str = Field(default=None, description='Linkedin post')
    is_hiring: str = Field(default=None, description= "Is the post about hiring")
    job_details: JobDetails = Field(default=None, description='Details of the Job')


def LLMInitialize():
    os.environ['GOOGLE_API_KEY'] = os.getenv("GOOGLE_API_1")

    llm = ChatGoogleGenerativeAI(
        model = "models/gemini-2.5-flash",
        temperature = 0
    )

    return llm

def clean_llm_output(text):
    text = re.sub(r"```json|```", "", text).strip()
    return json.loads(text)

def send_email(subject, body):
    from_email = os.getenv('From_Email')
    to_email = os.getenv('to_email')

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(from_email, os.getenv('Google_App_Password'))
        server.send_message(msg)



def classifypost(state: AgentState, config):
    post = state.post

    model = config['configurable']['model']

    template = """
    You're a helpful assistant. Your task is to read the given linkedin post and classify whether the post is related to hiring or not.

    Post : {post}

    Rules :
    - You should be 100% sure before classifying the post
    - No need to make assumptions regarding hiring in the post.
    - Answer only "Yes" or "No"

    """

    prompt_template = PromptTemplate(
        input_variables='post',
        template = template
    )

    prompt = prompt_template.format(
        post = post
    )

    response = model.invoke(prompt)

    return {'is_hiring': response.content}


def extract(state: AgentState, config):
    post = state.post

    model = config['configurable']['model']

    template = """
    You're a helpful assistant. You're task is to extract following details from the linkedin post.

    Details to Extract:-
    - role (str)
    - company (str)
    - skills (list(str))

    Post : {post}

    Rule:
    - No need to make assumptions regarding any details in the post.
    - If a role is not clearly specified, try to find most related title for the role.
    - If name of company and skills are not mentioned, Specify "Not mentioned in the post"
    - Return in JSON format
    """

    prompt_template = PromptTemplate(
        input_variables='post',
        template=template
    )

    prompt = prompt_template.format(
        post = post
    )

    response = model.invoke(prompt)

    parsed = clean_llm_output(response.content)
    job = JobDetails(**parsed)

    return {'job_details': job}


def save_notify(state: AgentState):
    data = state.job_details

    with open("leads.txt", "a") as f:
        f.write(str(data) + '\n')

    send_email(subject="Hiring Alert",
               body=f'{data.role} role at {data.company}')

    return state

def router(state: AgentState):
    if state.is_hiring.lower() == 'yes':
        return "extract"

    else:
        return END


# Build Graph

builder = StateGraph(AgentState)

# Add node
builder.add_node("classify", classifypost)
builder.add_node("extract", extract)
builder.add_node("save", save_notify)

builder.set_entry_point("classify")

builder.add_conditional_edges(
    "classify",
    router,
    {
        'extract':'extract',
        END : END
    }
)

builder.add_edge("extract", "save")
builder.add_edge('save', END)

graph = builder.compile()

if __name__ == "__main__":

    print("\n\nStarting Agent\n\n")

    agentstate = AgentState()
    agentstate.post = "We are hiring Data Scientists at Flipkart. Python and ML required."

    model = LLMInitialize()

    graph.invoke(
        agentstate,
        config = {'configurable': {'model': model}}
    )

    print("\n\nAgent successfully run\n\n")


