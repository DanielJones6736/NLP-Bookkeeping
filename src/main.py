from src.config import gemini_api_key
from fastapi import FastAPI, HTTPException
from google import genai
from google.genai import types
from src import database_tools



app = FastAPI()
database = database_tools.Database_Tools()

gemini_instructions = \
"You are being used in a bookkeeping personal finance app to perform CRUD operations to a database." \
" Based on the user input you must choose the appropriate function and populate its parameters. " \
"The functions are: " \
"add_expense(amount:float, location:str, date:str) -> bool, " \
"add_pay(amount:float, source:str, date:str) -> bool, " \
"update_expense(record_id:int, amount:float=None, location:str=None, date:str=None) -> bool, " \
"update_pay(record_id:int, amount:float=None, source:str=None, date:str=None) -> bool, " \
"delete_record(record_id:int = None) -> bool, " \
"get_total_amount_by_type(record_type:str=None) -> float, " \
"get_monthly_total(record_type:str=None, month:int=None, year:int=None) -> float, " \
"get_source_list(record_type:str, month:int, year:int) -> list, " \
"get_average_amount(record_type:str, month:int, year:int) -> float, " \
"get_transaction_history(record_type:str=None, month:int=None, year:int=None, file_format:str='json') -> Any. " \
"ai_analyze(record_type:str, month:int, year:int, question:str) -> Any. " \
"For any prompt that doesn't fall into any of the functions above, call the ai_analyze function. " \
"Make sure to only use the parameters that are needed for the function. " \
"For delete_record, if the latest record is to be deleted, then record_id should be None or the ID of the record. " \
"If no user input is provided, use the parameter value None " \
"Try to convert relative dates into absolute dates. Example, tody equals yyyy-mm-dd" \
"User prompt: "



def add_expense(amount:float, source:str, date:str):
    """
    Adds an expense record to the database.

    Args:
        amount (float): The monetary value of the expense.
        source (str): The source where the expense occurred.
        date (str): The date of the expense in string format (e.g., 'YYYY-MM-DD').

    Returns:
        bool: True if the expense was successfully added to the database, False otherwise.
    """
    # Logic to add expense to the database
    print(f"add_expense has been called with the following parameters: {str(amount)}, {str(source)}")
    return database.insert_data("expense", amount=amount, source=source, date=date)


def add_pay(amount: float, source: str, date: str):
    """
    Adds a payment record to the database.
    Args:
        amount (float): The amount of the payment.
        source (str): The source or description of the payment.
        date (str): The date of the payment in string format.
    Returns:
        bool: True if the payment was successfully added to the database, False otherwise.
    """
    # Logic to add payment to the database
    print(f"add_pay has been called with the following parameters: {str(amount)}, {str(source)}, {str(date)}")
    return database.insert_data("pay", amount=amount, source=source, date=date)

### THIS IMPLEMENTATION MIGHT NEED TO BE CHANGED TO DELETE THEN INSERT ###
### GEMINI DID NOT RECOGNIZE THE PROMPT FOR THIS FUNCTION ###
def update_expense(record_id:int, amount:float=None, source:str=None, date:str=None):
    """
    Parameters:
        record_id (int): The unique identifier of the expense record to update.
        amount (float, optional): The new amount for the expense. Defaults to None.
        location (str, optional): The new location associated with the expense. Defaults to None.
        date (str, optional): The new date of the expense in 'YYYY-MM-DD' format. Defaults to None.

    Returns:
        bool: True if the update was successful, False otherwise.
    """
    # Logic to update expense in the database
    print(f"update_expense has been called with the following parameters: {str(record_id)}, {str(amount)}, {str(source)}, {str(date)}")
    return database.update_data(record_type="expense", record_id=record_id, amount=amount, source=source, date=date)


### THIS IMPLEMENTATION MIGHT NEED TO BE CHANGED TO DELETE THEN INSERT ###
### GEMINI DID NOT RECOGNIZE THE PROMPT FOR THIS FUNCTION ###
def update_pay(record_id:int, amount:float=None, source:str=None, date:str=None):
    """
    Updates an existing payment record in the database.

    Args:
        record_id (int): The unique identifier of the payment record to update.
        amount (float, optional): The new payment amount. Defaults to None.
        source (str, optional): The source or description of the payment. Defaults to None.
        date (str, optional): The date of the payment in string format. Defaults to None.

    Returns:
        bool: True if the update was successful, False otherwise.
    """
    # Logic to update payment in the database
    print(f"update_pay has been called with the following parameters: {str(record_id)}, {str(amount)}, {str(source)}, {str(date)}")
    return database.update_data(record_type="pay", record_id=record_id, amount=amount, source=source, date=date)

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


def get_source_list(record_type:str, month:int, year:int):
    """
    Retrieves a list of sources from the database based on the specified record type, month, and year.

    Args:
        record_type (str): The type of record to filter the sources (e.g., 'financial', 'academic').
        month (int): The month for which to retrieve the sources (1-12).
        year (int): The year for which to retrieve the sources.

    Returns:
        list: A list of sources retrieved from the database matching the specified criteria.

    Raises:
        ValueError: If the provided arguments are invalid or out of range.
        DatabaseError: If there is an issue connecting to or querying the database.
    """
    # Logic to get source list from the database
    print(f"get_source_list has been called with the following parameters: {str(record_type)}, {str(month)}, {str(year)}")
    return database.list_sources(record_type=record_type, month=month, year=year)


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

    # Create a function declaration for the tool
    function_add_expense = types.FunctionDeclaration(
        name="add_expense",
        description="Add an expense to the database.",
        parameters=types.Schema(
            type="OBJECT",
            properties={
                "amount": types.Schema(type="NUMBER", description="The amount of the expense."),
                "source": types.Schema(type="STRING", description="The source of the expense."),
                "date": types.Schema(type="STRING", description="The date of the expense."),
            },
            required=["amount", "source", "date"],
        ),
    )
    function_add_pay = types.FunctionDeclaration(
        name="add_pay",
        description="Add a payment to the database.",
        parameters=types.Schema(
            type="OBJECT",
            properties={
                "amount": types.Schema(type="NUMBER", description="The amount of the payment."),
                "source": types.Schema(type="STRING", description="The source of the payment."),
                "date": types.Schema(type="STRING", description="The date of the expense."),
            },
            required=["amount", "source", "date"],
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
                "source": types.Schema(type="STRING", description="The new source of the expense."),
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
                "source": types.Schema(type="STRING", description="The new source of the payment."),
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
        description="Get the list of sources from the database.",
        parameters=types.Schema(
            type="OBJECT",
            properties={
                "record_type": types.Schema(type="STRING", description="The type of the record ('expense' or 'pay')."),
                "month": types.Schema(type="NUMBER", description="The month for which to get the sources."),
                "year": types.Schema(type="NUMBER", description="The year for which to get the sources."),
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
        function_add_expense, 
        function_add_pay,
        function_update_expense,
        function_update_pay,
        function_delete_record,
        function_get_total_amount,
        function_get_monthly_total,
        function_get_source_list,
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
    print(f"response.function_call[0]: {response.function_calls[0]}")

    # Refactor the function call handling using a dictionary-based switch
    # Define a mapping of function names to their corresponding handlers
    function_mapping = {
        "add_expense": add_expense,
        "add_pay": add_pay,
        "update_expense": update_expense,
        "update_pay": update_pay,
        "delete_record": delete_record,
        "get_total_amount_by_type": get_total_amount_by_type,
        "get_monthly_total": get_monthly_total,
        "get_source_list": get_source_list,
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