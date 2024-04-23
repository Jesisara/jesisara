class Contact:
    def __init__(self, name, phone_number):
        self.name = name
        self.phone_number = phone_number

class ContactBook:
    def __init__(self):
        self.contacts = []

    def add_contact(self, contact):
        self.contacts.append(contact)

    def display_contacts(self):
        if not self.contacts:
            print("Contact book is empty.")
        else:
            print("Contacts:")
            for i, contact in enumerate(self.contacts, start=1):
                print(f"{i}. Name: {contact.name}, Phone Number: {contact.phone_number}")

    def search_contact(self, name):
        for contact in self.contacts:
            if contact.name.lower() == name.lower():
                return contact
        return None

def main():
    contact_book = ContactBook()
    
    while True:
        print("\n1. Add Contact")
        print("2. Display Contacts")
        print("3. Search Contact")
        print("4. Quit")

        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter name: ")
            phone_number = input("Enter phone number: ")
            contact = Contact(name, phone_number)
            contact_book.add_contact(contact)
            print("Contact added successfully.")
        elif choice == '2':
            contact_book.display_contacts()
        elif choice == '3':
            name = input("Enter name to search: ")
            contact = contact_book.search_contact(name)
            if contact:
                print(f"Contact found - Name: {contact.name}, Phone Number: {contact.phone_number}")
            else:
                print("Contact not found.")
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
