import time
import paramiko as paramiko
from pathlib import Path
import tkinter as tk
from tkinter import filedialog
import os
import sys
from tqdm import tqdm
from timeit import default_timer as timer


# progress bar
class progressbar:
    def start(size, desc):
        loop = tqdm(total=size, position=0, leave=False)
        for k in range(size):
            loop.set_description(desc.format(k))
            loop.update(1)

    def stop(size):
        loop = tqdm(total=size, position=0, leave=False)
        loop.close()


progressbar.start(2500, 'Setting up storagerabbit client')
start = timer()

key_region = 'XXXXXXXXXXXXXXXXXX' # REMOVED

"""
print('\nWelcome to the StorageRabbit client.')
print(f'links: http://storagerabbit.ml/ / https://{key_region}.ngrok.io/\n')
print("Please note that accounts and files the under it may become inaccessible due to a various number of reasons and "
      "\nthat StorageRabbit or it's creator, HYKANTUS, should not be held responsible for any lost, damaged, "
      "\nor corrupted files. Hence, any files uploaded to StorageRabbit should be treated as temporary only.\n")

print("Also remember that anyone can access any user's account at anytime, "
      "\nso uploading confidential documents is not recommended\n")
"""

# SFTP
host = "0.tcp.in.ngrok.io"
port = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" # REMOVED
transport = paramiko.Transport((host, port))

transport.connect("XXXXXXXXXXXXXXXXXXX", "XXXXXXXXXXXXXXXXXXXXXXXXXX") # REMOVED
sftp = paramiko.SFTPClient.from_transport(transport)

# ssh to hp-server
ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, port=port, username=username, password=password)

end = timer()
progressbar.stop((start - end)*100)
print()

# login/register
login_register = input("login or register? [ L / R ]: ")

if login_register == 'L' or login_register == 'l':
    storagerabbit_username = input("\nLOGIN:\nusername: ")

if login_register == 'R' or login_register == 'r':
    storagerabbit_username = input("\nREGISTER:\nusername: ")
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(f'mkdir /var/www/html/storage/{storagerabbit_username}')

"""if login_register != 'L' or login_register != 'l' or login_register != 'R' or login_register != 'r':
    print('No option picked\nRestarting...')
    os.system('cls')
    os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)"""


def upload(sshpath="/var/www/html/storage/"):
    print(
        'pick a file to upload from the file selector window\nplease note that the filename may not contain spaces or '
        'any special characters')

    root = tk.Tk()
    root.withdraw()
    root.lift()
    filepath = filedialog.askopenfilename()

    localpath = filepath.replace('/', ("\\" + "\\"))
    mypath = Path(localpath)
    pathname = mypath.name
    print(f'file selected: {pathname} from {localpath}\n')
    remotepath = sshpath + f'{storagerabbit_username}/{pathname}'

    try:
        progressbar.start(2500, desc="UPLOADING")
        sftp.put(localpath, remotepath)
        progressbar.stop((start - end)*100)
    except FileNotFoundError:
        input('ERROR: You have either; not chosen a file / chosen a username with spaces or special '
              'characters / chosen a file path contained spaces or any special '
              'characters (such as using: "C:\\my pictures\\file™.png" [note '
              'the space in "my pictures" and the symbol in "file™.png"])\npress ENTER to exit\n')
        sys.exit(0)

    print(
        f"\nsuccessfully uploaded to:\nhttps://{key_region}.ngrok.io/storage/{storagerabbit_username}/{pathname}/\n"
        f"\nsee all uploaded files here:\nhttps://{key_region}.ngrok.io/storage/{storagerabbit_username}/")

    print()


def get_filenames():
    print(f'Files available in account "{storagerabbit_username}":\n')
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(f'ls /var/www/html/storage/{storagerabbit_username}',
                                                         get_pty=True)

    for line in ssh_stdout:
        print(line)


def delete():
    get_filenames()
    print()
    delete_choice = input("Pick a file from above to delete: ")

    try:
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
            f'rm "/var/www/html/storage/{storagerabbit_username}/{delete_choice}"')

    except Exception:
        print(
            f'unable to delete file.\nFile may have already been deleted.\nPlease check {key_region}.ngrok.io/{storagerabbit_username} to verify.')
        sys.exit(0)

    print('File successfully deleted.\n')


def choose_command():
    print('\nPICK A COMMAND:\n1. upload a file\n2. see all files in account\n3. delete a file\n4. exit\n')
    choice = input('COMMAND: ')

    if choice == '1':
        print()
        upload()
    elif choice == '2':
        print()
        get_filenames()
    elif choice == '3':
        delete()
        print()
    elif choice == '4':
        sys.exit(0)


while True:
    choose_command()

