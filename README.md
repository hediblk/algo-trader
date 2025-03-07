# Trading bot using machine learning classifiers
- This project is a trading bot that uses machine learning classifiers to suggest long entry points. The bot uses the historical data of a stock to train the classifiers agaisnt a predetermined strategy based on technical analysis.
- Currently, a random forest classifier is used to predict long entry points based on a 10 year long dataset of AAPL stock. The strategy is based on RSI and EMAs.

# Next steps
- Implement a backtesting function to evaluate the performance of the bot on unseen data + plot the results.
- Optimize the hyperparameters of the current classifier using a grid search.
- Explore using XGbost and/or other technical analysis indicators to be added to the strategy.
- Implement a short entry point strategy.