# Astra_Intel
AI-powered Defense Document Intelligence Application

ASTRA INTEL is a document intelligence application that allows users to upload PDF documents, extract and process their contents, generate concise summaries, ask questions about the uploaded documents, and view the relevant source pages used to answer each query.

The system is designed around document-grounded question answering: the AI is instructed to answer using only information retrieved from the uploaded documents and to explicitly indicate when the requested information is not present.

---

Project Overview

 Defence and technical documents can contain large amounts of information spread across many pages. Finding specific information manually can be time-consuming.

 ASTRA INTEL provides a simple interface for:

 Uploading one or multiple PDF documents

 Extracting text from PDF pages

 Splitting documents into searchable chunks

 Retrieving relevant document sections using TF-IDF

 Generating concise document summaries

 Asking natural-language questions about the uploaded documents

 Generating answers using retrieved document context

 Displaying document names and relevant page numbers

 Viewing the retrieved source evidence

 Handling questions where the requested information is not present

---

Features

 1. Multi-PDF Upload

 Users can upload multiple PDF documents simultaneously.

 2. PDF Text Extraction

 PDF content is extracted page-by-page using PyMuPDF.

 3. Document Chunking

 Extracted text is divided into overlapping chunks to make relevant information easier to retrieve.

 4. Intelligent Retrieval

 ASTRA INTEL uses:

 TF-IDF vectorization

 Cosine similarity
 to identify document chunks that are most relevant to the user's question.

5. AI-Powered Question Answering

 Relevant document sections are passed to an LLM through OpenRouter.

 The model is instructed to:

 Use only the supplied document context

 Avoid outside knowledge

 Avoid inventing information

 Provide relevant page references

 State when information cannot be found


6. Document Summarization

 ASTRA INTEL can generate concise summaries of uploaded documents.

 The summary focuses on information actually present in the supplied documents, including major topics, applications, capabilities, and limitations.

7. Source Evidence

 Each answer can be traced back to the retrieved document and page.

 Users can expand the source section to inspect the extracted evidence.

8. Unsupported-Question Handling

 If the requested information is not available in the retrieved document context, the system is designed to respond that the information was not found rather than inventing an answer.

---

Tech Stack

Technology	Purpose

 Python	Core application logic
 Streamlit	Web application interface
 PyMuPDF (fitz)	PDF text extraction
 Scikit-learn	TF-IDF and cosine similarity
 OpenRouter	LLM API
 requests	API communication
 python-dotenv	Environment variable management
 HTML/CSS	UI styling

---

How It Works

                  USER
                   |
                   v
          +------------------+
          |  Streamlit UI    |
          +------------------+
                   |
                   v
          +------------------+
          |   PDF Upload     |
          +------------------+
                   |
                   v
          +------------------+
          | PyMuPDF / fitz   |
          | Text Extraction  |
          +------------------+
                   |
                   v
          +------------------+
          | Text Chunking     |
          | + Overlap         |
          +------------------+
                   |
                   v
          +------------------+
          | TF-IDF Index      |
          +------------------+
                   |
          USER QUESTION
                   |
                   v
          +------------------+
          | Query Vector      |
          +------------------+
                   |
                   v
          +------------------+
          | Cosine Similarity |
          +------------------+
                   |
                   v
          Relevant Chunks
                   |
                   v
          +------------------+
          | OpenRouter LLM    |
          | Grounded Prompt   |
          +------------------+
                   |
          +--------+---------+
          |                  |
          v                  v
     AI Answer          Source Pages


---

Architecture

 ASTRA INTEL follows a retrieval-augmented document question-answering workflow.

 1. Document Ingestion

  The user uploads one or more PDF files through the Streamlit interface.

 2. Text Extraction

  PyMuPDF extracts text from every available PDF page.

  Each extracted section maintains metadata containing:

  Document name

  Page number

  Extracted text

 ![ASTRA INTEL Architecture]
 (architecture.png) 


 3. Chunking

  Long page text is divided into smaller overlapping chunks.

  The current implementation uses:

  Chunk size: 1800 characters
  Overlap: 200 characters

  This allows the retrieval system to work with smaller sections of the documents.

 4. Retrieval

  The extracted chunks are converted into TF-IDF vectors.

  When a user asks a question:

 1. The question is converted into a TF-IDF vector.


 2. Cosine similarity is calculated against the document chunks.


 3. The most relevant chunks are selected.


 4. Weakly matching chunks are filtered.



 5. Grounded AI Generation

T  he retrieved chunks are added to a structured prompt containing:

  Document name

  Page number

  Relevant text

  User question

  Grounding instructions


  The prompt is sent to an LLM through OpenRouter.

 6. Evidence Display

  The answer is displayed together with the relevant document and page information so the user can inspect the source evidence.

---

AI/ML Pipeline

    PDF Documents
         |
         v
    Text Extraction
          |
          v
    Text Chunking
          |
          v
    TF-IDF Vectorization
          |
          v
    User Question
          |
          v
    Question Vectorization
          |
          v
    Cosine Similarity
          |
          v
    Top Relevant Chunks
          |
          v
    Grounded Prompt
          |
          v
    OpenRouter LLM
          |
          v
    Final Answer
          |
          v
    Source Document + Page

  The application does not directly send the entire uploaded document to the model for every question. Instead, the local retrieval layer identifies relevant sections and provides those sections as context.


---

