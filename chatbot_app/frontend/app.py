import streamlit as st
import os
import sys 
import time
from langchain_core.messages import HumanMessage

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
config = {'configurable': {'thread_id': '2'}}

if user_input:
    st.session_state['messages'].append({"role": "user", "content": user_input})
    
    # display the user message in chat message container
    with st.chat_message("user"):
        st.text(user_input)
    
    ## enable below code for without streaming
    # start_time = time.time()
    # response = workflow.invoke({'user_input': user_input}, config=config) 
    # final_response = response['response']
    # end_time = time.time()
    # response_time = end_time - start_time
    # st.session_state['messages'].append({"role": "assistant", "content": final_response}) 
    # with st.chat_message("assistant"):
    #     st.markdown(final_response)
    #     st.caption(f"⏱️{response_time:.2f} seconds")

    ## with streaming
    with st.chat_message("assistant"):
        start_time = time.time()
        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in workflow.stream(
                {'user_input': user_input},
                config=config,
                stream_mode='messages'
            )
        )
        end_time = time.time()
        response_time = end_time - start_time

        st.caption(f"⏱️{response_time:.2f} seconds")

    st.session_state['messages'].append({"role": "assistant", "content": ai_message})
