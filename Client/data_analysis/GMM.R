AQ=read.csv("gmmdata.csv")

library(lmerTest)

n.groups <- 3 # number of groups
n.repeats <- 26 # samples per group
groups <- rep(1:n.groups, c(26,26,27))

typeof(groups)
groups

res = lmer(finalGoalAchievementWithoutGoalChange ~ milestoneAchievement+motivationBeforeDuringChange+milestoneAdherence+condition+agreementPercentage+futureWork+priorEfficacy+postEfficacy+efficacyChange+education+fakeNatural+machineHuman+consciousUnconscious+artificialLifelike+rigidElegant+deadAlive+stagnantLively+mechanicalOrganic+inertInteractive+apatheticResponsive+dislikeLike+unfriendlyFriendly+unkindKind+unpleasantPleasant+awfulNice+incompetentCompetent+ignorantKnowledgeable+irresponsibleResponsible+unintelligentIntelligent+foolishSensible+anxiousRelaxedBefore+agitatedCalmBefore+quiescentSurprisedBefore+anxiousRelaxedAfter+agitatedCalmAfter+quiescentSurprisedAfter+anxiousRelaxedChange+agitatedCalmChange+quiescentSurprisedChange+typeOfRelationship+usefulOrNotDiabetes+usefulOrNotObesity+convenience+preference+motivationBefore+motivation+motivationAfter+motivationBeforeDuringChange+motivationDuringAfterChange+engagement+autonomy+positiveNegative+similarSystem+duration+numberOfSessions+understandingDiabetes+(1+firstTime+gender+familyHistoryDiabetes+age+diabetes|groups),
           REML = TRUE,
           data = AQ)
summary(res)