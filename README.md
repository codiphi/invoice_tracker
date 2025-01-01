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
4. Deployment on AWS EC2 
    1. Ubuntu based t2.micro EC2 instance initialized.
    2. Ngnix reverse proxy set up with public IP.
    3. Changed the inbound rules to allow HTTP requests.


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
10. Serverless implementation.


## Sample Curl Commands

1. Upload a receipt:
```bash
curl -X POST -F "file=@test_data/geeksquad_fake_invoice.jpg" http://localhost:8000/upload-receipt/
```

2. Get monthly summary:
```bash
curl -X POST http://localhost:8000/monthly-summary/ -H "Content-Type: application/json" -d '{"month": 9, "year": 2022}'
```

## 🔮 Future Work

### Dynamic Database Analysis
1. Real-time database schema interpretation
2. Automatic relationship mapping between tables
3. Dynamic query generation based on natural language
4. Performance optimization for large-scale databases
5. Automated index suggestions

### Financial Chat Interface
1. Natural language processing for financial queries
2. Real-time balance updates and notifications
3. Customizable financial alerts
4. Transaction categorization using AI
5. Spending pattern analysis and insights
6. Multi-account support and aggregation

### Dynamic Report Generation
1. Customizable report templates
2. Automated scheduling of reports
3. Multi-format export options (PDF, Excel, CSV)
4. Interactive visualization components
5. Natural language report customization
6. Drill-down capabilities for detailed analysis

### Financial Advisory Features
1. AI-powered investment suggestions
2. Budget optimization recommendations
3. Expense reduction opportunities
4. Savings goal tracking and projections
5. Risk analysis and portfolio suggestions
6. Tax optimization strategies
7. Retirement planning assistance
8. Debt management recommendations

### Implementation Considerations
1. Integration with major financial institutions
2. Enhanced security measures for financial data
3. Compliance with financial regulations
4. Real-time market data integration
5. Machine learning models for predictive analytics
6. Mobile-first design approach
7. Multi-currency support
8. Blockchain integration for transaction verification