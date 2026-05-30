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
        print(analysis_text)
       


        return analysis_text
    except Exception as e:
       
        analysis_text = f"تحليل النص: {text[:100]}..."
        print(analysis_text)


import pandas as pd

df = pd.read_csv("Data/test_data.csv", sep =",")

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


df_result = pd.read_csv("C:/Sentiment_analysis_app/Sentiment_analysis_project/Data/sentiment_analysis_2026-05-27_13-02-17.csv")
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
       
    else:
        print(df["service_domain"][i] , df_result["التصنيف"][i])
    
# print(count)


# 55 sentiment 
# 24 service_domain
# 24 urgency

