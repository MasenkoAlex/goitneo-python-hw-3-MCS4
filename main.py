from collections import UserDict
from datetime import datetime, date


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if self.is_valid_phone(value):
            super().__init__(value)
        else:
            raise ValueError ('Invalid phone number')

    def is_valid_phone(self, phone):
        if len(phone) == 10 and phone.isdigit():
            return True
        else:
            return False
        

class Birthday(Field):
    def __init__(self, value):
        if self.validate_birthdate(value):
            super().__init__(value)
        else:
            raise ValueError ('Invalid format date birthdate')
        
    def validate_birthdate(self, b_date):
        try:
            datetime.strptime(b_date, '%d.%m.%Y')
            return True
        except ValueError:
            return False



class Record:
    def __init__(self, name, b_date = None):
        self.name = Name(name)
        self.phones = []
        self.b_date = b_date

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.b_date}"
    
    def add_phone(self, phone):
        self.phones.append(Phone(phone))
 
    def remove_phone(self, phone):
        object_phone = self.find_phone(phone)
        if object_phone:
            self.phones.remove(object_phone)
        
    def edit_phone(self, old_phone, new_phone):
        object_phone = self.find_phone(old_phone)
        if object_phone:
            if object_phone.is_valid_phone(new_phone):
                object_phone.value = new_phone
            else:
                raise ValueError ('Invalid phone number')

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p

    def add_birthday(self, b_date):
        self.b_date = Birthday(b_date)

    def show_birthday(self):
        return self.b_date



class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record    

    def find(self, name):
        return self.data.get(name)            

    def delete(self, name):
        addres_record = self.find(name)
        if addres_record:
            del self.data[name]

    def birthdays(self):
        birthday_users = {}

        for name, record in self.data.items():
         
            # Конвертуємо до типу date, обрізаємо час
            birthday = datetime.strptime(record.b_date.value, '%d.%m.%Y').date()
            today = date.today()
            birthday_this_year = birthday.replace(year=today.year)

            # Перевіряємо, чи вже минув день народження цього року
            if birthday_this_year < today:
                birthday_this_year = birthday.replace(year=today.year + 1)

            # Визначаємо різницю між днем народження та поточним днем, щоб знайти дні народження на тиждень вперед
            delta_days = (birthday_this_year - today).days

            if delta_days < 7:
                birthday = birthday_this_year.strftime('%A')

                if birthday in ('Saturday', 'Sunday'):
                    if not birthday_users.get('Monday'):
                        birthday_users['Monday'] = []
                    birthday_users['Monday'].append(str(record))
                else:
                    if not birthday_users.get(birthday):               
                        birthday_users[birthday] = []
                    birthday_users[birthday].append(str(record))

        return birthday_users


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def add_contact(args, contacts):
    name, phone = args
    new_record = Record(name)
    new_record.add_phone(phone)
    contacts.add_record(new_record)
    return "Contact added."


def change(args, contacts):
    username, new_phone = args
    record = contacts.find(username)
    if record.phones:
        record.edit_phone(record.phones[0].value, new_phone)
    else:
        record.add_phone(new_phone)
    return f"phone number {new_phone} for {username} has changed" 


def all(args, contacts:dict):
    res = ""
    if not contacts:
        return f"There no conacts!"
    for name, phone in contacts.items():
        res += f"{name}: {phone} \n"
    return res


def phone_username(args, contacts:dict):
    username = args[0]
    record = contacts.get(username)
    if record:
        return f"Username {username} has a phone numbers {'; '.join(p.value for p in record.phones)}"
    return f"Contact not found"


def add_birthday(args, contacts):
    username = args[0]
    birthday = args[1]
    record = contacts.get(username)
    
    if record:
        record.add_birthday(birthday)
        return f"The birthday {birthday} has added to {username}"
    else:
        return f"Contact not found"


def show_birthday(args, contacts:dict):
    username = args[0]
    record = contacts.get(username)

    if record:
        birthday = record.b_date.value if record.b_date else f"No data"
        return f"Username {username} was born in {birthday}"
    return f"Contact not found"


def birthday(args, contacts:dict):
    birth_days = ""
    for key, record in contacts.birthdays().items():
        birth_days += f"{key}: {record} \n"
    return birth_days
        

def main():
    contacts = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]: 
            print("Good bye!")
            break
        elif command == "hello":        
            print("How can I help you?")
        elif command == "add":           
            print(add_contact(args, contacts))
        elif command == "change":        
            print(change(args, contacts))
        elif command == "all":       
            print(all(args, contacts))
        elif command == "phone":      
            print(phone_username(args, contacts))
        elif command == "add-birthday":        
            print(add_birthday(args, contacts))
        elif command == "show-birthday":          
            print(show_birthday(args, contacts))
        elif command == "birthdays":            
            print(birthday(args, contacts))
        else:
            print("Invalid command.")


if __name__ == "__main__":

    main()

