# TODO(mirco): everything

from langchain.llms import LlamaCpp
from langchain.chains import LLMChain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains.conversation.memory import ConversationBufferMemory

callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

llm = LlamaCpp(
    model_path="/home/mirco/code/llama.cpp/models/luban-13b.Q5_K_M.gguf",
    temperature=0.75,
    max_tokens=50,
    top_p=1,
    verbose=True,
)

TEMPLATE = """
You are Alfonzo, the SmolStock assistant. Given a question, you need to answer appropriately.

REMEMBER: you must only answer to stock and business related questions
"""

prompt = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate.from_template(TEMPLATE),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{question}")
    ],
)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
conversation = LLMChain(
    llm=llm,
    prompt=prompt,
    verbose=True,
    memory=memory
)

output = conversation({"question": "what stock should I buy?"})
text = output['text']
print(text[10:])
