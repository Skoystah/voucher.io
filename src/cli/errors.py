def error_message(e: Exception) -> str:
    """Render an exception for display on the CLI.

    KeyError.__str__ wraps its argument in quotes ("'Voucher does not exist'"),
    which reads badly on a terminal, so take the message unwrapped.
    """
    if isinstance(e, KeyError) and e.args:
        return str(e.args[0])

    return str(e)
