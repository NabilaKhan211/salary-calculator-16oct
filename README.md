# Employee Salary Calculator

**Veda Technology: Python Programming Track · Level 1 · Task 16 (Day 16)**

A program that calculates an employee's **gross salary, deductions, and net salary** from configurable salary rules.

## Features
- Employee data stored as a dictionary of dictionaries (ID → details)
- All salary rules kept in one `SALARY_RULES` dictionary, so they are easy to change
- Separate functions for allowances, gross, tax rate, deductions, and net salary
- Detailed salary slip (calculation breakdown) for each employee
- Summary table for all employees
- Add employees; view and change salary rules while the program runs
- Validation: numeric input only, no negative values, no duplicate IDs

## Requirements
Python 3.6+ (standard library only)

## How to Run
```bash
python salary_calculator.py
```

## Menu
```
1. View employees
2. Salary breakdown for an employee
3. Salary summary of all employees
4. Add employee
5. View salary rules
6. Change a salary rule
7. Exit
```

## Salary Rules (default, all configurable)
| Rule | Default |
|---|---|
| HRA | 20% of basic |
| DA | 10% of basic |
| Travel allowance | Rs. 2,000 fixed |
| Provident Fund (PF) | 12% of basic |
| Professional tax | Rs. 200 if gross > Rs. 15,000 |
| Income tax (on gross) | up to 25,000: 0% · up to 50,000: 5% · up to 1,00,000: 10% · above: 20% |

> The income tax slabs are simplified for practice and are not real tax law.

## Formulas
```
Gross Salary = Basic + HRA + DA + Travel Allowance + Bonus
Net Salary   = Gross Salary - (PF + Professional Tax + Income Tax)
```

## Sample Output
```
--- Salary Slip: Aarav Sharma (E101, Engineering) ---
EARNINGS
  Basic Salary                 Rs. 40,000.00
  HRA                           Rs. 8,000.00
  DA                            Rs. 4,000.00
  Travel Allowance              Rs. 2,000.00
  Bonus                         Rs. 5,000.00
  GROSS SALARY                 Rs. 59,000.00
DEDUCTIONS
  Provident Fund                Rs. 4,800.00
  Professional Tax                Rs. 200.00
  Income Tax (10%)              Rs. 5,900.00
  TOTAL DEDUCTIONS             Rs. 10,900.00
  NET SALARY                   Rs. 48,100.00
```

## How to Change the Rules
Either edit the `SALARY_RULES` dictionary at the top of `salary_calculator.py`, or use menu option 6 at run time. The calculation functions do not need to be modified.

## Author
Nabila, Veda Technology Intern