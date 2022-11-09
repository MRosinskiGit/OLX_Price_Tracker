from datetime import datetime


def Log(text: str) -> None:
    print(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S.%f')[:-3]}: {text}")
