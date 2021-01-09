from chatterbot.trainers import ListTrainer
from chatterbot import ChatBot
from chatterbot import comparisons
from chatterbot import response_selection
import management_utils.cosine_similarity as cosine

import spacy


class SearchBasedConversation:
    def __init__(self, conversations, chatbotName):        
        self.nlp = spacy.load('en_core_web_md')
        self.chatbot = ChatBot(chatbotName,
                logic_adapters=[
                    {
                        "import_path": "chatterbot.logic.BestMatch",
                        "statement_comparison_function": comparisons.LevenshteinDistance,
                        "response_selection_method": response_selection.get_first_response
                    }
                ])

        self.conversations = [
            ["How do you treat type 2 diabetes?",
            "When you have type 2 diabetes, you first need to eat a healthy diet, stay physically active and lose any extra weight. If these lifestyle changes cannot control your blood sugar, you also may need to take pills and other injected medication, including insulin.\n"
            + "Eating a healthy diet, being physically active, and losing any extra weight is the first line of therapy. “Diet and exercise“ is the foundation of all diabetes management because it makes your body’s cells respond better to insulin (in other words, it decreases insulin resistance) and lowers blood sugar levels.\n"
            + "If you cannot normalize or control the blood sugars with diet, weight loss and exercise, the next treatment phase is taking medicine either orally or by injection.\n"
            + "Diabetes pills work in different ways – some lower insulin resistance, others slow the digestion of food or increase insulin levels in the blood stream. The non-insulin injected medications for type 2 diabetes have a complicated action but basically lower blood glucose after eating. Insulin therapy simply increases insulin in the circulation.\n"
            + "Don’t be surprised if you have to use multiple medications to control the blood sugar. Multiple medications, also known as combination therapy is common in the treatment of diabetes! If one medication is not enough, your medical provider may give you two or three or more different types of pills. Insulin or other injected medications also may be prescribed. Or, depending on your medical condition, you may be treated only with insulin or injected medication therapy.\n"
            + "Many people with type 2 diabetes have elevated blood fats (high triglycerides and cholesterol) and blood pressure, so you may be given medications for these problems as well."],
            ["Can type 2 diabetes go away? And if my blood sugar becomes normal, do I still have diabetes?",
            "Type 2 diabetes is a genetic condition or pre-disposition that doesn’t change with treatment. But diabetes is defined as an elevated blood sugar.\n"
            + "When your blood sugar is normal with no treatment, then the diabetes is considered to have gone away. However, even when the blood sugars are controlled, because type 2 diabetes is a genetic condition, the predisposition for diabetes always exists. High blood sugars can come back.\n"
            + "If you have type 2 diabetes and the blood sugar is controlled during treatment through diet, exercise and medications, it means that the treatment plan is working. You are getting the good blood sugar because of the treatment, NOT because diabetes predisposition has gone away. You will need to continue your treatment; otherwise your blood sugar will go back up."],
            ["Will I need to take insulin if I have type 2 diabetes?",
            "Historically, 30% or more of people with type 2 diabetes required insulin therapy. However there are many new drugs available that may delay or prevent the need for insulin therapy. It is expected that fewer and fewer individuals will need insulin replacement to control their blood sugars."],
            ["As someone with type 2 diabetes, do I turn into a type 1 diabetic when I take insulin?",
            "Taking insulin does not mean that you have type 1 diabetes. Your type of diabetes is determined by your genetics, not by the type of therapy."],
            ["If I have type 2 diabetes and take insulin, do I have to take it forever?",
            "If you can lose weight, change your diet, increase your activity level, or change your medications you may be able to reduce or stop insulin therapy. Under certain circumstances, you may only need insulin temporarily – such as during pregnancy, acute illness, after surgery or when treated with drugs that increase their body’s resistance to the action of insulin (such as prednisone or steroids). Often the insulin therapy can be stopped after the event or stress is over."],
            ["Will exercise help my diabetes?",
            "Exercise is very beneficial in the management of type 2 diabetes. Always consult with your doctor about exercise guidelines, to exercise safely and reduce risks."],
            ["Should I exercise?",
            "Exercise is very beneficial in the management of type 2 diabetes. Always consult with your doctor about exercise guidelines, to exercise safely and reduce risks."],
            ["If I have type 2 diabetes can I stop taking diabetes medications if I eliminate candy and cookies from my diet?",
            "If you eliminate concentrated sources of carbohydrates (foods that turn into sugar in your blood stream) like candy and cookies, you may be able to reduce or eliminate the need for diabetes medications. Everyone with type 2 diabetes will benefit from an improved diet, but you may still need other interventions, such as increased physical activity, weight loss or medications to keep your blood sugars in the target range. Check with your doctor about any diabetes medication dose adjustments that may be required if you change your diet."],
            ["Do I need to monitor my blood sugar when I have type 2 diabetes?",
            "You may feel fine, but that is no guarantee that your blood sugar levels are in the target range. Remember, diabetic complications do not appear right away. And complications may develop even when the blood sugar is only slightly elevated. Regular blood sugar monitoring can help you keep your blood sugars in control and prevent serious damage to your eyes, kidneys and nerves. If your sugar levels are out of line, consult your doctor."],
            ["Are my children at risk?",
            "Type 2 diabetes is a genetic disease. The risk is highest when multiple family members have diabetes, and if the children also are overweight, sedentary and have the other risk factors for type 2 diabetes. Your child has a 10-15% chance of developing type 2 diabetes when you have type 2 diabetes. And if one identical twin has type 2 diabetes, there is a 75% likelihood of the other twin developing type 2 diabetes also."],
            ["Can type 2 diabetes be prevented?",
            "Although we cannot change your genetic risk for developing type 2 diabetes, we do know that even modest exercise and weight loss can delay or prevent the development of type 2 diabetes."],
            ["What is type 2 diabetes?",
            "Type 2 diabetes is when your body doesn’t use insulin properly. In type 2 diabetes, some people are insulin resistant, meaning that their body produces a lot of insulin but can’t use it effectively. Some people with type 2 diabetes don’t produce enough insulin. Type 2 is different from type 1 diabetes because in type 1, your body doesn’t produce any insulin at all.\n"
            + "Whether you’re insulin resistant or have too little insulin, the end result is the same in type 2 diabetes: your blood glucose level is too high."],
            ["What are the symptoms of type 2 diabetes?",
            "The symptoms of type 2 diabetes (also called type 2 diabetes mellitus) develop gradually—so gradually, in fact, that it’s possible to miss them or to not connect them as related symptoms. Some of the common symptoms of type 2 diabetes are: "
            + "fatigue, extreme thirst, frequent urination, extreme hunger, weight loss, frequent infections, slow wound healing, and blurry vision."],
            ["What causes type 2 diabetes?",
            "Type 2 diabetes has several causes: genetics and lifestyle are the most important ones. A combination of these factors can cause insulin resistance, when your body doesn’t use insulin as well as it should. Insulin resistance is the most common cause of type 2 diabetes."],
            ["What are the risk factors for type 2 diabetes?",
            "Type 2 diabetes has many risk factors associated with it, mostly related to lifestyle choices. But in order to develop insulin resistance (an inability for your body to use insulin as it should) and type 2 diabetes, you must also have a genetic abnormality. Along the same lines, some people with type 2 diabetes don’t produce enough insulin; that is also due to a genetic abnormality.\n"
            + "That is, not everyone can develop type 2 diabetes. Additionally, not everyone with a genetic abnormality will develop type 2 diabetes; these risk factors and lifestyle choices influence the development."],
            ["How is type 2 diabetes treated?",
            "Type 2 diabetes is treated with a combination of healthy meal planning, physical activity, medications, and perhaps insulin.\n"
            + "Healthy meal planning changes and exercise are the cornerstones of type 2 diabetes treatment. They often help people lose weight, which in turn can help their bodies use insulin better. Many people, when they’re first diagnosed with type 2 diabetes, are overweight (BMI >25), so making healthy lifestyle choices—such as reducing calories and portion sizes and being more active can help them get to a healthier weight."],
            ["How do type 1 and type 2 diabetes differ?",
            "Type 1 diabetes used to be called juvenile diabetes because it tends to develop in childhood as a result of a damaged pancreas that produces little to no insulin. In contrast, type 2 diabetes used to be called adult-onset diabetes because it tends to be diagnosed later in life. In type 2 diabetes, the body has increasing difficulty absorbing and using the insulin produced by the pancreas."],
            ["What is the difference between type 1 and type 2 diabetes?",
            "Type 1 diabetes used to be called juvenile diabetes because it tends to develop in childhood as a result of a damaged pancreas that produces little to no insulin. In contrast, type 2 diabetes used to be called adult-onset diabetes because it tends to be diagnosed later in life. In type 2 diabetes, the body has increasing difficulty absorbing and using the insulin produced by the pancreas."],
            ["Which is more common? Type 1 diabetes or type 2 diabetes?",
            "Type 2 diabetes makes up about 90% of cases of all diabetes, making it far more common than type 1 diabetes."],
            ["What is another term for type 2 diabetes?",
            "Adult-onset diabetes is another term for type 2 diabetes, or diabetes mellitus. Type 2 diabetes is often referred to as adult-onset diabetes because it is often diagnosed in adults, though children and teens may also develop the disease. Type 2 diabetes is a chronic condition characterized by high blood sugar (glucose) levels caused by the body's inability to use insulin properly."],
            ["What is the name for the hormone that helps the body use sugar for energy?",
            "The hormone that helps the body use sugar (glucose) for energy is called insulin. Insulin is made by the body in the pancreas and when the body cannot produce enough insulin on its own, it needs to be taken by injection or other means. Everyone who has type 1 diabetes (previously known as juvenile diabetes) must take some form of insulin therapy. Some people with type 2 diabetes will also need insulin supplementation. There are different types of insulin available, and they differ in chemical structure and how long they last in the body."],
            ["What is insulin?",
            "The hormone that helps the body use sugar (glucose) for energy is called insulin. Insulin is made by the body in the pancreas and when the body cannot produce enough insulin on its own, it needs to be taken by injection or other means. Everyone who has type 1 diabetes (previously known as juvenile diabetes) must take some form of insulin therapy. Some people with type 2 diabetes will also need insulin supplementation. There are different types of insulin available, and they differ in chemical structure and how long they last in the body."],
            ["What is the pancreas?",
            "The organ in the body that makes insulin is the pancreas. This hand-sized organ is located behind the lower part of the stomach. It produces enzymes to help digest food in the intestine and makes hormones including insulin, which is important in regulating blood sugar levels."],
            ["What is the best predictor of type 2 diabetes?",
            "The best predictor – or most major risk factor – for type 2 diabetes is being overweight or obese. Nearly 90% of people with type 2 diabetes are overweight or obese, and this puts additional pressure on their body's ability to use insulin to efficiently control blood sugar (glucose) levels. The number of cases of diabetes among American adults grew by one-third in the 1990s and because obesity is on the rise in the U.S., the number of diabetes cases among American adults is expected to continue to increase. Other risk factors for type 2 diabetes include age, race, pregnancy, stress, certain medications, genetics or family history, and high cholesterol."],
            ["What type of foods should I eat?",
            "Foods to eat for a type 2 diabetic diet meal plan include complex carbohydrates such as brown rice, whole wheat, quinoa, oatmeal, fruits, vegetables, beans, and lentils. Foods to avoid include simple carbohydrates, which are processed, such as sugar, pasta, white bread, flour, and cookies, pastries. Foods with a low glycemic load (index) only cause a modest rise in blood sugar and are better choices for people with diabetes. Good glycemic control can help in preventing long-term complications of type 2 diabetes"],
            ["How does diabetes affect males and females?",
            "Diabetes, especially type 2, is more common in males rather than females. However, females often have more serious complications and a greater risk of death. Glucose is usually metabolised and regulated at low levels in the blood through the function of a pancreatic hormone called insulin."],
            ["How is gender related to diabetes?",
            "Diabetes, especially type 2, is more common in males rather than females. However, females often have more serious complications and a greater risk of death. Glucose is usually metabolised and regulated at low levels in the blood through the function of a pancreatic hormone called insulin."],
            ["How is my sex related to diabetes?",
            "Diabetes, especially type 2, is more common in males rather than females. However, females often have more serious complications and a greater risk of death. Glucose is usually metabolised and regulated at low levels in the blood through the function of a pancreatic hormone called insulin."],
            ["How does age affect diabetes?",
            "The risk of type 2 diabetes increases as you get older, especially after age 45. That's probably because people tend to exercise less, lose muscle mass and gain weight as they age. But type 2 diabetes is also increasing dramatically among children, adolescents and younger adults."]
        ]

        self.trainer = ListTrainer(self.chatbot)

        # Train each conversation 3 times
        for conversation in self.conversations:
            for i in range(3):
                self.trainer.train(conversation)


    def askQuestion(self, question):
        print(question)

        response = self.chatbot.get_response(question)
        print(response.confidence)
        print(response)

        #Try TF-IDF
        similarities = []
        cosineSimilarities = []
        questionDoc = self.nlp(question)
        maxQuestionIndex = 0
        maxQuestion = 0
        maxAnswerIndex = 0
        maxAnswer = 0

        for item in range(len(self.conversations)):
            conversation = self.conversations[item]
            questDoc = self.nlp(conversation[0])
            answerDoc = self.nlp(conversation[1])
            sims = [questDoc.similarity(questionDoc), answerDoc.similarity(questionDoc)]
            if sims[0] > maxQuestion:
                maxQuestion = sims[0]
                maxQuestionIndex = item
            if sims[1] > maxAnswer:
                maxAnswer = sims[1]
                maxAnswerIndex = item
            similarities.append(sims)


        maxACIndex = 0
        maxAC = 0
        maxQCIndex = 0
        maxQC = 0
        for item in range(len(self.conversations)):
            conversation = self.conversations[item]
            sims = [cosine.get_similarity(question, conversation[0]), cosine.get_similarity(question, conversation[1])]
            if sims[0] > maxQC:
                maxQC = sims[0]
                maxQCIndex = item
            if sims[1] > maxAC:
                maxAC = sims[1]
                maxACIndex = item
            cosineSimilarities.append(sims)

        print(maxQuestion)
        print(self.conversations[maxQuestionIndex])
        print(maxAnswer)
        print(self.conversations[maxAnswerIndex])

#        print(maxQC)
#        print(self.conversations[maxQCIndex])
#        print(maxAC)
#        print(self.conversations[maxACIndex])

        answer = self.conversations[maxQuestionIndex]
        print(answer)
        return answer[1]