"""Module that contains common enums."""
from enum import Enum


class BackgroundColor(Enum):
    """Background color enum."""
    BLUE = "Blue"
    RED = "Red"
    GREEN = "Green"
    CYAN = "Cyan"
    YELLOW = "Yellow"
    ORANGE = "Orange"
    PURPLE = "Purple"


class Priority(Enum):
    """Priority enum."""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class Category(Enum):
    """Category enum."""
    WORK = "Work"
    PERSONAL = "Personal"
    STUDY = "Study"
    HEALTH = "Health"
    HOBBY = "Hobby"
    OTHER = "Other"


class BudgetCategory(Enum):
    """Budget category enum."""
    SALARY = "Salary"
    FREELANCE = "Freelance"
    INVESTMENTS = "Investments"
    OTHER_INCOME = "Other Income"
    FOOD = "Food"
    TRANSPORT = "Transport"
    ENTERTAINMENT = "Entertainment"
    UTILITIES = "Utilities"
    SHOPPING = "Shopping"
    HEALTH = "Health"
    OTHER = "Other"


class TransactionType(Enum):
    """Transaction type enum."""
    INCOME = "Income"
    EXPENSE = "Expense"


class Frequency(Enum):
    """Frequency enum."""
    DAILY = "Daily"
    WEEKLY = "Weekly"
    MONTHLY = "Monthly"
