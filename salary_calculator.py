"""Employee Salary Calculator.

Calculates gross salary, deductions and net salary from configurable rules.

    Gross Salary = Basic + HRA + DA + Travel Allowance + Bonus
    Net Salary   = Gross Salary - (PF + Professional Tax + Income Tax)

All rules live in the SALARY_RULES dictionary, so changing a rule never
requires touching the calculation functions.
"""

# ---------- Configurable salary rules ----------
SALARY_RULES = {
    # Allowances
    "hra_percent": 20,            # House Rent Allowance: % of basic
    "da_percent": 10,             # Dearness Allowance: % of basic
    "travel_allowance": 2000,     # fixed amount per month
    # Deductions
    "pf_percent": 12,             # Provident Fund: % of basic
    "professional_tax": 200,      # fixed amount, applied if gross > threshold
    "professional_tax_threshold": 15000,
    # Income tax slabs on gross: (upper limit of gross, tax % on gross)
    # (simplified for practice, not real tax law)
    "tax_slabs": [
        (25000, 0),
        (50000, 5),
        (100000, 10),
        (float("inf"), 20),
    ],
}

# ---------- Sample employee records ----------
employees = {
    "E101": {"name": "Aarav Sharma", "department": "Engineering", "basic": 40000, "bonus": 5000},
    "E102": {"name": "Priya Verma", "department": "HR", "basic": 30000, "bonus": 0},
    "E103": {"name": "Rahul Khan", "department": "Sales", "basic": 55000, "bonus": 10000},
    "E104": {"name": "Sneha Patel", "department": "Support", "basic": 15000, "bonus": 0},
}


# ---------- Calculation functions (business rules) ----------
def calculate_allowances(basic, rules):
    """Return a dict of allowance name -> amount."""
    return {
        "HRA": basic * rules["hra_percent"] / 100,
        "DA": basic * rules["da_percent"] / 100,
        "Travel Allowance": rules["travel_allowance"],
    }


def calculate_gross(basic, bonus, rules):
    """Return (gross salary, allowances dict)."""
    allowances = calculate_allowances(basic, rules)
    return basic + sum(allowances.values()) + bonus, allowances


def get_tax_rate(gross, rules):
    """Find the income tax % for a given gross using the slab table."""
    for limit, rate in rules["tax_slabs"]:
        if gross <= limit:
            return rate
    return 0


def calculate_deductions(basic, gross, rules):
    """Return a dict of deduction name -> amount."""
    tax_rate = get_tax_rate(gross, rules)
    prof_tax = rules["professional_tax"] if gross > rules["professional_tax_threshold"] else 0
    return {
        "Provident Fund": basic * rules["pf_percent"] / 100,
        "Professional Tax": prof_tax,
        f"Income Tax ({tax_rate}%)": gross * tax_rate / 100,
    }


def calculate_salary(employee, rules=SALARY_RULES):
    """Full salary calculation for one employee. Returns a breakdown dict."""
    basic, bonus = employee["basic"], employee.get("bonus", 0)
    gross, allowances = calculate_gross(basic, bonus, rules)
    deductions = calculate_deductions(basic, gross, rules)
    total_deductions = sum(deductions.values())
    return {
        "basic": basic, "allowances": allowances, "bonus": bonus, "gross": gross,
        "deductions": deductions, "total_deductions": total_deductions,
        "net": gross - total_deductions,
    }


# ---------- Display and input helpers ----------
def money(amount):
    return f"Rs. {amount:,.2f}"


def print_breakdown(emp_id, employee):
    r = calculate_salary(employee)
    print(f"\n--- Salary Slip: {employee['name']} ({emp_id}, {employee['department']}) ---")
    print(f"{'EARNINGS':<28}")
    print(f"  {'Basic Salary':<26}{money(r['basic']):>16}")
    for name, amount in r["allowances"].items():
        print(f"  {name:<26}{money(amount):>16}")
    print(f"  {'Bonus':<26}{money(r['bonus']):>16}")
    print(f"  {'GROSS SALARY':<26}{money(r['gross']):>16}")
    print(f"{'DEDUCTIONS':<28}")
    for name, amount in r["deductions"].items():
        print(f"  {name:<26}{money(amount):>16}")
    print(f"  {'TOTAL DEDUCTIONS':<26}{money(r['total_deductions']):>16}")
    print(f"  {'NET SALARY':<26}{money(r['net']):>16}")


