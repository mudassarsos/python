from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoAuthenticationException, NetmikoTimeoutException


def show_ip_interface_brief(host: str, username: str, password: str, secret: str | None = None) -> str:
    device = {
        "device_type": "cisco_ios",
        "host": host,
        "username": username,
        "password": password,
    }
    if secret:
        device["secret"] = secret

    with ConnectHandler(**device) as connection:
        if secret:
            connection.enable()
        return connection.send_command("show ip interface brief")


if __name__ == "__main__":
    # Replace these values with your Cisco device credentials
    HOST = "172.16.41.13"
    USERNAME = "cisco"
    PASSWORD = "cisco123"
    SECRET = ""  # Set to None if not required

    try:
        output = show_ip_interface_brief(HOST, USERNAME, PASSWORD, SECRET)
        print(output)
    except NetmikoTimeoutException:
        print(f"Connection timed out while connecting to {HOST}")
    except NetmikoAuthenticationException:
        print(f"Authentication failed for {USERNAME}@{HOST}")
    except Exception as exc:
        print(f"Unexpected error: {exc}")
