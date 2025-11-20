import os
import random
import datetime

admin_file = "admins.txt"
student_file = "students.txt"
question_file = "questions.txt"
log_file = "scores.log"

students_db = {}
admins_db = {}
logged_user = None
is_admin = False

def load_admin():
    admins_db.clear()
    if os.path.exists(admin_file):
        with open(admin_file, "r") as f:
            for line in f:
                parts = line.strip().split("|")
                if len(parts) == 2:
                    admins_db[parts[0]] = parts[1]

def save_admin():
    with open(admin_file, "w") as f:
        for user, pwd in admins_db.items():
            f.write(f"{user}|{pwd}\n")

def load_student():
    students_db.clear()
    if os.path.exists(student_file):
        with open(student_file, "r") as f:
            for line in f:
                parts = line.strip().split("|")
                if len(parts) == 7:
                    enrollment, password, name, email, branch, year, number = parts
                    students_db[enrollment] = {
                        "Password": password, "Name": name, "Email": email,
                        "Branch": branch, "Year": year, "Number": number
                    }

def save_student():
    with open(student_file, "w") as f:
        for e, data in students_db.items():
            f.write(f"{e}|{data['Password']}|{data['Name']}|{data['Email']}|{data['Branch']}|{data['Year']}|{data['Number']}\n")

def register_student():
    enrollment = input("Enter enrollment number: ").strip()
    if enrollment in students_db:
        print("Enrollment already exists")
        return
    password = input("Enter password: ").strip()
    name = input("Enter full name: ").strip()
    email = input("Enter email: ").strip()
    branch = input("Enter branch: ").strip()
    year = input("Enter year: ").strip()
    number = input("Enter phone number: ").strip()

    students_db[enrollment] = {
        "Password": password, "Name": name, "Email": email,
        "Branch": branch, "Year": year, "Number": number
    }
    save_student()
    print("Registration successful!")

def login():
    global logged_user, is_admin
    username = input("Enter Username/Enrollment: ").strip()
    password = input("Enter password: ").strip()
    if username in admins_db and admins_db[username] == password:
        is_admin = True
        logged_user = username
        print(f" Welcome Admin, {username}!")
        admin_menu()
        return
    if username in students_db and students_db[username]["Password"] == password:
        is_admin = False
        logged_user = username
        print(f" Welcome {students_db[username]['Name']}!")
        student_menu()
    else:
        print("Invalid credentials.")

def logout():
    global logged_user, is_admin
    if logged_user:
        print(f"{logged_user} logged out.")
        logged_user = None
        is_admin = False
    else:
        print("No user logged in.")

def update_profile():
    global logged_user, is_admin
    if not logged_user:
        print("Please login first.")
        return
    if is_admin:
        print("--- Update Admin Profile ---")
        current_pwd = admins_db[logged_user]
        new_pwd = input(f"Enter new password (leave blank to keep current): ").strip() or current_pwd
        admins_db[logged_user] = new_pwd
        save_admin()
        print("Admin profile updated successfully!")

    else:
        print("--- Update Student Profile ---")
        user = students_db[logged_user]
        
        new_name = input(f"Name ({user['Name']}): ").strip() or user['Name']
        new_email = input(f"Email ({user['Email']}): ").strip() or user['Email']
        new_branch = input(f"Branch ({user['Branch']}): ").strip() or user['Branch']
        new_year = input(f"Year ({user['Year']}): ").strip() or user['Year']
        new_number = input(f"Phone ({user['Number']}): ").strip() or user['Number']
        new_pwd = input("New Password (leave blank to keep current): ").strip() or user['Password']
        students_db[logged_user] = {
            "Password": new_pwd, "Name": new_name, "Email": new_email,
            "Branch": new_branch, "Year": new_year, "Number": new_number
        }
        save_student()
        print("Student profile updated successfully!")

def add_admin():
    if not is_admin:
        print("Admin access required.")
        return
    username = input("Enter new admin username: ").strip()
    if username in admins_db:
        print("Admin already exists.")
        return
    password = input("Enter new admin password: ").strip()
    admins_db[username] = password
    save_admin()
    print(f"New admin '{username}' added successfully!")

def view_admin():
    if not is_admin:
        print("Admin access required.")
        return
    if not admins_db:
        print("No admins found.")
        return
    print("--- ADMIN LIST ---")
    for i, admin in enumerate(admins_db.keys(), 1):
        print(f"{i}. {admin}")

def load_questions():
    questions = []
    if os.path.exists(question_file):
        with open(question_file, "r") as f:
            for line in f:
                parts = line.strip().split("|")
                if len(parts) == 7:
                    questions.append(parts)
    return questions

