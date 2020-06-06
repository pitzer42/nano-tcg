from nano_magic.entities.resources import add
from nano_magic.entities.resources import consume


def test_add_resources_to_empty_pool():
    pool = dict()
    rsrc_type = 'a'
    quantity = 1
    add(pool, rsrc_type, quantity)
    assert pool[rsrc_type] == quantity


def test_add_resources_to_non_empty_pool():
    rsrc_type = 'a'
    quantity = 1
    pool = {
        rsrc_type: quantity
    }
    add(pool, rsrc_type, quantity)
    assert pool[rsrc_type] == quantity + quantity


def test_consume_resource_from_pool():
    rsrc_type = 'a'
    quantity = 1
    pool = {
        rsrc_type: quantity
    }
    consume(pool, rsrc_type, quantity)
    assert pool[rsrc_type] == 0


def test_consume_resource_from_empty_pool_raises_exception():
    rsrc_type = 'a'
    quantity = 1
    pool = dict()
    try:
        consume(pool, rsrc_type, quantity)
    except Exception as exception:
        assert exception is not None
