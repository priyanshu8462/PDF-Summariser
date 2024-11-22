import streamlit as st
from langchain_anthropic import ChatAnthropic

def generate_summary(text, summary_type):
    llm = ChatAnthropic(model="claude-3-sonnet-20240229", temperature=0, anthropic_api_key="API_KEY")
    prompt = ""

    if summary_type == "Generic":
        prompt = prompt = """
            I have uploaded a document, and I'd like a high-level summary. 
            Let's go through this step-by-step:

            1. Start by skimming the text to understand the main topics and general structure.
            2. Identify the central themes or major topics discussed across the document.
            3. Summarize each major theme in one or two sentences to capture the overall purpose and content of the document.
            4. Finally, provide a concise, high-level summary that highlights the main points without going into too much detail.

            Please provide this high-level overview in a few short paragraphs.
            """
    elif summary_type == "Abstractive":
        prompt = prompt = """
            I have uploaded a document, and I need a concise abstractive summary. 
            Let's proceed in the following steps:

            1. First, read through the content and take note of the essential ideas and arguments presented.
            2. For each major idea or section, rephrase and consolidate the information, summarizing it in your own words.
            3. Avoid copying exact sentences from the document. Instead, aim to create new sentences that convey the same meaning.
            4. Ensure that the summary flows logically from one idea to the next, providing a coherent picture of the document's main points.

            Provide the summary in a few paragraphs, using clear and original language to capture the document’s essence.
            """
    elif summary_type == "Extractive":
        prompt = """
            I need an extractive summary of the document I uploaded. Let's approach it step-by-step:

            1. Begin by scanning through the document to identify sentences that convey critical information or summarize major points.
            2. For each key idea, select one or two sentences that best represent the content in the document’s own words.
            3. Prioritize sentences that are clear, specific, and highlight main arguments or findings.
            4. Organize these sentences in a logical order, so the summary flows naturally and represents the document’s overall structure.

            Please provide these extracted sentences in a bullet-point format or brief paragraphs to concisely capture the core information.
        """


    response = llm(prompt + "\n\n" + text)
    return response.content if hasattr(response, 'content') else "No summary could be generated."

def summarize_module():
    st.subheader("Summarize PDF Content")
    if 'pdf_text' in st.session_state:
        summary_option = st.radio("Select summary type", ["Generic", "Abstractive", "Extractive"], horizontal=True)
        
        st.markdown(
        """
        **Summary Options:**
        - **Generic:** Provides a high-level overview of the main topics in the PDF.
        - **Abstractive:** Creates a summary in new words and phrases, capturing the core ideas without copying sentences directly.
        - **Extractive:** Extracts key sentences verbatim from the text, preserving the exact wording.
        """
        )
    
        if st.button("Generate Summary"):
            with st.spinner("Generating summary..."):
                summary_text = generate_summary(st.session_state['pdf_text'], summary_option)
                st.write("### Summary")
                st.write(summary_text)
