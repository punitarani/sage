import openai
import textwrap

class Agent:
    def __init__(self):
        self.task_executor = TaskExecutor()

    def handle_user_input(self, user_input):
        action = self.task_executor.execute_action(user_input)
        response = self.task_executor.generate_response(action)
        return response

class TaskExecutor:
    def __init__(self):
        # Set up OpenAI API credentials
        openai.api_key = ''  # Replace with your OpenAI API key

    def summarize_document(self, document):
        # Define the prompt
        prompt = f"Summarize the following document:\n\n{document}\n\nSUMMARY:"

        # Generate the summary using OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0.0,
            n=1,
            stop=None
        )

        # Extract the summary from the API response
        summary = response.choices[0]['message']['content'].strip()

        # Format the summary
        wrapped_text = textwrap.fill(summary, width=100, break_long_words=False, replace_whitespace=False)

        return wrapped_text

    def calculate_word_count(self, document):
        words = document.split()
        return len(words)

    def execute_action(self, user_input):
        # Check user input and determine the appropriate action
        if user_input.startswith("Summarize the following document:"):
            document = user_input.replace("Summarize the following document:", "").strip()
            return {'type': 'summarize_document', 'document': document}
        elif user_input.startswith("Calculate the word count of the document:"):
            document = user_input.replace("Calculate the word count of the document:", "").strip()
            return {'type': 'calculate_word_count', 'document': document}
        else:
            # Handle other actions as needed
            return {}

    def generate_response(self, action):
        # Check the action type
        if action['type'] == 'summarize_document':
            document = action['document']
            summary = self.summarize_document(document)
            return summary
        elif action['type'] == 'calculate_word_count':
            document = action['document']
            word_count = self.calculate_word_count(document)
            return f"The word count of the document is: {word_count}"
        else:
            # Handle other actions as needed
            return "Unknown action"

# Example usage
agent = Agent()
user_input = "Summarize the following document: World War I or the First World War (28 July 1914 11 November 1918), often abbreviated as WWI, was one of the deadliest global conflicts in history. It was fought between two coalitions, the Allies and the Central Powers. Fighting occurred throughout Europe, the Middle East, Africa, the Pacific, and parts of Asia. An estimated 9 million soldiers were killed in combat, plus another 23 million wounded, while 5 million civilians died as a result of military action, hunger, and disease. Millions more died as a result of genocide, while the 1918 Spanish flu pandemic was exacerbated by the movement of combatants during the war. The first decade of the 20th century saw increasing diplomatic tension between the European great powers. This reached breaking point on 28 June 1914, when a Bosnian Serb named Gavrilo Princip assassinated Archduke Franz Ferdinand, heir to the Austro-Hungarian throne. Austria-Hungary held Serbia responsible, and declared war on 28 July. Russia came to Serbia's defence, and by 4 August, defensive alliances had drawn in Germany, France, and Britain, with the Ottoman Empire joining the war in November. German strategy in 1914 was to first defeat France, then attack Russia. However, this failed, and by the end of 1914, the Western Front consisted of a continuous line of trenches stretching from the English Channel to Switzerland. The Eastern Front was more fluid, but neither side could gain a decisive advantage, despite a series of costly offensives. Fighting expanded onto secondary fronts as Bulgaria, Romania, Greece, and others entered the war between 1915 and 1916. The United States entered the war on the side of the Allies in April 1917, while the Bolsheviks seized power in the Russian October Revolution, and made peace with the Central Powers in early 1918. Freed from the Eastern Front, Germany launched an offensive in the west on March 1918, hoping to achieve a decisive victory before American troops arrived in significant numbers. Failure left the German Imperial Army exhausted and demoralised, and when the Allies took the offensive in August 1918, German forces could not stop the advance. Between 29 September and 3 November 1918, Bulgaria, the Ottoman Empire, and Austria-Hungary agreed to armistices with the Allies, leaving Germany isolated. Facing revolution at home, and with his army on the verge of mutiny, Kaiser Wilhelm II abdicated on 9 November. The Armistice of 11 November 1918 brought the fighting to a close, while the Paris Peace Conference imposed various settlements on the defeated powers, the best-known being the Treaty of Versailles. The dissolution of the Russian, German, Austro-Hungarian, and Ottoman Empires resulted in the creation of new independent states, among them Poland, Czechoslovakia, and Yugoslavia. Failure to manage the instability that resulted from this upheaval during the interwar period contributed to the outbreak of World War II in September 1939."
response = agent.handle_user_input(user_input)
print(response)

user_input = "Calculate the word count of the document: These papers cite the same papers as your selected paper. They tend to bias towards newer papers in the field."
response = agent.handle_user_input(user_input)
print(response)

'''
primary reaserch topic
different view points/ perspectives from the diff papers
how are they similar and the different findings
how does the 1st research paper relate to the other papers
'''
