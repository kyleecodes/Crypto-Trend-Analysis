import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('fivethirtyeight')

dec6 = pd.read_csv('data/coinmarketcap_06122017.csv')

market_cap_raw = dec6[['id', 'market_cap_usd']]

market_cap_raw.count()

# Filtering out rows without a market capitalization
cap = market_cap_raw.query('market_cap_usd > 0')

cap.count()

TOP_CAP_TITLE = 'Top 10 market capitalization'
TOP_CAP_YLABEL = '% of total cap'

cap10 = cap[:10].set_index('id')

# Calculating market_cap_perc
cap10 = cap10.assign(market_cap_perc=lambda x: (x.market_cap_usd / cap.market_cap_usd.sum()) * 100)

ax = cap10.market_cap_perc.plot.bar(title=TOP_CAP_TITLE)

# Annotating the y axis with the label defined above
ax.set_ylabel(TOP_CAP_YLABEL);

COLORS = ['orange', 'green', 'orange', 'cyan', 'cyan', 'blue', 'silver', 'orange', 'red', 'green']

# Plotting market_cap_usd as before but adding the colors and scaling the y-axis
ax = cap10.market_cap_usd.plot.bar(title=TOP_CAP_TITLE, logy=True, color=COLORS)

ax.set_ylabel('USD')
ax.set_xlabel('');

# Selecting the id, percent_change_24h and percent_change_7d columns
volatility = dec6[['id', 'percent_change_24h', 'percent_change_7d']]

# Setting the index to 'id' and dropping all NaN rows
volatility = volatility.set_index('id').dropna()

# Sorting the DataFrame by percent_change_24h in ascending order
volatility = volatility.sort_values('percent_change_24h')

volatility.head()

def top10_subplot(volatility_series, title):
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 6))
    
    # Plotting with pandas the barchart for the top 10 losers with the color RED
    ax = volatility_series[:10].plot.bar(color="darkred", ax=axes[0])
    fig.suptitle(title)
    ax.set_ylabel('% change')
    
    # Plotting top 10 winners and in darkblue
    ax = volatility_series[-10:].plot.bar(color="darkblue", ax=axes[1])
    return fig, ax


DTITLE = "24 hours top losers and winners"

fig, ax = top10_subplot(volatility.percent_change_24h, DTITLE)

volatility7d = volatility.sort_values("percent_change_7d")

WTITLE = "Weekly top losers and winners"

fig, ax = top10_subplot(volatility7d.percent_change_7d, WTITLE);

# Selecting everything bigger than 10 billion
largecaps = cap.query("market_cap_usd > 1E+10")

largecaps

# Making a nice function for counting different marketcaps from the
# "cap" DataFrame. 
def capcount(query_string):
    return cap.query(query_string).count().id

# Crypto labels
LABELS = ["biggish", "micro", "nano"]

biggish = capcount("market_cap_usd > 3E+8")
micro = capcount("market_cap_usd >= 5E+7 & market_cap_usd < 3E+8")
nano = capcount("market_cap_usd < 5E+7")

values = [biggish, micro, nano]

plt.bar(range(len(values)), values, tick_label=LABELS)

plt.show()
