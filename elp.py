import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from mysql_db import sqlOperations, sqlPoolOpen


connection = sqlPoolOpen.get_connection()
cursor = connection.cursor()
data = sqlOperations.get_inventory_history(cursor)
df = pd.DataFrame(data, columns=['date','league','stash','item_name','quantity'] )
df['date'] = pd.to_datetime(df['date'])

seeking = 'orb of Alteration' #input('Please enter the name of the item you\'re looking for: ')

currency_data = df[df['stash'].str.contains('Currency', case=False, na=False) & df['item_name'].str.contains('Orb of Alteration', case=False, na=False)]


daily_sum = currency_data.groupby(['date', 'item_name']).agg({'quantity': 'sum'}).reset_index()

daily_sum_pivot = daily_sum.pivot(index='date', columns='item_name', values='quantity').reset_index()
daily_sum_pivot = daily_sum_pivot.fillna(0)
plt.figure(figsize=(4, 3))

for currency in daily_sum_pivot.columns[1:]:
    plt.plot(
        daily_sum_pivot['date'],
        daily_sum_pivot[currency],
        linestyle='-',     
        linewidth=2,
        label=currency,
        color='orange',
        alpha=1
    )

plt.title(f'Trend over time', color='white')
plt.yticks([0, max(daily_sum_pivot[currency])], color='white')
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %d, %Y'))
plt.xticks([min(daily_sum_pivot['date']),max(daily_sum_pivot['date'])], color='white')
plt.grid(False)
plt.legend().set_visible(False)
plt.tight_layout()
plt.savefig('currency_plot.png', transparent=True, bbox_inches='tight', pad_inches=0)
plt.close()