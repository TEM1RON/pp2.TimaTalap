from datetime import datetime

date1 = datetime(2025, 10, 1)
date2 = datetime(2025, 10, 5)

difference = date2 - date1

seconds = difference.total_seconds()

print("Difference in seconds:", seconds)