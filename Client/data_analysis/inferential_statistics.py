import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.power import FTestAnovaPower
from pingouin import power_anova

data = pd.read_csv("output_files/summary.csv")
data1 = pd.read_csv("output_files/summary_1.csv")
data2 = pd.read_csv("output_files/summary_2.csv")
data3 = pd.read_csv("output_files/summary_3.csv")

powerAnalysis = FTestAnovaPower()

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
    print("Shapiro")
    print(p1)
    #Then Levene for Conditions 1, 2, and 3
    if assumption1:
        lev = False
        stat, p = stats.levene([data1[item], data2[item], data3[item]])
        if p >= 0.05:
            lev = True
        print("Levene")
        print(p)
        if lev:
            # Then Anova if Levene is > alpha (0.05)
            print("Anova")
            fstat, p = stats.f_oneway(data1[item], data2[item], data3[item])
            print(fstat, p)
            if p < 0.05:
                print("Reject NULL Hypothesis (YAY)")
            else:
                print("Can't reject H0. (OH NO)")
    else:
        print("Kruskal")
        fstat, p = stats.f_oneway(data1[item], data2[item], data3[item])
        print(fstat, p)
        fstat, p = stats.kruskal(data1[item], data2[item], data3[item])
        #Kruskal if no Anova
        print(fstat, p)
        if p < 0.05:
            print("Reject NULL Hypothesis (YAY)")
        else:
            print("CAN'T reject H0. (OH NO)")
    #Use f statistic to generate power analysis
    aov_table = sm.stats.anova_lm(model, typ=2)
    print(aov_table)
    sum_sq = aov_table["sum_sq"].tolist()
    effect_size = (sum_sq[0] / (sum_sq[0] + sum_sq[1]))
    print("Power")
    print(effect_size)


    #power = powerAnalysis.power(effect_size=effect_size, nobs=79, alpha=0.05, k_groups=3)
    print('power: %.4f' % power_anova(eta=effect_size, k=3, n=79))
    print('n: %.4f' % power_anova(eta=effect_size, k=3, power=0.80))
    #print(power)

    solution = powerAnalysis.solve_power(effect_size=effect_size, nobs=None, alpha=0.05, power=0.8, k_groups=3)
    print(solution)


calculateStats("motivationBeforeDuringChange")