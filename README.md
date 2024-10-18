


## Prerequisites

1. **Operating as Root**:  
   - All commands in this guide assume you are operating as the **root user**.  
     **If not**, use `sudo` before each command where appropriate.

2. **Fully Qualified Domain Name (FQDN)**:  
   - You must have control over a **domain name** and configure it via your **DNS provider** to point to your server’s IP address.  
   Example: `your-domain-name`.

3. **API Key from Alerts.in.ua**:  
   - To use the alerts data, **register an application** at [https://devs.alerts.in.ua](https://devs.alerts.in.ua) and obtain an **API key**.

4. **MariaDB and Nginx Installed**:  
   - Ensure your server allows **port 80 (HTTP)** and **443 (HTTPS)** through the firewall (e.g., using **UFW**).

---

## Step 1: Setting Up MariaDB

### 1.1 Install MariaDB and Required Packages

```bash
apt update
apt install mariadb-server mariadb-client libmariadb-dev
```

### 1.2 Secure the MariaDB Installation

```bash
mysql_secure_installation
```

### 1.3 Create the Database and Tables

```bash
mariadb -u root -p
```

Inside the MariaDB console:

```sql
CREATE DATABASE `api-db`;
USE `api-db`;

CREATE TABLE administrator (
    username VARCHAR(50) PRIMARY KEY,
    password VARCHAR(255) NOT NULL
);
```

### 1.4 Insert Admin Credentials

1. Open the Python 3 interpreter:

    ```bash
    python3
    ```

2. Inside the interpreter:

    ```python
    from passlib.context import CryptContext

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash("your_password")
    print(hashed_password)
    ```

3. Exit the interpreter by typing `exit()`.

4. Insert the hashed password into the database:

    ```sql
    INSERT INTO administrator (username, password) 
    VALUES ('administrator', 'your_hashed_password');
    ```

---

## Step 2: Set Up the Project

### 2.1 Create the Project Directory and Clone the Repository

1. Create the project directory:

   ```bash
   mkdir -p /root/api
   cd /root/api
   ```

2. Clone the GitHub repository:

   ```bash
   git clone https://github.com/samuel-edmund-morgan/alerts-api .
   ```

### 2.2 Create Virtual Environment and Install Dependencies

1. Create a virtual environment:

   ```bash
   python3 -m venv venv
   ```

2. Activate the virtual environment:

   ```bash
   source venv/bin/activate
   ```

3. Install dependencies from `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

---

## Step 3: Environment Variables with `python-dotenv`

1. Create a `.env` file:

   ```
   # .env
   DB_USER=root
   DB_PASSWORD=your_password
   SECRET_KEY=your_secret_key  # A key you make up yourself
   ALERTS_API_TOKEN=your_alerts_api_token
   ```

2. Add `.env` to `.gitignore`:

   ```
   # .gitignore
   .env
   ```

---

## Step 4: Nginx with HTTPS Setup

### 4.1 Install Nginx and Certbot

```bash
apt install nginx certbot python3-certbot-nginx
```

### 4.2 Configure Nginx

1. Create an Nginx configuration file:

   ```bash
   nano /etc/nginx/sites-available/your-domain-name
   ```

2. Insert the following content:

   ```nginx
   server {
       listen 80;
       server_name your-domain-name;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

3. Enable the site:

   ```bash
   ln -s /etc/nginx/sites-available/your-domain-name /etc/nginx/sites-enabled/
   ```

4. Test the Nginx configuration:

   ```bash
   nginx -t
   ```

5. Restart Nginx:

   ```bash
   systemctl restart nginx
   ```

6. Obtain an SSL certificate:

   ```bash
   certbot --nginx -d your-domain-name
   ```

---

## Step 5: Systemd Service Configuration

1. Create a systemd service file:

   ```bash
   nano /etc/systemd/system/fastapi.service
   ```

2. Insert the following content:

   ```ini
   [Unit]
   Description=FastAPI Application Service
   After=network.target

   [Service]
   User=root
   WorkingDirectory=/root/api
   ExecStart=/root/api/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
   Restart=always
   Environment="PATH=/root/api/venv/bin"

   [Install]
   WantedBy=multi-user.target
   ```

3. Reload systemd:

   ```bash
   systemctl daemon-reload
   ```

4. Enable the service:

   ```bash
   systemctl enable fastapi.service
   ```

5. Start the service:

   ```bash
   systemctl start fastapi.service
   ```

6. Check the service status:

   ```bash
   systemctl status fastapi.service
   ```

---

## Step 6: Generate Token and Use the API

### 6.1 Generate a Token

```bash
curl -X POST "https://your-domain-name/token" -H "Content-Type: application/x-www-form-urlencoded" --data-urlencode "username=administrator" --data-urlencode "password=your\$password"
```

### 6.2 Use the API with the Generated Token

```bash
curl -X GET "https://your-domain-name/alerts-state?token=YOUR_ACCESS_TOKEN"
```

---

## Troubleshooting Tips

1. **View FastAPI service logs**:
   ```bash
   journalctl -u fastapi.service -f
   ```

2. **Check Nginx logs**:
   ```bash
   tail -f /var/log/nginx/error.log
   ```

3. **Verify MariaDB service**:
   ```bash
   systemctl status mariadb
   ```

---

## Conclusion

This guide provides a **complete setup for a production-ready FastAPI application** with **token-based authentication**, **Nginx**, and **HTTPS**. Follow each step to ensure the system runs smoothly on startup with proper SSL security.
