import paramiko as paramiko
from pathlib import Path
import tkinter as tk
from tkinter import filedialog
import os
import sys

key_region = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' # REMOVED

print('\nWelcome to the StorageRabbit client.')
print(f'links: http://storagerabbit.ml/ / https://{key_region}.ngrok.io/\n')
print("Please note that accounts and files the under it may become inaccessible due to a various number of reasons and "
      "\nthat StorageRabbit or it's creator, HYKANTUS, should not be held responsible for any lost, damaged, "
      "\nor corrupted files. Hence, any files uploaded to StorageRabbit should be treated as temporary only.\n")

print("Also remember that anyone can access any user's account at anytime, "
      "\nso uploading confidential documents is not recommended\n")

# SFTP
host = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' # REMOVED
port = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' # REMOVED
transport = paramiko.Transport((host, port))

username = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' # REMOVED
password = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' # REMOVED
transport.connect(username=username, password=password)
sftp = paramiko.SFTPClient.from_transport(transport)

# ssh to hp-server
ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, port=port, username=username, password=password)


# login/register
login_register = input("login or register? [ L / R ]: ")

if login_register == 'L' or login_register == 'l':
    storagerabbit_username = input("\nLOGIN:\nusername: ")

if login_register == 'R' or login_register == 'r':
    storagerabbit_username = input("\nREGISTER:\nusername: ")
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(f'mkdir /var/www/html/storage/{storagerabbit_username}')

# upload
print('pick a file to upload from the file selector window\nplease note that the filename may not contain spaces or '
      'any special characters')

try:
    root = tk.Tk()
    root.withdraw()
    root.lift()
    filepath = filedialog.askopenfilename()
except FileNotFoundError:
    restart_choice = input('ERROR: You have either; not chosen a file / chosen a username with spaces or special '
                           'characters / chosen a file path contained spaces or any special '
                           'characters (such as using: "C:\\my pictures\\file™.png" [note '
                           'the space in "my pictures" and the symbol in "file™.png"])\nWould you like to '
                           'restart? [ Y / N ]: ')


localpath = filepath.replace('/', ("\\"+"\\"))
mypath = Path(localpath)
pathname = mypath.name
print(f'file selected: {pathname} from {localpath}\n')
remotepath = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' # REMOVED
print(remotepath)
try:
    sftp.put(localpath, remotepath)
except FileNotFoundError:
    restart_choice = input('ERROR: You have either; not chosen a file / chosen a username with spaces or special '
                           'characters / chosen a file path contained spaces or any special '
                           'characters (such as using: "C:\\my pictures\\file™.png" [note '
                           'the space in "my pictures" and the symbol in "file™.png"])\nWould you like to '
                           'restart? [ Y / N ]: ')
    if restart_choice == 'Y' or restart_choice == 'y':
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
    if restart_choice == 'N' or restart_choice == 'n':
        sys.exit(0)

print(f"\nsuccessfully uploaded to:\nhttps://{key_region}.ngrok.io/storage/{storagerabbit_username}/{pathname}\n\nsee all uploaded files here:\nhttps://{key_region}.ngrok.io/storage/{storagerabbit_username}/")
