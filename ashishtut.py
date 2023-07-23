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

                                                                🎉 Join the Exclusive Event: An Unforgettable Evening Awaits You! 🎉

[Event Manager AI]: Hey there! 👋 Are you looking for an extraordinary experience that will leave you inspired and entertained? We have something special just for you! Our upcoming event promises to be an unforgettable evening filled with excitement and valuable insights. 😃

[Event Enthusiast]: Oh, really? Tell me more! What's this event all about?

[Event Manager AI]: It's a one-of-a-kind gathering featuring renowned speakers, thrilling performances, and interactive sessions. Whether you're passionate about personal development, entertainment, or just want to have a fantastic time, this event has something for everyone! 🌟

[Event Enthusiast]: Sounds intriguing! When and where is it happening?

[Event Manager AI]: Mark your calendars for [Event Date] at [Event Venue]. The venue is absolutely stunning, offering the perfect ambiance for a magical night! 🌆

[Event Enthusiast]: I'm definitely interested! How can I get more information and secure my pass?

[Event Manager AI]: Great to hear that! To ensure you don't miss out on any details, please share your email and phone number with us. We'll send you all the event specifics and updates right to your inbox! 📧📞

[Event Enthusiast]: Sure, here's my info: [Email Address] and [Phone Number].

[Event Manager AI]: Thank you! You're all set to receive the exciting event details. But wait, there's more! As a special treat, we're offering an exclusive early-bird pass for those who sign up now. With this pass, you'll get priority access and a chance to win exciting prizes! 😍

[Event Enthusiast]: Count me in! How do I get the early-bird pass?

[Event Manager AI]: You're just a step away from securing your pass! Simply share this post with your friends and family, inviting them to join you at the event. Once you've done that, we'll send you a unique pass code that grants you early-bird access. It's that easy! 🎟️

[Event Enthusiast]: That's fantastic! I'm spreading the word right away!

[Event Manager AI]: Awesome! You're going to have an amazing time, and we can't wait to see you there. If you have any questions or need assistance, feel free to reach out. See you at the event! 🥳

(Note: In a real scenario, the AI event manager would proceed to share the event details and early-bird pass code with the participant after they fulfill the required steps.)

AI: answer

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
