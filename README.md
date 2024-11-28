# Receipt Processing API

A FastAPI-based service that processes receipts using OpenAI's vision capabilities and provides detailed financial analytics.

## 🚀 Features

- Receipt/invoice image processing and data extraction
- Monthly financial summaries and analytics
- AI-powered natural language reporting
- Structured data storage and querying
- RESTful API endpoints

## 🛠️ Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **OpenAI API**: AI-powered image processing and text generation
- **SQLite**: Lightweight database for data storage
- **Python 3.11+**: Core programming language
- **Pydantic**: Data validation using Python type annotations
- **uvicorn**: ASGI server implementation

## 📋 Prerequisites

- Python 3.11 or higher
- OpenAI API key
- Virtual environment (recommended)

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/receipt-processing-api.git
cd receipt-processing-api
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set the OpenAI API key:
```bash
export OPENAI_API_KEY=<your-openai-api-key>
```

5. Run the server:
```bash
uvicorn app.main:app --reload
```

## Approach Used

1. The image is processed using OpenAI's vision API to extract information.
    1. Extracted information is in JSON format.
    2. The JSON is then converted to SQL queries.
2. The information is then stored in a SQLite database.
    1. The database is initialized and the queries are executed.
    2. There are 3 tables in the database:
        1. `receipt_or_invoice`: Stores the receipt data.
        2. `items`: Stores the items data.
        3. `vendors`: Stores the vendors data.
3. The data is then queried to provide a monthly summary and analytics. 
    1. Multiple queries are executed to get the required data.
    2. The data is then formatted in text format.
    3. The text is sent over to OpenAI to generate a report.


## Scaling for enterprise

1. Deploying the database on an SQL database like AWS RDS or Azure SQL.
2. Implementing better error handling and logging.
3. Implement a confidence score to check the reliability of the data first with a smaller model and then use a more accurate model if required.
4. User login and authentication.
5. Segregating of prompts that should be dynamically updated if there are changes to the database schema. 
6. Rate limiting to prevent abuse.
7. Monitoring using Langfuse or Langsmith. 
8. An API that can dynamically generate queries and provide response based on the user input
9. Versioning, CI/CD pipeline, Rollbacks, etc.


## Sample Curl Commands

1. Upload a receipt:
```bash
curl -X POST -F "file=@test_data/geeksquad_fake_invoice.jpg" http://localhost:8000/upload-receipt/
```

2. Get monthly summary:
```bash
curl -X POST http://localhost:8000/monthly-summary/ -H "Content-Type: application/json" -d '{"month": 9, "year": 2022}'
```

