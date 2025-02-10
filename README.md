# Django online shopping website.

<p align='center'>
  <img src="https://img.shields.io/badge/Django-092E20?logo=django&logoColor=white" alt=""/>
  <img src="https://img.shields.io/badge/Python-306998?logo=python&logoColor=white"  alt=""/>
  <img src="https://img.shields.io/badge/PostgreSQL-336791?logo=postgresql&logoColor=white"  alt=""/>
  <img src="https://img.shields.io/badge/Github-2C2C2C?logo=github&logoColor=white"  alt=""/>
</p>

<hr class="dotted">
It is a robust online shopping website crafted with the Django Rest Framework, offering a seamless foundation for managing products and creating a high-quality, feature-rich shopping experience. It’s all you need to build and scale your store with elegance and efficiency.

## Screenshots

### Home
![App Screenshot](https://i.imgur.com/itySk8M.png)
### Profile
![App Screenshot](https://i.imgur.com/BkL7tFJ.png)
### Product
![App Screenshot](https://i.imgur.com/TjW6DLs.png)
### Cart
![App Screenshot](https://i.imgur.com/ZCZ2h3k.png)

## About this Project:

I'll be happy if you provide any feedback or code improvements or suggestions.

Connect with me at:

<p align='center'>

  <a href="https://www.instagram.com/t1ch_coder/">
    <img src="https://img.shields.io/badge/instagram-%23E1306C.svg?&style=for-the-badge&logo=instagram&logoColor=white" />
  </a>&nbsp;&nbsp;
  <a href="https://x.com/T1chCoder">
    <img src="https://img.shields.io/badge/x-%23000000.svg?&style=for-the-badge&logo=x&logoColor=white" />        
  </a>&nbsp;&nbsp;
  <a href="https://discordapp.com/users/1299474775239823392">
    <img src="https://img.shields.io/badge/discord-%235865F2.svg?&style=for-the-badge&logo=discord&logoColor=white" />        
  </a>&nbsp;&nbsp;
  <a href="https://t.me/T1chCoder">
    <img src="https://img.shields.io/badge/telegram-%230088CC.svg?&style=for-the-badge&logo=telegram&logoColor=white" />        
  </a>&nbsp;&nbsp;


</p>

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

Create a .env file on ecom folder (/.env) setting all requirements without using space after "=".

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

## License

<a href="https://github.com/T1chCoder/ShopSmart/blob/master/LICENSE.md">
    <img alt="NPM" src="https://img.shields.io/npm/l/license?style=for-the-badge">
</a>&nbsp;&nbsp;

This project is licensed under the MIT License - see
the [LICENSE.md](https://github.com/T1chCoder/ShopSmart/blob/master/LICENSE.md) file for details.

<img src="https://t.bkit.co/w_6777d980e766c.gif" />
