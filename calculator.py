# encoding: utf-8

# (c) 2014-2023 Open Risk, all rights reserved
#
# FuriousBanker is licensed under the MIT license a copy of which is included
# in the source distribution of FuriousBanker. This is notwithstanding any licenses of
# third-party software included in this distribution. You may not use this file except in
# compliance with the License.
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions and
# limitations under the License.


import random

import concentrationMetrics as cm


# initialize portfolio to random values
def init(size):
    # print('init')
    portfolio = {}

    large_i = int(10 * random.random())
    medium_i = int(10 * random.random())

    for i in range(size):
        el = max(0.005, random.gauss(0.05, 0.05))
        s = min(1.0, max(0.0, el * (1 + random.random())))
        exp = min(0.3, max(0.1, 0.3 * random.random()))
        if i == medium_i:
            exp = 0.8
        if i == large_i:
            exp = 1.0
        portfolio[i] = {"index": i, "el": round(el, 2), "s": round(s, 2), "exp": round(exp, 2)}

    return portfolio


# create random new loan
def newloan():
    # print('newloan')
    el = max(0.005, random.gauss(0.05, 0.05))
    s = min(1.0, max(0.0, el * (1 + random.random())))
    exp = min(1.0, max(0.1, random.random()))
    return [round(el, 2), round(s, 2), round(exp, 2)]


# calculate profitability of portfolio
def profit(portfolio):
    # print('profit')
    sum = 0
    total = exposure(portfolio)
    for i in range(len(portfolio)):
        loan = portfolio[i]
        sum += (loan['s'] - loan['el']) * loan['exp']
    return 100 * sum / total


# calculate total exposure
def exposure(portfolio):
    # print('exp')
    total = 0
    for i in range(len(portfolio)):
        loan = portfolio[i]
        total += loan['exp']
    return round(total, 2)


# calculate concentration index using concentrationMetrics
def basic_hhi(portfolio):
    Index = cm.Index()
    hhi = Index.hhi(portfolio)
    return hhi


# calculate a risk weighted concentration index
def risky_hhi(portfolio):
    hhi = 0
    average = 0
    total = exposure(portfolio)
    for i in range(len(portfolio)):
        loan = portfolio[i]
        average += loan['el'] * loan['exp']
        hhi += loan['el'] * loan['exp'] * loan['exp'] / total / total
    average = average / total
    result = round(100 * hhi / average, 0)
    return round(result, 0)


# calculate game score index
def score(portfolio):
    risk = risky_hhi(portfolio)
    ret = profit(portfolio)
    return round(1000 * ret / risk, 1)
