import cloudscraper
import requests

# Initialize cloudscraper

scraper = cloudscraper.create_scraper()

# URL to fetch the data
def stats(ca):
    url1 = "https://gmgn.ai/defi/quotation/v1/smartmoney/sol/walletNew/"+ca+"?period=30d"
    url2 = "https://gmgn.ai/api/v1/wallet_holdings/sol/"+ca+"?orderby=last_active_timestamp&direction=desc&showsmall=true&sellout=true&limit=50&tx30d=true"

    def dot(pnl):   return "🟢" if float(pnl) > 0 else "🔴"

    # Fetch the data
    response = scraper.get(url1)
    sol = float(requests.get('https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd').json()['solana']['usd'])

    if response.status_code == 200:
        # Extract data
        data = response.json()
        balance = f"{float(data.get('data', {}).get('balance', "0")):.2f}"
        buy = data.get('data', {}).get('buy_30d', 0)
        sell = data.get('data', {}).get('sell_30d', 0)
        winrate = f"{data.get('data', {}).get('winrate', 0)*100:.2f}"
        token_avg_cost = f"{data.get('data', {}).get('token_avg_cost', 0)/sol:.2f}"
        pnl_30d = f"{data.get('data', {}).get('pnl_30d', 0)*100:.2f}"
        realized_profit_30d = f"{data.get('data', {}).get('realized_profit_30d', 0)/sol:.2f}"
        loss = data.get('data', {}).get('pnl_lt_minus_dot5_num', 0)
        gain = int(data.get('data', {}).get('pnl_2x_5x_num', 0))+int(data.get('data', {}).get('pnl_gt_5x_num', 0))
        
        response2 = scraper.get(url2)
        if response2.status_code == 200:
            trades = response2.json().get('data', {}).get('holdings', [])
            
            # Format and save the output as desired
            
            formatted_output = f"""📊 Stats for last 30 days 📊
    💰 Balance : {balance} SOL
    🏆 Winrate : {winrate}%
    📈 ROI : {pnl_30d}%
    💵 Profit : {realized_profit_30d} SOL
    🛒 Avg buys : {token_avg_cost} SOL

    🟢 Buys : {buy} | 🔴 Sells : {sell}

    📉 (Loss > 50%) : {loss}
    🚀 (Gain 2x+) : {gain}

    📌 Last 5 trades :
    {dot(trades[0]['total_profit_pnl'])} {trades[0]['token']['symbol'].upper()} - {f"{float(trades[0]['total_profit_pnl']):.2f}"}x | {f"{float(trades[0]['total_profit'])/sol:.2f}"} Sol earned
    {dot(trades[1]['total_profit_pnl'])} {trades[1]['token']['symbol'].upper()} - {f"{float(trades[1]['total_profit_pnl']):.2f}"}x | {f"{float(trades[1]['total_profit'])/sol:.2f}"} Sol earned
    {dot(trades[2]['total_profit_pnl'])} {trades[2]['token']['symbol'].upper()} - {f"{float(trades[2]['total_profit_pnl']):.2f}"}x | {f"{float(trades[2]['total_profit'])/sol:.2f}"} Sol earned
    {dot(trades[3]['total_profit_pnl'])} {trades[3]['token']['symbol'].upper()} - {f"{float(trades[3]['total_profit_pnl']):.2f}"}x | {f"{float(trades[3]['total_profit'])/sol:.2f}"} Sol earned
    {dot(trades[4]['total_profit_pnl'])} {trades[4]['token']['symbol'].upper()} - {f"{float(trades[4]['total_profit_pnl']):.2f}"}x | {f"{float(trades[4]['total_profit'])/sol:.2f}"} Sol earned
        """

            # Save to a text file
            with open("stats.txt", "w", encoding="utf-8") as file:
                file.write(formatted_output)

            print("Data saved to stats.txt")
        else:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

# Example Usage
stats('FYGgfgZFeVxnJKF2RS6MKYHBsUpfJdCwumzkPpxWPM4u')