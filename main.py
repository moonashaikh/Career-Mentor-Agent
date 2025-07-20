
import os

from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel ,RunConfig
from roadmap import get_career_roadmap
from agents.run import RunConfig

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

external_client= AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai",
)
# model = OpenAIChatCompletionsModel(
#    model="gpt-4o",
#      openai_client=external_client
#      )

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client,
)
config = RunConfig(
     model=model,
     model_provider=external_client,
     tracing_disabled=True
 )

career_agent = Agent(
     name="CareerAgent",
     instructions="You ask about interest and suggest career field",
     model = model
)

skills_agent = Agent(
     name="skillsAgent",
     instructions="You you share roadmap using get_career_roadmap tool field",
     model = model,
     tools=[get_career_roadmap]
)

job_agent = Agent(
     name="jobAgent",
     instructions="You suggest job title in the chosen career field",
     model = model
)

def main():
    print("\nu0001F393 Career Mentor Agent\n")
    interest= input("... What are your Interest?->")
    
    result1 = Runner.run_sync(career_agent , interest , run_config=config)
    field = result1.final_output.strip()
    print("\n suggest career:", field)

    result2 = Runner.run_sync(skills_agent , field , run_config=config)
    
    print("\n Required Skills:", result2.final_output)
    
    result3 = Runner.run_sync(job_agent , field , run_config=config)
    
    print("\n possible jobs:", result3.final_output)

if __name__ == "__main__":
     main()