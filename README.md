# AI Marketing Email Generator

## Project Overview
The AI Marketing Email Generator is a FastAPI-based tool that leverages OpenAI's GPT models to automatically generate high-converting email subject lines and full marketing emails. This project is designed for marketers, founders, and businesses looking to save time and increase engagement with AI-powered email content.

## Project Objectives
- Automatically generate multiple catchy subject lines for marketing emails.
- Generate complete email content based on a selected subject line.
- Provide an AI-driven quality score for each email.
- Persist generated emails in a database for analytics and future reference.
- Demonstrate integration of FastAPI, LangChain, and OpenAI in a real-world application.

## Features
- Generate multiple email subject lines.
- Generate full email content using selected subject line.
- Assign a quality score to each generated email.
- Store all emails and metadata in SQLite database.

## Tech Stack
- **Python**: Backend logic and API implementation.
- **FastAPI**: API framework for endpoints.
- **OpenAI GPT**: AI for generating email content.
- **LangChain**: Orchestrating AI prompts and workflow.
- **SQLite + SQLAlchemy**: Database for storing generated emails.
- **Pydantic**: Data validation and schema definitions.

## Installation
Clone the repository and navigate to the project folder:
```bash
git clone https://github.com/yourusername/ai-marketing-email-generator.git
cd ai-marketing-email-generator
```

Create and activate a virtual environment (optional but recommended):
```bash
python -m venv venv
# Windows
env\\Scripts\\activate
# macOS/Linux
source venv/bin/activate
```

Install required dependencies:
```bash
pip install -r requirements.txt
```

## Configuration
Create a `.env` file in the project root and add the following:
```env
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=sqlite:///./test.db
HOST=0.0.0.0
PORT=8000
```

## Running the Project
Start the FastAPI server:
```bash
python -m app.main
```
Access the API documentation at:
```
http://127.0.0.1:8000/docs
```

## Example API Workflow
1. **Generate Subject Lines**: POST request to `/generate-subject-lines` with product details.
2. **Select a Subject Line** from the response.
3. **Generate Email**: POST request to `/generate-email` with the selected subject line and product details.

## Screenshots
*You can add screenshots of the API in action here.*
1. Input to generate different subjects for an email
   <img width="1656" height="860" alt="image" src="https://github.com/user-attachments/assets/d6717145-fa2c-4ff5-ae3a-16b7c0a8f4e2" />
   
2. Output for various Subjects
    <img width="1670" height="588" alt="image" src="https://github.com/user-attachments/assets/a48e2b90-14b5-407c-b9d6-e341d37fa960" />
    
3. Input to generate an email
   <img width="1443" height="727" alt="image" src="https://github.com/user-attachments/assets/239a81bd-bbf0-4860-b13e-78c9efa6ea8d" />
   
4. Output of the generated email
   <img width="1576" height="633" alt="image" src="https://github.com/user-attachments/assets/127a96da-d7ef-447c-85de-ba2602ee4690" />

5. Data stored in SQLyog
   <img width="1704" height="751" alt="image" src="https://github.com/user-attachments/assets/c372f5f2-93d8-4b6c-8967-60573aa158d2" />

   <img width="827" height="443" alt="image" src="https://github.com/user-attachments/assets/2960d317-4d57-4044-b88e-3bf7a8d19bfc" />



Example:
```
curl -X POST http://127.0.0.1:8000/generate-subject-lines -H 'Content-Type: application/json' -d '{"product_name": "GlowMax Serum", "product_description": "Vitamin C serum", "audience": "women 22-40", "tone": "friendly", "goal": "increase signups"}'
```

## License
MIT License
