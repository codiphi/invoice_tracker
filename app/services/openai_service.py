from openai import OpenAI
from app.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def extract_info(base64_image, client):
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """return name of the vendor, itemized breakdown with cost and address. Return it in json based on this schema, if the info is not there, return Not Provided
            {
  "receipt_or_invoice": {
    "category": "string"               // Assign a category for the receipt/invoice out of [ Travel, Food, Miscellanous, Office Supplies, Software, Repairs ]
    "id": "string",                    // Unique identifier for the receipt/invoice
    "date": "string",                 // Date of the transaction in ISO 8601 format (e.g., "2024-11-27")
    "vendor": {
      "name": "string",               // Vendor name
      "address": {
        "street": "string",           // Street address
        "city": "string",             // City name
        "state_or_province": "string",// State or province
        "postal_code": "string",      // Postal code
        "country": "string",          // Country name
        "phone": "string",            // Vendor phone number
        "email": "string"             // Vendor email
      }
    },
    "items": [
      {
        "description": "string",      // Item description
        "unit_price": "number",       // Price per unit
        "quantity": "number",         // Quantity purchased
        "line_total": "number"        // Total price for the line item (unit_price * quantity)
      }
    ],
    "totals": {
      "subtotal": "number",           // Subtotal before any discounts or taxes
      "discount": "number",           // Discount applied
      "tax": "number",                // Tax amount
      "tip": "number",                // Tip amount (if applicable)
      "total": "number",              // Total after all calculations
      "balance": "number"             // Remaining balance (if applicable)
    },
    "payment": {
      "method": "string",             // Payment method (e.g., "Credit Card", "Auto-Debit")
      "details": "string"             // Payment details (e.g., "Visa ending in 1234")
    },
    "notes": "string"                 // Additional notes or information
  }
}
    """,
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
    )
    print(response.choices[0].message.content)
    return response.choices[0].message.content

