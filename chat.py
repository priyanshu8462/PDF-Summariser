import streamlit as st
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain.tools.retriever import create_retriever_tool
from langchain.agents import initialize_agent, AgentExecutor, create_tool_calling_agent
from pdf_processing import embeddings
from langchain_community.vectorstores import FAISS
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
import textwrap

def download_chat_history():
    pdf_path = "./chat_history.pdf"

    # Initialize a canvas for the PDF with A4 page size
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4
    y_position = height - 40  # Start near the top of the page

    # Set font settings
    c.setFont("Helvetica", 12)
    margin = 40  # Left margin for text
    text_width = width - 2 * margin  # Width available for text after margins

    # Loop through the chat history and add content to PDF
    for chat in st.session_state['chat_history']:
        user_text = f"You: {chat['user']}"
        bot_text = f"Claude: {chat['bot']}"

        # Add user question in bold
        c.setFont("Helvetica-Bold", 12)
        wrapped_user_text = textwrap.wrap(user_text, width=int(text_width / 7))  # Estimate chars per line
        for line in wrapped_user_text:
            c.drawString(margin, y_position, line)
            y_position -= 15

        # Add system response in italic with text wrapping
        c.setFont("Helvetica-Oblique", 12)
        wrapped_bot_text = textwrap.wrap(bot_text, width=int(text_width / 7))  # Estimate chars per line
        for line in wrapped_bot_text:
            c.drawString(margin, y_position, line)
            y_position -= 15

        # Move down for the next entry in chat history
        y_position -= 10

        # Add new page if necessary
        if y_position < 40:
            c.showPage()
            c.setFont("Helvetica", 12)
            y_position = height - 40

    c.save()

    return pdf_path


def get_conversational_chain(tools, ques):
    llm = ChatAnthropic(model="claude-3-sonnet-20240229", temperature=0, anthropic_api_key="API_KEY")
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful assistant. Use the provided pdf_extractor tool to answer questions about the PDF content. The PDF has already been processed and its content is available through the tool. Always use the tool to retrieve information before answering."
            ),
            ("human", "{input}"),
            ("human", "Please use the pdf_extractor tool to find information related to my question and then provide a comprehensive answer. {agent_scratchpad}")        
        ]
    )
    tool = [tools]
    agent = create_tool_calling_agent(llm, tool, prompt)
    
    agent_executor = AgentExecutor(agent=agent, tools=tool, verbose=True)
    response = agent_executor.invoke({"input": ques})
    
    return response['output']

def user_input(user_question):
    new_db = FAISS.load_local("faiss_db", embeddings, allow_dangerous_deserialization=True)
    retriever = new_db.as_retriever()
    retrieval_chain = create_retriever_tool(retriever, "pdf_extractor", "Extracts relevant information from the PDF.")
    response = get_conversational_chain(retrieval_chain, user_question)
    text_output = response[0].get("text", "No relevant information found") if isinstance(response, list) else "No response generated."

    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
    st.session_state.chat_history.append({"user": user_question, "bot": text_output})

def display_chat_history(chat_placeholder):
    with chat_placeholder.container():
        if 'chat_history' in st.session_state:
            for chat in st.session_state.chat_history:
                st.markdown(f"<div style='text-align: right; background-color: #E0F7FA; padding: 10px;'><b>You:</b> {chat['user']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='text-align: left; background-color: #F1F8E9; padding: 10px;'><b>Assistant:</b> {chat['bot']}</div>", unsafe_allow_html=True)

def chat_interface():
    chat_placeholder = st.empty()
    display_chat_history(chat_placeholder)
    user_question = st.text_input("Ask a Question about the PDF", label_visibility="collapsed", key="user_input")
    if user_question:
        user_input(user_question)
        display_chat_history(chat_placeholder)
    if st.button("Download PDF"):
        pdf_path = download_chat_history()
        with open(pdf_path, "rb") as f:
            st.download_button("Download Chat History as PDF", f, file_name="chat_history.pdf", mime="application/pdf")

