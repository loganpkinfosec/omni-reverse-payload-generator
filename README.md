# omni-reverse-payload-generator
Omni-Reverse-Payload-Generator is a versatile tool designed for penetration testers and security professionals to efficiently generate diverse types of reverse shell payloads offline and at moments notice. This Python-based tool offers a robust feature set that includes generating commands for Bash, Netcat, Perl, Python, and PowerShell, among others. It uniquely supports encoding options like URL encoding and Base64, and caters to specialized scenarios with IFS variable manipulation for command injection or server-side template injection (SSTI).

# Key Features
- **Multiple Reverse Payload Generation**: Generate reverse shell payloads with ease using various technologies including Bash, Python, PowerShell, and much more.
- **Environment Testing**: Includes functionality to generate payloads for identifying shell environments, such as PowerShell/CMD (Windows) and Bash/Sh (Unix/Linux).
- **Advanced Encoding Options**: Supports URL, Internal Field Separator (IFS), and Base64 encoding to obfuscate and bypass Web Application Firewalls (WAF), enhancing penetration testing efforts.

# Useage
python3 Omni-Payload-Generator.py $PAYLOAD_TYPE $LHOST $LPORT $OPTIONS

python3 Omni-Payload-Generator.py -ps 10.10.14.20 443

python3 Omni-Payload-Generator.py -b 10.10.14.20 443 -e

python3 Omni-Payload-Generator.py -y3 10.10.14.20 443 -ifs injection

python3 Omni-Payload-Generator.py -y 10.10.14.20 443 -ifs ssti -e




