import click
from apis import currency, spanglish_apis
import inspect

apis = {
    1: 'currency',
    2: 'spanglish',
    }

def main():
    """ 
    prints a list of the apis and their option number to be selected. 
    waits for a user input to be one of the options number. 
    """

    for api, name in apis.items():
        print(api," - ", name)

    api = int(input("api number: "))
    print("api type: ", type(api))
    if api == 1:
        for function_id, name in enumerate(currency.funcs.values(), 1):
            print(function_id, name[0])

        currency.run_function()


    elif api == 2:
        for function_id, name in enumerate(spanglish_apis.funcs.values(), 1):            
            print(function_id, name[0])

        spanglish_apis.run_function()

    else:
         print("nothing yet")   


    #menu.run_function()

if __name__ == "__main__":
    main()

