import dotenv
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chat_models import PromptLayerChatOpenAI
from langchain.document_loaders import PyMuPDFLoader
from langchain.indexes import VectorstoreIndexCreator

from sage import DATA_DIR

dotenv.load_dotenv()


class Chat():
    def __init__(self, pdf_folder_path=DATA_DIR):
        loaders = [
            PyMuPDFLoader(str(pdf_file))
            for pdf_file in pdf_folder_path.iterdir() if pdf_file.is_file()
        ]
        self.llm = PromptLayerChatOpenAI(
            streaming=True,
            callbacks=[StreamingStdOutCallbackHandler()],
            temperature=0.7,
            model_name='gpt-4'
        )
        self.index = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory": '.'}).from_loaders(loaders)

    def query(self, query):
        return self.index.query_with_sources(query, llm=self.llm)
