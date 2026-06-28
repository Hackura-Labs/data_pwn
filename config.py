class Config:
    # Tool paths
    WORDLISTS = {
        'rockyou': '/usr/share/wordlists/rockyou.txt',
        'dirbuster': '/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt',
        'subdomains': '/usr/share/wordlists/SecLists/Discovery/DNS/subdomains-top1million-110000.txt',
        'unix_users': '/usr/share/wordlists/metasploit/unix_users.txt',
        'windows_users': '/usr/share/wordlists/metasploit/windows_users.txt',
        'mysql_users': '/usr/share/wordlists/metasploit/mysql_users.txt',
        'postgres_users': '/usr/share/wordlists/metasploit/postgres_users.txt',
        'mssql_users': '/usr/share/wordlists/metasploit/mssql_users.txt'
    }

    # Common passwords (built-in fallback)
    DEFAULT_PASSWORDS = [
        '', 'root', 'admin', 'password', '123456', 'toor', 'welcome',
        'qwerty', 'abc123', 'letmein', 'monkey', 'dragon', 'master',
        'changeit', 'sa', 'oracle', 'postgres', 'mysql', 'test',
        'guest', 'user', 'demo', '12345', 'password123', 'admin123'
    ]

    # Database port mapping
    DB_PORTS = {
        3306: 'mysql',
        5432: 'postgresql',
        1433: 'mssql',
        1521: 'oracle',
        27017: 'mongodb',
        6379: 'redis',
        9200: 'elasticsearch'
    }

    # Sensitive files to check
    SENSITIVE_FILES = [
        '.env', '.env.local', '.env.production',
        'config.php', 'wp-config.php', 'database.yml',
        'settings.py', 'appsettings.json', 'web.config',
        'application.properties', 'db.php', 'config.ini',
        '.git/config', 'composer.json', 'package.json',
        'Dockerfile', 'docker-compose.yml', 'backup.sql',
        'dump.sql', 'backup.zip', 'data.sql'
    ]
