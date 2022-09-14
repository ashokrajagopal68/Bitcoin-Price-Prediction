# Bitcoin-Price-Prediction
Attempt to predict the highly volatile Bitcoin prices.

![image](https://user-images.githubusercontent.com/32412569/166312336-fef8184a-6cc1-4bf3-9250-1d830da6c370.png)



Bitcoin (₿) is a decentralized digital currency, without a central bank or single administrator, that can be sent from user to user on the peer-to-peer bitcoin network without the need for intermediaries. Transactions are verified by network nodes through cryptography and recorded in a public distributed ledger called a blockchain. The cryptocurrency was invented in 2008 by an unknown person or group of people using the name Satoshi Nakamoto. The currency began use in 2009 when its implementation was released as open-source software.

Bitcoin has also fueled a rise of plethora of other cryptocurrencies, but Bitcoin still remains the king of them all. Bitcoin has the highest Market Capitalization of any cryptocurrency. Since Bitcoin and other cryptocurrencies are actively traded 24/7 and as Bitcoin remains as the most dominant of all the cryptocurrencies, the price of other crytos are mostly dictated with according to the price action of Bitcoin. So Bitcoin's Price prediction can be a game changer for crypto enthusiastic traders accross the globe.

The Historic market data, which is a time series data of 1 day(1D) time frame is used for this project. From the historic price action we can see that Bitcoin is highly volatile compared to conventional stocks. Also because Cryptocurrencies are still an emerging asset class, the historic market data is limited compared to conventional stocks. 

The Prediction is done using two strategies, firstly using only the Close price. The model is trained on past 75 days of Close price as input and the next day Close price as Output. So the idea is if we provide the trained model with the past 75 days Close Price, the model will predict the next days Closing Price. Same strategy is used to predict the next 5 days price for BTC and a webapp is hosted in the below site using Streamlit.

https://ashokrajagopal68-bitcoin-price-prediction-final-n24egq.streamlitapp.com/

Also another strategy is considering various other indicators capturing market sentiment and On-chain metrics of the past 75 days to predict the next days Close price. Eventhough we are able to provide the model with useful information that could help prediction, Since the On-chain metrics and Fear and Greed indices are lagging indicators, the prediction will only be possible for the following day.

![image](https://user-images.githubusercontent.com/32412569/166311332-d8d21c62-03f6-4a89-b8bd-7af729948020.png)
