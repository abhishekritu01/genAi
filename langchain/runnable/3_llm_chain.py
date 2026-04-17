from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain



llm = OpenAI(model="gpt-3.5-turbo", temperature=0.9)


prompt = PromptTemplate.from_template(
    input_variables=["topic"],
    template="What are the top 3 most important things to know about {topic}?",
)

topic = input("Enter a topic: ")


#format the prompt with the topic
formatted_prompt = prompt.format(topic=topic)


chain = LLMChain(llm=llm, prompt=prompt)

#define the topic
response = chain.run(topic=topic)
print(response)


