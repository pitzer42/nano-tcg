from bot import wrap_message


def test_wrap_messages_returns_bytes():
    wrapped = wrap_message('foo')
    assert isinstance(wrapped, bytes)


def test_wrap_message_ends_with_line_break():
    wrapped = wrap_message('foo')
    assert wrapped.endswith(b'\n')

