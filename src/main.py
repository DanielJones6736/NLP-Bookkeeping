from src.config import gemini_api_key
from fastapi import FastAPI, HTTPException, Query, Path, Body, status
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from google.genai import types
from src import database_tools
from datetime import datetime
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field



app = FastAPI()

# add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all sources, recommend specifying specific domains in production
    allow_credentials=True,
    allow_methods=["*"],  # allow all HTTP methods
    allow_headers=["*"],  # allow all request headers
)

database = database_tools.Database_Tools()

gemini_instructions = \
"You are being used in a bookkeeping personal finance app to perform CRUD operations to a database." \
" Based on the user input you must choose the appropriate function and populate its parameters. " \
"The functions are: " \
"add_expense(amount:float, note:str, category:str, date:str) -> bool, " \
"add_pay(amount:float, note:str, category:str, date:str) -> bool, " \
"update_expense(record_id:int, amount:float=None, note:str=None, category:str=None, date:str=None) -> bool, " \
"update_pay(record_id:int, amount:float=None, note:str=None, category:str=None, date:str=None) -> bool, " \
"delete_record(record_id:int = None) -> bool, " \
"get_total_amount_by_type(record_type:str=None) -> float, " \
"get_monthly_total(record_type:str=None, month:int=None, year:int=None) -> float, " \
"get_notes_list(record_type:str, month:int, year:int) -> list, " \
"get_category_list(record_type:str, month:int, year:int) -> list, " \
"get_average_amount(record_type:str, month:int, year:int) -> float, " \
"get_transaction_history(record_type:str=None, month:int=None, year:int=None, file_format:str='json') -> Any. " \
"ai_analyze(record_type:str, month:int, year:int, question:str) -> Any. " \
"batch_add_records(records:list) -> dict, " \
"For any prompt that doesn't fall into any of the functions above, call the ai_analyze function. " \
"Make sure to only use the parameters that are needed for the function. " \
"For delete_record, if the latest record is to be deleted, then record_id should be None or the ID of the record. " \
"If no user input is provided, use the parameter value None. " \
"Try to convert relative dates into absolute dates. Example, today equals yyyy-mm-dd. " \
"For expenses, use appropriate categories from: Food, Groceries, Transportation, Housing, Entertainment, Shopping, Utilities, Health, Education, Travel, Other. " \
"For income, use appropriate categories from: Salary, Bonus, Gift, Investment, Refund, Other. " \
"If the user input contains multiple transactions, use batch_add_records function with array of records. Each record must contain all required fields. " \
"User prompt: "



def add_expense(amount:float, note:str, category:str, date:str):
    """
    Adds an expense record to the database.

    Args:
        amount (float): The monetary value of the expense.
        note (str): The note describing the expense.
        category (str): The category of the expense.
        date (str): The date of the expense in string format (e.g., 'YYYY-MM-DD').

    Returns:
        bool: True if the expense was successfully added to the database, False otherwise.
    """
    # Logic to add expense to the database
    print(f"add_expense has been called with the following parameters: {str(amount)}, {str(note)}, {str(category)}, {str(date)}")
    return database.insert_data("expense", amount=amount, note=note, category=category, date=date)


def add_pay(amount: float, note: str, category: str, date: str):
    """
    Adds a payment record to the database.
    Args:
        amount (float): The amount of the payment.
        note (str): The note or description of the payment.
        category (str): The category of the payment.
        date (str): The date of the payment in string format.
    Returns:
        bool: True if the payment was successfully added to the database, False otherwise.
    """
    # Logic to add payment to the database
    print(f"add_pay has been called with the following parameters: {str(amount)}, {str(note)}, {str(category)}, {str(date)}")
    return database.insert_data("pay", amount=amount, note=note, category=category, date=date)


