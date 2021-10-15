# app.py
from flask import Flask, request, render_template
import ccxt
app = Flask(__name__)
# app.debug = True

final_dict = {}
exchanges = ccxt.exchanges
coins = {'Bitcoin': 'BTC/USDT', 'Ethereum':'ETH/USDT'}


@app.route('/exchange', methods=['GET', 'POST'])
def exchange():

    ex1 = request.form.get('exchange1')
    ex2 = request.form.get('exchange2')

    exchange1 = ccxt.__getattribute__(ex1)()
    exchange2 = ccxt.__getattribute__(ex2)()
    coin =request.form.get('coins')


    res_arr_1 = [] 
    try:
        dict_1 = exchange1.fetchTickers(symbols = coin)

        if dict_1[coin].get('open', 0)==0:
            res_arr_1.append('N/A')
        else:
            res_arr_1.append(f"{dict_1[coin]['open']:.2f}")

        if dict_1[coin].get('close', 0)==0:
            res_arr_1.append('N/A')
        else:
            res_arr_1.append(f"{dict_1[coin]['close']:.2f}")
    except:
        res_arr_1.append(f'Exchange Does not support {coin}')
    res_arr_2 = [] 
    try:
        dict_2 = exchange2.fetchTickers(symbols = coin)

        if dict_2[coin].get('open', 0)==0:
            res_arr_2.append('N/A')
        else:
            res_arr_2.append(f"{dict_2[coin]['open']:.2f}")
        if dict_2[coin].get('close', 0)==0:
            res_arr_2.append('N/A')
        else:
            res_arr_2.append(f"{dict_2[coin]['close']:.2f}")
    except:
        res_arr_2.append(f'Exchange Does not support {coin}')

    rec = None
    if res_arr_1[0]!=f'Exchange Does not support {coin}' and res_arr_2[0]!=f'Exchange Does not support {coin}':
        if float(res_arr_1[0])<float(res_arr_2[0]):
            rec = (ex1.upper(), ex2.upper(), res_arr_1[0], res_arr_2[0],  f'{(float(res_arr_2[0])-float(res_arr_1[0])):.2f}')
        else:
            rec = (ex2.upper(), ex1.upper(), res_arr_2[0], res_arr_2[0],  f'{(float(res_arr_1[0])-float(res_arr_2[0])):.2f}')
    return render_template('index.html', mydict=final_dict, exchanges= exchanges, coins = coins,\
                             comparision={ex1.upper():res_arr_1, ex2.upper():res_arr_2},\
                             rec = rec)



@app.route('/')
def index():
    return render_template('index.html', mydict=final_dict, exchanges= exchanges, coins = coins, comparision=None)


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
