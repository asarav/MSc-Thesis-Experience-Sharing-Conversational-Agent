import statsmodels.api as sm
import statsmodels.formula.api as smf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
'''
AQ = pd.read_csv('Beijing.csv')#read data
dic = {1: "Winter",
       2: "Winter",
       3: "Spring",
       4: "Spring",
       5: "Spring",
       6: "Summer",
       7: "Summer",
       8: "Summer",
       9: "Fall",
       10: "Fall",
       11: "Fall",
       12: "Winter"}
AQ['season'] = AQ['month'].map(dic)
AQ = AQ.dropna()
AQ = AQ[AQ['pm2.5'] > 0] #remove unresonable response values
AQ['pm25_log'] = np.log(AQ['pm2.5']) #do the log transformation on the response variable
# remove the outliers
AQ_cv = AQ[AQ['cbwd'] == 'cv']
AQ_cv = AQ_cv[(AQ_cv['pm25_log'] > 2.2) & (AQ_cv['pm25_log'] < 6.8)]
AQ_NE = AQ[AQ['cbwd'] == 'NE']
AQ_NE = AQ_NE[(AQ_NE['pm25_log'] > 0.5)]
AQ_NW = AQ[AQ['cbwd'] == 'NW']
AQ_NW = AQ_NW[(AQ_NW['pm25_log'] > 0.5)]
AQ_SE = AQ[AQ['cbwd'] == 'SE']
AQ_SE.sort_values(['pm25_log'], ascending=[False])
AQ_SE = AQ_SE[(AQ_SE['pm25_log'] > 0.5) & (AQ_SE['pm25_log'] < 6.291569)]
AQ_new = pd.concat([AQ_cv, AQ_NE, AQ_NW, AQ_SE])

#fit the model
mixed = smf.mixedlm("pm25_log ~ year+month+day+hour+DEWP+TEMP+PRES+Is+Ir", AQ_new, groups = AQ_new["cbwd"], re_formula="~hour+PRES")
mixed_fit = mixed.fit()
#print the summary
print(mixed_fit.summary())

model = mixed_fit

plt.scatter(AQ_new['pm25_log'] - model.resid, model.resid, alpha = 0.5)
plt.title("Residual vs. Fitted")
plt.xlabel("Fitted Values")
plt.ylabel("Residuals")
plt.show()
'''

data = pd.read_csv("output_files/summary.csv")

modelData = data
#Remove string data
del modelData['id']
del modelData['gender']
del modelData['countryOfOrigin']
modelData['finalGoalAchievement'] = modelData['finalGoalAchievement'].astype(int)
modelData['milestoneAchievement'] = modelData['milestoneAchievement'].astype(int)
modelData['futureWork'] = modelData['futureWork'].astype(int)
modelData['finalGoalAchievementWithoutGoalChange'] = modelData['finalGoalAchievementWithoutGoalChange'].astype(int)

modelData.info()

dependentVariable = "finalGoalAchievement"

mixed = smf.mixedlm(dependentVariable + " ~"
                    " milestoneAchievement+"
                    "age+"
                    "motivationBeforeDuringChange+"
                    "milestoneAdherence+"
                    "condition+"
                    "agreementPercentage+"
                    "futureWork+"
                    "priorEfficacy+"
                    "postEfficacy+"
                    "efficacyChange+"
                    "education+"
                    "fakeNatural+"
                    "machineHuman+"
                    "consciousUnconscious+"
                    "artificialLifelike+"
                    "rigidElegant+"
                    "deadAlive+"
                    "stagnantLively+"
                    "mechanicalOrganic+"
                    "inertInteractive+"
                    "apatheticResponsive+"
                    "dislikeLike+"
                    "unfriendlyFriendly+"
                    "unkindKind+"
                    "unpleasantPleasant+"
                    "awfulNice+"
                    "incompetentCompetent+"
                    "ignorantKnowledgeable+"
                    "irresponsibleResponsible+"
                    "unintelligentIntelligent+"
                    "foolishSensible+"
                    "anxiousRelaxedBefore+"
                    "agitatedCalmBefore+"
                    "quiescentSurprisedBefore+"
                    "anxiousRelaxedAfter+"
                    "agitatedCalmAfter+"
                    "quiescentSurprisedAfter+"
                    "anxiousRelaxedChange+"
                    "agitatedCalmChange+"
                    "quiescentSurprisedChange+"
                    "typeOfRelationship+"
                    "usefulOrNotDiabetes+"
                    "usefulOrNotObesity+"
                    "convenience+"
                    "preference+"
                    "motivationBefore+"
                    "motivation+"
                    "motivationAfter+"
                    "motivationBeforeDuringChange+"
                    "motivationDuringAfterChange+"
                    "engagement+"
                    "autonomy+"
                    "positiveNegative+"
                    "diabetes+"
                    "firstTime+"
                    "familyHistoryDiabetes+"
                    "similarSystem+"
                    "duration+"
                    "numberOfSessions+"
                    "understandingDiabetes", modelData, groups = modelData["condition"])
mixed_fit = mixed.fit()
#print the summary
print(mixed_fit.summary())

model = mixed_fit

plt.scatter(data[dependentVariable] - model.resid, model.resid, alpha = 0.5)
plt.title("Residual vs. Fitted")
plt.xlabel("Fitted Values")
plt.ylabel("Residuals")
plt.show()