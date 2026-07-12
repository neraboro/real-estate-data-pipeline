import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
import seaborn as sns

conn = psycopg2.connect(
    host= "localhost",
    database= "cian_database",
    user= "postgres",
    password= "1234",
    port= "5432")

df = pd.read_sql_query('SELECT * FROM cian_table', conn)
print(f'Информация о ценах за метр на 1-комнатную новостройку: \n{df['price_per_meter'].describe().round(2)}')
fig,axes = plt.subplots(2,2,figsize=(10,8))
axes[0,0].boxplot(df['price_per_meter'])
axes[0,0].set_title('Поиск аномалий среди цен на метр')
axes[0,1].scatter(df['square_meters'],df['price'],alpha=0.7,linestyle='--')
axes[0,1].set_title('Корреляция цены и квадратных метров')
axes[0,1].set_ylabel('Цена (млн)')
axes[0,1].set_xlabel('м²')
axes[1,0].bar(df['minutes_to_subway'],df['price_per_meter'])
axes[1,0].set_title('Корреляция цены на метр и минут до метро')
axes[1,0].set_ylabel('Цена на м²')
axes[1,0].set_xlabel('Минуты до метро')
corr = df[['price',
           'square_meters',
           'price_per_meter',
           'minutes_to_subway',
           'ceiling_height']].corr()

sns.heatmap(corr,
            annot=True,
            cmap='coolwarm',
            fmt='.2f',
            linewidths=0.5,
            ax=axes[1,1])

axes[1,1].set_title('Корреляционная матрица признаков')
fig.tight_layout()
plt.show()
conn.close()
