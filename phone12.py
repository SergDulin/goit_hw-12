from clphone import *

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError) as e:
            return str(e)
    return wrapper

address_book = AddressBook()

def save_address_book(address_book, filename):
    with open(filename, 'wb') as file:
        pickle.dump(address_book.data, file)

def load_address_book(filename):
    address_book = AddressBook()
    if os.path.exists(filename):
        with open(filename, 'rb') as file:
            address_book.data = pickle.load(file)
    return address_book

@input_error
def add(*args):
    if len(args) < 2:
        raise ValueError("Please provide both name and phone number")

    name = Name(args[0].lower())  
    phones = []
    birthday = None

    for arg in args[1:]:
        if arg.startswith("+"):
            phones.append(Phone(arg))
        elif arg.count(".") == 2:
            birthday = Birthday(arg)
        else:
            name.value += " " + arg

    rec = address_book.find_record_by_name(str(name))
    if rec:
        for phone in phones:
            rec.add_phone(phone)
        if birthday:
            rec.birthday = birthday
    else:
        rec = Record(name)
        rec.birthday = birthday
        for phone in phones:
            rec.add_phone(phone)
        address_book.add_record(rec)
    return f"Contact {name}: {', '.join(str(num) for num in rec.phones)}{', ' + str(rec.birthday) if rec.birthday else ''} added successfully"

@input_error
def change(*args):
    if len(args) < 3:
        raise ValueError("Please provide the name, old phone number, and new phone number")

    name = " ".join(args[:-2]).lower()  
    old_phone = Phone(args[-2])
    new_phone = Phone(args[-1])

    return address_book.change_record(name, old_phone, new_phone)

@input_error
def remove(*args):
    if len(args) != 1:
        raise ValueError("Please provide the name of the contact to remove")

    name = " ".join(args).lower()  
    return address_book.remove_record(name)

@input_error
def search(*args):
    if len(args) != 1:
        raise ValueError("Please provide the search term (name or phone number)")

    search_term = args[0].capitalize()

    matches = []
    for record in address_book:
        if (search_term in str(record.name).capitalize() or
                any(search_term in str(phone) for phone in record.phones)):
            matches.append(record)

    result = ""
    if matches:
        for record in matches:
            result += str(record) + "\n"
    else:
        raise KeyError(f"No matches found for '{search_term}'")
    return result

def show_all():
    return address_book.show_all_records()

def clear_all():
    return address_book.clear_all()
    
def hello_command():
    return "How can I help you?"

def goodbye_command():
    return "Goodbye!"

def no_command():
    return "Invalid command. Please try again."

command_handlers = {
    add: ("add",),
    change: ("change",),
    remove: ("remove",),
    search: ("search",),
    clear_all: ("clear all",),
    show_all: ("show all",),
    hello_command: ("hello",),
    goodbye_command: ("good bye", "exit", "close")
}

def command(user_input):
    for func, keywords in command_handlers.items():
        for keyword in keywords:
            if user_input.lower().startswith(keyword):
                return func, user_input[len(keyword):].strip().split()
    return no_command, []


def main():
    while True:
        user_input = input("Enter a command: ")
        func, data = command(user_input)
        print(func(*data))
        if func == goodbye_command:
            save_address_book(address_book, "address_book.dat")
            print("Address book saved to file: address_book.dat")
            break

if __name__ == "__main__":
    address_book = load_address_book("address_book.dat")
    main()
