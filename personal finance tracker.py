import datetime
import sqlite3
import xlsxwriter
import matplotlib.pyplot as plt

class ExpenseTracker:
    def __init__(self):
        self.expenses = {}
        self.conn = sqlite3.connect('expenses.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS expenses (date TEXT, category TEXT, amount REAL, description TEXT)')
        self.conn.commit()

    def add_expense(self):
        date = input("Enter date (YYYY-MM-DD): ")
        category = input("Enter category: ")
        amount = float(input("Enter amount: "))
        description = input("Enter description: ")
        self.expenses[category] = self.expenses.get(category, 0) + amount
        self.cursor.execute('INSERT INTO expenses VALUES (?, ?, ?, ?)', (date, category, amount, description))
        self.conn.commit()

    def view_expenses(self):
        for category, amount in self.expenses.items():
            print(f"{category}: ${amount:.2f}")

    def export_to_excel(self):
        workbook = xlsxwriter.Workbook('expenses.xlsx')
        worksheet = workbook.add_worksheet()
        worksheet.write('A1', 'Date')
        worksheet.write('B1', 'Category')
        worksheet.write('C1', 'Amount')
        worksheet.write('D1', 'Description')
        row = 2
        self.cursor.execute('SELECT * FROM expenses')
        for expense in self.cursor.fetchall():
            worksheet.write(f'A{row}', expense[0])
            worksheet.write(f'B{row}', expense[1])
            worksheet.write(f'C{row}', expense[2])
            worksheet.write(f'D{row}', expense[3])
            row += 1
        workbook.close()

    def export_to_text(self):
        with open('expenses.txt', 'w') as file:
            file.write('Expenses:\n')
            self.cursor.execute('SELECT * FROM expenses')
            for expense in self.cursor.fetchall():
                file.write(f"{expense[0]} - {expense[1]}: ${expense[2]:.2f} ({expense[3]})\n")

    def visualize_expenses(self):
        categories = list(self.expenses.keys())
        amounts = list(self.expenses.values())
        plt.bar(categories, amounts)
        plt.xlabel('Category')
        plt.ylabel('Amount ($)')
        plt.title('Expense Distribution')
        plt.show()

def main():
    tracker = ExpenseTracker()
    while True:
        print("\n1. Add Expense\n2. View Expenses\n3. Export to Excel\n4. Export to Text File\n5. Visualize Expenses\n6. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            tracker.add_expense()
        elif choice == "2":
            tracker.view_expenses()
        elif choice == "3":
            tracker.export_to_excel()
            print("Expenses exported to expenses.xlsx")
        elif choice == "4":
            tracker.export_to_text()
            print("Expenses exported to expenses.txt")
        elif choice == "5":
            tracker.visualize_expenses()
        elif choice == "6":
            break
        else:
            print("Invalid option")

if __name__ == "__main__":
    main()
