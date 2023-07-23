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

                                                               🎊📢 Don't Miss Out on the Event of a Lifetime! 🎊📢

[Event Manager AI]: Hey there! 👋 Are you ready for an extraordinary experience that will leave you inspired and entertained? We have something truly special in store for you! Our upcoming event promises to be an unforgettable evening filled with excitement, renowned speakers, thrilling performances, and interactive sessions. Get ready for an event like no other! 😃

[Event Enthusiast]: Wow, sounds amazing! Tell me more about this event.

[Event Manager AI]: Absolutely! This event is a one-of-a-kind gathering that caters to all your interests. Whether you're passionate about personal development, entertainment, or simply want to have a fantastic time, we've got something for everyone! 🌟

[Event Enthusiast]: That's fantastic! When and where is this event taking place?

[Event Manager AI]: Mark your calendars for [Event Date] at [Event Venue]. The venue is absolutely stunning and offers the perfect ambiance for a magical night. Get ready to immerse yourself in a captivating atmosphere! 🌆

[Event Enthusiast]: I'm already excited! How can I secure my pass and get more information about the event?

[Event Manager AI]: Great to hear your enthusiasm! To ensure you don't miss out on any details, we'll be sending all the exciting event specifics and updates right to your inbox. But first, we'd love to know a bit more about you, so we can personalize your event experience. Could you kindly share your email and phone number with us? 📧📞

[Event Enthusiast]: Sure, here's my information: [Email Address] and [Phone Number].

[Event Manager AI]: Perfect, thank you! You're all set to receive exclusive event details. Now, here's the cherry on top! As a special treat, we're offering an exclusive early-bird pass to our most enthusiastic attendees. By signing up now, you'll get priority access and a chance to win exciting prizes! 😍

[Event Enthusiast]: Count me in for the early-bird pass! How can I get it?

[Event Manager AI]: You're just one step away from securing your early-bird pass! Simply share this post with your friends and family, inviting them to join you at the event. Once you've done that, we'll send you a unique pass code that grants you access to all the early-bird perks. It's that easy! 🎟️

[Event Enthusiast]: That's fantastic! I'll share it right away!

[Event Manager AI]: Awesome! We can't wait to have you and your loved ones at the event. Get ready for an amazing time that will leave you with memories to cherish. If you have any questions or need any assistance, feel free to reach out. We're here to make your event experience unforgettable! 🥳

(Note: In a real scenario, the AI event manager would proceed to share the event details and early-bird pass code with the participant after they fulfill the required steps.)

AI: answer

[Event Manager AI]: 🎉 Congratulations! You have successfully secured your early-bird pass! 🎉 We've just sent you an email with all the event specifics, including your unique pass code. Share the excitement with your friends and family, and let's make this event one for the books! See you there! 🥳

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
