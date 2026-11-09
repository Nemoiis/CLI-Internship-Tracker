import sqlite3

WIDTH = 40
con = sqlite3.connect("tracker.db")
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS applications
            (custID INTEGER PRIMARY KEY,
            company TEXT NOT NULL,
            role INT NOT NULL,
            status TEXT NOT NULL, 
            date TEXT NOT NULL)''')

def show_menu():
    options = [
        ("1", "View all Entries"),
        ("2", "Search by Company"),
        ("3", "Filter by Status"),
        ("4", "Add a Entry"),
        ("5", "Update an Entry"),
        ("6", "Delete a movie"),
        ("0", "Exit"),
    ]
    print("\n╔" + "═" * WIDTH + "╗")
    print("║" + "MOVIE DATABASE".center(WIDTH) + "║")
    print("╠" + "═" * WIDTH + "╣")
    for key, label in options:
        print("║  " + f"[{key}]  {label}".ljust(WIDTH - 2) + "║")
    print("╚" + "═" * WIDTH + "╝")
    return input("Choose an option: ").strip()
            
def add_entry():
        company = input("Enter the Company name: \n")
        role = input("Enter the role name: \n")
        date = input("Enter the date you applied: \n")

        while True:
            status = input("Enter 1 (Applied), 2 (Interview), 3 (Offer), or 4 (Rejected): \n")

            if status == "1":
                status = "Applied"
                break

            elif status == "2":
                status = "Interview"
                break

            elif status == "3":
                status = "Offer"
                break

            elif status == "4":
                status = "Rejected"
                break

            else:
                print("Please type a valid number.")
        
        cur.execute('''INSERT INTO applications (company, role, status, date)
        VALUES ( ?, ?, ?, ?)''', (company, role, status, date))
            
        con.commit()
        return "Data Added!"
    
def delete_entry():
    delete = int(input("Enter ID of what you want to delete: "))
    cur.execute(f"DELETE FROM applications WHERE custID = {delete}")
    con.commit()
    
    return "That shi gone GANGSTA"
    
def view_companies(rows):
    if not rows:
        print("\nNo results.")
        return
    print(f"\n{'ID':<5}{'Company':<15}{'Role':<7}{'Status':<12}Date")
    print("-" * 85)
    for custID, company, role, status, date in rows:
        print(f"{custID:<5}{company:<15}{role:<7}{status:<12}{date}")
        
def main():
    
    while True:
        choice = show_menu()
        
        if choice == "0":
            break
        
        elif choice == "1":
            cur.execute("SELECT * FROM applications ORDER BY custID")
            view_companies(cur.fetchall())
            
        elif choice == "2":
            term = input("Enter Company Name: ")
            cur.execute("SELECT * FROM applications WHERE company LIKE ?", (f"%{term}%",))
            view_company(cur.fetchall())

        elif choice == "3":
            status = input("Enter a status: ")
            cur.execute("SELECT * FROM applications WHERE status LIKE ?", (f"%{status}%",))
            view_company(cur.fetchall())

        elif choice == "5":
            choice = input("Enter the ID you wanna delete: ")

            while True:
                status = input("Enter 1 (Applied), 2 (Interview), 3 (Offer), or 4 (Rejected): \n")

                if status == "1":
                    status = "Applied"
                    break

                elif status == "2":
                    status = "Interview"
                    break

                elif status == "3":
                    status = "Offer"
                    break

                elif status == "4":
                    status = "Rejected"
                    break

                else:
                    print("Please type a valid number.")
            
            cur.execute('''
            UPDATE applications
            SET status = ? WHERE custID = ?
            ''', (status, choice))

        elif choice == "4":
            print(add_entry())
            
        elif choice == "6":
            print(delete_entry())

    
if __name__ == "__main__":
    main()