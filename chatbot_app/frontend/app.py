import streamlit as st
import os
import sys


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.main import workflow

# to create a session state for messages
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# to render previous messages on ui
for message in st.session_state['messages']:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

# to get the user input
user_input = st.chat_input("Type here: ")
config= {'configurable':{'thread_id': '1'}}

if user_input:
    st.session_state['messages'].append({"role": "user", "content": user_input})
    
    # display the user message in chat message container
    # icon can be changed using avatar parameter like st.chat_message("user", avatar="🧑")
    with st.chat_message("user"):
        st.text(user_input)
    
    response = workflow.invoke({'user_input': user_input}, config=config) 
    final_response = response['response']
    st.session_state['messages'].append({"role": "assistant", "content": final_response}) 

    # display the assistant response in chat message container
    with st.chat_message("assistant"):
        st.text(final_response)
        