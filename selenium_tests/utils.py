import uuid

from selenium_tests.Data.Paths import Paths


def get_random_str():
    return str(uuid.uuid4())

def get_portfolio_link_len():
    return len(str(uuid.uuid4()))

def get_random_username_password():
    un = f'{get_random_str()}@gmail.com'
    ps = str(uuid.uuid4())
    return un, ps


def get_driver_in_self(drv):
    class Empty():
        driver = drv
    return Empty()

def get_portfolio_url(link):
    return Paths.PORTFOLIO + f"/{link}"

def get_cluster_title_url(title, page=1, new_post=False):
    if page:
        return Paths.FORUM + f"/{title}/{page}"
    if new_post:
        return Paths.FORUM + Paths.NEW_POST + f"/{title}"
    return Paths.FORUM + f"/{title}"