def update_expense(record_id:int, amount:float=None, note:str=None, category:str=None, date:str=None):
    """
    Parameters:
        record_id (int): The unique identifier of the expense record to update.
        amount (float, optional): The new amount for the expense. Defaults to None.
        note (str, optional): The new note associated with the expense. Defaults to None.
        category (str, optional): The new category of the expense. Defaults to None.
        date (str, optional): The new date of the expense in 'YYYY-MM-DD' format. Defaults to None.

    Returns:
        bool: True if the update was successful, False otherwise.
    """
    # Logic to update expense in the database
    print(f"update_expense has been called with the following parameters: {str(record_id)}, {str(amount)}, {str(note)}, {str(category)}, {str(date)}")
    return database.update_data(record_type="expense", record_id=record_id, amount=amount, note=note, category=category, date=date)


def update_pay(record_id:int, amount:float=None, note:str=None, category:str=None, date:str=None):
    """
    Updates an existing payment record in the database.

    Args:
        record_id (int): The unique identifier of the payment record to update.
        amount (float, optional): The new payment amount. Defaults to None.
        note (str, optional): The note or description of the payment. Defaults to None.
        category (str, optional): The category of the payment. Defaults to None.
        date (str, optional): The date of the payment in string format. Defaults to None.

    Returns:
        bool: True if the update was successful, False otherwise.
    """
    # Logic to update payment in the database
    print(f"update_pay has been called with the following parameters: {str(record_id)}, {str(amount)}, {str(note)}, {str(category)}, {str(date)}")
    return database.update_data(record_type="pay", record_id=record_id, amount=amount, note=note, category=category, date=date)


def delete_record(record_id:int = None):
    """
    Deletes a record from the database.

    Args:
        record_id (int, optional): The unique identifier of the record to be deleted. Defaults to None.

    Returns:
        bool: True if the record was successfully deleted, False otherwise.
    """
    # Logic to delete expense from the database
    print(f"delete_record has been called with the following parameters: {str(record_id)}")
    return database.delete_data(record_id=record_id)


def get_total_amount_by_type(record_type:str=None):
    """
    Get the total amount of expenses by a specific type from the database.

    This function retrieves the total amount of expenses filtered by the specified 
    record type. If no record type is provided, it calculates the total amount 
    for all types.

    Args:
        record_type (str, optional): The type of record to filter expenses by. 
            Defaults to None, which means no filtering is applied.

    Returns:
        float: The total amount of expenses for the specified type or all types 
            if no type is specified.
    """
    # Logic to get total amount by type from the database
    print(f"get_total_amount_by_type has been called with the following parameters: {str(record_type)}")
    return database.calculate_total_amount(record_type=record_type)


def get_monthly_total(record_type:str=None, month:int=None, year:int=None):
    """
    Args:
        record_type (str, optional): The type of record to filter by (e.g., "expense", "income"). Defaults to None.
        month (int, optional): The month for which the total is calculated (1 for January, 12 for December). Defaults to None.
        year (int, optional): The year for which the total is calculated. Defaults to None.

    Returns:
        float: The total amount of expenses for the specified month and year.
    """
    # Logic to get monthly total from the database
    print(f"get_monthly_total has been called with the following parameters: {str(record_type)}, {str(month)}, {str(year)}")
    return database.calculate_monthly_total(record_type=record_type, month=month, year=year)


def get_notes_list(record_type:str, month:int, year:int):
    """
    Retrieves a list of notes from the database based on the specified record type, month, and year.

    Args:
        record_type (str): The type of record to filter the notes (e.g., 'expense', 'pay').
        month (int): The month for which to retrieve the notes (1-12).
        year (int): The year for which to retrieve the notes.

    Returns:
        list: A list of notes retrieved from the database matching the specified criteria.
    """
    # Logic to get note list from the database
    print(f"get_source_list has been called with the following parameters: {str(record_type)}, {str(month)}, {str(year)}")
    return database.list_notes(record_type=record_type, month=month, year=year)


def get_category_list(record_type:str, month:int, year:int):
    """
    Retrieves a list of categories from the database based on the specified record type, month, and year.

    Args:
        record_type (str): The type of record to filter the categories (e.g., 'expense', 'pay').
        month (int): The month for which to retrieve the categories (1-12).
        year (int): The year for which to retrieve the categories.

    Returns:
        list: A list of categories retrieved from the database matching the specified criteria.
    """
    # Logic to get category list from the database
    print(f"get_category_list has been called with the following parameters: {str(record_type)}, {str(month)}, {str(year)}")
    return database.list_categories(record_type=record_type, month=month, year=year)


