import requests
from dotenv import load_dotenv
import os
import sys
import socket

load_dotenv()
api_key = os.getenv("API_KEY")


# I want to check if the command which tape have parameters or not

def check_command():
    if len(sys.argv) > 1:
        return True
    else:
        return False

# get the parameters from the command line


def get_parameters():
    parameters = {}
    for index, arg in enumerate(sys.argv):
        if arg == "-i" or arg == "--ip":
            if index + 1 < len(sys.argv):
                parameters["ip"] = sys.argv[index + 1]
            else:
                print("ip is required")
                return False
    if "ip" not in parameters:
        print("ip is required")
        return False
    return parameters

# the interactive mode to get the ip address


def interactive_mode():
    print("You are in interactive mode")
    parameters = {}
    ip = ""
    while not ip or not ip.replace(".", "").isdigit() or len(ip.split(".")) != 4:
        if not ip:
            print("Enter the ip address")
        elif not ip.replace(".", "").isdigit():
            print("The ip address should be a number")
        elif len(ip.split(".")) != 4:
            print("The ip address should have 4 numbers")
        ip = input()
    parameters["ip"] = ip
    return parameters


# create the request to the API and return the response


def request_api(parameters):
    url = f"https://api.securitytrails.com/v1/domain/{parameters}/subdomains?children_only=true&include_inactive=false"
    headers = {
        "accept": "application/json",
        "APIKEY": api_key
    }
    response = requests.get(url, headers=headers)
    return response.json()

# print the response


def print_response(response):
    with open("results/response.json", "w", encoding="utf-8") as file:
        file.write(str(response))
    records = response["subdomains"]
    count = 0
    for item in records:
        print(f"subdomains: {item}")
        count += 1
    print(f"Total records: {count}")


# get the domain name from the ip address

def get_domain_name(ip):
    response = socket.gethostbyaddr(ip)
    domain_name = response[0].split(".")
    domain_name = domain_name[-2] + "." + domain_name[-1]
    return domain_name


# main function


def main():
    if check_command():
        domain = get_domain_name(get_parameters()["ip"])
        print(domain)
        response = request_api(domain)
        print(response)
    else:
        domain = get_domain_name(interactive_mode()["ip"])
        print(domain)
        response = request_api(domain)
        print_response(response)


if __name__ == "__main__":
    main()
