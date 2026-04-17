from langchain_openai import ChatOpenAI

from dotenv import load_dotenv

load_dotenv()


# chat = ChatOpenAI(model="gpt-3.5-turbo-instruct", temperature=0.9 ,max_completion_tokens=100 )
model = ChatOpenAI(model='gpt-4-0613', temperature=0.9, max_completion_tokens=100)

model.invoke("What is the capital of india?")

response = model.invoke("What is the capital of india?")
# print(response)            # content='The capital of India is New Delhi.' additional_kwargs={'refusal': None} response_metadata={'token_usage': {'completion_tokens': 8, 'prompt_tokens': 14, 'total_tokens': 22, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_provider': 'openai', 'model_name': 'gpt-4-0613', 'system_fingerprint': None, 'id': 'chatcmpl-DCsA68tDxtxdQE3rhVTYedvc2eqrj', 'service_tier': 'default', 'finish_reason': 'stop', 'logprobs': None} id='lc_run--019c9113-9819-78b3-8a45-453d9c9ec8db-0' tool_calls=[] invalid_tool_calls=[] usage_metadata={'input_tokens': 14, 'output_tokens': 8, 'total_tokens': 22, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}

print(response.content)    