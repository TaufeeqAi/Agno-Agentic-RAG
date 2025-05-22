# Agentic RAG

Agentic RAG is a Retrieval-Augmented Generation (RAG) system with agentic capabilities, designed to provide accurate and informative responses to user queries by combining retrieval from a knowledge base with generation using a large language model.

## Key Features

- **Retrieval of relevant documents** from a configurable knowledge base.
- **Generation of responses** using a large language model (LLM) like Groq's Llama models.
- **Agentic capabilities** that allow the system to reason, make decisions, and use tools to enhance its responses.
- **Integration with tools** such as reasoning tools for structured thinking and problem-solving.
- **User-friendly interface** built with Streamlit for easy interaction and visualization of results.

## Table of Contents

- [Installation](#installation)
- [Setup](#setup)
- [Running the Application](#running-the-application)
- [Usage](#usage)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/TaufeeqAi/Agno-Agentic-RAG.git
   cd agentic-rag
   ```

2. **Install dependencies**:
   - Ensure you have Python 3.10+ installed.
   - Install the required packages:
     ```bash
     pip install -r requirements.txt
     ```

## Setup

1. **Environment Variables**:
   - Create a `.env` file in the root directory.
   - Add necessary environment variables, such as API keys for Groq or other services:
     ```env
     GROQ_API_KEY=your_groq_api_key
     PINECONE_API_KEY=your_pinecone_api_key
     PINECONE_ENV=your_pinecone_environment
     PINECONE_INDEX=your_pinecone_index_name
     ```

2. **Knowledge Base**:
   - The system uses a knowledge base stored in the `docs` directory.
   - You can add your own PDF documents to this directory to expand the knowledge base.

3. **Vector Database**:
   - The project uses Pinecone for vector storage and retrieval.
   - Ensure your Pinecone index is set up and configured in the `.env` file.

## Running the Application

1. **Start the FastAPI Server**:
   - Navigate to the `backend` directory:
     ```bash
     cd backend
     ```
   - Run the FastAPI server:
     ```bash
     uvicorn app.main:app --reload
     ```

2. **Start the Streamlit UI**:
   - In a new terminal, navigate to the `frontend` directory:
     ```bash
     cd frontend
     ```
   - Run the Streamlit app:
     ```bash
     streamlit run ui.py
     ```

3. **Access the Application**:
   - Open your browser and go to `http://localhost:8501` to interact with the Streamlit UI.

## Usage

1. **Submit a Query**:
   - Enter your question in the text input field on the Streamlit UI.
   - Click the "Submit" button to send the query to the FastAPI server.

2. **View the Response**:
   - The system will retrieve relevant documents, generate a response using the LLM, and display the answer.
   - If reasoning steps are available, they can be viewed by expanding the "Show Reasoning Steps" section.

## Examples

- **Sample Query**: "What are liquid neural networks?"
- **Sample Response**:
  ```
  Liquid neural networks (LNNs) are a type of artificial neural network that is designed to mimic the properties of the human brain, particularly its ability to learn and adapt in a continuous and dynamic manner. They are called "liquid" because they can change and adapt their structure and function in response to new information or experiences, much like a liquid changes shape and form in response to its environment.
  ```

- **Reasoning Steps**:
  ```
  **Step 1:**
  **Title**: Liquid Neural Networks and Chain of Skills
  **Reasoning**: The concept of Liquid Neural Networks is promising for creating AI systems that can learn and adapt in a human-like manner. Their application in building chains of skills could revolutionize how we approach complex tasks in AI.
  **Action**: Explore the current research and limitations of LNNs.
  **Confidence**: 0.8

  **Step 2:**
  **Title**: Potential of LNNs in AI
  **Reasoning**: These features are crucial for building chains of skills, but challenges like scalability, stability, and interpretability need to be addressed.
  **Action**: None
  **Confidence**: 0.9
  ```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a clear description of your changes.

For major changes, please open an issue first to discuss what you would like to change.
