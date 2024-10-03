# md2json-gpt3-metadata

![Python](https://img.shields.io/badge/Python-3.7%2B-blue) ![License: MIT](https://img.shields.io/badge/License-MIT-green.svg) ![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3-orange)

A Python script that converts Markdown files into individual JSON files via the Windows CLI, enriched with metadata, including top keywords and GPT-3 embeddings. It uses OpenAI's API for semantic embeddings and provides robust error handling and retry logic to ensure reliability. Processed files are skipped automatically, making the script suitable for efficient batch processing of Markdown documents. This is ideal for use cases like **Retrieval-Augmented Generation (RAG)**, where informative content metadata is required.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Prerequisites](#prerequisites)
- [Options and Configurations](#options-and-configurations)
- [License](#license)
- [Contributing](#contributing)

## Features
- **Markdown to JSON Conversion**: Converts `.md` files to `.json` while maintaining clean structure and metadata.
- **Metadata Extraction**: Generates metadata such as the first line of the document and the top 5 keywords.
- **GPT-3 Embeddings**: Uses OpenAI's GPT-3 to create content embeddings, making the JSON output suitable for AI retrieval tasks like RAG.
- **Efficient Processing**: The script skips JSON files that already exist to save API costs and processing time.
- **Retry Logic & Timeout Handling**: Built-in retries with delays to handle network or API-related issues.

## Installation
1. Clone this repository:
   ```sh
   git clone https://github.com/yourusername/md2json-gpt3-metadata.git
   ```
2. Navigate to the project directory:
   ```sh
   cd md2json-gpt3-metadata
   ```
3. Create a virtual environment and activate it:
   ```sh
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```
4. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Prerequisites
- **Windows 11**
- **Python 3.7+**
- **OpenAI API Key**: Set up an API key from [OpenAI](https://beta.openai.com/signup/).
- **Environment Variable Setup**: Add your OpenAI API key as an environment variable:
  ```sh
  export OPENAI_API_KEY='your_openai_api_key_here'
  ```
  On Windows, you can set the environment variable like this:
  ```cmd
  set OPENAI_API_KEY=your_openai_api_key_here
  ```

## Usage
1. Set up your environment variable for the OpenAI API key.
2. Run the script to convert Markdown files:
   ```sh
   python gpt_embedding_json_move.py
   ```
3. Configure directories inside the script:
   - **`directory_to_process`**: Directory containing `.md` files to process.
   - **`json_output_directory`**: Directory where the generated JSON files will be stored.

### Options and Configurations
- **Retry Logic**: The script retries failed requests up to `MAX_RETRIES` times with a delay (`RETRY_DELAY`) between attempts.
- **Timeout**: API calls have a timeout of `30 seconds` to prevent indefinite hanging.
- **Token Limit Handling**: Automatically truncates content to ensure the input size is within GPT-3's token limit (8192 tokens).

## Example Output
A sample `.json` file created by the script might look like this:
```json
{
    "filename": "example.md",
    "metadata": {
        "first_line": "This is an example markdown file.",
        "top_keywords": ["example", "markdown", "file"],
        "embedding": [0.123, -0.456, ...]
    },
    "content": "This is the full content of the markdown file..."
}
```

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

![MIT License](https://img.shields.io/badge/License-MIT-green.svg)

## Contributing
Contributions are welcome! Please open an issue or submit a pull request to suggest improvements or bug fixes.
