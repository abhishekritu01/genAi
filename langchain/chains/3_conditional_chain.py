from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel,RunnableBranch,RunnableSequence,RunnableLambda
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Literal



load_dotenv()

model = ChatOpenAI()   # initialize the model



parser = StrOutputParser()

class FeedbackSentiment(BaseModel):
    sentiment: Literal["positive", "negative", "neutral"] = Field(description="Give the sentiment of the feedback") 


parser2 = PydanticOutputParser(pydantic_object=FeedbackSentiment)

prompt1 = PromptTemplate(
    template="Classify the sentiment of the following text as positive, negative or neutral \n {feedback}  \n {format_instructions} ",
    input_variables=["feedback"],
    partial_variables={"format_instructions": parser2.get_format_instructions()}
)



classification_chain = prompt1 | model | parser2

# print(classification_chain.invoke({"feedback": "I love this product! It has changed my life."}))
# result =classification_chain.invoke({"feedback": "This is the worst experience I've ever had."})
# print(result)


prompt2 = PromptTemplate(
    template="Generate a positive response to the following feedback \n {feedback}",
    input_variables=["feedback"]
)

prompt3 = PromptTemplate(
    template="Generate a negative response to the following feedback \n {feedback}",
    input_variables=["feedback"]
)

branch_chain = RunnableBranch(
    (lambda x: x.sentiment == "positive", prompt2 | model | parser),
    (lambda x: x.sentiment == "negative", prompt3 | model | parser),
    RunnableLambda(lambda x: "Neutral feedback received. No response generated.")


)

chain = classification_chain | branch_chain

result = chain.invoke({"feedback": "I love this product! It has changed my life."})

print(result)