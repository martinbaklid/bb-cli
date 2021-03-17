def prompt(promt_text: str) -> str:
    response = ''
    while not response:
        response = input(promt_text)
    return response
