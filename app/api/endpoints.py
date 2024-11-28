from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from openai import OpenAI
from app.services.database import init_database, insert_data
from app.services.openai_service import extract_info
from app.services.query_builder import json2query
from app.api.models import MonthRequest
from app.config import DATABASE_PATH, OPENAI_API_KEY
import sqlite3
import json
import base64
from datetime import datetime

router = APIRouter()
client = OpenAI(api_key=OPENAI_API_KEY)

@router.post("/upload-receipt/", response_class=JSONResponse)
async def upload_receipt(file: UploadFile = File(...)):
    try:
        # Init Database
        init_database("receipts.db")
        
        # Read and encode the image
        contents = await file.read()
        base64_image = base64.b64encode(contents).decode("utf-8")

        # Extract information using OpenAI
        json_response = extract_info(base64_image, client)
        json_data = json.loads(json_response)

        # Convert JSON to SQL queries
        queries = json2query(json_data)

        # Connect to database and insert data
        connection = sqlite3.connect("receipts.db")
        try:
            insert_data(connection, queries)
            return JSONResponse(
                content={
                    "message": "Receipt processed successfully",
                    "data": json_data,
                },
                status_code=200,
            )
        finally:
            connection.close()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/monthly-summary/", response_class=JSONResponse)
async def get_monthly_summary(request: MonthRequest):
    try:
        # Validate month
        if not 1 <= request.month <= 12:
            raise HTTPException(
                status_code=400, detail="Month must be between 1 and 12"
            )

        # Use current year if not provided
        year = request.year if request.year is not None else datetime.now().year

        # Format dates
        month_str = str(request.month).zfill(2)
        start_date = f"{year}-{month_str}-01"

        # Calculate end date
        if request.month == 12:
            end_date = f"{year + 1}-01-01"
        else:
            end_date = f"{year}-{str(request.month + 1).zfill(2)}-01"

        # Connect to the database
        try:
            connection = sqlite3.connect("receipts.db")
            cursor = connection.cursor()
        except:
            raise HTTPException(status_code=500, detail=str(e))

        try:
            # Analytics queries
            queries = [
                "SELECT SUM(total) AS total_revenue FROM receipt_or_invoice WHERE date BETWEEN ? AND ?;",
                "SELECT COUNT(*) AS total_invoices FROM receipt_or_invoice WHERE date BETWEEN ? AND ?;",
                "SELECT AVG(total) AS avg_invoice_total FROM receipt_or_invoice WHERE date BETWEEN ? AND ?;",
                "SELECT SUM(tax) AS total_tax FROM receipt_or_invoice WHERE date BETWEEN ? AND ?;",
                "SELECT SUM(discount) AS total_discount FROM receipt_or_invoice WHERE date BETWEEN ? AND ?;",
                "SELECT category, SUM(total) AS category_total FROM receipt_or_invoice WHERE date BETWEEN ? AND ? GROUP BY category ORDER BY category_total DESC LIMIT 3;",
                "SELECT payment_method, COUNT(*) AS method_count FROM receipt_or_invoice WHERE date BETWEEN ? AND ? GROUP BY payment_method ORDER BY method_count DESC LIMIT 1;",
                "SELECT COUNT(*) AS invoices_with_balance FROM receipt_or_invoice WHERE date BETWEEN ? AND ? AND balance > 0;",
                "SELECT SUM(tip) AS total_tips FROM receipt_or_invoice WHERE date BETWEEN ? AND ?;",
            ]

            # Execute queries and collect results
            results = []
            for query in queries:
                cursor.execute(query, (start_date, end_date))
                result = cursor.fetchone()
                results.append(result)

            # Get month name for better readability
            month_name = datetime.strptime(str(request.month), "%m").strftime("%B")

            # Prepare summary
            analytics_summary = {
                "period": f"{month_name} {year}",
                "total_revenue": float(results[0][0]) if results[0][0] else 0,
                "total_invoices": results[1][0],
                "average_invoice_total": float(results[2][0]) if results[2][0] else 0,
                "total_tax": float(results[3][0]) if results[3][0] else 0,
                "total_discount": float(results[4][0]) if results[4][0] else 0,
                "top_categories": results[5] if results[5] else [],
                "most_common_payment": {
                    "method": results[6][0] if results[6] else None,
                    "count": results[6][1] if results[6] else 0,
                },
                "outstanding_balance_count": results[7][0],
                "total_tips": float(results[8][0]) if results[8][0] else 0,
            }

            # Prepare text summary for OpenAI
            analytics_text = [
                f"Summary for {month_name} {year}:",
                (
                    f"Total revenue: ${results[0][0]:,.2f}"
                    if results[0][0]
                    else "No revenue."
                ),
                f"Total invoices: {results[1][0]}",
                (
                    f"Average invoice total: ${results[2][0]:,.2f}"
                    if results[2][0]
                    else "No invoices."
                ),
                (
                    f"Total tax collected: ${results[3][0]:,.2f}"
                    if results[3][0]
                    else "No tax."
                ),
                (
                    f"Total discount applied: ${results[4][0]:,.2f}"
                    if results[4][0]
                    else "No discounts."
                ),
                (
                    f"Top 3 categories by revenue: {results[5]}"
                    if results[5]
                    else "No categories."
                ),
                (
                    f"Most common payment method: {results[6][0]} ({results[6][1]} occurrences)"
                    if results[6]
                    else "No payment methods."
                ),
                f"Invoices with outstanding balance: {results[7][0]}",
                (
                    f"Total tip amount: ${results[8][0]:,.2f}"
                    if results[8][0]
                    else "No tips."
                ),
            ]

            # Create prompt for OpenAI
            prompt = (
                "\n".join(analytics_text)
                + "\n\nGenerate a well rounded verbose paragraph in simple english in simple formatting based on the above analytics."
            )

            # Query OpenAI for natural language summary
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                        ],
                    }
                ],
            )

            # Combine analytics data with AI-generated summary
            final_response = {
                "analytics": analytics_summary,
                "ai_summary": response.choices[0].message.content,
            }

            return JSONResponse(content=final_response["ai_summary"], status_code=200)

        finally:
            connection.close()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))