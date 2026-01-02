from langchain_community.llms import Ollama
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType

class PDFAgent:
    def __init__(self):
        self.llm = Ollama(
            model="mistral",
            temperature=0
        )

        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )

        self.vectorstore = None

    def load_pdf(self, pdf_path):
        try:
            loader = PyPDFLoader(pdf_path)
            docs = loader.load()

            splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )

            chunks = splitter.split_documents(docs)

            self.vectorstore = FAISS.from_documents(
                chunks,
                self.embeddings
            )

        except Exception as e:
            raise RuntimeError(f"PDF loading failed: {e}")

    def create_agent(self):
        if self.vectorstore is None:
            raise ValueError("No document indexed")

        retriever = self.vectorstore.as_retriever()

        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=retriever,
            memory=self.memory
        )

        tools = [
            Tool(
                name="PDF_QA",
                func=qa_chain.run,
                description="Answer questions from the uploaded PDF"
            )
        ]

        agent = initialize_agent(
            tools=tools,
            llm=self.llm,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            memory=self.memory,
            verbose=True,
            handle_parsing_errors=True
        )

        return agent
