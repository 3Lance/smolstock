from langchain.chains import LLMMathChain
from langchain.llms.openai import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.utilities import SerpAPIWrapper
from langchain.agents import initialize_agent, Tool, AgentExecutor
import chainlit as cl


from chain import conversation

@cl.on_chat_start
def start():
    cl.user_session.set("agent", conversation)


@cl.on_message
async def main(message: cl.Message):
    agent = cl.user_session.get("agent")
    cb = cl.LangchainCallbackHandler(stream_final_answer=True)

    await cl.make_async(conversation)(message.content, callbacks=[cb])