def get_average_amount(record_type:str, month:int, year:int):
    """
    Calculate the average amount of expenses for a specific record type, month, and year.

    Args:
        record_type (str): The type of record to filter by (e.g., "expense", "income").
        month (int): The month for which to calculate the average (1 for January, 12 for December).
        year (int): The year for which to calculate the average.

    Returns:
        float: The average amount of the specified record type for the given month and year.

    Raises:
        ValueError: If the provided month is not in the range 1-12.
        DatabaseError: If there is an issue querying the database.
    """
    # Logic to get average amount from the database
    print(f"get_average_amount has been called with the following parameters: {str(record_type)}, {str(month)}, {str(year)}")
    return database.calculate_average_amount(record_type=record_type, month=month, year=year)


def get_transaction_history(record_type:str=None, month:int=None, year:int=None, file_format:str="list"):
    """
    Retrieves the transaction history from the database based on the specified parameters.

    Args:
        record_type (str, optional): The type of transaction records to retrieve (e.g., "income", "expense").
        month (int, optional): The month for which to retrieve transaction history (1-12).
        year (int, optional): The year for which to retrieve transaction history.
        file_format (str, optional): The format in which to export the data (default is "json").

    Returns:
        Any: The exported transaction data in the specified file format.

    Raises:
        ValueError: If invalid parameters are provided.
        DatabaseError: If there is an issue accessing the database.
    """
    # Logic to get transaction history from the database
    print(f"get_transaction_history has been called with the following parameters: {str(record_type)}{str(month)}, {str(year)}, {str(file_format)}")
    return database.export_data(file_format=file_format, record_type=record_type, month=month, year=year)


def ai_analyze(question: str, record_type:str=None, month:int=None, year:int=None):
    """
    Retrieves transaction history and analyzes it using Gemini AI.

    Args:
        record_type (str): The type of transaction records to retrieve (e.g., "income", "expense").
        month (int): The month for which to retrieve transaction history (1-12).
        year (int): The year for which to retrieve transaction history.
        question (str): The question to analyze the transaction data.

    Returns:
        dict: The analysis result from Gemini AI.
    """
    print(f"ai_analyze has been called with the following parameters: {str(record_type)}, {str(month)}, {str(year)}, {str(question)}")

    # Retrieve transaction history
    transaction_history = database.export_data(
        file_format="csv", record_type=record_type, month=month, year=year
    )

    if not transaction_history:
        raise HTTPException(status_code=404, detail="No transaction history found.")

    # Set up the client
    client = genai.Client(api_key=gemini_api_key)

    # Prepare the prompt for analysis
    analysis_prompt = (
        f"Here is the transaction history in CSV format: {transaction_history}\n"
        f"Question: {question}\n"
        f"Provide a detailed analysis based on the data that answers the prompted question."
    )

    # Generate content using the model
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[analysis_prompt],
        config=types.GenerateContentConfig(),
    )

    # Return the analysis result
    analysis_result = response.candidates[0].content.parts[0].text.strip()
    return {"status": "success", "analysis": analysis_result}


def batch_add_records(records):
    """
    批量添加多条交易记录。

    Args:
        records (list): 包含多条记录数据的列表，每条记录应包含：
                       type, amount, note, category, date

    Returns:
        dict: 包含操作结果和添加的记录ID列表
    """
    print(f"batch_add_records has been called with {len(records)} records")
    try:
        # 确保所有数值都是Python原生类型
        for record in records:
            if 'amount' in record:
                record['amount'] = float(record['amount'])
        
        added_ids = database.batch_insert_data(records)
        
        # 确保返回的ID是Python原生类型
        added_ids = [int(id) for id in added_ids]
        
        return {"status": "success", "message": f"成功添加{len(added_ids)}条记录", "record_ids": added_ids}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.get("/")
async def root():
    return {"message": "Hello World..."}

