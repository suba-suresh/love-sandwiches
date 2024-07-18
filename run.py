import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')


def get_sales_data():
    """
    Get sales figures input from the user.
    Run a while loop to collect a valid string of data from the user
    via the terminal, which must be a string of 6 numbers separated
    by commas. The loop will repeatedly request data, until it is valid.
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here: ")

        sales_data = data_str.split(",")

        if validate_data(sales_data):
            print("Data is valid!")
            break

    return sales_data


def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True


#def update_sales_worksheet(data):
   #"""
    #Update sales worksheet, add new row with the list data provided
   #  """
   #  print("Updating sales worksheet...\n")
    # sales_worksheet = SHEET.worksheet("sales")
    # sales_worksheet.append_row(data)
    #print("Sales worksheet updated successfully.\n")


# def update_surplus_worksheet(data):
   # """
   # Update surplus worksheet, add new row with the list data provided
   # """
    # print("Updating surplus worksheet...\n")
    #surplus_worksheet = SHEET.worksheet("surplus")
    #surplus_worksheet.append_row(data)
    # print("Surplus worksheet updated successfully.\n")

    # Now we're going to refactor these two functions into one
# that we can reuse every time we want to update a worksheet with a single row of data.
# But first, let’s talk about what refactoring means. Refactoring is the restructuring of code
# to improve its operation, without altering its functionality. The first refactoring you’ll do
# as a student or junior developer will almost certainly be rewriting your code to prevent repetition.
# As developers, you’ll always be looking for ways to avoid repeating yourself.
# So, how can we go about creating one function that can replace these two?
# Well, first we need to identify where the differences are in our code.
# And you know that the differences are here because you did the code along challenge in the previous video.
# So our new function needs to be able to change these parts of the code,
# depending on which worksheet we want to update.
# This first argument here in both our functions can hold the data we need to insert. But to create our
# new refactored function, we need to pass it another argument, that tells it which worksheet we want to update.
# This is the key to the differences between these two separate functions.

# Let’s start by writing our new function. I’m going to name this one update_worksheet.
# And like before, I’m going to pass it our data to be inserted.
# But this time, I’ll create a second argument for my function called worksheet, which is going to
# hold the name of the worksheet we want to update. Now, I’ll add in my print statement again.
# I’ll just copy and paste it from the function above. But this time I’ll use an f-string
# to insert the worksheet name that we're updating into the print statement.
# Now let’s make our call to our worksheet. We’ll name this variable worksheet_to_update.
# And again we'll use our worksheet variable here to choose which worksheet we want to access.
# Now we can append our new row to our worksheet_to_update.
# And finally we’ll add in our other print statement, again using the f-string to insert our worksheet variable.


def update_worksheet(data, worksheet):
    """
    Receives a list of integers to be inserted into a worksheet
    Update the relevant worksheet with the data provided
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully\n")



def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.

    The surplus is defined as the sales figure subtracted from the stock:
    - Positive surplus indicates waste
    - Negative surplus indicates extra made when stock was sold out.
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)

    return surplus_data

# Now let’s change our calls to our update worksheet functions down in our main function.
# Now, instead of our update_sales_worksheet function, we can call our new update_worksheet function.
# And remember to pass it that second value, for the worksheet parameter.
# For this one, that's “sales”.
# And here we can reuse the same function again,
# passing it the value of “surplus” as this time we want to update the surplus worksheet.

def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")

# So, before running the code, let’s walk through what our function will do each time it is called.
# The first time it is called, we pass it our data for our new sales row,
# and we pass it the string value of “sales”. Our program would then go up to our
# update_worksheet function, and our sales data list is assigned to the data variable,
# and our worksheet variable gets the string value of “sales”. Our function then prints
# “Updating sales worksheet...” and then uses that worksheet variable to access the sales worksheet
# and insert the data. Then our function ends and goes back to our main function,
# where the program calculates our surplus data and returns it to the new_surplus_data variable.
# Then we call our update_worksheet function again. This time, we pass it our new_surplus_data, and
# we tell the function we want it to update the “surplus” worksheet, with our new parameter value.
# And so our function runs again. This time the worksheet variable value is the “surplus” string,
# and so it does its thing, printing the messages to the user, and updating the surplus worksheet.
# Now let’s run the main function to see the output
# Here you can see the first time our update function ran,
# printing the messages to the terminal with the value for the worksheet variable inserted in there.
# And then the function is called again to update our surplus data.
# This time with the surplus value. So let's check the spreadsheet,
# and we can see that both our sales and surplus rows have been added!
# So we have our refactored function that does what both of these functions were doing separately.

print("Welcome to Love Sandwiches Data Automation")
main()