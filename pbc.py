"""
Contains tools to transform a set of numerical data into
annotated Process Behavior Charts as defined by Donald J. Wheeler
in his book Understanding Variation: The Key to Managing Chaos

Author: Bob Hannon < bob@bobhannon.com>

License: MIT
"""

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

URL_CONSTANT = 3.27
NPL_CONSTANT = 2.66


def get_limits(s, less_than_zero=False):
    """ for a given Series, return DataFrame containing
    X, XBar, mR, mRBar, URL, UNPL, & LNPL"""
    df = pd.DataFrame(s)
    XBar = s.mean()
    df['XBar'] = XBar
    df['mR'] = abs(s.diff())
    mRBar = abs(s.diff()).mean()
    df['mRBar'] = mRBar
    df['URL'] = mRBar * URL_CONSTANT
    df['UNPL'] = XBar + (mRBar * NPL_CONSTANT)
    lnpl = XBar - (mRBar * NPL_CONSTANT)
    if not less_than_zero:
        df['LNPL'] = lnpl if lnpl > 0 else 0
    else:
        df['LNPL'] = lnpl
    return df


def get_charts(s):
    """
    :param s: Series or List of numbers :
    :return: figure containing X-mR charts and Histogram
    """
    if type(s) is not 'pandas.core.series.Series':
        try:
            s = pd.Series(s)
        except:
            raise TypeError('Must be numerical data')

    s.name = s.name if s.name is not None else 'X'
    idx = s.index if s.index is not None else range(0, len(s))

    df = get_limits(s)
    plt.style.use('ggplot')
    figure = plt.figure(0, figsize=(15, 8))
    ax1 = plt.subplot2grid((2, 3), (0, 0), colspan=2)   # X plot
    ax2 = plt.subplot2grid((2, 3), (1, 0), colspan=2)   # mR plot
    ax3 = plt.subplot2grid((2, 3), (0, 2), rowspan=2)   # hist plot

    # plot X chart
    ax1.plot(idx, df[s.name], label=s.name, marker='o', ms=3)     # X vals
    ax1.plot(idx, df['XBar'], color="#245f9c", label='_nolegend_', linewidth=1.5)       # XBar
    ax1.plot(idx, df['UNPL'], '--', color="#245f9c", linewidth=1, label='_nolegend_')
    if df['LNPL'][0] != 0:
        ax1.plot(idx, df['LNPL'], '--', color="#245f9c", linewidth=1, label='_nolegend_')
        ax1.annotate('  Lower Limit:\n  ' + str(df['LNPL'][0].round(2)), xy=(idx[-1] + 4, df['LNPL'][0]))
    ax1.annotate('  Avg:\n  ' + str(df['XBar'][0].round(2)), xy=(idx[-1]+4,df['XBar'][0]))
    ax1.annotate('  Upper Limit:\n  ' + str(df['UNPL'][0].round(2)), xy=(idx[-1]+4,df['UNPL'][0]))

    ax1.set_title(s.name)
    ax1.legend()

    # plot mR chart
    ax2.plot(idx, df['mR'], label='mR', marker='o', ms=3)
    ax2.plot(idx, df['mRBar'], label='_nolegend_')
    ax2.plot(idx, df['URL'], '--', color="#245f9c", linewidth=1, label='_nolegend_')
    ax2.annotate('  Avg Range:\n  ' + str(df['mRBar'][0].round(2)), xy=(idx[-1] + 4, df['mRBar'][0]))
    ax2.annotate('  Upper Range Limit:\n  ' + str(df['URL'][0].round(2)), xy=(idx[-1] + 4, df['URL'][0]))
    ax2.set_title(s.name + ' - Moving Range (mR)')
    ax2.legend()


    # plot historgram
    ax3.hist(df[s.name], rwidth=0.95, color='#245f9c')
    ax3.set_title(s.name + ' Distribution')

    # adjust spacing and axis label rotation
    plt.subplots_adjust(wspace=0.75, hspace=0.5)
    for ax in figure.axes:
        plt.sca(ax)
        plt.xticks(rotation=25)

    return figure




