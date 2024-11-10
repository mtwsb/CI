import json
import os

class NoteManager:
    def __init__(self, filename='notes.json'):
        self.filename = filename
        self.load_notes()

    def load_notes(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                self.notes = json.load(f)
        else:
            self.notes = []

    def save_notes(self):
        with open(self.filename, 'w') as f:
            json.dump(self.notes, f, indent=4)

    def add_note(self, note):
        self.notes.append(note)
        self.save_notes()
        print("Notatka dodana.")

    def remove_note(self, index):
        if 0 <= index < len(self.notes):
            removed = self.notes.pop(index)
            self.save_notes()
            print(f"Usunięto notatkę: {removed}")
        else:
            print("Nieprawidłowy indeks.")

    def display_notes(self):
        if not self.notes:
            print("Brak notatek.")
            return
        for index, note in enumerate(self.notes):
            print(f"{index}: {note}")

def main():
    manager = NoteManager()

    while True:
        print("1. Dodaj notatkę")
        print("2. Usuń notatkę")
        print("3. Wyświetl notatki")
        print("4. Zakończ")

        choice = input("Wybierz opcję: ")

        if choice == '1':
            note = input("Wpisz notatkę: ")
            manager.add_note(note)
        elif choice == '2':
            manager.display_notes()
            index = int(input("Podaj indeks notatki do usunięcia: "))
            manager.remove_note(index)
        elif choice == '3':
            manager.display_notes()
        elif choice == '4':
            break
        else:
            print("Nieprawidłowy wybór. Spróbuj ponownie.")

if __name__ == "__main__":
    main()

