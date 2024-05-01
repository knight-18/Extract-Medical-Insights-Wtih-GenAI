import streamlit as st
import summarization_lib as glib
import rag_chatbot_lib as raglib #reference to local lib script
import boto3
import uuid
s3 = boto3.resource('s3')    
st.set_page_config(page_title="Document Summarization")
st.title("Document Summarization")

@st.cache_resource #this decorator causes Streamlit to automatically cache the returned value
def get_download_file():
    return glib.get_example_file_bytes()


download_button = st.download_button(
    label="Download example PDF to upload",
    data=get_download_file(),
    file_name="summarization_example.pdf",
    mime="application/pdf"
)



uploaded_file = st.file_uploader("Select a PDF", type=['pdf'])

upload_button = st.button("Upload", type="primary")

if upload_button:
    with st.spinner("Uploading..."):

        upload_response = glib.save_file( file_bytes=uploaded_file.getvalue())

        st.success(upload_response)
        
        st.session_state.has_document = True

            
            
if 'has_document' in st.session_state: #see if document has been uploaded
    # s3PutRes = s3.Object('', 'uploaded_file.pdf').put(Body=open('./uploaded_file.pdf', 'rb'))

    # print type of filename
    filename = "uploaded_file.pdf"
    s3PutRes = s3.Bucket('document-summarization').upload_file('./uploaded_file.pdf',filename)
    print("Put success")
    return_intermediate_steps = st.checkbox("Return intermediate steps", value=True)
    summarize_button = st.button("Summarize", type="primary")
    
    
    if summarize_button:
        st.subheader("Combined summary")

        with st.spinner("Running..."):
            response_content = glib.get_summary(filename, return_intermediate_steps=return_intermediate_steps)


        if return_intermediate_steps:

            st.write(response_content["output_text"])

            st.subheader("Section summaries")

            for step in response_content["intermediate_steps"]:
                st.write(step)
                st.markdown("---")

        else:
            # st.text(response_content)
            st.write(response_content)
    if 'memory' not in st.session_state: #see if the memory hasn't been created yet
        st.session_state.memory = raglib.get_memory() #initialize the memory


    if 'chat_history' not in st.session_state: #see if the chat history hasn't been created yet
        st.session_state.chat_history = [] #initialize the chat history

    if 'vector_index' not in st.session_state: #see if the vector index hasn't been created yet
        with st.spinner("Indexing document..."): #show a spinner while the code in this with block runs
            st.session_state.vector_index = raglib.get_index() #retrieve the index through the supporting library and store in the app's session cache

    #Re-render the chat history (Streamlit re-runs this script, so need this to preserve previous chat messages)
    for message in st.session_state.chat_history: #loop through the chat history
        with st.chat_message(message["role"]): #renders a chat line for the given role, containing everything in the with block
            st.markdown(message["text"]) #display the chat content
    input_text = st.chat_input("Chat with your bot here") #display a chat input box

    if input_text: #run the code in this if block after the user submits a chat message
        
        with st.chat_message("user"): #display a user chat message
            st.markdown(input_text) #renders the user's latest message
        
        st.session_state.chat_history.append({"role":"user", "text":input_text}) #append the user's latest message to the chat history
        
        chat_response = raglib.get_rag_chat_response(input_text=input_text, memory=st.session_state.memory, index=st.session_state.vector_index,) #call the model through the supporting library
        
        with st.chat_message("assistant"): #display a bot chat message
            st.markdown(chat_response) #display bot's latest response
        
        st.session_state.chat_history.append({"role":"assistant", "text":chat_response}) #append the bot's latest message to the chat history
        




# st.set_page_config(page_title="RAG Chatbot") #HTML title
# st.title("RAG Chatbot") #page title







