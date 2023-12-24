from langchain.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts.prompt import PromptTemplate

callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

llm = LlamaCpp(
    model_path="/Users/mirco.dezorzi/code/llama.cpp/m/neural-chat-7b-v3-16k-q8_0.gguf",

    max_tokens=2000,
    n_ctx=16384,
    temperature=0.75,
    top_p=1,

    n_gpu_layers=1,
    n_batch=512,
    f16_kv=True,

    streaming=True,

    callback_manager=callback_manager,
)

### System: You are an expert writer tasked to write detailed and intricate stories.

template = """
### System: You are a chatbot tasked with helping users to buy and sell stocks based on informed decisions.
{history}
### User: {input}
"""

prompt = PromptTemplate(template=template, input_variables=["history", "input"])
conversation = ConversationChain(
    llm=llm,
    prompt=prompt,
    verbose=True,
    memory=ConversationBufferWindowMemory(k=3, ai_prefix="### Assistant", human_prefix="### User"),
)

if __name__ == '__main__':
    while i := input():
        output = conversation({"input": i})
        print(output['response'].strip())
