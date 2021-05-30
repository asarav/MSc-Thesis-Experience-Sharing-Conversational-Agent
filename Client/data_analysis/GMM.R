AQ=read.csv("gmmdata.csv")
library(nlme)

resc=lme(finalGoalAchievementWithoutGoalChange ~ milestoneAchievement+age+motivationBeforeDuringChange+milestoneAdherence+condition+agreementPercentage+futureWork+priorEfficacy+postEfficacy+efficacyChange+education+fakeNatural+machineHuman+consciousUnconscious+artificialLifelike+rigidElegant+deadAlive+stagnantLively+mechanicalOrganic+inertInteractive+apatheticResponsive+dislikeLike+unfriendlyFriendly+unkindKind+unpleasantPleasant+awfulNice+incompetentCompetent+ignorantKnowledgeable+irresponsibleResponsible+unintelligentIntelligent+foolishSensible+anxiousRelaxedBefore+agitatedCalmBefore+quiescentSurprisedBefore+anxiousRelaxedAfter+agitatedCalmAfter+quiescentSurprisedAfter+anxiousRelaxedChange+agitatedCalmChange+quiescentSurprisedChange+typeOfRelationship+usefulOrNotDiabetes+usefulOrNotObesity+convenience+preference+motivationBefore+motivation+motivationAfter+motivationBeforeDuringChange+motivationDuringAfterChange+engagement+autonomy+positiveNegative+diabetes+firstTime+familyHistoryDiabetes+similarSystem+duration+numberOfSessions+understandingDiabetes,
         method = 'ML', data = AQ)
summary(resc)


library(lme4)

n.groups <- 3 # number of groups
n.repeats <- 26 # samples per group
groups <- rep(1:n.groups, c(26,26,27))

typeof(groups)
groups

res = lmer(finalGoalAchievementWithoutGoalChange ~ milestoneAchievement+age+motivationBeforeDuringChange|groups,
           REML = TRUE,
           data = AQ)
summary(res)