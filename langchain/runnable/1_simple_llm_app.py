from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate


llm = OpenAI(model="gpt-3.5-turbo", temperature=0.9)

prompt = PromptTemplate.from_template(
    input_variables=["topic"],
    template="What are the top 3 most important things to know about {topic}?",
) 


#define the topic
topic = input("Enter a topic: ")


#format the prompt with the topicformatted_prompt = prompt.format(topic=topic)
formatted_prompt = prompt.format(topic=topic)   

#generate the response
blog_title = llm.predict(formatted_prompt)



print(blog_title)