AI Models and Tools Used

 OpenRouter

 OpenRouter is used as the LLM API layer.

 The application uses:

 openrouter/free

 The exact underlying model may vary because the free router can select an available free model.

 TF-IDF

 TF-IDF is used to represent document chunks and user queries numerically.

 This provides a lightweight retrieval mechanism without requiring a dedicated vector database.

 Cosine Similarity

 Cosine similarity measures the similarity between the user's question vector and document chunk vectors.

 The highest-scoring relevant chunks are passed to the LLM.


---

Installation

 1. Clone the Repository

  git clone YOUR_GITHUB_REPOSITORY_URL
  cd Astra_Intel

 2. Create a Virtual Environment

  python -m venv venv

  Windows

  venv\Scripts\activate

  macOS/Linux

  source venv/bin/activate

 3. Install Dependencies

  pip install -r requirements.txt


---

Environment Variables

 Create a .env file in the project directory:

 OPENROUTER_API_KEY=your_openrouter_api_key

 The API key should never be committed to GitHub.

 Add the following to .gitignore:

 .env
 venv/
 __pycache__/
 *.pyc


---

Running the Application

 Run:

  streamlit run app.py

 Then open the local Streamlit URL displayed in the terminal.


---

Using ASTRA INTEL

 Step 1 — Upload Documents

 Upload one or more PDF documents.

 Step 2 — Process Documents

 ASTRA INTEL extracts and indexes the document content.

 Step 3 — Generate a Summary

 Select:

 GENERATE DOCUMENT SUMMARY

 The system generates a concise summary from the uploaded document content.

 Step 4 — Ask a Question

 Enter a question in:

 ENTER QUERY

 Then select:

 RUN INTELLIGENCE QUERY

 Step 5 — Inspect the Evidence

 The answer includes relevant document/page information.

 The source evidence can be expanded to inspect the retrieved text.


---

Testing

 The application was tested using multiple uploaded technical PDF documents.

 Testing included:

  Document Upload

  Single PDF upload

  Multiple PDF upload


  Extraction

  Page-level text extraction

  Empty/non-text page handling


  Retrieval

  Questions targeting specific sections

  Questions requiring information from multiple documents

  Similarity-based filtering


  Question Answering

  The system was tested with questions involving:

  Document categories

  Applications

  Capabilities

  Comparisons

  Limitations and risks

  Information distributed across multiple documents


  Grounding / Honesty Test

  The system was also tested with questions requesting information that was not actually present in the documents.

  For example, a question asking for a specific percentage that the documents do not provide should result in a response indicating that the information was not found rather than an invented statistic.


---

Limitations

 1. Retrieval Quality

  TF-IDF is a lexical retrieval method. Questions using terminology very different from the document wording may retrieve less relevant sections.

 2. Context Size

  Only the most relevant retrieved chunks are passed to the LLM. Information outside those   retrieved chunks may not be available to the model when generating an answer.
 
 3. PDF Extraction

  Scanned PDFs or PDFs with unusual layouts may not extract correctly if they do not contain machine-readable text.

 4. LLM Availability

  The application depends on the availability and limitations of the configured OpenRouter model.

  Free models may have restrictions on:

  Context size

  Output length

  Availability

  Rate limits


 5. Summary Coverage

  Very large documents may require additional summarization strategies to guarantee complete coverage of every section.

 6. No Permanent Document Database

  Documents are processed during the application session. The current implementation does not provide a persistent document storage or vector database layer.


---

Future Improvements

 Potential improvements include:

 Semantic embeddings for improved retrieval

 Vector database integration

 OCR support for scanned documents

 Better table extraction

 Section-aware document parsing

 Automatic document classification

 Hybrid keyword + semantic retrieval

 More advanced citation mapping

 Per-document and cross-document summary modes

 Persistent document collections

 Improved retrieval evaluation

 Streaming LLM responses

 User authentication and access control

 More comprehensive automated testing



---

Project Structure

 ASTRA-INTEL/
 │
 ├── app.py
 ├── requirements.txt
 ├── README.md
 ├── .gitignore
 ├── .env
 │
 └── sample-documents/
     ├── unmanned-aerial-vehicle-overview.pdf
     ├── defence-electronics-electronic-warfare.pdf
     └── autonomous-systems-unmanned-ground-vehicle.pdf

 > .env should remain local and should not be committed to the repository.




---

AI Usage Disclosure

 AI tools were used during development as development assistance.

 AI-assisted activities

 Used in generation major amount of source code

 Debugging Python and Streamlit code

 Troubleshooting API responses

 Improving prompt structure

 Reviewing retrieval logic

 Identifying implementation errors

 Improving UI formatting

 Developing documentation

 Testing edge cases and unsupported questions


Human implementation

 The project was assembled, configured, tested, and modified to meet the challenge requirements. The final implementation decisions, integration, testing, debugging, and project workflow were validated against the application's actual behavior.

 AI-generated suggestions were reviewed and modified before being incorporated into the project.


---

Security Considerations

 API credentials are stored through environment variables.

 API keys should not be included in source code.

 Uploaded document content is used as context for the requested document-intelligence operation.

 The system is designed to restrict generated answers to retrieved document content.

 The application should not be used as a substitute for expert review of high-stakes information.



---

Conclusion

 ASTRA INTEL provides a lightweight document intelligence workflow combining local document retrieval with LLM-based generation.

 The system focuses on the core requirements of the challenge:

 Upload → Extract → Retrieve → Summarize → Ask → Answer → Show Evidence

 The architecture is intentionally lightweight and can be extended with semantic retrieval, vector databases, OCR, and more advanced document-processing capabilities in future versions.


video link drive 
https://drive.google.com/file/d/1KsgniukYfje8_zuJ1n_nzLRAFDPDm4P5/view?usp=sharing