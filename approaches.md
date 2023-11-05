# Webservers
1. Spider website (e.g. using Burp Suite Proxy without intercept)
2. Enumerate subdomains and dirs (e.g. with `gobuster`)
3. Gain read access on webserver
    - Enumerate login forms
    - XSS, SQL-Injection
4. Gain write access on webserver
    - Access OS shell
    - Set up reverse shell with `nc -lvnp` (e.g. /usr/share/webshells/php/php-reverse-shell.php)
        - Spawn other shell (e.g. `python3 -c 'import pty;pty.spawn("/bin/bash")'`)
        - Use ssh if credentials found at some point
6. Search webserver
    - Interesting text data
        - `find . -type f -name '<glob pattern>' | xargs cat | grep -i <glob pattern>`
    - Binaries
        - Find binaries with permissions for user group `find / -group <group_name> 2>/dev/null`
        - Query infos about files `ls -la <path_to_file> && file <path_to_file>`
        - Append PATH `export PATH=<directory>:$PATH`


# Remote Shell

## Windows
`impacket-psexec`