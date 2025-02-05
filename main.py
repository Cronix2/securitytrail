import requests
from dotenv import load_dotenv
import os
import sys
import mariadb
import socket
import ip_generator
import subdomain_discover

global api_key
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
    while not ip or not ip.replace(".", "").isdigit() or len(ip.split(".")) != 4 or ip == "%":
        if not ip:
            print("Enter the ip address")
        elif not ip.replace(".", "").isdigit() and ip != "%":
            print("The ip address should be a number")
        elif len(ip.split(".")) != 4 and ip != "%":
            print("The ip address should have 4 numbers")
        elif ip == "%":
            print("you're in an automatic mode")
            parameters["ip"] = ip_generator.generate_1_ip()
            print(f"ip: {parameters['ip']}")
            return parameters
        ip = input()
    parameters["ip"] = ip
    return parameters


# create the request to the API and return the response


def request_api(parameters):
    if parameters != "nothing":
        url = f"https://api.securitytrails.com/v1/domain/{parameters}/subdomains?children_only=true&include_inactive=false"
        headers = {
            "accept": "application/json",
            "APIKEY": api_key
        }
        try:
            response = requests.get(url, headers=headers)
        except requests.exceptions.ConnectionError:
            print("Connection error")
            return "nothing"
        except requests.exceptions.Timeout:
            print("Timeout error")
            return "nothing"
        except requests.exceptions.RequestException:
            print("Request error")
            return "nothing"
        print(api_key)
        if response.status_code == 200:
            return response.json()
        else:
            print("error")
            return "nothing"
    else:
        return "nothing"


# print the response


def print_response(response):
    if response != "nothing" and "subdomains" in response:
        with open("results/response.json", "w", encoding="utf-8") as file:
            file.write(str(response))
        records = response["subdomains"]
        count = 0
        for item in records:
            print(f"subdomains: {item}")
            count += 1
        print(f"Total records: {count}")
    else:
        print("no subdomains")

# get the domain name from the ip address


def get_domain_name(ip):
    try:
        response = socket.gethostbyaddr(ip)
        domain_name = response[0].split(".")
        if len(domain_name) > 2:
            domain_name = domain_name[-2] + "." + domain_name[-1]
        else:
            domain_name = response[0]
    except socket.herror:
        print("host not found")
        return "nothing"
    return domain_name


# main function


def main():
    global api_key
    load_dotenv()
    api_key = os.getenv("API_KEY")
    if check_command():
        domain = get_domain_name(get_parameters()["ip"])
        print(domain)
        response = request_api(domain)
        print_response(response)
    else:
        domain = get_domain_name(interactive_mode()["ip"])
        print(domain)
        response = request_api(domain)
        print_response(response)
        # if domain != "nothing":
        #     subdomain_discover.subdomain_brutforce_dictionnary(domain)
        #     print("subdomains found")


if __name__ == "__main__":
    main()
