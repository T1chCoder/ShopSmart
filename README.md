# Django online shopping website.

<p align='center'>
<img src="https://img.shields.io/badge/Django-239120?logo=django&logoColor=white" alt=""/>
<img src="https://img.shields.io/badge/Python-239120?logo=python&logoColor=white"  alt=""/>
<img src="https://img.shields.io/badge/SQL%20Server-CC2927?logo=microsoft-sql-server&logoColor=white"  alt=""/>
<img src="https://img.shields.io/badge/Github-181717?logo=github&logoColor=white"  alt=""/>
</p>


<hr class="dotted">
It is a robust online shopping website crafted with the Django Rest Framework, offering a seamless foundation for managing products and creating a high-quality, feature-rich shopping experience. It’s all you need to build and scale your store with elegance and efficiency.

## Screenshots

### Home
![App Screenshot](https://imgur.com/nKniQGc)
### Products
![App Screenshot]([https://imgur.com/M8LUsyo.png](https://imgur.com/a/li8yamX))

## About this Project:

I'll be happy if you provide any feedback or code improvements or suggestions.

Connect with me at:

<p align='center'>
  📫 How to reach me: <a href='mailto:t1chcoder@gmail.com'>t1chcoder@gmail.com</a>
</p>

## Some technical information:

- Django - 5.1.3
- Django Rest Framework - 3.15.2
- Django Database URL - 2.3.0
- Django Crispy Forms - 2.3
- Gunicorn - 23.0.0
- Pillow - 11.0.0

## To Install:

Cloning the Repository:

```
$ git clone github.com/T1chCoder/ShopSmart.git
$ cd ShopSmart
```

Installing the environment control:

```
$ pip install virtualenv
$ virtualenv env
```

Activating the environment:

on Windows:

```
env\Scripts\activate
```

on Mac OS / Linux:

```
$ source env/bin/activate
```

Installing dependencies:

```
$ pip install -r requirements.txt
```

Create a .env file on ecom folder (/root/.env) setting all requirements without using space after "=".

Copy and paste on our .env file:

```
# Secret key
SECRET_KEY=SECRET_KEY

# Database settings
DATABASE_NAME=DATABASE_NAME
DATABASE_USER=DATABASE_USER
DATABASE_PASSWORD=DATABASE_PASSWORD

# Additional settings
ADMIN_PANEL_KEY=ADMIN_PANEL_KEY
API_V1_KEY
DEBUG=DEBUG
```

Installing MAKE:

On Mac OS & Linux:

```
sudo apt install make
sudo apt install build-essential
```

On Windows:

```
1. Press Win + X keys together to open the Power menu.
2. Select Windows Powershell(Admin).
3. Type the command ‘Set-ExecutionPolicy Bypass -Scope Process -Force; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))' and press Enter
4. Downloads and installs chocolatey as available from their official source: https://community.chocolatey.org/courses/installation/installing?method=installing-chocolatey#powershell
5. Type choco to verify if the installation worked.
6. Now, type the command ‘choco install make‘ to install Make.
7. Go to the installation directory C:\Program Files(x86)\GnuWin32\ to confirm the installation worked.
```

Install HStoreExtension:

With database:
```
sudo su - postgres              //switch to postgres user
\c DATABASENAME;                     //connect your database
CREATE EXTENSION IF NOT EXISTS hstore;      //create extension
```

With migrations:

```
Add "HStoreExtension()" to your operations in migrations.
```


Type this command to make migrations and migrate:

```
make mig
```

Create a super user:

```
$ make admin
```

Finishing running server:

```
$ python manage.py runserver
```

Add some random data:
```
$ python manage.py create
```

To test project:
```
$ pytest
```


## Contributing

You can send how many PR's do you want, I'll be glad to analyse and accept them! And if you have any question about the
project...

📫Email-me: <a href='mailto:t1chcoder@gmail.com'>t1chcoder@gmail.com</a>

Thank you!
