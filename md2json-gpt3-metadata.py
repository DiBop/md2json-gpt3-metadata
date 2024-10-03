import os
import json
from openai import OpenAI
import shutil
import re
from collections import Counter
import time

# Create OpenAI client with API key
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

MAX_TOKENS = 8192  # Maximum token limit for "text-embedding-ada-002"
MAX_RETRIES = 3    # Maximum number of retries for failed API requests
RETRY_DELAY = 5    # Delay in seconds between retries

def get_top_keywords(text, num_keywords=5):
    """Extracts the top recurring words from the given text."""
    words = re.findall(r'\b\w+\b', text.lower())
    word_counts = Counter(words)

    # Remove common stop words (you can add more to this list as needed)
    stop_words = set([
        'the', 'is', 'in', 'and', 'to', 'a', 'of', 'for', 'with', 'on', 'at', 
        'by', 'an', 'be', 'this', 'that', 'from', 'it', 'as', 'are', 'or', 'was', 
        'but', 'if', 'then', 'than', 'when', 'while', 'where', 'which', 'who', 'what'
    ])
    filtered_words = {word: count for word, count in word_counts.items() if word not in stop_words}

    top_keywords = [word for word, _ in Counter(filtered_words).most_common(num_keywords)]
    return top_keywords

def truncate_text(text, max_tokens=MAX_TOKENS):
    """Truncate text to be within the token limit."""
    words = text.split()
    if len(words) > max_tokens:
        return ' '.join(words[:max_tokens])
    return text

def generate_gpt3_embedding(text):
    """Generates an embedding for the given text using OpenAI's new client API for embeddings with retries."""
    truncated_text = truncate_text(text)
    
    for attempt in range(MAX_RETRIES):
        try:
            response = client.embeddings.create(
                model="text-embedding-ada-002",  # Use the recommended model
                input=truncated_text,            # The input text for generating the embedding
                timeout=30                       # Timeout for the API request in seconds
            )
            embedding = response.data[0].embedding
            return embedding
        except Exception as e:
            print(f"Error while generating embedding (attempt {attempt + 1}/{MAX_RETRIES}): {e}")
            if attempt < MAX_RETRIES - 1:
                print(f"Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
            else:
                print("Max retries reached. Skipping this file.")
                return None

def markdown_to_individual_json(directory, json_output_directory):
    """Converts all markdown files in the directory into individual JSON files with metadata and moves them to json_output_directory."""
    if not os.path.exists(json_output_directory):
        os.makedirs(json_output_directory)

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                json_file_name = os.path.splitext(file)[0] + '.json'
                json_file_path = os.path.join(json_output_directory, json_file_name)

                # Skip processing if JSON file already exists
                if os.path.exists(json_file_path):
                    print(f"Skipping {file_path} - JSON already exists.")
                    continue

                with open(file_path, 'r', encoding='utf-8') as infile:
                    content = infile.read()

                    # Extract the first line as metadata
                    first_line = content.split('\n', 1)[0].strip() if content else ""

                    # Extract keywords from the content
                    keywords = get_top_keywords(content)

                    # Generate an embedding for the content
                    embedding = generate_gpt3_embedding(content)
                    if embedding is None:
                        continue  # Skip this file if embedding generation failed

                    # Create metadata combining the first line, keywords, and embedding
                    metadata = {
                        "first_line": first_line,
                        "top_keywords": keywords,
                        "embedding": embedding
                    }

                    # Create JSON structure
                    json_data = {
                        "filename": file,
                        "metadata": metadata,
                        "content": content.strip()
                    }

                    # Write the data to individual JSON file
                    with open(json_file_path, 'w', encoding='utf-8') as json_file:
                        json.dump(json_data, json_file, indent=4)

                    print(f"Converted: {file_path} to {json_file_path}")

if __name__ == "__main__":
    # Directory containing markdown files to process
    directory_to_process = "path/to/your/markdown/files"
    # Directory to store the generated JSON files
    json_output_directory = "path/to/your/json/output/directory"

    # Convert each markdown file to its own JSON file and move to the target directory
    markdown_to_individual_json(directory_to_process, json_output_directory)
