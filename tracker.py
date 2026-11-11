import sqlite3

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
            role INT NOT NULL,
            status TEXT NOT NULL,
            date TEXT NOT NULL)''')


# ============================================================
# DISPLAY HELPERS
# ============================================================

def show_menu():
    options = [
        ("1", "View all Entries"),
        ("2", "Search by Company"),
        ("3", "Filter by Status"),
        ("4", "Add a Entry"),
        ("5", "Update a Entries Status"),
        ("6", "Delete a movie"),
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
    print("-" * 85)
    for custID, company, role, status, date in rows:
        print(f"{custID:<5}{company:<15}{role:<15}{status:<12}{date}")


# ============================================================
# INPUT HELPERS
# ============================================================

def statusCheck(numStatus):
    if numStatus == 1:
        return "Applied"

    elif numStatus == 2:
        return "Interview"

    elif numStatus == 3:
        return "Offer"

    elif numStatus == 4:
        return "Rejected"


# ============================================================
# DATABASE ACTIONS
# ============================================================

def add_entry():
        company = input("Enter the Company name: \n")
        role = input("Enter the role name: \n")
        date = input("Enter the date you applied: \n")

        while True:
            numStatus = int(input("Enter 1 (Applied), 2 (Interview), 3 (Offer), or 4 (Rejected): \n"))

            if numStatus >= 1 and numStatus <= 4:
                break

            else:
                print("Please use an appropriate number.")

        status = statusCheck(numStatus)

        cur.execute('''INSERT INTO applications (company, role, status, date)
        VALUES ( ?, ?, ?, ?)''', (company, role, status, date))

        con.commit()
        return "Data Added!"


def delete_entry():
    delete = int(input("Enter ID of what you want to delete: "))


    cur.execute(f"DELETE FROM applications WHERE custID = {delete}")
    con.commit()

    return "Result Deleted."


# ============================================================
# MAIN PROGRAM LOOP
# ============================================================

def main():

    while True:
        choice = show_menu()

        # [0] Exit
        if choice == "0":
            break

        # [1] View all entries
        elif choice == "1":
            cur.execute("SELECT * FROM applications ORDER BY custID")
            view_companies(cur.fetchall())

        # [2] Search by company
        elif choice == "2":
            term = input("Enter Company Name: ")

            try:
                cur.execute("SELECT * FROM applications WHERE company LIKE ?", (f"%{term}%",))
                view_companies(cur.fetchall())

            except NameError:
                print("That name wasn't found. Please type the name exactly how it is in the database.")

        # [3] Filter by status
        elif choice == "3":
            while True:
                numStatus = int(input("Enter 1 (Applied), 2 (Interview), 3 (Offer), or 4 (Rejected): \n"))

                if numStatus >= 1 and numStatus <= 4:
                    break

                else:
                    print("Please use an appropriate number.")

            status = statusCheck(numStatus)
            cur.execute("SELECT * FROM applications WHERE status LIKE ?", (f"%{status}%",))
            view_companies(cur.fetchall())

        # [4] Add an entry
        elif choice == "4":
            print(add_entry())

        # [5] Update an entry's status
        elif choice == "5":
            choice = input("Enter the ID of the status you would like to update: ")
            print("\n")

            while True:
                numStatus = int(input("Enter 1 (Applied), 2 (Interview), 3 (Offer), or 4 (Rejected): \n"))

                if numStatus >= 1 and numStatus <= 4:
                    break

                else:
                    print("Please use an appropriate number.")

            status = statusCheck(numStatus)

            cur.execute('''
            UPDATE applications
            SET status = ? WHERE custID = ?
            ''', (status, choice))

        # [6] Delete an entry
        elif choice == "6":
            print(delete_entry())


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()