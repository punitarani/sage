from langchain.document_loaders import UnstructuredPDFLoader
from langchain.indexes import VectorstoreIndexCreator
import dotenv
import os
from langchain.chat_models import PromptLayerChatOpenAI
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

dotenv.load_dotenv()

class Chat():
    def __init__(self, pdf_folder_path = 'data'):
        loaders = [UnstructuredPDFLoader(os.path.join(pdf_folder_path, fn)) for fn in os.listdir(pdf_folder_path) if os.path.isfile(os.path.join(pdf_folder_path, fn))]
        self.llm = PromptLayerChatOpenAI(streaming=True, callbacks=[StreamingStdOutCallbackHandler()], temperature=0.7, model_name='gpt-4')
        self.index = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory": '.'}).from_loaders(loaders)

    def query(self, query):
        return self.index.query_with_sources(query, llm=self.llm)