@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/genai/{prompt}")
async def genai_api(prompt:str, max_output_tokens:int=512):
    """
    Generate text using Google GenAI API.
    """
    # Set up the client
    client = genai.Client(
        api_key=gemini_api_key,
    )

    # 添加批量添加函数声明
    # Create a function declaration for the tool
    function_batch_add = types.FunctionDeclaration(
        name="batch_add_records",
        description="批量添加多条交易记录。",
        parameters=types.Schema(
            type="OBJECT",
            properties={
                "records": types.Schema(
                    type="ARRAY",
                    description="包含多条记录数据的列表，每条记录需包含type, amount, note, category, date",
                    items=types.Schema(
                        type="OBJECT",
                        properties={
                            "type": types.Schema(type="STRING", description="记录类型 ('expense' 或 'pay')"),
                            "amount": types.Schema(type="NUMBER", description="交易金额"),
                            "note": types.Schema(type="STRING", description="交易说明"),
                            "category": types.Schema(type="STRING", description="交易分类"),
                            "date": types.Schema(type="STRING", description="交易日期")
                        },
                        required=["type", "amount", "note", "category", "date"]
                    )
                )
            },
            required=["records"]
        )
    )
    function_add_expense = types.FunctionDeclaration(
        name="add_expense",
        description="Add an expense to the database.",
        parameters=types.Schema(
            type="OBJECT",
            properties={
                "amount": types.Schema(type="NUMBER", description="The amount of the expense."),
                "note": types.Schema(type="STRING", description="The note describing the expense."),
                "category": types.Schema(type="STRING", description="The category of the expense."),
                "date": types.Schema(type="STRING", description="The date of the expense."),
            },
            required=["amount", "note", "category", "date"],
        ),
    )
    function_add_pay = types.FunctionDeclaration(
        name="add_pay",
        description="Add a payment to the database.",
        parameters=types.Schema(
            type="OBJECT",
            properties={
                "amount": types.Schema(type="NUMBER", description="The amount of the payment."),
                "note": types.Schema(type="STRING", description="The note describing the payment."),
                "category": types.Schema(type="STRING", description="The category of the payment."),
                "date": types.Schema(type="STRING", description="The date of the expense."),
            },
            required=["amount", "note", "category", "date"],
        ),
    )
    function_update_expense = types.FunctionDeclaration(
        name="update_expense",
        description="Update an existing expense in the database.",
        parameters=types.Schema(
            type="OBJECT",
            properties={
                "record_id": types.Schema(type="NUMBER", description="The ID of the record to update."),
                "amount": types.Schema(type="NUMBER", description="The new amount of the expense."),
                "note": types.Schema(type="STRING", description="The new note for the expense."),
                "category": types.Schema(type="STRING", description="The new category of the expense."),
                "date": types.Schema(type="STRING", description="The new date of the expense."),
            },
            required=["record_id"],
        ),
    )
    function_update_pay = types.FunctionDeclaration(
        name="update_pay",
        description="Update an existing payment in the database.",
        parameters=types.Schema(
            type="OBJECT",
            properties={
                "record_id": types.Schema(type="NUMBER", description="The ID of the record to update."),
                "amount": types.Schema(type="NUMBER", description="The new amount of the payment."),
                "note": types.Schema(type="STRING", description="The new note for the payment."),
                "category": types.Schema(type="STRING", description="The new category of the payment."),
                "date": types.Schema(type="STRING", description="The new date of the payment."),
            },
            required=["record_id"],
        ),
    )
    function_delete_record = types.FunctionDeclaration(
        name="delete_record",
        description="Delete a record from the database.",
        parameters=types.Schema(
            type="OBJECT",
            properties={
                "record_id": types.Schema(type="NUMBER", description="The ID of the record to delete."),
            },
            required=[],
        ),
    )
    function_get_total_amount = types.FunctionDeclaration(
        name="get_total_amount_by_type",
        description="Get the total amount of a record type in the database.",
        parameters=types.Schema(
            type="OBJECT",
            properties={
                "record_type": types.Schema(type="STRING", description="The type of the record ('expense' or 'pay')."),
            },
            required=[],
        ),
    )
    function_get_monthly_total = types.FunctionDeclaration(
        name="get_monthly_total",
        description="Get the total amount of expenses for a specific month in the database.",
        parameters=types.Schema(
            type="OBJECT",
            properties={
                "record_type": types.Schema(type="STRING", description="The type of the record ('expense' or 'pay')."),
                "month": types.Schema(type="NUMBER", description="The month for which to get the total."),
                "year": types.Schema(type="NUMBER", description="The year for which to get the total."),
            },
            required=[],
        ),
    )
    function_get_source_list = types.FunctionDeclaration(
        name="get_source_list",
        description="Get the list of notes from the database.",
        parameters=types.Schema(
            type="OBJECT",
            properties={
                "record_type": types.Schema(type="STRING", description="The type of the record ('expense' or 'pay')."),
                "month": types.Schema(type="NUMBER", description="The month for which to get the notes."),
                "year": types.Schema(type="NUMBER", description="The year for which to get the notes."),
            },
            required=[],
        ),
    )
    function_get_category_list = types.FunctionDeclaration(
        name="get_category_list",
        description="Get the list of categories from the database.",
        parameters=types.Schema(
            type="OBJECT",
            properties={
                "record_type": types.Schema(type="STRING", description="The type of the record ('expense' or 'pay')."),
                "month": types.Schema(type="NUMBER", description="The month for which to get the categories."),
                "year": types.Schema(type="NUMBER", description="The year for which to get the categories."),
            },
            required=[],
        ),
    )
    function_get_average_amount = types.FunctionDeclaration(
        name="get_average_amount",
        description="Get the average amount of expenses for a specific month in the database.",
        parameters=types.Schema(
            type="OBJECT",
            properties={
                "record_type": types.Schema(type="STRING", description="The type of the record ('expense' or 'pay')."),
                "month": types.Schema(type="NUMBER", description="The month for which to get the average."),
                "year": types.Schema(type="NUMBER", description="The year for which to get the average."),
            },
            required=[],
        ),
    )
    function_get_transaction_history = types.FunctionDeclaration(
        name="get_transaction_history",
        description="Get the transaction history for a specific month in the database.",
        parameters=types.Schema(
            type="OBJECT",
            properties={
                "file_format": types.Schema(type="STRING", description="The format in which to export the data (default is 'json')."),
                "record_type": types.Schema(type="STRING", description="The type of the record ('expense' or 'pay')."),
                "month": types.Schema(type="NUMBER", description="The month for which to get the transaction history."),
                "year": types.Schema(type="NUMBER", description="The year for which to get the transaction history."),
            },
            required=[],
        ),
    )
    function_ai_analyze = types.FunctionDeclaration(
        name="ai_analyze",
        description="Analyze transaction history using AI.",
        parameters=types.Schema(
            type="OBJECT",
            properties={
                "question": types.Schema(type="STRING", description="The question to analyze the transaction data."),
                "record_type": types.Schema(type="STRING", description="The type of transaction records to retrieve (e.g., 'income', 'expense')."),
                "month": types.Schema(type="NUMBER", description="The month for which to retrieve transaction history (1-12)."),
                "year": types.Schema(type="NUMBER", description="The year for which to retrieve transaction history."),
            },
            required=["question"],
        ),
    )
    tool = types.Tool(function_declarations=[
        function_batch_add,
        function_add_expense, 
        function_add_pay,
        function_update_expense,
        function_update_pay,
        function_delete_record,
        function_get_total_amount,
        function_get_monthly_total,
        function_get_source_list,
        function_get_category_list,
        function_get_average_amount,
        function_get_transaction_history,
        function_ai_analyze
    ])


    # Generate content using the model
    response = client.models.generate_content(
        model="gemini-2.0-flash", 
        contents = [gemini_instructions + prompt],
        config=types.GenerateContentConfig(
            tools =[
                tool,
            ]
        ),
    )
    
    # check if response.function_calls exists
    print(f"response.function_call[0]: {response.function_calls[0]}")

    # Define a mapping of function names to their corresponding handlers
    function_mapping = {
        "batch_add_records": batch_add_records,
        "add_expense": add_expense,
        "add_pay": add_pay,
        "update_expense": update_expense,
        "update_pay": update_pay,
        "delete_record": delete_record,
        "get_total_amount_by_type": get_total_amount_by_type,
        "get_monthly_total": get_monthly_total,
        "get_notes_list": get_notes_list,
        "get_category_list": get_category_list,
        "get_average_amount": get_average_amount,
        "get_transaction_history": get_transaction_history,
        "ai_analyze": ai_analyze,
    }
    
    # Call the function based on the response
    function_call = response.candidates[0].content.parts[0].function_call
    function_name = function_call.name
    function_args = function_call.args
    
    if function_name in function_mapping:
        print(f"Function call: {function_name}")
        print(f"Function content: {function_args}")
        result = function_mapping[function_name](**function_args)
        print(result)
        return {"status": "success", "result": result}
    else:
        raise HTTPException(status_code=400, detail="Invalid function call")


