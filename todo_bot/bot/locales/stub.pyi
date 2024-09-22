from typing import Literal

    
class TranslatorRunner:
    def get(self, path: str, **kwargs) -> str: ...
    
    lang: Lang

    @staticmethod
    def start_menu_message() -> Literal["""Hello!"""]: ...


class Lang:
    @staticmethod
    def ru() -> Literal["""🇷🇺 Русский"""]: ...

    @staticmethod
    def en() -> Literal["""🇬🇧 English"""]: ...

