class CustomError(Exception):
    pass
def get_error():
    try:
        # Some code that might raise your custom exception
        raise CustomError("This is a custom exception.")
    except CustomError as e:
        # Handle the custom exception
        print(f"Custom Error: {e}")
        return str(e)
    return 1
result:CustomError = get_error()
if 'custom' in result:
    print("Error")
else:
    print(result)

