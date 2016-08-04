n this project you will transform your regression learner into a stock trading strategy. You should train a learner to predict the change in price of a stock over the next five trading days (one week). You will use data from Dec 31 2007 to 2009 to train your prediction model, then you will test it from Dec 31 2009 to 2011.

Now, just predicting the change in price isn't enough, you need to also code a policy that uses the forecaster you built to buy or sell shares. Your policy should buy when it thinks the price will go up, and short when it thinks the price will go down. You can then feed those buy and sell orders into your market simulator to backtest the strategy. For ease of comparison between strategies, please observe these rules:

Starting cash is $10,000.
Allowable positions are: 100 shares long, 100 shares short, 0 shares.
There is no limit on leverage.
Finding features, a learner, and a policy that all work together to provide a reliably winning strategy with live stock data is HARD! It is possible, and people have done it, but we can't reasonably expect you to be successful at it in this short class. Accordingly, we want you to work with some easy data first, namely we will provide you with sinusoidal historical price data. Once you've got something that works with that, you can try your learner on real stock data.
