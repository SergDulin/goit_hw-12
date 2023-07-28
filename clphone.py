from datetime import datetime
from typing import Optional
import pickle
import os
from collections import UserDict


class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

    def __str__(self) -> str:
        return str(self._value)

    def __repr__(self) -> str:
        return str(self)


class Name(Field):
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = " ".join(word.capitalize() for word in new_value.split())


class Phone(Field):
    @Field.value.setter
    def value(self, new_value):
        if not new_value.startswith("+") or not new_value[1:].isdigit() or len(new_value) != 13:
            raise ValueError("Invalid phone number")
        self._value = new_value


class Birthday(Field):
    @Field.value.setter
    def value(self, new_value):
        if new_value:
            try:
                datetime.strptime(new_value, "%d.%m.%Y")
            except ValueError:
                raise ValueError("Invalid birthday format. Please use the format 'dd.mm.yyyy'")
            self._value = new_value

    @property
    def date(self):
        if self.value:
            return datetime.strptime(self.value, "%d.%m.%Y").date()
        return None


class Record:
    def __init__(self, name: Name):
        self.name = name
        self.phones = []
        self.birthday: Optional[Birthday] = None

    def add_phone(self, phone: Phone):
        if phone.value not in [p.value for p in self.phones]:
            self.phones.append(phone)

    def change_phone(self, old_phone, new_phone):
        for idx, p in enumerate(self.phones):
            if old_phone.value == p.value:
                self.phones[idx] = new_phone

    def days_to_birthday(self):
        if self.birthday and self.birthday.date:
            today = datetime.now().date()
            next_birthday = datetime(today.year, self.birthday.date.month, self.birthday.date.day).date()
            if next_birthday < today:
                next_birthday = datetime(today.year + 1, self.birthday.date.month, self.birthday.date.day).date()
            days_left = (next_birthday - today).days
            return days_left
        else:
            return None

    def __str__(self) -> str:
        name_str = str(self.name)
        phone_numbers = ", ".join(str(p) for p in self.phones)
        birthday_str = f", {self.birthday}" if self.birthday else ""
        days_until_birthday = f", Days until the next birthday: {self.days_to_birthday()}" if self.birthday else ""
        return f"{name_str}: {phone_numbers}{birthday_str}{days_until_birthday}"


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()

    def add_record(self, record: Record):
        self.data[str(record.name).lower()] = record
        return f"Contact {record.name}: {', '.join(str(p) for p in record.phones)}{', ' + str(record.birthday) if record.birthday else ''} added successfully"

    def remove_record(self, name):
        name = name.lower()
        if name in self.data:
            del self.data[name]
            return f"Contact '{str(name).capitalize()}' removed from address book"
        else:
            raise KeyError(f"Contact '{str(name).capitalize()}' not found in address book")

    def change_record(self, name, old_phone, new_phone):
        name = name.lower()
        if name in self.data:
            record = self.data[name]
            record.change_phone(old_phone, new_phone)
            return f"Old phone {old_phone} changed to {new_phone} for contact '{str(name).capitalize()}'"
        else:
            raise KeyError(f"Contact '{str(name).capitalize()}' not found in address book")

    def clear_all(self):
        self.data.clear()
        return "All contacts have been cleared from the address book."

    def show_all_records(self):
        if not self.data:
            return "There are no contacts saved."
        return "\n".join(str(record) for record in self.data.values())

    def find_record_by_name(self, name):
        name_lower = name.lower()
        if name_lower in self.data:
            return self.data[name_lower]
        return None

    def __iter__(self):
        self._iter_keys = list(self.data.keys())
        return self

    def __next__(self):
        if len(self._iter_keys) == 0:
            raise StopIteration
        else:
            record_key = self._iter_keys.pop(0)
            return self.data[record_key]