# Define Pydantic models for API requests and responses
class TransactionBase(BaseModel):
    """Base model for transaction data"""
    date: str = Field(..., description="Transaction date in MM.DD.YYYY format")
    day: str = Field(..., description="Abbreviated day of week")
    category: str = Field(..., description="Transaction category")
    note: str = Field(..., description="Description of the transaction")
    amount: float = Field(..., description="Transaction amount (positive for income, negative for expense)")

class TransactionCreate(TransactionBase):
    """Model for creating a new transaction"""
    pass

class TransactionUpdate(BaseModel):
    """Model for updating an existing transaction"""
    date: Optional[str] = Field(None, description="Transaction date in MM.DD.YYYY format")
    day: Optional[str] = Field(None, description="Abbreviated day of week")
    category: Optional[str] = Field(None, description="Transaction category")
    note: Optional[str] = Field(None, description="Description of the transaction")
    amount: Optional[float] = Field(None, description="Transaction amount (positive for income, negative for expense)")

class Transaction(TransactionBase):
    """Model for transaction response with ID"""
    id: int = Field(..., description="Unique transaction identifier")

class ResponseModel(BaseModel):
    """Standard API response model"""
    success: bool = Field(..., description="Operation success status")
    data: Optional[Union[List[Dict[str, Any]], Dict[str, Any]]] = Field(None, description="Response data")
    message: Optional[str] = Field(None, description="Response message")
    timestamp: Optional[str] = Field(None, description="Response timestamp in ISO format")

