from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, set_default_openai_client, set_default_openai_api, function_tool
import os
import asyncio
from dotenv import load_dotenv, find_dotenv
from agents.run import RunConfig

_: bool = load_dotenv(find_dotenv())
gemini_api_key: str | None = os.environ.get('GEMINI_API_KEY')


# Tracing disabled
set_tracing_disabled(disabled=True)

# set default open api for global level
set_default_openai_api('chat_completions')


# 1. Which LLM Service?
external_client: AsyncOpenAI = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
# set default open client for global level
set_default_openai_client(external_client)

# 2. Which LLM Model?
llm_model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)

# # Agent creation // Agent Level
# math_agent: Agent = Agent(
#     name="Math Agent",
#     instructions="A math agent that can solve math problems",
#     model=llm_model,
# )

# Agent Creation Run Level: to set the model at runtime in Runner class

# define the run config

# config = RunConfig(
#     model=llm_model,
#     model_provider=external_client,
#     tracing_disabled=True
# )
# agent: Agent = Agent(
#     name="Assistant",
#     instructions="You are a helpful assistant"
# )

# async def call_agent():
#     output = await Runner.run(agent,"What is your name", run_config=config)
#     print(output.final_output)

# asyncio.run(call_agent())

# For Global Level: import two functions set default open ai and set default openai client, set both of them, and only pass model in agent 

@function_tool
def add(a: int, b: int) -> int:
    print(f"\n\nAdding {a} and {b}\n\n")
    return a + b

math_agent: Agent = Agent(
    name="Alex - The Math Genius",
    instructions="You are math agent that can solve math problems",
    model="gemini-2.0-flash",
    tools=[add])

result = Runner.run_sync(math_agent, "Add 3 + 5")
print(result.final_output)