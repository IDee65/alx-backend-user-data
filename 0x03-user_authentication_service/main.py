#!/usr/bin/env python3
"""
Main module
"""
import requests


def register_user(email: str, password: str) -> None:
    """ Test register user endpoint

    Args:
        email (str): Description
        password (str): Description
    """
    res = requests.post("http://0.0.0.0:5001/users",
                        data={"email": email,
                              "password": password})
    if res.status_code == 200:
        assert (res.json() == {"email": email, "message": "user created"})
    else:
        assert (res.json() == {"message": "email already registered"})


def log_in_wrong_password(email: str, password: str) -> None:
    """ Test login endpoint

    Args:
        email (str): user's email
        password (str): user's password
    """
    res = requests.post("http://0.0.0.0:5001/sessions",
                        data={"email": email,
                              "password": password})
    assert (res.status_code == 401)


def profile_unlogged() -> None:
    """ Test profile not logged in
    """
    res = requests.get("http://0.0.0.0:5001/profile")
    assert (res.status_code == 403)


def log_in(email: str, password: str) -> str:
    """ test login

    Args:
        email (str): user email
        password (str): user password
    """
    res = requests.post("http://0.0.0.0:5001/sessions",
                        data={"email": email,
                              "password": password})
    assert (res.status_code == 200)
    assert (res.json() == {"email": email, "message": "logged in"})
    return res.cookies['session_id']


def profile_logged(session_id: str) -> None:
    """ Test profile endpoint when logged in

    Args:
        session_id (str): session id
    """
    cookies = {"session_id": session_id}
    res = requests.get("http://0.0.0.0:5001/profile", cookies=cookies)
    assert ("email" in res.json())
    assert (res.status_code == 200)


def log_out(session_id: str) -> None:
    """ Test logout endpoint

    Args:
        session_id (str): session id
    """
    cookies = {"session_id": session_id}
    res = requests.get("http://0.0.0.0:5001/profile", cookies=cookies)
    if res.status_code == 302:
        assert (res.url == "http://0.0.0.0:5001/")
    else:
        assert (res.status_code == 200)


def reset_password_token(email: str) -> str:
    """ Test reset password endpoint

    Args:
        email (str): User's email
    """
    res = requests.post("http://0.0.0.0:5001/reset_password",
                        data={"email": email})
    if res.status_code == 200:
        return res.json()['reset_token']
    assert (res.status_code == 401)


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ Test update password endpoint

    Args:
        email (str): user's email
        reset_token (str): password reset token
        new_password (str): new password
    """
    res = requests.put(
        "http://0.0.0.0:5001/reset_password",
        data={"email": email,
              "reset_token": reset_token, "new_password": new_password})
    if res.status_code == 200:
        # print(res.json())
        assert (res.json() == {"email": f"{email}",
                               "message": "Password updated"})
    else:
        assert (res.status_code == 403)


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
