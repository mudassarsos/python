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
    DEVICES = [
        "172.16.41.13",
        "172.16.41.14",
        "172.16.41.17",
        "172.16.41.18",
    ]
    USERNAME = "cisco"
    PASSWORD = "cisco123"
    SECRET = ""  # Set to None if not required
    OUTPUT_FILE = "interface_brief_output.txt"

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out_file:
        for host in DEVICES:
            header = f"\n===== {host} =====\n"
            print(header, end="")
            out_file.write(header)
            try:
                output = show_ip_interface_brief(host, USERNAME, PASSWORD, SECRET)
                print(output)
                out_file.write(output + "\n")
            except NetmikoTimeoutException:
                error_msg = f"Connection timed out while connecting to {host}\n"
                print(error_msg, end="")
                out_file.write(error_msg)
            except NetmikoAuthenticationException:
                error_msg = f"Authentication failed for {USERNAME}@{host}\n"
                print(error_msg, end="")
                out_file.write(error_msg)
            except Exception as exc:
                error_msg = f"Unexpected error for {host}: {exc}\n"
                print(error_msg, end="")
                out_file.write(error_msg)

    print(f"\nSaved command output to {OUTPUT_FILE}")