def read_number(prompt, allow_zero=True):
    """Read a non-negative number. Returns None if invalid."""
    raw = input(prompt).strip()
    try:
        value = float(raw)
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None
    if value < 0 or (value == 0 and not allow_zero):
        print("Invalid input. The value must be " + ("positive." if not allow_zero else "zero or more."))
        return None
    return value


# ---------- Menu actions ----------
def view_employees():
    print(f"\n{'ID':<7}{'Name':<16}{'Department':<13}{'Basic':>12}{'Bonus':>10}")
    print("-" * 58)
    for emp_id, e in employees.items():
        print(f"{emp_id:<7}{e['name']:<16}{e['department']:<13}{e['basic']:>12,.0f}{e['bonus']:>10,.0f}")


def salary_for_employee():
    emp_id = input("Enter employee ID (e.g. E101): ").strip().upper()
    if emp_id not in employees:
        print("Employee not found.")
        return
    print_breakdown(emp_id, employees[emp_id])


def salary_summary():
    print(f"\n{'ID':<7}{'Name':<16}{'Gross':>14}{'Deductions':>14}{'Net':>14}")
    print("-" * 65)
    for emp_id, e in employees.items():
        r = calculate_salary(e)
        print(f"{emp_id:<7}{e['name']:<16}{r['gross']:>14,.2f}{r['total_deductions']:>14,.2f}{r['net']:>14,.2f}")


def add_employee():
    emp_id = input("Enter new employee ID: ").strip().upper()
    if not emp_id:
        print("ID cannot be empty.")
        return
    if emp_id in employees:
        print("Duplicate ID: that employee already exists.")
        return
    name = input("Enter name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return
    department = input("Enter department: ").strip() or "General"
    basic = read_number("Enter basic salary: ", allow_zero=False)
    if basic is None:
        return
    bonus = read_number("Enter bonus (0 if none): ")
    if bonus is None:
        return
    employees[emp_id] = {"name": name, "department": department, "basic": basic, "bonus": bonus}
    print(f"Employee {name} added.")


def show_rules():
    print("\nCurrent salary rules:")
    for key, value in SALARY_RULES.items():
        if key != "tax_slabs":
            print(f"  {key:<28}: {value}")
    print("  tax_slabs (gross up to -> tax %):")
    for limit, rate in SALARY_RULES["tax_slabs"]:
        label = "above" if limit == float("inf") else f"{limit:,.0f}"
        print(f"      {label:>10} -> {rate}%")


def change_rule():
    editable = [k for k in SALARY_RULES if k != "tax_slabs"]
    show_rules()
    key = input("\nEnter rule name to change: ").strip()
    if key not in editable:
        print("Unknown rule name.")
        return
    value = read_number(f"Enter new value for {key}: ")
    if value is not None:
        SALARY_RULES[key] = value
        print(f"{key} updated to {value}. All calculations now use the new rule.")


MENU = """
====== EMPLOYEE SALARY CALCULATOR ======
1. View employees
2. Salary breakdown for an employee
3. Salary summary of all employees
4. Add employee
5. View salary rules
6. Change a salary rule
7. Exit
========================================
"""
ACTIONS = {"1": view_employees, "2": salary_for_employee, "3": salary_summary,
           "4": add_employee, "5": show_rules, "6": change_rule}


def main():
    while True:
        print(MENU)
        choice = input("Choose an option (1-7): ").strip()
        if choice == "7":
            print("Goodbye!")
            break
        action = ACTIONS.get(choice)
        if action:
            action()
        else:
            print("Invalid choice. Please enter a number from 1 to 7.")


if __name__ == "__main__":
    main()
    