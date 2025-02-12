from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def calculate_future_date(current_date, interval):
    # Split the interval to get the number and the unit
    amount, unit = interval.split()
    amount = int(amount)
    
    if unit.endswith('s'):  # Make unit singular if it's plural
        unit = unit[:-1]
    
    # Calculate the future date based on the unit
    if unit == 'day':
        future_date = current_date + timedelta(days=amount)
    elif unit == 'week':
        future_date = current_date + timedelta(weeks=amount)
    elif unit == 'month':
        future_date = current_date + relativedelta(months=amount)
    else:
        raise ValueError("Invalid time interval unit. Use 'day', 'week', or 'month'.")
    
    # return future_date.date()  # Return only the date part
    return future_date.strftime("%d-%m-%Y")


# Example usage
current_date = datetime.now()
interval = "3 weeks"

future_date = calculate_future_date(current_date, interval)
print(f"Current Date: {current_date.date()}")
print(f"Future Date: {future_date}")
