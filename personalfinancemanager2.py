import matplotlib.pyplot as plt
import pandas as pd
import csv

class Transaction:
    def __init__(self, amount, date, description):
        self.amount = amount
        self.date = date
        self.description = description

    def get_attributes(self):
        return [self.amount, self.date, self.description]


class Expense(Transaction):
    def __init__(self, amount, date, description):
        super().__init__(amount, date, description)


class OneTimePurchase(Expense):
    def __init__(self, amount, date, description):
        super().__init__(amount, date, description)


class Subscription(Expense):
    def __init__(self, amount, date, description):
        super().__init__(amount, date, description)


class Income(Transaction):
    def __init__(self, amount, date, description):
        super().__init__(amount, date, description)


class OneTimePayment(Income):
    def __init__(self, amount, date, description):
        super().__init__(amount, date, description)


class Salary(Income):
    def __init__(self, amount, date, description):
        super().__init__(amount, date, description)


class User:
    def __init__(self, user_id, username):
        self.user_id = user_id
        self.username = username
        self.transactions = []  # Store user transactions
        self.history_transactions = []  # Store history of transactions

    def add_transaction(self, transaction):
        self.transactions.append(transaction)
        self.history_transactions.append(transaction.get_attributes())

    def get_history_transactions(self):
        return self.history_transactions

    def get_total_income(self):
        return sum(transaction.amount for transaction in self.transactions if isinstance(transaction, Income))

    def get_total_expenses(self):
        return sum(transaction.amount for transaction in self.transactions if isinstance(transaction, Expense))

    def get_savings(self):
        return self.get_total_income() - self.get_total_expenses()

    def get_user_id(self):
        return self.user_id


class PersonalFinanceManager:
    def __init__(self):
        self.users = []
        self.users_id = []

    @property
    def get_users_id(self):
        return self.users_id
    @property
    def get_userslist(self):
        return self.users
        
    def create_user(self, user_id, username):
        new_user = User(user_id, username)
        self.users.append(new_user)
        self.users_id.append(new_user.get_user_id())
        return new_user

    def get_user(self, username):
        for user in self.users:
            if user.username == username:
                return user
        return None

    @property
    def get_users_transaction(self):
        # Return transactions for all users
        return [user.get_history_transactions() for user in self.users]

    def add_transaction_to_user(self, username, transaction):
        user = self.get_user(username)
        if user:
            user.add_transaction(transaction)
        else:
            print(f"User '{username}' not found.")

    def create_user(self, user_id, username):
        # Check if a user with the same user_id already exists
        if user_id in self.users_id:
            print(f"User with user_id '{user_id}' already exists. Cannot create a new user.")
            return None

        # Check if a user with the same username already exists
        existing_user = self.get_user(username)
        if existing_user:
            # Check if the existing user has the same user_id
            if existing_user.get_user_id() == user_id:
                print(
                    f"User with username '{username}' and user_id '{user_id}' already exists. Cannot create a new user.")
                return None

            # If the user has a different user_id, print a warning
            print(
                f"Warning: User with username '{username}' already exists with a different user_id. Creating a new user.")

        # Create a new user
        new_user = User(user_id, username)
        self.users.append(new_user)
        self.users_id.append(new_user.get_user_id())
        return new_user


pf_manager = PersonalFinanceManager()

user_ids = []
# Открываем CSV файл для чтения
with open('data_users.csv', 'r') as csvfile:
    # Создаем объект    csv.reader
    csvreader = csv.reader(csvfile)
    
    # Читаем заголовок
    headers = next(csvreader)
    
    # Задаем индекс столбца " "
    user_id_index = headers.index('user_id')
    user_income_index = headers.index('income')
    user_expense_index = headers.index('expense')
    user_description_index = headers.index('description')
    user_date_index = headers.index('date')
    user_name_index = headers.index('username')
    # Перебираем строки CSV файла
   # ...
    for row in csvreader:
        user_name = row[user_name_index]
        user_id = row[user_id_index]
        date = row[user_date_index]
        description = row[user_description_index]
        
        # Преобразование 'income', 'expense' и 'savings' в числа
        income = float(row[user_income_index])
        expense = float(row[user_expense_index])
        
        # Инициализация объектов
        income_transaction = Income(income, date, description)
        expense_transaction = Expense(expense, date, description)
        
        # Добавление транзакций к пользователю
        if user_id not in user_ids:
            user = pf_manager.create_user(user_id, user_name)
            user_ids.append(user_id)
        else:
            users_id_list = pf_manager.get_users_id
            index = users_id_list.index(user_id)
            users_manager = pf_manager.get_userslist
            user = users_manager[index]
        
        user.add_transaction(income_transaction)
        user.add_transaction(expense_transaction)
    # ...

