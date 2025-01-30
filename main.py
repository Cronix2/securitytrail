import requests
from dotenv import load_dotenv
import os
import sys

load_dotenv()
api_key = os.getenv("API_KEY")


# I want to check if the command which tape have parameters or not

def check_command():
    if len(sys.argv) > 1:
        return True
    else:
        return False

# with sys check if the command have arguments I want to get the argument and verify if the parameters are correct or not
# the correct parameters are hostname (-h or --hostname) and page (-p or --page)
# page is optional if the user don't put it I will put it by default to 1, and it's number between 1 and 100
# hostname is required and it’s a string


def get_parameters():
    parameters = {}
    for index, arg in enumerate(sys.argv):
        if arg == "-h" or arg == "--hostname":
            if index + 1 < len(sys.argv):
                parameters["hostname"] = sys.argv[index + 1]
            else:
                print("Hostname is required")
                return False
        if arg == "-p" or arg == "--page":
            if index + 1 < len(sys.argv):
                if sys.argv[index + 1].isdigit():
                    if 1 <= int(sys.argv[index + 1]) <= 100:
                        parameters["page"] = sys.argv[index + 1]
                    else:
                        print("page must be a number between 1 and 100")
                        return False
                else:
                    print("page must be a number between 1 and 100")
                    return False
            else:
                print("page is required")
                return False
    if "hostname" not in parameters:
        print("Hostname is required")
        return False
    return parameters

# if there is no parameters we enter in an interactive mode where the user can enter the hostname and the page number
# if the user don't enter the page number i will put it by default to 1


def interactive_mode():
    print("You are in interactive mode")
    parameters = {}
    hostname = ""
    while not hostname:
        print("Enter the hostname")
        hostname = input()
    parameters["hostname"] = hostname
    print("Enter the page number (optional)")
    page = input()
    if page:
        if page.isdigit():
            if 1 <= int(page) <= 100:
                parameters["page"] = page
            else:
                print("page must be a number between 1 and 100")
                return False
        else:
            print("page must be a number between 1 and 100")
            return False
    else:
        parameters["page"] = "1"
    return parameters

# create the request to the API and return the response


def request_api(parameters):
    url = f"https://api.securitytrails.com/v1/domain/{parameters['hostname']}/associated?page={parameters['page']}"
    headers = {"APIKEY": api_key}
    response = requests.get(url, headers=headers)
    return response.json()

# print the response


def print_response(response):
    with open("response.json", "w", encoding="utf-8") as file:
        file.write(str(response))
    records = response["records"]
    count = 0
    for item in records:
        print(f"Hostname: {item['hostname']}")
        count += 1
    print(f"Total records: {count}")

# main function


def main():
    if check_command():
        response = request_api(get_parameters())
        print_response(response)
    else:
        response = request_api(interactive_mode())
        print_response(response)


if __name__ == "__main__":
    main()