# API endpoints for direct database operations
@app.get("/transactions", response_model=ResponseModel, status_code=status.HTTP_200_OK)
async def get_transactions(
    year: Optional[int] = Query(None, description="Filter by year"),
    month: Optional[int] = Query(None, description="Filter by month (1-12)"),
    limit: Optional[int] = Query(None, description="Maximum number of transactions to return"),
    offset: Optional[int] = Query(None, description="Number of transactions to skip")
):
    """
    Retrieve all transactions with optional filtering.
    
    Args:
        year: Optional filter by year
        month: Optional filter by month (1-12)
        limit: Maximum number of transactions to return
        offset: Number of transactions to skip (for pagination)
        
    Returns:
        List of transactions matching the filter criteria
    """
    try:
        # Get data from database
        data = database.export_data(file_format="json", year=year, month=month)
        
        # Convert to Python objects
        import json
        transactions = json.loads(data)
        
        # Apply pagination if requested
        if offset is not None:
            transactions = transactions[offset:]
        if limit is not None:
            transactions = transactions[:limit]
            
        # Format the response
        for transaction in transactions:
            # Convert date from YYYY-MM-DD to MM.DD.YYYY
            date_obj = datetime.strptime(transaction['date'], '%Y-%m-%d')
            transaction['date'] = date_obj.strftime('%m.%d.%Y')
            
            # Add day of week
            transaction['day'] = date_obj.strftime('%a')
            
            # Ensure amount is a float (already handled in database export but double-check)
            transaction['amount'] = float(transaction['amount'])
            
            # Ensure ID is an integer
            transaction['id'] = int(transaction['id'])
            
            # Rename fields to match the expected format
            if 'note' not in transaction and 'source' in transaction:
                transaction['note'] = transaction.pop('source')
                
        return {
            "success": True,
            "data": transactions,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve transactions: {str(e)}"
        )

