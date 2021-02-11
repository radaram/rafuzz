import sys
from enum import Enum


class OutputType(Enum):
    ALL = "all"
    FOUND = "found"


class ResponseHandler(object):

    def __init__(
            self, 
            stop_status: int=None, 
            output_type=OutputType.FOUND.value,
            print_request: bool=False
    ):
        self.stop_status = stop_status
        self.output_type = output_type
        self.print_request = print_request

    async def handle(self, request, response):
        if self.output_type == OutputType.ALL.value:
            if self.print_request:
                print(request, end="\n\n")
            await self.print_response(response)
        else:
            print(".", end="")

        if self.stop_status and self.stop_status == response.status:
            if self.output_type == OutputType.FOUND.value:
                if self.print_request:
                    print(request, end="\n\n")
                await self.print_response(response) 
            sys.exit()
        
        if self.output_type == OutputType.ALL.value:
            print("==============\n")
    
    def print_request(self, request):
        print(request)

    async def print_response(self, response):
        if not response:
            print("Response is not received")
            return
        print(f"http status: {response.status}.", end=" ")
        data = await response.read()
        print(f"Response: {data}")


