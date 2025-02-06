import requests
from dotenv import load_dotenv
import time
import os
import sys
import mariadb
import socket
import ip_generator
import supervision_site
# import subdomain_discover

global api_key
# I want to check if the command which tape have parameters or not

def check_command():
    if len(sys.argv) > 1:
        return True
    else:
        return False


# get the parameters from the command line

def connect_to_db(db_user, db_password, db_host):
    print("Tentative de connexion à la base de données...")
    for i in range(10):
        try:
            conn = mariadb.connect(
                user=db_user,
                password=db_password,
                host=db_host,
                port=3306,
                database="subdomains"
            )
            print("Connected to MariaDB Platform!")
            return conn
        except mariadb.Error as e:
            print(f"User: {db_user}\nPassword: {db_password}\nHost: {db_host}")
            print(f"Error connecting to MariaDB Platform: {e}")
            print(f"Erreur de connexion : {e}")
            print("Nouvelle tentative dans 5 secondes...")
            time.sleep(5)  # Attendre 5 secondes avant de réessayer

    print("Impossible de se connecter à la base de données")
    sys.exit(1)

def get_parameters():
    parameters = {}
    for index, arg in enumerate(sys.argv):
        if arg == "-a" or arg == "--automatic":
            parameters["autonomous"] = "True"
            parameters["ip"] = ip_generator.generate_1_ip()
            return parameters  # Retourne bien un dictionnaire ici

    if "autonomous" not in parameters:
        print("argument(s) missing")
        return {}  # Retourner un dictionnaire vide au lieu de False

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
        with open("../results/response.json", "w", encoding="utf-8") as file:
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


# inject the informations in the database


def inject_informations_in_db(con, cur, response, ip):
    if response != "nothing":
        records = response["subdomains"]
        for item in records:
            # find ip address of the subdomain
            try:
                ip_address = socket.gethostbyname(item)
            except socket.herror:
                ip_address = "not found"
            # check if ip address is already in the database
            if cur.execute("SELECT * FROM `subdomains-link-to-IP` WHERE ip_address = ?", (ip_address,)):
                if cur.execute("SELECT subdomains FROM `subdomains-link-to-IP` WHERE ip_address = ?", (ip_address,)):
                    subdomains = cur.fetchone()[0]
                    subdomains.append(item)
                    cur.execute("UPDATE `subdomains-link-to-IP` SET subdomains = ? WHERE ip_address = ?", (subdomains, ip_address))
            else:
                cur.execute("INSERT INTO `subdomains-link-to-IP` (ip_address, subdomains) VALUES (?, ?)", (ip_address, [item]))
    else:
        if cur.execute("SELECT * FROM `subdomains-link-to-IP` WHERE ip_address = ?", (ip,)):
            if cur.execute("SELECT subdomains FROM `subdomains-link-to-IP` WHERE ip_address = ?", (ip,)):
                records = cur.fetchone()[0]
                cur.execute("UPDATE `subdomains-link-to-IP` SET subdomains = ? WHERE ip_address = ?", (records, ip))
        else:
            records = ""
            try:
                insert = ("INSERT INTO `subdomains-link-to-IP` (ip_address, subdomains) VALUES ('"+ip+"', '"+records+"')")
                print(insert, flush=True)
                cur.execute(insert)
                print("send to the database", flush=True)  
            except mariadb.Error as e:
                print(f"Error mariadb: {e}", flush=True)
            except Exception as e:
                print(f"Error: {e}", flush=True)    
    con.commit()


# main function


def main():
    try:
        print("1", flush=True)
        global api_key
        load_dotenv()
        supervision_site.start()
        api_key = os.getenv("API_KEY")
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_host = os.getenv("DB_HOST")
        con = connect_to_db(db_user, db_password, db_host)
        cur = con.cursor()
        print("2", flush=True)
    except Exception as e:
        print(f"Error: {e}")
    if check_command():
        while True:
            ip = get_parameters()["ip"]
            print(ip, flush=True)
            if not cur.execute("SELECT * FROM `subdomains-link-to-IP` WHERE ip_address = ?", (ip,)):
                domain = get_domain_name(ip)
                response = request_api(domain)
                inject_informations_in_db(con, cur, response, ip)
    else:
        domain = get_domain_name(interactive_mode()["ip"])
        print(domain)
        response = request_api(domain)
        print_response(response)


if __name__ == "__main__":
    main()
