import os
import streamlit as st
from langchain import LLMChain
from langchain.agents import load_tools
from langchain.memory import ConversationBufferWindowMemory
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)
import streamlit as st
from streamlit_chat import message
from utils import *
os.environ['SERPAPI_API_KEY'] = '4150cf22ec6b59eb414683e90a97cd1838b598058f8d3457c1feb8acf01dbfc7'
st.subheader("testing")

if 'responses' not in st.session_state:
    st.session_state['responses'] =["How can i assist you"]





if 'requests' not in st.session_state:
    st.session_state['requests'] = []
llm = ChatOpenAI(model_name="gpt-4", openai_api_key="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")
tools = load_tools(["serpapi", "llm-math"], llm=llm)

if 'buffer_memory' not in st.session_state:
            st.session_state.buffer_memory=ConversationBufferWindowMemory(k=3,return_messages=True)


system_msg_template = SystemMessagePromptTemplate.from_template(template="""
As a psychiatrist/psychologist, you have a user who seeks your guidance for their psychological concerns. he will type something you have to ask questions . To provide the most effective therapy, you decide to assess their needs and preferences before determining the approach to take. You plan to ask them a series of questions to understand their symptoms, goals, and personal characteristics. Based on their answers, you will identify the most appropriate therapeutic approach among psychodynamic therapy, behavioral therapy, cognitive-behavioral therapy, and humanistic therapy.

{history}
Human: {input}
AI:""")


human_msg_template = HumanMessagePromptTemplate.from_template(template="{input}")

prompt_template = ChatPromptTemplate.from_messages([system_msg_template, MessagesPlaceholder(variable_name="history"), human_msg_template])

conversation = ConversationChain(memory=st.session_state.buffer_memory, prompt=prompt_template, llm=llm, verbose=True)




# container for chat history
response_container = st.container()
# container for text box
textcontainer = st.container()


with textcontainer:
    query = st.text_input("Query: ", key="input")
    if query:
        with st.spinner("typing..."):
            conversation_string = get_conversation_string()
            # st.code(conversation_string)
            refined_query = query_refiner(conversation_string, query)
            st.subheader("Refined Query:")
            st.write(refined_query)
            context = find_match(refined_query)
            # print(context)  
            response = conversation.predict(input=f"Context:\n {context} \n\n Query:\n{query}")
        st.session_state.requests.append(query)
        st.session_state.responses.append(response) 
with response_container:
    if st.session_state['responses']:

        for i in range(len(st.session_state['responses'])):
            message(st.session_state['responses'][i],key=str(i))
            if i < len(st.session_state['requests']):
                message(st.session_state["requests"][i], is_user=True,key=str(i)+ '_user')
