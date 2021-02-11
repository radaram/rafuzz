from request import Request


def find_world_in_request(request: Request, world="FUZZ"):
    for key, value in request.items():
        if key == "headers":
            for subkey, v in value.items():
                if v.find(world) != -1:
                    return (key, subkey)
        else:
            if value.find(world) != -1:
                return (key, None)

    raise ValueError(f"Not found world {world}.")


def replace_world_in_request(
        request: Request, 
        key_request: str,
        subkey_request: str, 
        new_value,
        world="FUZZ"
):
    if subkey_request:
        request[key_request][subkey_request] = request[key_request][subkey_request].replace(world, new_value)
    else:
        request[key_request] = request[key_request].replace(world, new_value)


