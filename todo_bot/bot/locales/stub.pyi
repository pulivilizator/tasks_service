from typing import Literal

    
class TranslatorRunner:
    def get(self, path: str, **kwargs) -> str: ...
    
    menu: Menu
    todo: Todo
    back: Back
    lang: Lang


class Menu:
    @staticmethod
    def start_message() -> Literal["""&lt;b&gt;This is the main menu of the note taking bot.&lt;/b&gt;
You can choose your language and start working with notes."""]: ...

    @staticmethod
    def start_todo_button() -> Literal["""My notes"""]: ...


class Todo:
    list: TodoList
    end_time: TodoEnd_time

    @staticmethod
    def message(*, title, description, created, end_time, is_done, tags) -> Literal["""&lt;b&gt;Title:&lt;/b&gt; { $title }

&lt;b&gt;Description:&lt;/b&gt; { $description }

&lt;b&gt;Created: &lt;/b&gt; { $created }
&lt;b&gt;End time:&lt;/b&gt; { $end_time }

&lt;b&gt;{ $is_done }&lt;/b&gt;

---------------
{ $tags }"""]: ...

    @staticmethod
    def done() -> Literal["""✅ Done"""]: ...

    @staticmethod
    def not_done() -> Literal["""❌ Not done"""]: ...

    @staticmethod
    def change_status() -> Literal["""✅ Change note status ❌"""]: ...

    @staticmethod
    def delete_button() -> Literal["""❌ Delete ❌"""]: ...


class TodoList:
    @staticmethod
    def message() -> Literal["""&lt;b&gt;Notes:&lt;/b&gt;"""]: ...


class Back:
    @staticmethod
    def button() -> Literal["""Back"""]: ...


class Lang:
    @staticmethod
    def ru() -> Literal["""🇷🇺 Русский"""]: ...

    @staticmethod
    def en() -> Literal["""🇬🇧 English"""]: ...


class TodoEnd_time:
    @staticmethod
    def default() -> Literal["""Not set"""]: ...