@app.post("/transactions", response_model=ResponseModel, status_code=status.HTTP_201_CREATED)
async def add_transaction(transaction: TransactionCreate):
    """
    Create a new transaction.
    
    Args:
        transaction: Transaction data to create
        
    Returns:
        Newly created transaction with ID
    """
    try:
        # Determine record type based on amount
        record_type = "pay" if transaction.amount > 0 else "expense"
        
        # Convert date from MM.DD.YYYY to YYYY-MM-DD
        date_obj = datetime.strptime(transaction.date, '%m.%d.%Y')
        date_str = date_obj.strftime('%Y-%m-%d')
        
        # Insert data into database
        result = database.insert_data(
            record_type=record_type,
            amount=abs(transaction.amount),  # Database will handle the sign
            note=transaction.note,
            category=transaction.category,
            date=date_str
        )
        
        # Extract the ID from the result message
        import re
        id_match = re.search(r"ID: (\d+)", result)
        if id_match:
            transaction_id = int(id_match.group(1))
        else:
            transaction_id = database.data['id'].max()
        
        # Create response with the new transaction including ID
        new_transaction = {
            "id": transaction_id,
            "date": transaction.date,
            "day": transaction.day,
            "category": transaction.category,
            "note": transaction.note,
            "amount": transaction.amount
        }
        
        return {
            "success": True,
            "data": new_transaction,
            "message": "Transaction created successfully"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create transaction: {str(e)}"
        )

@app.put("/transactions/{id}", response_model=ResponseModel, status_code=status.HTTP_200_OK)
async def update_transaction(
    id: int = Path(..., description="Transaction ID"),
    transaction: TransactionUpdate = Body(...)
):
    """
    Update an existing transaction.
    
    Args:
        id: Transaction ID to update
        transaction: Updated transaction data
        
    Returns:
        Updated transaction
    """
    try:
        # Get the existing transaction to determine if it's pay or expense
        if id not in database.data['id'].values:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Transaction with ID {id} not found"
            )
        
        existing_record = database.data[database.data['id'] == id].iloc[0]
        record_type = existing_record['type']
        
        # Process date if provided
        date_str = None
        if transaction.date:
            date_obj = datetime.strptime(transaction.date, '%m.%d.%Y')
            date_str = date_obj.strftime('%Y-%m-%d')
        
        # Process amount if provided
        amount = None
        if transaction.amount is not None:
            amount = abs(transaction.amount)
            # If amount sign changed, update record type
            if (transaction.amount > 0 and record_type == 'expense') or \
               (transaction.amount < 0 and record_type == 'pay'):
                record_type = "pay" if transaction.amount > 0 else "expense"
        
        # Update the record
        database.update_data(
            record_id=id,
            record_type=record_type,
            amount=amount,
            note=transaction.note,
            category=transaction.category,
            date=date_str
        )
        
        # Get the updated record
        updated_record = database.data[database.data['id'] == id].iloc[0]
        
        # Format the response
        date_obj = datetime.strptime(updated_record['date'], '%Y-%m-%d')
        
        updated_transaction = {
            "id": int(updated_record['id']),
            "date": date_obj.strftime('%m.%d.%Y'),
            "day": transaction.day if transaction.day else date_obj.strftime('%a'),
            "category": updated_record['category'],
            "note": updated_record['note'],
            "amount": float(updated_record['amount'])
        }
        
        return {
            "success": True,
            "data": updated_transaction,
            "message": "Transaction updated successfully"
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update transaction: {str(e)}"
        )

@app.delete("/transactions/{id}", response_model=ResponseModel, status_code=status.HTTP_200_OK)
async def delete_transaction(id: int = Path(..., description="Transaction ID")):
    """
    Delete an existing transaction.
    
    Args:
        id: Transaction ID to delete
        
    Returns:
        Success message
    """
    try:
        # Check if transaction exists
        if id not in database.data['id'].values:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Transaction with ID {id} not found"
            )
        
        # Delete the transaction
        database.delete_data(record_id=id)
        
        return {
            "success": True,
            "message": f"Transaction with ID {id} deleted successfully"
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete transaction: {str(e)}"
        )