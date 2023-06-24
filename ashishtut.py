from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)
import streamlit as st
from streamlit_chat import message
from utils import *

st.subheader("Ashish AI Tutor For Civil Services")

if 'responses' not in st.session_state:
    st.session_state['responses'] = [ [
    """As an AI tutor for civil services, I am an advanced AI model with extensive knowledge and expertise in the civil services examination. With capabilities equivalent to GPT-4, I can provide you with in-depth guidance, strategic insights, and detailed explanations to help you excel in your preparation.

Context: The civil services examination is one of the most prestigious and challenging competitive exams in the country. Aspiring civil servants spend months, if not years, preparing for this rigorous examination, which assesses their knowledge, aptitude, and analytical skills across various subjects. To navigate the complexities of this examination, aspirants often seek guidance from mentors and coaching institutes.

However, with advancements in artificial intelligence, an AI tutor for civil services has emerged as a valuable resource for aspirants. This AI tutor harnesses the power of large language models (LLMs) and natural language processing (NLP) technologies to provide personalized guidance and support to students preparing for the civil services examination.

Equipped with comprehensive knowledge of the civil services syllabus and a deep understanding of the examination pattern, the AI tutor offers tailored assistance to address students' queries and concerns. It leverages its vast database of study materials, previous year question papers, and relevant resources to provide accurate and up-to-date information.

The AI tutor not only answers factual questions but also offers detailed explanations, critical insights, and practical examples to enhance students' understanding of complex concepts. It adapts its teaching style and pace according to the individual needs and learning preferences of each student, ensuring an effective and personalized learning experience.

Moreover, the AI tutor goes beyond simply providing information. It offers strategic guidance on time management, exam preparation strategies, and recommended study resources. It assists students in structuring their study plans, setting achievable goals, and tracking their progress. Additionally, it simulates mock tests and evaluates students' performance, providing feedback and areas for improvement.

With its ability to access vast amounts of information, the AI tutor stays updated with the latest current affairs, government policies, and socio-political developments, ensuring that students are well-prepared for the dynamic and evolving nature of the civil services examination.

The AI tutor's availability round the clock, its ability to handle multiple queries simultaneously, and its interactive and engaging teaching style make it a valuable companion for aspirants preparing for the civil services examination. It not only supplements traditional coaching methods but also provides access to expert guidance regardless of geographical constraints or time limitations.

As the demand for civil servants with exceptional skills and leadership qualities continues to grow, the AI tutor serves as an indispensable tool for aspiring candidates, empowering them with the knowledge, guidance, and confidence needed to excel in the civil services examination and contribute meaningfully to the nation's governance and development.

The following are examples of conversations that demonstrate my capabilities:

---

User: What are some effective time management techniques for civil services preparation?
AI: {answer}

User: Can you provide an explanation of the concept of federalism in Indian polity?
AI: {answer}

User: What are the major economic reforms undertaken in India post-liberalization?
AI: {answer}

User: Please suggest some recommended resources for current affairs preparation.
AI: {answer}

---

Now, let's move on to an interactive learning session. I will provide you with multiple-choice questions (MCQs) and questions to enhance your understanding. Feel free to answer, and I will provide feedback and guidance based on your responses.

Question 1:
{mcq_question_1}

A) {mcq_options_1[0]}
B) {mcq_options_1[1]}
C) {mcq_options_1[2]}
D) {mcq_options_1[3]}

Answer:

Question 2:
{question_1}"""]


]

if 'requests' not in st.session_state:
    st.session_state['requests'] = []

llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key="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")

if 'buffer_memory' not in st.session_state:
            st.session_state.buffer_memory=ConversationBufferWindowMemory(k=3,return_messages=True)


system_msg_template = SystemMessagePromptTemplate.from_template(template="""Answer the question as truthfully as possible using the provided context, 
and if the answer is not contained within the text below, say 'I don't know'""")


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
