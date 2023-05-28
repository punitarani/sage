# import pdfplumber
# from azure.ai.textanalytics import TextAnalyticsClient
# from azure.core.credentials import AzureKeyCredential

# # Replace with your Azure Cognitive Services credentials
# endpoint = "https://test1211223.cognitiveservices.azure.com/"
# key = "55d5a3c4a9044c249799002bc4e545d7"

# credential = AzureKeyCredential(key)
# client = TextAnalyticsClient(endpoint=endpoint, credential=credential)

# def convert_pdf_to_text(pdf_path):
#     with pdfplumber.open(pdf_path) as pdf:
#         text = ""
#         for page in pdf.pages:
#             text += page.extract_text()
#     return text

# def analyze_document(document):
#     chunks = split_document(document)
#     study_plan = {
#         "key_phrases": [],
#         "sentiment": 0.0,
#         "confidence_scores": {
#             "positive": 0.0,
#             "neutral": 0.0,
#             "negative": 0.0
#         },
#     }
#     if len(chunks) == 0:
#         return study_plan
    
#     sentiment_map = {
#         "positive": 1.0,
#         "neutral": 0.0,
#         "negative": -1.0,
#         "mixed": 0.0  # Default value for unknown sentiment
#     }
    
#     for chunk in chunks:
#         key_phrases = extract_key_phrases(chunk)
#         sentiment, confidence_scores = analyze_sentiment(chunk)
#         study_plan["key_phrases"].extend(key_phrases)
#         study_plan["sentiment"] += float(sentiment_map.get(sentiment, 0.0))
#         study_plan["confidence_scores"] = add_confidence_scores(study_plan["confidence_scores"], confidence_scores)
    
#     if len(chunks) > 0:
#         study_plan["sentiment"] /= len(chunks)
#         study_plan["confidence_scores"] = divide_confidence_scores(study_plan["confidence_scores"], len(chunks))
    
#     return study_plan

# def split_document(document, max_chunk_size=5000):
#     # Split the document into smaller chunks based on the max_chunk_size
#     chunks = []
#     current_chunk = ""
#     words = document.split()
    
#     for word in words:
#         if len(current_chunk) + len(word) + 1 <= max_chunk_size:
#             current_chunk += word + " "
#         else:
#             chunks.append(current_chunk.strip())
#             current_chunk = word + " "
    
#     if current_chunk:
#         chunks.append(current_chunk.strip())
    
#     return chunks

# def extract_key_phrases(text):
#     response = client.extract_key_phrases(documents=[text], language="en")
#     if response[0].is_error:
#         # Handle any errors in the response
#         print("Error:", response[0].error)
#         return []
#     key_phrases = response[0].key_phrases
#     return key_phrases

# def analyze_sentiment(text):
#     response = client.analyze_sentiment(documents=[text], language="en")
#     if response[0].is_error:
#         # Handle any errors in the response
#         print("Error:", response[0].error)
#         return "0.0", {}
#     sentiment = response[0].sentiment
#     confidence_scores = response[0].confidence_scores
#     return sentiment, confidence_scores

# def add_confidence_scores(scores1, scores2):
#     # Add individual confidence score values
#     return {
#         "positive": scores1["positive"] + scores2["positive"],
#         "neutral": scores1["neutral"] + scores2["neutral"],
#         "negative": scores1["negative"] + scores2["negative"],
#     }

# def divide_confidence_scores(scores, divisor):
#     # Divide individual confidence score values by a divisor
#     return {
#         "positive": scores["positive"] / divisor,
#         "neutral": scores["neutral"] / divisor,
#         "negative": scores["negative"] / divisor,
#     }

# # Path to your PDF document
# pdf_path = "ijms-24-02780.pdf"

# # Convert PDF to text
# text = convert_pdf_to_text(pdf_path)

# # Analyze the document and build the research study plan
# study_plan = analyze_document(text)

# # Print the study plan
# print("Research Study Plan:")
# print(study_plan)

import pdfplumber
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

# Replace with your Azure Cognitive Services credentials
endpoint = "https://test1211223.cognitiveservices.azure.com/"
key = "55d5a3c4a9044c249799002bc4e545d7"

credential = AzureKeyCredential(key)
client = TextAnalyticsClient(endpoint=endpoint, credential=credential)

def convert_pdf_to_text(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

def analyze_document(document):
    chunks = split_document(document)
    study_plan = {
        "key_phrases": [],
        "sentiment": 0.0,
        "confidence_scores": {
            "positive": 0.0,
            "neutral": 0.0,
            "negative": 0.0
        },
    }
    if len(chunks) == 0:
        return study_plan
    
    sentiment_map = {
        "positive": 1.0,
        "neutral": 0.0,
        "negative": -1.0,
        "mixed": 0.0  # Default value for unknown sentiment
    }
    
    for chunk in chunks:
        key_phrases = extract_key_phrases(chunk)
        sentiment, confidence_scores = analyze_sentiment(chunk)
        study_plan["key_phrases"].extend(key_phrases)
        study_plan["sentiment"] += float(sentiment_map.get(sentiment, 0.0))
        study_plan["confidence_scores"] = add_confidence_scores(study_plan["confidence_scores"], confidence_scores)
    
    if len(chunks) > 0:
        study_plan["sentiment"] /= len(chunks)
        study_plan["confidence_scores"] = divide_confidence_scores(study_plan["confidence_scores"], len(chunks))
    
    return study_plan

def split_document(document, max_chunk_size=5000):
    # Split the document into smaller chunks based on the max_chunk_size
    chunks = []
    current_chunk = ""
    words = document.split()
    
    for word in words:
        if len(current_chunk) + len(word) + 1 <= max_chunk_size:
            current_chunk += word + " "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = word + " "
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

def extract_key_phrases(text):
    response = client.extract_key_phrases(documents=[text], language="en")
    if response[0].is_error:
        # Handle any errors in the response
        print("Error:", response[0].error)
        return []
    key_phrases = response[0].key_phrases
    return key_phrases

def analyze_sentiment(text):
    response = client.analyze_sentiment(documents=[text], language="en")
    if response[0].is_error:
        # Handle any errors in the response
        print("Error:", response[0].error)
        return "0.0", {}
    sentiment = response[0].sentiment
    confidence_scores = response[0].confidence_scores
    return sentiment, confidence_scores

def add_confidence_scores(scores1, scores2):
    # Add individual confidence score values
    return {
        "positive": scores1["positive"] + scores2["positive"],
        "neutral": scores1["neutral"] + scores2["neutral"],
        "negative": scores1["negative"] + scores2["negative"],
    }

def divide_confidence_scores(scores, divisor):
    # Divide individual confidence score values by a divisor
    return {
        "positive": scores["positive"] / divisor,
        "neutral": scores["neutral"] / divisor,
        "negative": scores["negative"] / divisor,
    }

# Path to your PDF document
pdf_path = "ijms-24-02780.pdf"

# Convert PDF to text
text = convert_pdf_to_text(pdf_path)

# Analyze the document and build the research study plan
study_plan = analyze_document(text)

# Print the study plan
# print("Research Study Plan:")
# print(study_plan)

study_plan = analyze_document(text)

# Access the key phrases
key_phrases = study_plan["key_phrases"]

# Print the extracted key phrases
print("Extracted Key Phrases:")
for phrase in key_phrases:
    print(phrase)
