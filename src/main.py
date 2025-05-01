from src.config import gemini_api_key
from fastapi import FastAPI, HTTPException
from google import genai
from google.genai import types



app = FastAPI()

gemini_instructions = "You are being used in a bookkeeping personal finance app to perform CRUD operations to a database." \
" Based on the user input you must choose the appropriate function and populate its parameters. " \
"The functions are: addExpense(float, location), addPay(float, source)"

def add_expense(amount:float, location:str):
    """
    Add an expense to the database.
    """
    # Logic to add expense to the database
    # return {"message": f"Added expense of {amount} at {location}"}
    return "add_expense has been called with the following parameters: " + str(amount) + ", " + str(location)



def add_pay(amount:float, source:str):
    """
    Add a payment to the database.
    """
    # Logic to add payment to the database
    # return {"message": f"Added payment of {amount} from {source}"}
    return "add_pay has been called with the following parameters: " + str(amount) + ", " + str(source)



@app.get("/")
async def root():
    return {"message": "Hello World..."}



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
            },
            required=["amount", "location"],
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
            },
            required=["amount", "source"],
        ),
    )
    tool = types.Tool(function_declarations=[function_add_expense, function_add_pay])


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



