import os

import pandas as pd
from langchain.chains import ChatVectorDBChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import CSVLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts.chat import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from config import Config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChatBot:
    def __init__(self):
        self.persist_dir = Config.PERSIST_DIR
        self.chat_history = []
        self.qa = None

    def initialize(self):
        try:
            if not os.path.exists(self.persist_dir):
                df = pd.read_csv('data/hotel.csv')
                df = df[["city", "name", "reviews.text"]].head(1000)
                df.to_csv("data/hotel_sample.csv", index=False)

                loader = CSVLoader('data/hotel_sample.csv')
                documents = loader.load()
                text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
                documents = text_splitter.split_documents(documents)

                embeddings = OpenAIEmbeddings(openai_api_key=Config.OPENAI_API_KEY)
                vectorstore = Chroma.from_documents(documents, embeddings, persist_directory=self.persist_dir)
            else:
                vectorstore = Chroma(persist_directory=self.persist_dir, embedding_function=OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY']))

            system_template = """
            Use the following piece of context and chat history and try to respond user's question with few words.
            If you don't know answer "Sorry I don't have this information." 
            If the question is not in the context reply "This is not part of the scope of this chat" 
            ---------
            {context}
            ------------
            {chat_history}
            """

            messages = [SystemMessagePromptTemplate.from_template(system_template),
                        HumanMessagePromptTemplate.from_template("{question}")]

            prompt = ChatPromptTemplate.from_messages(messages)

            self.qa = ChatVectorDBChain.from_llm(ChatOpenAI(temperature=0), vectorstore, qa_prompt=prompt)
            logger.info("Initialization successful.")
        except Exception as e:
            logger.error(f"Error occurred during initialization: {e}")
            raise

    def chat_response(self, query):
        try:
            result = self.qa({"question": query, "chat_history": self.chat_history})
            self.chat_history.append((query, result["answer"]))
            return result["answer"]
        except Exception as e:
            logger.error(f"Error occurred during chat response: {e}")
            return "Sorry, I encountered an issue and cannot respond at the moment."


if __name__ == "__main__":
    chat_bot = ChatBot()
    chat_bot.initialize()
