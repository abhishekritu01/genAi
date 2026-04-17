from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# initialize model
model = ChatOpenAI(model="gpt-4o-mini")

st.header("Research Assistant")

user_input = st.text_input("Enter your prompt:")

if st.button("Generate Response"):
    if user_input:
        result = model.invoke(user_input)
        st.write("Response:")
        st.write(result.content)
    else:
        st.write("Please enter a prompt")