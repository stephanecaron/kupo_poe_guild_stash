import matplotlib.pyplot as plt
import pandas as pd
from mysql_db import sqlOperations, sqlPoolOpen


connection = sqlPoolOpen.get_connection()
cursor = connection.cursor()
## get inventory_history from mySQL
data = sqlOperations.get_inventory_history(cursor)
df = pd.DataFrame(data, columns=['date','league','stash','item_name','quantity'] )
df['date'] = pd.to_datetime(df['date'])

alteration_orb_data = df[df['item_name'] == 'Portal Scroll']
daily_sum = alteration_orb_data.groupby(df['date'].dt.strftime('%Y-%m-%d %H')).agg({'quantity': 'sum'}).reset_index()

plt.figure(figsize=(10, 6))
plt.plot(daily_sum['date'], daily_sum['quantity'], marker='o', linestyle='-', color='green', label='Portal Scroll')
plt.title('Trendline of Sum of Quantity for "Portal Scroll" Over Time')
plt.xlabel('Date and Hour')
plt.ylabel('Sum of Quantity')
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()