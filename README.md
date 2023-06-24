# Social media API

Social media API written on DRF

## Installing using GitHub
```shell 
git clone https://github.com/yuraua5/py-social-media-api.git
cd py-social-media-api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Set the following environment variables:

```shell
set SECRET_KEY=<your secret key>
```

Apply database migrations:

```shell
python manage.py migrate
```

Start the server:

```shell
python manage.py runserver
```

## Getting access

To get access to the API:

- Create a user via `/api/user/register/`.
- Obtain an access token via `/api/user/token/`.

## Features

- User Registration and Authentication
- Admin panel: `/admin/`
- Documentation is located at `/api/doc/swagger/`
- User Profile
- Follow/Unfollow
- Post Creation and Retrieval
- Filtering profiles and posts