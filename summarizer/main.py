import time
from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders import PyPDFLoader
from langchain import OpenAI, PromptTemplate
import glob
import openai
import textwrap

# python
llm = OpenAI(temperature=0.2)

class Agent:
    def __init__(self):
        self.task_executor = TaskExecutor()

    def handle_user_input(self, user_input):
        action = self.task_executor.execute_action(user_input)
        response, response_time = self.task_executor.generate_response(action)
        return response, response_time

class TaskExecutor:
    def __init__(self):
        # Set up OpenAI API credentials
        # openai.api_key = ''  # Replace with your OpenAI API key
        pass
    
    def pdfs(self, pdfs_folder):
        return glob.glob(pdfs_folder + "/*.pdf")

    def summarize_pdfs_from_folder(self, pdfs_folder):
        summaries = []
        for pdf_file in self.pdfs(pdfs_folder):
            loader = PyPDFLoader(pdf_file)
            docs = loader.load_and_split()
            chain = load_summarize_chain(llm, chain_type="map_reduce")
            summary = chain.run(docs)
            print("Summary for: ", pdf_file)
            print(summary)
            print("\n")
            summaries.append(summary)
        
        return summaries
    
    def execute_action(self, user_input):
        # Check user input and determine the appropriate action
        if user_input.startswith("Summarize the following documents:"):
            pdfs_folder = user_input.replace("Summarize the following documents:", "").strip()
            return {'type': 'summarize_document', 'document': pdfs_folder}
        else:
            # Handle other actions as needed
            return {}
        
    def generate_response(self, action):
        # Check if the 'type' key exists in the action dictionary
        if 'type' in action:
            # Check the action type
            if action['type'] == 'summarize_document':
                pdfs_folder = action['document']
                start_time = time.time()
                summary = self.summarize_pdfs_from_folder(pdfs_folder)
                end_time = time.time()
                response_time = end_time - start_time
                return summary, response_time
        
        # Handle the case where the action type is not recognized
        return "Unknown action", 0


# Example usage
agent = Agent()
pdf_folder = "./pdfs"  # Replace "./pdfs" with the desired PDF folder path
user_input = f"Summarize the following documents: {pdf_folder}"
response, response_time = agent.handle_user_input(user_input)
print(response)

print(f"Response Time: {response_time} seconds")
