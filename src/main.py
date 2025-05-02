from src.config import gemini_api_key
from fastapi import FastAPI, HTTPException
from google import genai
from google.genai import types



app = FastAPI()

gemini_instructions = "You are being used in a bookkeeping personal finance app to perform CRUD operations to a database." \
" Based on the user input you must choose the appropriate function and populate its parameters. " \
"The functions are: addExpense(float, location), addPay(float, source)"


def add_expense(amount:float, location:str, date:str):
    """
    Add an expense to the database.
    """
    # Logic to add expense to the database
    # return {"message": f"Added expense of {amount} at {location}"}
    return "add_expense has been called with the following parameters: " + str(amount) + ", " + str(location)



def add_pay(amount:float, source:str, date:str):
    """
    Add a payment to the database.
    """
    # Logic to add payment to the database
    # return {"message": f"Added payment of {amount} from {source}"}
    return "add_pay has been called with the following parameters: " + str(amount) + ", " + str(source)



def update_expense(record_id:int, amount:float=None, location:str=None, date:str=None):
    """
    Update an existing expense in the database.
    """
    # Logic to update expense in the database
    # return {"message": f"Updated expense with ID {record_id}"}
    return "update_expense has been called with the following parameters: " + str(record_id) + ", " + str(amount) + ", " + str(location)


def update_pay(record_id:int, amount:float=None, source:str=None, date:str=None):
    """
    Update an existing payment in the database.
    """
    # Logic to update payment in the database
    # return {"message": f"Updated payment with ID {record_id}"}
    return "update_pay has been called with the following parameters: " + str(record_id) + ", " + str(amount) + ", " + str(source)


def delete_record(record_id:int):
    """
    Delete an expense from the database.
    """
    # Logic to delete expense from the database
    # return {"message": f"Deleted expense with ID {record_id}"}
    return "delete_record has been called with the following parameters: " + str(record_id)


def get_total_amount():
    """
    Get the total amount of expenses in the database.
    """
    # Logic to get total amount from the database
    # return {"total_amount": 1000}
    return "get_total_amount has been called"


def get_total_amount_by_type(record_type:str):
    """
    Get the total amount of expenses by type in the database.
    """
    # Logic to get total amount by type from the database
    # return {"total_amount": 500}
    return "get_total_amount_by_type has been called with the following parameters: " + str(record_type)


def get_monthly_total(record_type:str, month:int, year:int):
    """
    Get the total amount of expenses for a specific month in the database.
    """
    # Logic to get monthly total from the database
    # return {"monthly_total": 100}
    return "get_monthly_total has been called with the following parameters: " + str(record_type) + ", " + str(month) + ", " + str(year)


def get_source_list(record_type:str, month:int, year:int):
    """
    Get the list of sources from the database.
    """
    # Logic to get source list from the database
    # return {"sources": ["source1", "source2"]}
    return "get_source_list has been called with the following parameters: " + str(record_type) + ", " + str(month) + ", " + str(year)


def get_average_amount(record_type:str, month:int, year:int):
    """
    Get the average amount of expenses for a specific month in the database.
    """
    # Logic to get average amount from the database
    # return {"average_amount": 50}
    return "get_average_amount has been called with the following parameters: " + str(record_type) + ", " + str(month) + ", " + str(year)




@app.get("/")
async def root():
    return {"message": "Hello World..."}

@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/genai/{prompt}")
async def genai_api(prompt:str, max_output_tokens:int=1024):
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
                "location": types.Schema(type="STRING", description="The location of the expense."),
                "date": types.Schema(type="STRING", description="The date of the expense."),
            },
            required=["amount", "location", "date"],
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
                "location": types.Schema(type="STRING", description="The new location of the expense."),
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
        description="Delete an expense from the database.",
        parameters=types.Schema(
            type="OBJECT",
            properties={
                "record_id": types.Schema(type="NUMBER", description="The ID of the record to delete."),
            },
            required=["record_id"],
        ),
    )
    function_get_total_amount = types.FunctionDeclaration(
        name="get_total_amount",
        description="Get the total amount of expenses in the database.",
        parameters=types.Schema(
            type="OBJECT",
            properties={
                "record_type": types.Schema(type="STRING", description="The type of the record ('expense' or 'pay')."),
            },
            required=["record_type"],
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
            required=["record_type", "month", "year"],
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
            required=["record_type", "month", "year"],
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
            required=["record_type", "month", "year"],
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
    print(response.function_calls[0])



    # Call the function based on the response
    if response.candidates[0].content.parts[0].function_call.name == "add_expense":
        function_call = response.candidates[0].content.parts[0].function_call
        print(f"Function call: {function_call.name}")
        print(f"Function content: {function_call.args}")
        result = add_expense(**function_call.args)
        print(result)
    elif response.candidates[0].content.parts[0].function_call.name == "add_pay":
        function_call = response.candidates[0].content.parts[0].function_call
        print(f"Function call: {function_call.name}")
        print(f"Function content: {function_call.args}")
        result = add_pay(**function_call.args)
        print(result)
    else:
        raise HTTPException(status_code=400, detail="Invalid function call")



