from collections import Counter

import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.power import FTestAnovaPower
from pingouin import power_anova
import statsmodels.stats.multicomp as mc
import scikit_posthocs as sp


#pd.read_csv("output_files/summary.csv")
data = pd.read_csv("output_files/summary.csv")
data1 = pd.read_csv("output_files/summary_1.csv")
data2 = pd.read_csv("output_files/summary_2.csv")
data3 = pd.read_csv("output_files/summary_3.csv")
#data = pd.concat([data2, data3])
#powerAnalysis = FTestAnovaPower()

print(data['condition'].unique())

def anova_table(aov):
    aov['mean_sq'] = aov[:]['sum_sq']/aov[:]['df']

    aov['eta_sq'] = aov[:-1]['sum_sq']/sum(aov['sum_sq'])

    aov['omega_sq'] = (aov[:-1]['sum_sq']-(aov[:-1]['df']*aov['mean_sq'][-1]))/(sum(aov['sum_sq'])+aov['mean_sq'][-1])

    cols = ['sum_sq', 'df', 'mean_sq', 'F', 'PR(>F)', 'eta_sq', 'omega_sq']
    aov = aov[cols]
    return aov

def calculateStats(item):
    fstat = 0
    #First generate residuals to feed in for shapiro and levene
    modelData = data[['condition', item]].copy()
    modelData['condition'] = modelData['condition'].map(str)
    model = ols(item + ' ~ C(condition)', data=modelData).fit()
    #First Shapiro for Conditions: 1, 2, and 3
    assumption1 = False
    stat1, p1 = stats.shapiro(model.resid)
    if p1 >= 0.05:
        assumption1 = True
    print("Shapiro: %.8f" % p1)
    #Then Levene for Conditions 1, 2, and 3
    stat, p = stats.levene(data2[item], data3[item])
    if p >= 0.05:
        lev = True
    print('Levene: %.6f' % p)
    print("Anova")
    fstat, p = stats.f_oneway(data2[item], data3[item])
    print(fstat, p)
    if p < 0.05:
        print("Reject NULL Hypothesis (YAY)")
    else:
        print("CAN'T reject H0. (OH NO)")
    fstat, p = stats.kruskal(data2[item], data3[item])
    print("Kruskal")
    #Kruskal if no Anova
    print(fstat, p)
    if p < 0.05:
        print("Reject NULL Hypothesis (YAY)")
    else:
        print("CAN'T reject H0. (OH NO)")
    #Use f statistic to generate power analysis
    aov_table = sm.stats.anova_lm(model, typ=2)
    #print(aov_table)
    sum_sq = aov_table["sum_sq"].tolist()
    effect_size = (sum_sq[0] / (sum_sq[0] + sum_sq[1]))
    print("Power")
    print(effect_size)

    print('power: %.4f' % power_anova(eta=effect_size, k=2, n=53))
    print('n: %.4f' % power_anova(eta=effect_size, k=2, power=0.80))
    #print('alpha: %.4f' % power_anova(eta=effect_size, n=79, k=3, power=0.80, alpha=None))

def frequency(item):
    items = [data1, data2, data3]
    for item in items:
        print("ITEM")
        words = item["futureWork"].tolist()

        # print(mean(words), stdev(words), median(words))
        print(Counter(words).keys())  # equals to list(set(words))
        print(Counter(words).values())  # counts the elements' frequency

def fisherExact(contingency):
    print(stats.fisher_exact(contingency))

def chiSquare3(contingency):
    print(stats.chi2_contingency(contingency))

def tukey(item):
    modelData = data[['condition', item]].copy()
    modelData['condition'] = modelData['condition'].map(str)

    comp = mc.MultiComparison(modelData[item], modelData['condition'])
    post_hoc_res = comp.tukeyhsd()
    post_hoc_res.summary()
    print(post_hoc_res.summary())

def bonferroni(item):
    modelData = data[['condition', item]].copy()
    modelData['condition'] = modelData['condition'].map(str)

    comp = mc.MultiComparison(modelData[item], modelData['condition'])
    tbl, a1, a2 = comp.allpairtest(stats.ttest_ind, method="bonf")
    print(tbl)

def dunn(item):
    modeldata1 = data1[item].tolist()
    modeldata2 = data2[item].tolist()
    modeldata3 = data3[item].tolist()
    print(sp.posthoc_dunn([modeldata1, modeldata2, modeldata3], p_adjust ='bonferroni'))

#calculateStats("agreementPercentage")
one = [11, 15]
two = [12, 14]
three = [14, 13]
'''
# 1 2
fisherExact([one, two])
# 1 3
fisherExact([one, three])
# 2 3
fisherExact([two, three])
'''

item = "motivationBeforeDuringChange"

#chiSquare3([one, two, three])
print("Tukey")
tukey(item)
print("Bonferroni")
bonferroni(item)
print("DUNN")
dunn(item)

