Budget App
budget management application with GUI built using Python and Tkinter. Manage your income and expenses, 
set budget limits, analyze spending patterns, and export data to Excel.


**Features**

**Record Income**: Add income transactions with amount, category, and date

**Record Expense**: Add expense transactions with amount, category, and date

**Set Budget Limits**: Set monthly budget limits for each spending category

**View Budget Limits**: Monitor your budget limits and current spending for each category

**Budget **Alerts****: Receive warnings when expense exceeds the set budget limit

**Reset Budget: Reset** budget limits for specific categories

**View Statistics**: See total income, total expenses, balance, and expense ratio

**Expense Analysis**: Visualize spending patterns with interactive pie charts showing expense breakdown by category with percentages

**View Transactions**: Display all transactions in a table format with sorting options

**Delete Transactions**: Delete single or multiple transactions at once

****Export to Excel**: Export all transaction data and statistics to Excel file with proper formatting:**

Transactions sheet with all transaction records
Statistics sheet with summary data
Automatic column width adjustment
Currency formatting with $ symbol


**Data Persistence**: All data is saved in JSON format and automatically loaded on startup

**Requirements**

Python 3.7+
tkinter (included with Python)
pandas
matplotlib
openpyxl

Installation

**Clone the repository**:

git clone https://github.com/yoonkevin2010-source/budget-app.git
cd budget-app

**Install required packages**:

pip install pandas matplotlib openpyxl

**Run the application**:

python budget_gui.py

**How to Use**

**Recording Transactions**: Click "Record Income" or "Record Expense" to add new transactions

**Setting Budgets**: Use "Set Budget Limits" to set monthly spending limits by category

**Monitoring Budget**: Click "View Budget Limits" to see current spending vs budget

**Analyzing Spending**: Click "Expense Analysis" to see pie chart visualization of your spending

**Managing Transactions**: Use "View/Delete" to view all transactions and delete any as needed

**Exporting Data**: Click "Export to Excel" to save all data to an Excel file

**File Structure**

**budget_gui.py** - Main GUI application

**transactions.json** - Transaction data file (auto-created)

**budget_limits.json** - Budget limits data file (auto-created)

**budget_data.xlsx** - Exported Excel file (created on export)

**Categories**

Salary

-Food

-Transportation

-Entertainment

-Other



**Future Enhancements**

-Dark mode theme

-Monthly comparison charts

-Recurring transaction templates

-Budget forecasting



**Author**

Kevin Yoon