# Теперь user_ids содержит все значения из столбца "user_id"
# Iterating amen user-i ev ir transactions-i vra
data = []
for user in pf_manager.users:
    user_id = user.get_user_id()
    username = user.username
    # yndhanur savingsner stexcenq dicti tesqov keyerry klinen datanery valuyenery running savingnery
    savings_by_date = {}
    # stecenq popoxakan vor kpahi kutakvac savingnery
    running_savings = 0

    # yuraqanchyur transactioni hamar avelacnum enq datanery(tvyalnery)
    for transaction in user.transactions:
        temp = True
        amount, date, description = transaction.get_attributes()
        income = amount if isinstance(transaction, Income) else 0
        expense = amount if isinstance(transaction, Expense) else 0
        saving = income - expense

        # Update cumulative savings for the user
        running_savings += saving
        # Update savings for the date
        savings_by_date[date] = running_savings
        for item in data:
            if date in item and user_id == item[0]:
                temp = False
                index = item.index(date)
                item[index + 1] += income
                item[index + 2] += expense
                item[index + 3] += saving

        if temp:  # Append enq anum datanery  listum
            data.append([user_id, username, date, income, expense, saving])
    for i in range(len(data) - 1):
        item = data[i]
        next_item = data[i + 1]
        if user_id == item[0] and user_id == next_item[0]:
            next_item[5] += item[5]
print(data)

# stexcum enq  DataFrame
columns = ["user_id", "username", "date", "income", "expense", "savings"]
transaction_df = pd.DataFrame(data, columns=columns)

# DataFrame to CSV file
transaction_df.to_csv('vizualization_data.csv', index=False)

# DataFrame-i tesqy
print(transaction_df)

user_ids = transaction_df['user_id'].unique()
fig, axs = plt.subplots(len(user_ids), 3, figsize=(15, 5 * len(user_ids)))

if len(user_ids) == 1:
    user_id = user_ids[0]
    user_data = transaction_df[transaction_df['user_id'] == user_id]
    username = user_data['username'].iloc[0]
    axs[0].bar(user_data['date'], user_data['income'], color='green')
    axs[0].set_title(f'Total Income (Username: {username}, User ID: {user_id})')
    axs[0].set_xlabel('Date')
    axs[0].set_ylabel('Income')

    axs[1].bar(user_data['date'], user_data['expense'], color='red')
    axs[1].set_title(f'Total Expenses (Username: {username}, User ID: {user_id})')
    axs[1].set_xlabel('Date')
    axs[1].set_ylabel('Expenses')

    axs[2].plot(user_data['date'], user_data['savings'], marker='o', linestyle='-')
    axs[2].set_title(f'Savings (Username: {username}, User ID: {user_id})')
    axs[2].set_xlabel('Date')
    axs[2].set_ylabel('Savings')
else:
    for i, user_id in enumerate(user_ids):
        user_data = transaction_df[transaction_df['user_id'] == user_id]
        username = user_data['username'].iloc[0]  # Get the username for the user_id
        # Plot Total Income
        axs[i, 0].bar(user_data['date'], user_data['income'], color='green')
        axs[i, 0].set_title(f'Total Income (Username: {username}, User ID: {user_id})')
        axs[i, 0].set_xlabel('Date')
        axs[i, 0].set_ylabel('Income')

        # Plot Total Expenses
        axs[i, 1].bar(user_data['date'], user_data['expense'], color='red')
        axs[i, 1].set_title(f'Total Expenses (Username: {username}, User ID: {user_id})')
        axs[i, 1].set_xlabel('Date')
        axs[i, 1].set_ylabel('Expenses')

        # Plot Savings
        axs[i, 2].plot(user_data['date'], user_data['savings'], marker='o', linestyle='-')
        axs[i, 2].set_title(f'Savings (Username: {username}, User ID: {user_id})')
        axs[i, 2].set_xlabel('Date')
        axs[i, 2].set_ylabel('Savings')

plt.tight_layout()
plt.show()