
import os
from datetime import datetime


class JournalManager:
    def __init__(self, filename="journal.txt"):
        self.filename = filename

    def add_entry(self):
        print("\nWrite your journal entry.")
        print("Type END on a new line when you finish:")

        lines = []

        while True:
            line = input()
            if line.strip().upper() == "END":
                break
            lines.append(line)

        text = "\n".join(lines).strip()

        if not text:
            print("Entry cannot be empty.")
            return

        try:
            stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            with open(self.filename, "a", encoding="utf-8") as file:
                file.write(f"[{stamp}]\n{text}\n\n")

            print("Journal entry saved successfully!")

        except OSError as error:
            print("Unable to save the entry:", error)

    def get_entries(self):
        with open(self.filename, "r", encoding="utf-8") as file:
            content = file.read()

        return [
            entry.strip()
            for entry in content.split("\n\n")
            if entry.strip()
        ]

    def view_entries(self):
        try:
            entries = self.get_entries()
        except FileNotFoundError:
            print("No journal entries found. Add an entry first.")
            return
        except OSError as error:
            print("Unable to read the journal:", error)
            return

        if not entries:
            print("Your journal is empty.")
            return

        print("\n========== YOUR JOURNAL ==========")

        for number, entry in enumerate(entries, start=1):
            print(f"\nEntry {number}")
            print("-" * 35)
            print(entry)

        print("\n==================================")

    def search_entries(self):
        keyword = input("Enter a keyword or date: ").strip()

        if not keyword:
            print("Please enter something to search.")
            return

        try:
            entries = self.get_entries()
        except FileNotFoundError:
            print("No journal entries found.")
            return
        except OSError as error:
            print("Unable to read the journal:", error)
            return

        found = [
            entry for entry in entries
            if keyword.casefold() in entry.casefold()
        ]

        if found:
            print("\nSearch Results")
            print("-" * 35)

            for number, entry in enumerate(found, start=1):
                print(f"\nResult {number}")
                print(entry)
        else:
            print("No matching entries found.")

    def delete_entries(self):
        if not os.path.exists(self.filename):
            print("There is no journal file to delete.")
            return

        confirm = input(
            "Delete all journal entries? Type YES to confirm: "
        ).strip()

        if confirm != "YES":
            print("Deletion cancelled.")
            return

        try:
            os.remove(self.filename)
            print("All journal entries have been deleted.")
        except OSError as error:
            print("Unable to delete the journal:", error)

    def show_menu(self):
        print("\n===== PERSONAL JOURNAL MANAGER =====")
        print("1. Add a New Entry")
        print("2. View All Entries")
        print("3. Search Entries")
        print("4. Delete All Entries")
        print("5. Exit")

    def run(self):
        while True:
            self.show_menu()
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.add_entry()

            elif choice == "2":
                self.view_entries()

            elif choice == "3":
                self.search_entries()

            elif choice == "4":
                self.delete_entries()

            elif choice == "5":
                print("Thank you for using Personal Journal Manager!")
                print("Goodbye!")
                break

            else:
                print("Invalid choice. Please select 1 to 5.")


if __name__ == "__main__":
    try:
        journal = JournalManager()
        journal.run()
    except (KeyboardInterrupt, EOFError):
        print("\nProgram closed. Goodbye!")
