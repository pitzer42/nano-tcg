from gameplay.nano_magic.protocol import (
    pack,
    unpack
)


def test_wrap_messages_returns_bytes():
    packet = pack('foo')
    assert isinstance(packet, bytes)


def test_wrap_message_ends_with_line_break():
    packet = pack('foo')
    assert packet.endswith(b'\n')


def test_pack_and_unpack():
    original = 'foo'
    packet = pack(original)
    unpacket = unpack(packet)
    assert original == unpacket