def save_question(questions):
    with open(question_file, "w") as f:
        for q in questions:
            f.write("|".join(q) + "\n")

def add_question():
    category = input("Enter category: ").strip().upper()
    question = input("Enter question: ").strip()
    optA = input("Option A: ").strip()
    optB = input("Option B: ").strip()
    optC = input("Option C: ").strip()
    optD = input("Option D: ").strip()
    ans = input("Correct answer (A/B/C/D): ").strip().upper()
    with open(question_file, "a") as f:
        f.write(f"{category}|{question}|{optA}|{optB}|{optC}|{optD}|{ans}\n")
    print("Question added successfully!")

def delete_question():
    questions = load_questions()
    if not questions:
        print("No questions to delete.")
        return
    for i, q in enumerate(questions, 1):
        print(f"{i}. [{q[0]}] {q[1]} (Ans: {q[-1]})")
    try:
        qid = int(input("Enter question number to delete: ").strip()) - 1
        if 0 <= qid < len(questions):
            del questions[qid]
            save_question(questions)
            print("Question deleted successfully!")
        else:
            print("Invalid number.")
    except ValueError:
        print("Invalid input.")

def take_quiz():
    if not logged_user or is_admin:
        print("Only logged-in students can take quizzes.")
        return
    questions = load_questions()
    if not questions:
        print("No questions found.")
        return
    categories = sorted(set(q[0].upper() for q in questions))
    print("\nAvailable Categories:")
    for cat in categories:
        print(f"- {cat}")
    category = input("Enter category: ").strip().upper()
    selected = [q for q in questions if q[0].upper() == category]
    if not selected:
        print("Invalid or empty category.")
        return
    random.shuffle(selected)
    selected = selected[:min(5, len(selected))]
    print(f"Starting {category} Quiz — {len(selected)} Questions\n")
    score = 0
    for i, q in enumerate(selected, 1):
        print(f"\nQ{i}. {q[1]}")
        print(f"A) {q[2]}")
        print(f"B) {q[3]}")
        print(f"C) {q[4]}")
        print(f"D) {q[5]}")
        ans = input("Enter answer (A/B/C/D): ").strip().upper()
        if ans == q[6].strip().upper():
            print(" Correct!")
            score += 1
        else:
            print(f" Wrong! Correct answer: {q[6]}")
    total = len(selected)
    print(f"\nQuiz Finished! Your Score: {score}/{total}")
    with open(log_file, "a") as f:
        f.write(
            f"Enrollment: {logged_user}, Category: {category}, Score: {score}/{total}, "
            f"Datetime: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        )

def view_all_students():
    if not students_db:
        print("No students found.")
        return
    print("\n--- STUDENT LIST ---")
    for e, s in students_db.items():
        print(f"{e} | {s['Name']} | {s['Email']} | {s['Branch']} | {s['Year']} | {s['Number']}")

def view_logs():
    if not os.path.exists(log_file):
        print("No quiz logs yet.")
        return
    print("\n--- QUIZ LOGS ---")
    with open(log_file, "r") as f:
        print(f.read())

def admin_menu():
    while True:
        print("\n**** ADMIN MENU ****")
        print("1. Manage Questions")
        print("2. View Students")
        print("3. View Quiz Logs")
        print("4. Add New Admin")
        print("5. View Admins")
        print("6. Update Profile")
        print("7. Logout")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            print("\n--- Question Management ---")
            print("1. Add Question")
            print("2. Delete Question")
            sub = input("Enter choice: ").strip()
            if sub == "1":
                add_question()
            elif sub == "2":
                delete_question()
            else:
                print("Invalid input.")
        elif choice == "2":
            view_all_students()
        elif choice == "3":
            view_logs()
        elif choice == "4":
            add_admin()
        elif choice == "5":
            view_admin()
        elif choice == "6":
            update_profile()
        elif choice == "7":
            logout()
            break
        else:
            print("Invalid choice.")

def student_menu():
    while True:
        print("\n**** STUDENT MENU ****")
        print("1. Take Quiz")
        print("2. Update Profile")
        print("3. Logout")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            take_quiz()
        elif choice == "2":
            update_profile()
        elif choice == "3":
            logout()
            break
        else:
            print("Invalid choice.")

def main():
    load_admin()
    load_student()
    while True:
        print("\n**** MAIN MENU ****")
        print("1. Register Student")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter choice: ").strip()
        if choice == "1":
            register_student()
        elif choice == "2":
            login()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()