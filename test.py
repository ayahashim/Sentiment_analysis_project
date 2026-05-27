import ollama
import json
from datetime import datetime
from prompt import build_prompt, validate_and_map_category




def analyze(text):
    try:
        response = ollama.chat(
            model="qwen3:1.7b",
            messages=[{"role": "user", "content": f"{build_prompt(text)}"}]
        )
        # Get the analysis result
        analysis_text = response["message"]["content"]
        analysis_text = json.loads(analysis_text)
        analysis_text.update({
                "الوقت": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        # Add to history
       


        return analysis_text
    except Exception as e:
       
        analysis_text = f"تحليل النص: {text[:100]}..."


import pandas as pd

df = pd.read_csv("./test_data.csv", sep =",")

df_map= {"متابعة المعاملات والطلبات لدى الإمارة": "متابعة", 
         "المركز الشامل وخدمات الجمهور": "خدمات",
         "الشكاوى والملاحظات المحالة لجهات خدمية":"الشكاوى",
          "الشكاوى والملاحظات المحالة لجهات خدمية":"شكاوى",
         "الشكاوى والملاحظات المحالة لجهات خدمية":"شكوى",
         "المحافظات والمراكز والقرى والهجر": "المحافظات",
         "القنوات الرقمية والنماذج الإلكترونية": "الإلكترونية",
         
         "القنوات الرقمية والنماذج الإلكترونية": "إلكترونية",
         "الاستفسارات عن المتطلبات والإجراءات": "الاستفسارات",
         "الاستفسارات عن المتطلبات والإجراءات": "استفسار",
         "اقتراحات تحسين تجربة المستفيد": "اقتراحات",
         "اقتراحات تحسين تجربة المستفيد": "اقتراح",
         "رضا وشكر": "شكر",
         "حالات عاجلة وحرجة":"عاجلة"
         
         }
df_reverse ={}
for k,v in df_map.items():
    df_reverse[v] = k
# df_result = pd.read_csv("C:/Sentiment_analysis_app/Sentiment_analysis_project/2026-05-25T22-09_export.csv", sep=",")


df_result = pd.read_csv("C:/Sentiment_analysis_app/Sentiment_analysis_project/sentiment_analysis_2026-05-27_13-02-17.csv")
df_result["درجة_الأولوية"] = df_result["درجة_الأولوية"].replace("عاجلة", "حرج")

print(df_result["درجة_الأولوية"].unique(), df["urgency"].unique())
count = 0
for i in range(82):
    # text = df["text_ar"][i]
    # result = analyze(text)
    # print(result)

    # output = {
    #     "التصنيف": df_result["service_domain"][i],
    #     "نوع_الطلب": df_result["request_type"][i],
    #     "المشاعر": df_result["sentiment"][i],
    #     "الملخص": df_result["topic_label"][i],
    #     "درجة_الأولوية": df_result["urgency"][i],
    #     "الإجراء_المقترح": df_result["recommended_action"][i]
    # }
    # print(result["التصنيف"], text)
    # category, is_valid, error = validate_and_map_category(
    #         result.get("التصنيف", ""),
    #         strict=False
    #     )
    
    # result.update({"التصنيف": category})
    # if not is_valid:
    #         print(f"Warning: {error}")
    
    # result["التصنيف"] = category
    # print(result)
    if df["urgency"][i] == df_result["درجة_الأولوية"][i]:
        count +=1
        print(count)
       
    # else:
    #     print(df["service_domain"][i] , df_result["التصنيف"][i])
    
print(count)


# 55 sentiment 
# 24 service_domain
# 24 urgency


#     {
#         "input": "نعاني منذ أكثر من أسبوع من انقطاع الكهرباء بشكل متكرر في الحي خلال ساعات الليل",
#         "التصنيف": "كهرباء",
#         "المشاعر": "سلبي",
#         "درجة_الأولوية": "عالي",
#         "الملخص": "انقطاع متكرر للكهرباء في الحي"
#     },
#     {
#         "input": "يوجد تسرب كبير للمياه أمام المنازل في الشارع الرئيسي منذ عدة أيام",
#         "التصنيف": "مياه",
#         "المشاعر": "سلبي",
#         "درجة_الأولوية": "عالي",
#         "الملخص": "تسرب مياه في الشارع الرئيسي"
#     },
#     {
#         "input": "الطريق المؤدي إلى المدرسة مليء بالحفر الكبيرة التي تسبب أضرارًا للسيارات",
#         "التصنيف": "طرق",
#         "المشاعر": "سلبي",
#         "درجة_الأولوية": "عالي",
#         "الملخص": "وجود حفر خطيرة في الطريق"
#     },
#     {
#         "input": "المركز الصحي في الحي يقدم خدمات ممتازة والموظفون متعاونون جدًا",
#         "التصنيف": "صحة",
#         "المشاعر": "إيجابي",
#         "درجة_الأولوية": "منخفض",
#         "الملخص": "رضا عن خدمات المركز الصحي"
#     },
#     {
#         "input": "لا أستطيع تسجيل ابني في المدرسة بسبب تعطل المنصة التعليمية",
#         "التصنيف": "تعليم",
#         "المشاعر": "سلبي",
#         "درجة_الأولوية": "متوسط",
#         "الملخص": "تعطل منصة تسجيل الطلاب"
#     }
# ]

# # إنشاء DataFrame
# df = pd.DataFrame(data)

# # عرض البيانات


# # حفظ الملف
# # df["input"].to_csv("government_complaints.txt", index=False, encoding="utf-8-sig")

# file = "./government_complaints.txt"

# with open("./government_complaints.txt", "r", encoding="utf-8") as f:
#     content = f.read()

# lines = content.strip().split("\n")

# import csv
# from io import StringIO

# csv_reader = csv.DictReader(StringIO(content))
# complaints = list(csv_reader)

# print(lines[2])
# # df = pd.read_csv("government_complaints.txt")
# # with open("government_complaints.txt", "r", encoding="utf-8") as file:
# #     first_line = file.readline().strip()

# #     print(first_line)
# # print(analyze("تم إنجاز معاملتي بسرعة وأشكر الموظفين على حسن التعامل."))