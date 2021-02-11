"""
python3 rafuzz.py --frequest request.txt --range_start 1 --range_end 5
--min_len 4 --protocol http --fproxies proxies.txt --stop_status 200
--output_type all --print_request True
"""

import argparse
import asyncio
import json
import random
import sys
import urllib
from copy import deepcopy

import aiohttp

from burp_request_parser import BurpRequestParser
from proxies_handler import ProxiesHandler
from request import Request
from request_editor import find_world_in_request, replace_world_in_request
from request_parser import RequestParser
from response_handler import ResponseHandler


def read_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--frequest", dest="frequest", type=str, required=True)
    parser.add_argument("--protocol", dest="protocol", type=str, required=True)
    parser.add_argument("--fproxies", dest="fproxies", type=str, required=False)
    parser.add_argument("--range_start", dest="range_start", type=int, required=True)
    parser.add_argument("--range_end", dest="range_end", type=int, required=True)
    parser.add_argument("--range_step", dest="range_step", type=int, required=False)
    parser.add_argument("--min_len", dest="min_len", type=int, required=False)
    parser.add_argument("--stop_status", dest="stop_status", type=int, required=False)
    parser.add_argument("--output_type", dest="output_type", type=str, required=False)
    parser.add_argument("--print_request", dest="print_request", type=bool, required=False)
    return parser.parse_args()


async def main(args):
    backend_parser = BurpRequestParser
    rp = RequestParser(args.frequest, backend_parser)
    request = rp.parse_text()
    request.url = args.protocol + "://" + request.url

    key_request, subkey_request = find_world_in_request(request)
    if args.fproxies:
        ph = ProxiesHandler(args.fproxies)
    else:
        ph = None
    
    response_handler = ResponseHandler(
        stop_status=args.stop_status,
        output_type=args.output_type,
        print_request=args.print_request,
    )
    range_step = args.range_step or 1
    
    async with aiohttp.ClientSession() as session:
        for value in get_values_from_range(args.range_start, args.range_end, range_step, args.min_len):
            replica_request = Request(request.get_data().copy())
            replica_request.url = request.url
            
            replace_world_in_request(replica_request, key_request, subkey_request, value)
           
            no_answer = True
            attempt_request_limit = 10
            request_count = 0
            response = None
            
            while no_answer:
                proxy = None
                if ph:
                    if not ph.proxies:
                        print("List of working proxies is empty")
                        sys.exit()

                    proxy = ph.get_random_proxy()
                
                try:
                    response = await do_request(session, replica_request, proxy=proxy)
                except (aiohttp.client_exceptions.ClientProxyConnectionError, asyncio.TimeoutError):
                    print(f"There was failed request attempt with the proxy {proxy}")
                    if ph:
                        ph.exclude_not_working_proxy(proxy)
                else:
                    no_answer = False
                finally:
                    request_count += 1
                
                if no_answer and request_count > attempt_request_limit:
                    print("you have exceeded maximum request limit")
                    break

            await response_handler.handle(replica_request, response)


def get_values_from_range(
    range_start: int, 
    range_end: int,
    range_step: int,
    min_len=4,
):
    assert range_start < range_end

    for value in range(range_start, range_end, range_step):
        len_value = len(str(value))
        if len_value < min_len:
            diff = min_len - len_value 
            value = f"{diff * '0'}{value}"

        yield value

    
async def do_request(
        session: aiohttp.ClientSession,  
        request: Request, 
        proxy: str=None
    ):
    request_method = request.method.lower()
    
    if request_method == "post":
        return await session.post(
                request.url,
                data=request.post_data,
                headers=request.headers,
                proxy=proxy,
                timeout=4
            )
    elif request_method == "get":
        return await session.get(
                request.url,
                headers=request.headers,
                proxy=proxy,
                timeout=4
            )
    else:
        raise NotImplemented(f"Method {request.method} is not supported.")
        

if __name__ == "__main__":
    args = read_args()
    asyncio.run(main(args)) 


