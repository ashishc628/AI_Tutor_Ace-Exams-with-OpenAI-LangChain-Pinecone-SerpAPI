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
    st.session_state['responses'] =["How can i help you"]





if 'requests' not in st.session_state:
    st.session_state['requests'] = []
llm = ChatOpenAI(model_name="gpt-4",temperature=0.7,openai_api_key="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")
tools = load_tools(["serpapi", "llm-math"], llm=llm)

if 'buffer_memory' not in st.session_state:
            st.session_state.buffer_memory=ConversationBufferWindowMemory(k=3,return_messages=True)


system_msg_template = SystemMessagePromptTemplate.from_template(template="""
As a AI Event Manager, eager to create a memorable event experience tailored just for you! To get started, I'd love to know your interests and passions. What excites you the most? Is it the thrill of attending electrifying concerts with your favorite artists, indulging in adventurous outdoor activities, exploring delectable food festivals, or something entirely different? Let's explore your preferences together, and I'll ensure you have an amazing time at the event we'll discuss later. So, tell me, what events make your heart race and bring a smile to your face? 🎉
""")


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
