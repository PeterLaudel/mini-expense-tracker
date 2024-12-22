from dataclasses import dataclass
from datetime import datetime


@dataclass
class Expense:
    date: datetime
    category: str
    amount: float
    description: str
