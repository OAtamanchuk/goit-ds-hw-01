def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except IndexError:
            command = func.__name__
            formats = {
                "add_contact": "Use: add [name] [phone]",
                "change_contact": "Use: change [name] [old_phone] [new_phone]",
                "show_phone": "Use: phone [name]",
                "add_birthday": "Use: add-birthday [name] [DD.MM.YYYY]",
                "show_birthday": "Use: show-birthday [name]",
            } # Словник з інформацією про правильне використання команд для повідомлень про помилки
            return f"Not enough arguments. {formats.get(command, '')}"

        except KeyError as e:
            return str(e) if str(e) else "Contact not found."

        except ValueError as e:
            return str(e) 

        except Exception as e:
            return f"Unexpected error: {e}" # На випадок неочікуваних помилок

    return inner
