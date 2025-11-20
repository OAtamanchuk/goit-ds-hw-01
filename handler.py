from collections import UserDict
from datetime import datetime, date, timedelta
from decorators import input_error

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value: str):
        # Валідація телефону ільки 10 цифр
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must contain exactly 10 digits.")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value: str):
        try:
            bd_date = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(value)
        self.date = bd_date # Зберігаємо як date для зручності обробки

class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.birthday: Birthday | None = None

    def add_phone(self, phone: str):
        new_phone = Phone(phone)
        self.phones.append(new_phone)

    def remove_phone(self, phone: str):
        target = self.find_phone(phone)
        if target:
            self.phones.remove(target)
        else:
            raise ValueError("Phone not found.")

    def edit_phone(self, old_phone: str, new_phone: str):
        old_obj = self.find_phone(old_phone)
        if not old_obj:
            raise ValueError("Old phone not found.")
        new_obj = Phone(new_phone)
        old_obj.value = new_obj.value

    def find_phone(self, phone: str):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday_str: str):
        self.birthday = Birthday(birthday_str)

    def __str__(self):
        phones = "; ".join(p.value for p in self.phones) if self.phones else "no phones"
        if self.birthday:
            return f"Contact name: {self.name.value}, phones: {phones}, birthday: {self.birthday.value}"
        return f"Contact name: {self.name.value}, phones: {phones}"
    

class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str) -> Record | None:
        return self.data.get(name)

    def delete(self, name: str):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        # Повертає список словників для дн, які випадають у найближчі 7 днів включно з сьогоднішнім та перенос на понеділок, якщо випадає на вихідний
        today = date.today()
        end_date = today + timedelta(days=7)
        result = []

        for record in self.data.values():
            if not record.birthday:
                continue

            bd = record.birthday.date  # дата народження без року
            # День народження цього року
            congrat_date = bd.replace(year=today.year)
            if congrat_date < today:
                # Якщо вже минув, дивимося наступний рік
                congrat_date = congrat_date.replace(year=today.year + 1)

            if today <= congrat_date <= end_date:
                # Якщо день народження у вихідний переносимо на понеділок
                if congrat_date.weekday() >= 5: 
                    days_to_monday = 7 - congrat_date.weekday()
                    congrat_date += timedelta(days=days_to_monday)

                result.append(
                    {
                        "name": record.name.value,
                        "birthday": congrat_date.strftime("%d.%m.%Y"),
                    }
                )

        return result

    def __str__(self):
        if not self.data:
            return "No contacts saved yet."
        return "\n".join(str(record) for record in self.data.values())

@input_error
def add_contact(args, book: AddressBook):
    if len(args) < 2:
        raise IndexError

    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)  
    return message


@input_error
def change_contact(args, book: AddressBook):
    if len(args) < 3:
        raise IndexError
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found.")
    record.edit_phone(old_phone, new_phone)
    return "Phone number updated."


@input_error
def show_phone(args, book: AddressBook):
    if len(args) < 1:
        raise IndexError
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found.")
    if not record.phones:
        return "No phone numbers for this contact."
    phones = "; ".join(p.value for p in record.phones)
    return f"{name}: {phones}"


@input_error
def show_all(book: AddressBook):
    return str(book)


@input_error
def add_birthday(args, book: AddressBook):
    if len(args) < 2:
        raise IndexError
    
    name, birthday_str, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found. Add contact first.")
    record.add_birthday(birthday_str) 
    return "Birthday added."


@input_error
def show_birthday(args, book: AddressBook):
    if len(args) < 1:
        raise IndexError

    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found.")
    if not record.birthday:
        return "Birthday is not set for this contact."
    return f"{name}'s birthday: {record.birthday.value}"


@input_error
def birthdays(book: AddressBook):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays."
    lines = ["Upcoming birthdays:"]
    for item in upcoming:
        lines.append(f"{item['name']}: {item['birthday']}")
    return "\n".join(lines)
