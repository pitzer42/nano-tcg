def add(pool: dict, rsrc_type, quantity: int):
    if rsrc_type in pool:
        pool[rsrc_type] += quantity
    else:
        pool[rsrc_type] = quantity


def consume(pool: dict, rsrc_type, quantity: int):
    pool[rsrc_type] -= quantity
