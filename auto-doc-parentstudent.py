import os
import re

FILENAME = "educational_assistance_list.txt"
BACKUP = "educational_assistance_list.bak"

def get_input(label, default=""):
    inp = input(f"{label} [{default}]: ").strip()
    return inp if inp else default

def collect_info(info_type, fields, defaults=None):
    data = {}
    print(f"\n--- {info_type} ---")
    for field in fields:
        default = defaults.get(field, "") if defaults else ""
        data[field] = get_input(f"{field}", default)
    return data

PARENT_FIELDS = [
    "Last Name", "First Name", "Middle Name", "Extension Name",
    "Address", "Sex", "Civil Status", "Date of Birth",
    "Contact Number", "Occupation", "Monthly Salary", "Relationship to Beneficiary"
]

STUDENT_FIELDS = [
    "Last Name", "First Name", "Middle Name", "Extension Name",
    "Address", "Date of Birth", "Sex", "Year Level",
    "Civil Status", "Contact Number", "Occupation", "Monthly Salary"
]

def save_to_txt(entries, filename=FILENAME):
    with open(BACKUP, "w", encoding="utf-8") as b:
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as orig:
                b.write(orig.read())
    with open(filename, "w", encoding="utf-8") as f:
        for i, (p, s) in enumerate(entries, 1):
            f.write(f"==== Entry #{i} ====\n")
            f.write("Parent/Guardian Information:\n")
            for k, v in p.items():
                f.write(f"  {k}: {v}\n")
            f.write("\nStudent Information:\n")
            for k, v in s.items():
                f.write(f"  {k}: {v}\n")
            f.write("\n--------------------------\n\n")
    print(f"Saved {len(entries)} entries to {filename}")

def load_entries(filename):
    if not os.path.exists(filename):
        return []

    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()

    entries = []
    blocks = re.findall(r"==== Entry #\d+ ====\n(.*?)\n--------------------------", content, re.DOTALL)
    for block in blocks:
        parent_block = re.search(r"Parent/Guardian Information:\n(.*?)\n\nStudent Information:", block, re.DOTALL)
        student_block = re.search(r"Student Information:\n(.*)", block, re.DOTALL)

        parent = {}
        student = {}
        if parent_block:
            for line in parent_block.group(1).splitlines():
                if ':' in line:
                    k, v = line.strip().split(":", 1)
                    parent[k.strip()] = v.strip()
        if student_block:
            for line in student_block.group(1).splitlines():
                if ':' in line:
                    k, v = line.strip().split(":", 1)
                    student[k.strip()] = v.strip()

        entries.append((parent, student))
    return entries

def display_entry(i, p, s):
    print(f"\n==== Entry #{i + 1} ====")
    print("Parent/Guardian Info:")
    for k, v in p.items():
        print(f"  {k}: {v}")
    print("Student Info:")
    for k, v in s.items():
        print(f"  {k}: {v}")
    print("--------------------------")

def main():
    entries = load_entries(FILENAME)

    while True:
        print("\n--- MENU ---")
        print("1. Add Entry")
        print("2. Edit Entry")
        print("3. Delete Entry")
        print("4. View All Entries")
        print("5. Save and Exit")

        choice = input("Choose: ").strip()

        if choice == "1":
            parent = collect_info("Parent/Guardian Information", PARENT_FIELDS)
            student = collect_info("Student Information", STUDENT_FIELDS)
            entries.append((parent, student))

        elif choice == "2":
            if not entries:
                print("No entries yet.")
                continue
            for i, (p, s) in enumerate(entries):
                print(f"[{i + 1}] {p.get('Last Name')}, {s.get('First Name')}...")
            idx = int(input("Enter entry number to edit: ")) - 1
            parent, student = entries[idx]
            parent = collect_info("Parent/Guardian Information", PARENT_FIELDS, parent)
            student = collect_info("Student Information", STUDENT_FIELDS, student)
            entries[idx] = (parent, student)

        elif choice == "3":
            if not entries:
                print("No entries to delete.")
                continue
            for i, (p, s) in enumerate(entries):
                print(f"[{i + 1}] {p.get('Last Name')}, {s.get('First Name')}...")
            idx = int(input("Enter entry number to delete: ")) - 1
            entries.pop(idx)
            print("Entry deleted.")

        elif choice == "4":
            if not entries:
                print("No entries yet.")
            for i, (p, s) in enumerate(entries):
                display_entry(i, p, s)

        elif choice == "5":
            save_to_txt(entries)
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
