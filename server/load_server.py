import paramiko
import os
from os import listdir
from os.path import isfile, join

NAME = 'martylee.ru'
USERNAME = 'martylee42'

PATH = '/home/martylee42/math_writer/'

def getClient():
    ssh = paramiko.SSHClient()
    k = paramiko.RSAKey.from_private_key_file("id_rsa")

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect( hostname = NAME , username =  USERNAME, pkey = k )

    return ssh

def getFilesLocal(dir):
    files = [f for f in listdir(dir) if isfile(join(dir, f))]
    files = [f for f in files if f[0] != "."]

    return files

def putFiles(ssh, dir, remote_dir = ""):
    ftp = ssh.open_sftp()
    files = getFilesLocal(dir)

    for f in files:
        print("loading {}".format(f))
        ftp.put(dir + f, PATH + remote_dir + f)

    ftp.close()

def execCommand(ssh, command):
    stdin, stdout,stderr = ssh.exec_command(command)
    return stdout.read().decode()


if __name__ == "__main__" :
    ssh = getClient()
    putFiles(ssh, "../")
    putFiles(ssh, "../server/", "server/")
