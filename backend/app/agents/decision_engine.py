from decimal import Decimal
from datetime import date
def priority(balance:Decimal, due_date:date|None)->tuple[int,str]:
    overdue=max(0,(date.today()-(due_date or date.today())).days)
    score=min(100,int(balance/Decimal("50"))+overdue*2)
    return score, f"₹{balance:.0f} outstanding"+(f" · {overdue} days overdue" if overdue else " · follow up today")
