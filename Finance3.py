

'''
Theory: Prices of similar stock will follow each other and are correlated.


Logic:
1. Finding out for which price the stock will go: up , down or stay within bounds within a period of 1 week.
2. Normalise all closing values for all companies.
3. ML: Feed normalised of all closing values as feature sets and step 1 values as labels

What Happens: When 499 of the companies have __ values this specific company will go up.

Problmes With Backtesting:
1. The companies on S&P don't stay the same.

How to practially use results? If [logic] should buy

Notes:
1. Test using differnt date ranges.
'''


#machile learning with compnay data

from collections import Counter
import numpy as np
import pandas as pd
import pickle
from sklearn import svm, cross_validation, neighbors
from sklearn.ensemble import VotingClassifier, RandomForestClassifier

#made decision based on these days
hm_days = 7
counts = []

def process_data_for_labels(ticker):

                                                #removes numbered colums
    df = pd.read_csv('sp500_joined_closes3.csv',index_col = 0)
    tickers = df.columns.values
    df.fillna(0, inplace = True)


    for i in range(1,hm_days+1):
                                                #shifting up getting value in future
        df['{}_{}d'.format(ticker, i)] = (df[ticker].shift(-i) - df[ticker])/ df[ticker]


    df.fillna(0, inplace = True)
    return tickers, df



def buy_sell_hold(*args):
    cols = [c for c in args]
    counts.append(1)
    requirement = 0.02
    for col in cols:
        if col > requirement:
            return 1
        if col < -requirement:
            return -1
    return 0



def extract_featuresets(ticker):
    tickers, df = process_data_for_labels(ticker)
                                        #iterating through df['{}_{}d'.format(ticker, i)]
    df["{}_target".format(ticker)] = list(map(buy_sell_hold, *[df['{}_{}d'.format(ticker, i)]for i in range(1, hm_days+1)]))

    vals = df["{}_target".format(ticker)].values
    str_vals = [str(i) for i in vals]
    strVal = open("strVal.txt","w")
    for x in str_vals:
        strVal.write(str(x).strip()+"\n")

    print("Data spread:", Counter(str_vals))


    #price going from 0 to a number is probablmatic. #nan signifies missing data or invalid output
    df.fillna(0, inplace = True)
    df = df.replace([np.inf, -np.inf], np.nan)
    df.dropna(inplace = True)

    df_vals = df[[ticker for ticker in tickers]].pct_change()
    df_vals = df_vals.replace([np.inf, -np.inf], 0)
    df_vals.fillna(0, inplace = True)

    #feature sets - things that describe it and label - target
    X = df_vals.values
    df_vals = open("dfVals.txt","w")
    for x in X:
        df_vals.write(str(x)+"\n")


    y = df['{}_target'.format(ticker)].values
    #print(df['{}_target'.format(ticker)].head())

    return X, y , df





def do_ml(ticker):
    X,y,df = extract_featuresets(ticker)
    X_train,X_test, y_train, y_test = cross_validation.train_test_split(X,y,test_size=0.15)
    print("Xtrain",X_train)
    xTrainWrite = open("xTrain.txt","w")
    for x in X_train:
        xTrainWrite.write(str(x).strip()+"\n")

    xTestWrite = open("xTest.txt","w")
    for x in X_test:
        xTestWrite.write(str(x).strip()+"\n")
    #clf = neighbors.KNeighborsClassifier()

    clf = VotingClassifier([('lsvc', svm.LinearSVC()),('knn', neighbors.KNeighborsClassifier()),('rfor', RandomForestClassifier())])



    clf.fit(X_train,y_train)
    confidence = clf.score(X_test, y_test)

    print('Accuracy', confidence )
    predictions = clf.predict(X_test)
    print('Predicted spread:',Counter(predictions))
    print(predictions)
    bob = open("predictions.txt","w")
    # for x in predictions:
    #     bob.write(str(x)+"\n")
    return confidence

do_ml("AAPL")
