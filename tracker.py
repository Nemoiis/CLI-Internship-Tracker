import sqlite3
import datetime


# ============================================================
# CONFIG
# ============================================================

WIDTH = 40


# ============================================================
# DATABASE SETUP
# ============================================================

con = sqlite3.connect("tracker.db")
cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS applications
            (custID INTEGER PRIMARY KEY,
            company TEXT NOT NULL,
            role TEXT NOT NULL,
            status TEXT NOT NULL,
            date TEXT NOT NULL)''')


# ============================================================
# DISPLAY HELPERS
# ============================================================

def show_menu():
    options = [
        ("1", "Add an Entry"),
        ("2", "View all Entries"),
        ("3", "Search by Company"),
        ("4", "Filter Entries"),
        ("5", "Update an Entry's Status"),
        ("6", "Delete an Entry"),
        ("0", "Exit"),
    ]

    print("\n╔" + "═" * WIDTH + "╗")
    print("║" + "INTERNSHIP DATABASE".center(WIDTH) + "║")
    print("╠" + "═" * WIDTH + "╣")

    for key, label in options:
        print("║  " + f"[{key}]  {label}".ljust(WIDTH - 2) + "║")

    print("╚" + "═" * WIDTH + "╝")

    return input("Choose an option: ").strip()


def view_companies(rows):
    if not rows:
        print("\nNo results.")
        return

    print(f"\n{'ID':<5}{'Company':<15}{'Role':<15}{'Status':<12}Date")
    print("-" * 57)

    for custID, company, role, status, date in rows:
        print(f"{custID:<5}{company:<15}{role:<15}{status:<12}{date}")


# ============================================================
# INPUT HELPERS
# ============================================================

def getText(prompt):
    while True:
        value = input(prompt).strip()

        if value:
            return value

        print("This field can't be blank.")


def getStatus():
    while True:
        try:
            numStatus = int(input("Enter 1 (Applied), 2 (Interview), 3 (Offer), or 4 (Rejected): \n"))

            if numStatus >= 1 and numStatus <= 4:
                break

            else:
                print("Please use an appropriate number.")

        except ValueError:
            print("Please only type the number options provided")

    if numStatus == 1:
        return "Applied"

    elif numStatus == 2:
        return "Interview"

    elif numStatus == 3:
        return "Offer"

    elif numStatus == 4:
        return "Rejected"


def getDate():
    while True:
        dateCheck = input("Would you like to use the current date or type in a date manually: ").strip().lower()

        if dateCheck == "current":
            return datetime.date.today().strftime("%Y/%m/%d")

        elif dateCheck == "manual":
            while True:
                text = input("Enter date in the following format (YYYY/MM/DD): ").strip()

                try:
                    return datetime.datetime.strptime(text, "%Y/%m/%d").strftime("%Y/%m/%d")

                except ValueError:
                    print("That isn't a valid date. Please use YYYY/MM/DD.")

        else:
            print("Please input proper options.")


# ============================================================
# DATABASE ACTIONS
# ============================================================

def add_entry():
    company = getText("Enter the Company name: \n")
    role = getText("Enter the role name: \n")
    date = getDate()
    status = getStatus()

    cur.execute('''INSERT INTO applications (company, role, status, date)
    VALUES ( ?, ?, ?, ?)''', (company, role, status, date))

    con.commit()

    return "Data Added!"


def delete_entry():
    try:
        delete = int(input("Enter ID of what you want to delete: "))

        cur.execute("DELETE FROM applications WHERE custID = ?", (delete,))
        con.commit()

        return f"{str(cur.rowcount)} row(s) were deleted"

    except ValueError:
        return "Invalid input. Try again."


# ============================================================
# MAIN PROGRAM LOOP
# ============================================================

def main():

    while True:
        choice = show_menu()

        # [0] Exit
        if choice == "0":
            con.close()
            break

        # [1] Add an entry
        elif choice == "1":
            print(add_entry())

        # [2] View all entries
        elif choice == "2":
            cur.execute("SELECT * FROM applications ORDER BY custID")
            view_companies(cur.fetchall())

        # [3] Search by company
        elif choice == "3":
            term = input("Enter Company Name: ")

            cur.execute("SELECT * FROM applications WHERE company LIKE ?", (f"%{term}%",))
            view_companies(cur.fetchall())

        # [4] Filter entries
        elif choice == "4":
            option = input("What would you like to filter by (Status or Date): ").lower()

            if option == "status":
                statusfilter = getStatus()

                cur.execute("SELECT * FROM applications WHERE status LIKE ?", (f"%{statusfilter}%",))
                view_companies(cur.fetchall())

            elif option == "date":
                datefilter = input("Enter date in YYYY/MM/DD format: ")

                cur.execute("SELECT * FROM applications WHERE date like ?", (f"%{datefilter}%",))
                view_companies(cur.fetchall())

            else:
                print("Invalid Option.")

        # [5] Update an entry's status
        elif choice == "5":
            try:
                entry_id = int(input("Enter the ID of the entry you would like to update: "))

            except ValueError:
                print("Invalid input. Try again.")
                continue

            print("\n")
            status = getStatus()

            cur.execute('''
            UPDATE applications
            SET status = ? WHERE custID = ?
            ''', (status, entry_id))

            con.commit()

            print(f"{str(cur.rowcount)} row(s) were updated")

        # [6] Delete an entry
        elif choice == "6":
            print(delete_entry())


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()