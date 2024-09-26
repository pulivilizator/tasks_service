from typing import Literal

    
class TranslatorRunner:
    def get(self, path: str, **kwargs) -> str: ...
    
    menu: Menu
    todo: Todo
    back: Back
    lang: Lang
    edit: Edit
    create: Create
    comment: Comment

    @staticmethod
    def incorrect_message() -> Literal["""&lt;b&gt;Enter a correct text message&lt;/b&gt;"""]: ...

    @staticmethod
    def input_end_time_error() -> Literal["""&lt;b&gt;Enter correct date&lt;/b&gt;"""]: ...

    @staticmethod
    def comments_empty() -> Literal["""&lt;b&gt;Comments not found&lt;/b&gt;"""]: ...

    @staticmethod
    def register_yes() -> Literal["""Yes"""]: ...

    @staticmethod
    def register_no() -> Literal["""No"""]: ...

    @staticmethod
    def setup_password() -> Literal["""&lt;b&gt;Someone is trying to set a password on your bot profile via browser, is it you? &lt;/b&gt;"""]: ...


class Menu:
    @staticmethod
    def start_message() -> Literal["""&lt;b&gt;This is the main menu of the note taking bot.&lt;/b&gt;
You can choose your language and start working with tasks."""]: ...

    @staticmethod
    def start_todo_button() -> Literal["""My tasks"""]: ...


class Todo:
    list: TodoList
    end_time: TodoEnd_time

    @staticmethod
    def message(*, title, description, created, end_time, is_done, tags) -> Literal["""&lt;b&gt;Title:&lt;/b&gt; { $title }

&lt;b&gt;Description:&lt;/b&gt; { $description }

&lt;b&gt;Created: &lt;/b&gt; { $created }
&lt;b&gt;End time:&lt;/b&gt; { $end_time }

&lt;b&gt;{ $is_done }&lt;/b&gt;

------------------------------------------------------------
{ $tags }"""]: ...

    @staticmethod
    def done() -> Literal["""✅ Done"""]: ...

    @staticmethod
    def not_done() -> Literal["""❌ Not done"""]: ...

    @staticmethod
    def change_status() -> Literal["""✅ Change note status ❌"""]: ...

    @staticmethod
    def delete_button() -> Literal["""🗑 Delete 🗑"""]: ...

    @staticmethod
    def edit_button() -> Literal["""🛠 Edit 🛠"""]: ...

    @staticmethod
    def create_button() -> Literal["""Create task"""]: ...

    @staticmethod
    def show_comments_button() -> Literal["""💬 Comments 💬"""]: ...


class TodoList:
    @staticmethod
    def message() -> Literal["""&lt;b&gt;Tasks:&lt;/b&gt;"""]: ...


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


class Edit:
    @staticmethod
    def skip() -> Literal["""➡️ Skip ➡️"""]: ...

    @staticmethod
    def back() -> Literal["""⬅️ Back ⬅️"""]: ...

    @staticmethod
    def cancel() -> Literal["""Cancel and return"""]: ...

    @staticmethod
    def save() -> Literal["""✔️ Save ✔️"""]: ...

    @staticmethod
    def new_title() -> Literal["""&lt;b&gt;Enter a new title&lt;/b&gt;"""]: ...

    @staticmethod
    def new_description() -> Literal["""&lt;b&gt;Enter a new description&lt;/b&gt;"""]: ...

    @staticmethod
    def new_end_time() -> Literal["""&lt;b&gt;Enter a new end time in the format DD.MM.YYYY HH:MM&lt;/b&gt;"""]: ...

    @staticmethod
    def new_tags() -> Literal["""&lt;b&gt;Enter new comma-delimited tags&lt;/b&gt;"""]: ...

    @staticmethod
    def confirm() -> Literal["""&lt;b&gt;Confirm change:&lt;/b&gt;"""]: ...


class Create:
    @staticmethod
    def title() -> Literal["""&lt;b&gt;Enter title&lt;/b&gt;"""]: ...

    @staticmethod
    def description() -> Literal["""&lt;b&gt;Enter description&lt;/b&gt;"""]: ...

    @staticmethod
    def end_time() -> Literal["""&lt;b&gt;Enter end time in the format DD.MM.YYYY HH:MM&lt;/b&gt;"""]: ...

    @staticmethod
    def tags() -> Literal["""&lt;b&gt;Enter comma-delimited tags&lt;/b&gt;"""]: ...

    @staticmethod
    def confirm() -> Literal["""&lt;b&gt;Confirm create:&lt;/b&gt;"""]: ...


class Comment:
    create: CommentCreate
    delete: CommentDelete
    edit: CommentEdit


class CommentCreate:
    @staticmethod
    def button() -> Literal["""Add comment"""]: ...

    @staticmethod
    def message() -> Literal["""&lt;b&gt;Enter comment text&lt;/b&gt;"""]: ...


class CommentDelete:
    @staticmethod
    def button() -> Literal["""🗑 Delete 🗑"""]: ...


class CommentEdit:
    @staticmethod
    def button() -> Literal["""🛠 Edit 🛠"""]: ...

    @staticmethod
    def message() -> Literal["""&lt;b&gt;Enter comment text&lt;/b&gt;"""]: ...

