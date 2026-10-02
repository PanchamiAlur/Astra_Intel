import os
import html
import requests

import fitz
import streamlit as st

from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="ASTRA INTEL",
    page_icon="📄",
    layout="wide"
)


# ============================================================
# ASTRA VISUAL DESIGN
# ============================================================

st.markdown("""
<style>

/* ===== GLOBAL ===== */

.stApp {
    background-color: #080909;
    color: #F5F0E6;
}

.stApp p,
.stApp h1,
.stApp h2,
.stApp h3,
.stApp label,
.stApp button,
.stApp input,
.stApp textarea {
    font-family: "Trebuchet MS", sans-serif !important;
}


/* ===== STREAMLIT HEADER ===== */

[data-testid="stHeader"] {
    background-color: #080909;
}

[data-testid="stToolbar"] {
    display: none;
}


/* ===== ASTRA TOP BAR ===== */

.astra-topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;

    padding: 12px 0;
    margin-bottom: 20px;

    border-bottom: 1px solid #3A3A34;

    color: #9BA6A8;

    font-family: monospace !important;
    font-size: 13px;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.astra-topbar span:last-child {
    color: #F5D27A;
}


/* ===== ASTRA TITLE ===== */

.astra-title {
    color: #F5D27A;

    font-size: 64px;
    font-weight: 700;

    letter-spacing: 5px;
    line-height: 1.1;

    margin-top: 10px;
    margin-bottom: 8px;
}


/* ===== ASTRA SUBTITLE ===== */

.astra-subtitle {
    color: #9BA6A8;

    font-family: monospace !important;

    font-size: 14px;
    letter-spacing: 3px;

    text-transform: uppercase;

    margin-bottom: 30px;
}


/* ===== SECTION LABEL ===== */

.section-label {
    color: #F5D27A;

    font-family: monospace !important;

    font-size: 13px;
    font-weight: 700;

    letter-spacing: 3px;
    text-transform: uppercase;

    border-bottom: 1px solid #3A3A34;

    padding-bottom: 10px;

    margin-top: 20px;
    margin-bottom: 15px;
}


/* ===== FILE UPLOADER ===== */

[data-testid="stFileUploader"] {
    background: #111212 !important;

    border: 1px solid #343632 !important;

    border-radius: 0px !important;

    padding: 18px !important;
}

[data-testid="stFileUploaderDropzone"] {
    background: #111212 !important;

    border: 1px dashed #55574F !important;

    border-radius: 0px !important;
}

[data-testid="stFileUploaderDropzoneInstructions"] {
    color: #9BA6A8 !important;
}

[data-testid="stFileUploaderDropzoneInstructions"] svg {
    fill: #F5D27A !important;
}

[data-testid="stFileUploader"] button {
    background: #F5D27A !important;

    color: #080909 !important;

    border: none !important;

    border-radius: 0px !important;

    font-weight: 700 !important;
}


/* ===== MISSION STATUS ===== */

.status-card {
    background: #111212;

    border: 1px solid #343632;

    padding: 20px;

    min-height: 90px;
}

.status-label {
    color: #7F898B;

    font-family: monospace !important;

    font-size: 11px;

    letter-spacing: 2px;

    margin-bottom: 12px;
}

.status-value {
    color: #F5D27A;

    font-family: monospace !important;

    font-size: 22px;

    font-weight: bold;

    letter-spacing: 1px;
}


/* ===== STREAMLIT ALERTS ===== */

.stAlert {
    border-radius: 0px !important;
}


/* ===== BUTTONS ===== */

.stButton button {
    border-radius: 0px !important;
}


/* ===== INPUTS ===== */

.stTextInput input {
    background-color: #111212 !important;

    color: #F5F0E6 !important;

    border: 1px solid #343632 !important;

    border-radius: 0px !important;
}


/* ===== EXPANDERS ===== */

[data-testid="stExpander"] {
    background-color: #111212 !important;

    border: 1px solid #343632 !important;

    border-radius: 0px !important;
}


/* ===== DOCUMENT PROCESSING ===== */

.process-panel {
    background: #0D0E0E;

    border: 1px solid #343632;

    padding: 18px 20px;

    margin-top: 10px;
    margin-bottom: 25px;
}

.process-row {
    display: flex;

    justify-content: space-between;

    align-items: center;

    padding: 9px 0;

    border-bottom: 1px solid #242622;

    color: #9BA6A8;

    font-family: monospace !important;

    font-size: 12px;

    letter-spacing: 1.5px;
}

.process-row:last-child {
    border-bottom: none;
}

.process-value {
    color: #F5D27A;

    font-weight: 700;
}

.process-ok {
    color: #8FD694;

    font-weight: 700;
}


/* ===== INTELLIGENCE OUTPUT META ===== */

.answer-meta {
    display: flex;

    justify-content: space-between;

    background: #0D0E0E;

    border: 1px solid #343632;

    border-bottom: none;

    padding: 10px 16px;

    color: #7F898B;

    font-family: monospace !important;

    font-size: 11px;

    letter-spacing: 2px;

    text-transform: uppercase;
}

.answer-meta span:last-child {
    color: #8FD694;
}


/* ===== INTELLIGENCE OUTPUT ===== */

.answer-panel {
    background: #111212;

    border: 1px solid #343632;

    border-left: 3px solid #F5D27A;

    padding: 24px;

    margin-top: 0;

    margin-bottom: 30px;

    color: #F5F0E6;

    font-family: "Trebuchet MS", sans-serif !important;

    font-size: 16px;

    line-height: 1.7;
}


/* ===== SOURCE RECORDS ===== */

.source-record {
    background: #0D0E0E;

    border: 1px solid #343632;

    margin-bottom: 10px;

    padding: 14px 18px;

    font-family: monospace !important;
}

.source-record-header {
    display: flex;

    justify-content: space-between;

    color: #F5D27A;

    font-size: 12px;

    font-weight: 700;

    letter-spacing: 2px;
}

.source-record-status {
    color: #8FD694;

    font-size: 11px;
}


/* ===== ASTRA SYSTEM FOOTER ===== */

.astra-footer {
    margin-top: 50px;

    padding: 14px 0;

    border-top: 1px solid #3A3A34;

    border-bottom: 1px solid #242622;

    display: flex;

    justify-content: space-between;

    align-items: center;

    color: #7F898B;

    font-family: monospace !important;

    font-size: 11px;

    letter-spacing: 2px;

    text-transform: uppercase;
}

.astra-footer-left {
    color: #F5D27A;

    font-weight: 700;
}

.astra-footer-center {
    color: #7F898B;
}

.astra-footer-right {
    color: #8FD694;
}


/* ===== RESPONSIVE LAYOUT ===== */

@media (max-width: 900px) {

    .astra-title {
        font-size: 42px;

        letter-spacing: 3px;
    }

    .astra-subtitle {
        font-size: 11px;

        letter-spacing: 2px;
    }

    .status-card {
        margin-bottom: 10px;
    }

    .answer-panel {
        padding: 18px;

        font-size: 15px;
    }

    .astra-footer {
        flex-direction: column;

        align-items: flex-start;

        gap: 8px;
    }

}

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    st.error(
        "OPENROUTER_API_KEY was not found in the .env file."
    )
    st.stop()


# ============================================================
# SESSION STATE
# ============================================================

if "ai_engine" not in st.session_state:
    st.session_state.ai_engine = 0


# ============================================================
# ASTRA HEADER
# ============================================================

col_logo, col_status = st.columns([1, 5])

with col_logo:

    st.image(
        "ASTRA_logo.jpeg",
        width=120
    )

with col_status:

    st.html("""
    <div class="astra-topbar">

        <span>
            ASTRA / NX-01
        </span>

        <span>
            ● SYSTEM ONLINE
        </span>

    </div>
    """
    )


# ============================================================
# ASTRA TITLE
# ============================================================

st.markdown("""
<div class="astra-title">
    ASTRA INTEL
</div>
""", unsafe_allow_html=True)


st.markdown("""
<div class="astra-subtitle">
    AI POWERED DOCUMENT INTELLIGENCE
</div>
""", unsafe_allow_html=True)


# ============================================================
# DOCUMENT UPLOAD
# ============================================================

uploaded_files = st.file_uploader(
    "Upload PDF documents",
    type=["pdf"],
    accept_multiple_files=True
)


# ============================================================
# MISSION STATUS
# ============================================================

document_status = "STANDBY"

pages_indexed = "--"


if uploaded_files:

    document_status = "READY"

    total_pages = 0

    try:

        for uploaded_file in uploaded_files:

            temp_document = fitz.open(
                stream=uploaded_file.getvalue(),
                filetype="pdf"
            )

            total_pages += len(temp_document)

            temp_document.close()

        pages_indexed = total_pages

    except Exception:

        pages_indexed = "--"


ai_engine = "OPENROUTER"


st.html("""
<div class="section-label">
    MISSION STATUS
</div>
""")


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.html(
        f"""
        <div class="status-card">

            <div class="status-label">
                DOCUMENT
            </div>

            <div class="status-value">
                {document_status}
            </div>

        </div>
        """
    )


with col2:

    st.html(
        f"""
        <div class="status-card">

            <div class="status-label">
                PAGES INDEXED
            </div>

            <div class="status-value">
                {pages_indexed}
            </div>

        </div>
        """
    )


with col3:

    st.html(
        f"""
        <div class="status-card">

            <div class="status-label">
                AI ENGINE
            </div>

            <div class="status-value">
                {ai_engine}
            </div>

        </div>
        """
    )


with col4:

    st.html(
        """
        <div class="status-card">

            <div class="status-label">
                SYSTEM STATUS
            </div>

            <div class="status-value">
                ONLINE
            </div>

        </div>
        """
    )


# ============================================================
# PDF PROCESSING
# ============================================================

if uploaded_files:

    try:

        chunks = []

        # Size of each searchable text chunk
        chunk_size = 1800

        # Overlap between chunks
        overlap = 200


        # ========================================================
        # PROCESS EVERY UPLOADED DOCUMENT
        # ========================================================

        for uploaded_file in uploaded_files:

            document_name = uploaded_file.name

            document = fitz.open(
                stream=uploaded_file.getvalue(),
                filetype="pdf"
            )


            for page_number, page in enumerate(document):

                text = page.get_text().strip()

                if not text:
                    continue


                # ------------------------------------------------
                # SPLIT PAGE INTO SMALLER RETRIEVAL CHUNKS
                # ------------------------------------------------

                start = 0

                while start < len(text):

                    end = start + chunk_size

                    chunk_text = text[start:end].strip()


                    if chunk_text:

                        chunks.append(
                            {
                                "document": document_name,
                                "page": page_number + 1,
                                "text": chunk_text
                            }
                        )


                    # Move forward while keeping overlap
                    start += chunk_size - overlap


            document.close()


        # ========================================================
        # CHECK EXTRACTION
        # ========================================================

        if not chunks:

            st.warning(
                "No selectable text was found in the uploaded PDFs. "
                "They may be scanned documents."
            )


        else:

            # ====================================================
            # DOCUMENT PROCESSING STATUS
            # ====================================================

            st.html(
                f"""
                <div class="process-panel">

                    <div class="process-row">

                        <span>
                            FILES
                        </span>

                        <span class="process-value">
                            {len(uploaded_files)} DOCUMENT(S) LOADED
                        </span>

                    </div>


                    <div class="process-row">

                        <span>
                            PAGES INDEXED
                        </span>

                        <span class="process-value">
                            {pages_indexed}
                        </span>

                    </div>


                    <div class="process-row">

                        <span>
                            CHUNKS CREATED
                        </span>

                        <span class="process-value">
                            {len(chunks)}
                        </span>

                    </div>


                    <div class="process-row">

                        <span>
                            TEXT EXTRACTION
                        </span>

                        <span class="process-ok">
                            COMPLETE
                        </span>

                    </div>


                    <div class="process-row">

                        <span>
                            INDEX STATUS
                        </span>

                        <span class="process-ok">
                            READY
                        </span>

                    </div>

                </div>
                """
            )


            # ====================================================
            # BUILD RETRIEVAL CORPUS
            # ====================================================

            chunk_texts = [
                chunk["text"]
                for chunk in chunks
            ]


            vectorizer = TfidfVectorizer(
                stop_words="english"
            )


            tfidf_matrix = vectorizer.fit_transform(
                chunk_texts
            )

            # ====================================================
            # DOCUMENT SUMMARY
            # ====================================================

            st.markdown("""
            <div class="section-label">
                DOCUMENT SUMMARY
            </div>
            """, unsafe_allow_html=True)


            summary_button = st.button(
                "GENERATE DOCUMENT SUMMARY",
                type="primary"
            )


            if summary_button:

            # ------------------------------------------------
            # Collect text from all uploaded documents
            # ------------------------------------------------

                summary_parts = []

                documents = {}


                for chunk in chunks:

                    document_name = chunk["document"]

                    if document_name not in documents:
                        documents[document_name] = []
                        
                    documents[document_name].append(
                            f""" PAGE {chunk["page"]}:
                            {chunk["text"]}
                            """
                        )

                for document_name,document_chunks in documents.items():

                    summary_context = "\n\n".join(document_chunks)

                    # Limit each document separately

                    if len(summary_context)>12000:
                        summary_context = summary_context[:12000]

                    summary_parts.append(
                        f"""
                        DOCUMENT: {document_name}
                        {summary_context}
                        """
                    )
                summary_context = "\n\n".join(summary_parts)
                

                # ------------------------------------------------
                # SUMMARY PROMPT
                # ------------------------------------------------

                summary_prompt = f"""
You are ASTRA INTEL, a document intelligence system.

Create a concise summary using ONLY the provided document content.

Do not use outside knowledge.
Do not invent information.
Do not include your thinking or reasoning process.

Summarize the major topics, categories, applications,
capabilities, and limitations that are actually present
in the provided documents.

If multiple documents are provided, identify the document
when necessary.

Return ONLY the final concise summary.

DOCUMENT CONTENT:

{summary_context}
"""


                # ------------------------------------------------
                # OPENROUTER SUMMARY REQUEST
                # ------------------------------------------------

                try:

                    summary_response = requests.post(

                "https://openrouter.ai/api/v1/chat/completions",

                        headers={
                            "Authorization": f"Bearer {api_key}",
                            "Content-Type": "application/json"
                        },

                        json={

                            "model": "openrouter/free",

                            "messages": [
                                {
                                    "role": "user",
                                    "content": summary_prompt
                                }
                            ],

                            "temperature": 0.1,

                            "max_tokens": 4000,

                            "reasoning": {
                                "exclude": True
                            }
                        },

                        timeout=60
                    )


                    summary_response.raise_for_status()


                    summary_result = summary_response.json()


                    summary_choices = summary_result.get(
                        "choices",
                        []
                    )


                    if not summary_choices:

                        raise ValueError(
                            f"OpenRouter returned no summary choices: "
                            f"{summary_result}"
                        )


                    summary_message = summary_choices[0].get(
                        "message",
                        {}
                    )


                    summary = summary_message.get(
                        "content",
                        ""
                    )


                    if not summary:

                        raise ValueError(
                            f"OpenRouter returned no summary text: "
                           f"{summary_result}"
                        )


                    # ------------------------------------------------
                    # DISPLAY SUMMARY
                    # ------------------------------------------------

                    st.markdown("""
                        <div class="section-label">
                            DOCUMENT SUMMARY
                        </div>
                    """, unsafe_allow_html=True)


                    st.markdown(
                        f"""
                        <div class="answer-panel">
                        {summary}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )


                except requests.exceptions.Timeout:

                    st.error(
                        "Summary request timed out. Please try again."
                    )


                except requests.exceptions.HTTPError:

                    try:

                        summary_error = summary_response.json()

                    except Exception:

                        summary_error = summary_response.text


                        st.error(
                            f"Summary request failed: {summary_error}"
                        )


                except Exception as e:

                    st.error(
                        f"Summary generation failed: {str(e)}"
                    )


            # ====================================================
            # INTELLIGENCE QUERY
            # ====================================================

            st.markdown("""
            <div class="section-label">
                INTELLIGENCE QUERY
            </div>
            """, unsafe_allow_html=True)


            question = st.text_input(
                "ENTER QUERY",
                placeholder="Ask about the document...",
                key="document_question"
            )


            ask_button = st.button(
                "RUN INTELLIGENCE QUERY",
                type="primary"
            )


            if ask_button and question.strip():

                # ================================================
                # RETRIEVE RELEVANT CHUNKS
                # ================================================

                question_vector = vectorizer.transform(
                    [question]
                )


                similarity_scores = cosine_similarity(
                    question_vector,
                    tfidf_matrix
                )[0]


                # Retrieve more evidence because multiple documents may be relevant
                top_k = min(5,len(chunks))

                top_indices = similarity_scores.argsort()[-top_k:][::-1]


                relevant_chunks = []


                for index in top_indices:

                    if similarity_scores[index] > 0.10:

                        chunk = chunks[index].copy()
                        
                        chunk["score"] = float(similarity_scores[index])
                        
                        relevant_chunks.append(chunk)


                # ================================================
                # BUILD CONTEXT
                # ================================================

                if not relevant_chunks:

                    st.warning(
                        "No relevant information was found in the document."
                    )


                else:

                    context_parts = []


                    for chunk in relevant_chunks:

                        context_parts.append(
                            f"""
                        DOCUMENT: {chunk["document"]}
                        PAGE: {chunk["page"]}    

                        {chunk["text"]}
                        """
                        )


                    context = "\n\n".join(
                        context_parts
                    )


                    # ============================================
                    # ASTRA PROMPT
                    # ============================================

                    prompt = f"""
You are ASTRA INTEL, a document question-answering system.

Answer the user's question using ONLY the provided document context.

Do not use outside knowledge.
Do not invent information.

If the answer cannot be found in the provided context, say:
"Not found in the provided document."

For questions asking about major applications, categories, uses,
or topics discussed throughout the document, identify all relevant
categories found in the provided context rather than focusing on
one isolated phrase.

Answer clearly and concisely.
Use only the information necessary to answer the question.
Do not repeat question.
Prefer a short bullet list when multiple points are required. 

Include the relevant source page numbers in this format:
[Page X]

If multiple pages support a statement, use:
[Pages X-Y]

Do not cite pages that do not support the answer.

USER QUESTION:
{question}

DOCUMENT CONTEXT:
{context}
"""


                    # ============================================
                    # OPENROUTER AI REQUEST
                    # ============================================

                    try:

                        response = requests.post(
                            "https://openrouter.ai/api/v1/chat/completions",

                            headers={
                                "Authorization": f"Bearer {api_key}",
                                "Content-Type": "application/json",
                            },

                            json={
                                "model": "openrouter/free",

                                "messages": [
                                    {
                                        "role": "user",
                                        "content": prompt
                                    }
                                ],

                                "temperature": 0.1,

                                "max_tokens": 4000,

                                "reasoning": {
                                    "exclude": True
                                }
                            },

                            timeout=60
                        )


                        response.raise_for_status()


                        result = response.json()


                        choices = result.get(
                            "choices",
                            []
                        )


                        if not choices:

                            raise ValueError(
                                f"OpenRouter returned no choices: {result}"
                            )


                        message = choices[0].get(
                            "message",
                            {}
                        )


                        answer = message.get(
                            "content",
                            ""
                        )


                        if not answer:

                            raise ValueError(
                                f"OpenRouter returned no text content: {result}"
                            )


                        # Count only successful AI responses
                        st.session_state.ai_engine += 1


                        # ========================================
                        # INTELLIGENCE OUTPUT
                        # ========================================

                        st.markdown("""
                        <div class="section-label">
                            INTELLIGENCE OUTPUT
                        </div>
                        """, unsafe_allow_html=True)


                        st.html("""
                        <div class="answer-meta">

                            <span>
                                ASTRA INTEL RESPONSE
                            </span>

                            <span>
                                ● ANALYSIS COMPLETE
                            </span>

                        </div>
                        """)


                        st.markdown(
                            f"""
                            <div class="answer-panel">
                            """,
                            unsafe_allow_html=True
                            )

                        st.markdown(answer)

                        st.markdown(
                            f"""
                            </div>
                            """,
                            unsafe_allow_html=True
                        )


                        # ========================================
                        # SOURCE PAGES
                        # ========================================

                        st.html("""
                        <div class="section-label">
                            SOURCE PAGES
                        </div>
                        """)


                        # Avoid displaying the same page repeatedly
                        displayed_pages = set()


                        for chunk in relevant_chunks:

                            source_key = (
                                chunk["document"],
                                chunk["page"]
                            )


                            if source_key in displayed_pages:
                                continue


                            displayed_pages.add(
                                source_key
                            )


                            st.html(
                                f"""
                                <div class="source-record">

                                    <div class="source-record-header">

                                        <span>
                                            SOURCE / PAGE {page_number}
                                        </span>

                                        <span class="source-record-status">
                                            ● RETRIEVED
                                        </span>

                                    </div>

                                </div>
                                """
                            )


                            with st.expander(
                                f"VIEW PAGE {chunk['document']} PAGE {chunk['page']} EVIDENCE"
                            ):

                                st.write(
                                    chunk["text"]
                                )


                    except requests.exceptions.Timeout:

                        st.error(
                            "OpenRouter request timed out. "
                            "Please try again."
                        )


                    except requests.exceptions.HTTPError:

                        try:

                            error_details = response.json()

                        except Exception:

                            error_details = response.text


                        st.error(
                            f"OpenRouter API request failed: "
                            f"{error_details}"
                        )


                    except Exception as e:

                        st.error(
                            f"AI request failed: {str(e)}"
                        )


    except Exception as e:

        st.error(
            f"PDF processing failed: {str(e)}"
        )


# ============================================================
# ASTRA SYSTEM FOOTER
# ============================================================

st.html("""
<div class="astra-footer">

    <div class="astra-footer-left">
        ASTRA INTEL
    </div>

    <div class="astra-footer-center">
        NX-01 / DOCUMENT INTELLIGENCE
    </div>

    <div class="astra-footer-right">
        ● SYSTEM ONLINE
    </div>

</div>
""")