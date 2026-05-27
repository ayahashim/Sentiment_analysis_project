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


df_result = pd.read_csv("C:/Sentiment_analysis_app/Sentiment_analysis_project/sentiment_analysis_project_output.csv")
df_result["درجة_الأولوية"] = df_result["درجة_الأولوية"].replace("عاجلة", "حرج")

print(df_result["درجة_الأولوية"].unique(), df["urgency"].unique())
count = 0
for i in range(82):
   
    if df["urgency"][i] == df_result["درجة_الأولوية"][i]:
        count +=1
        print(count)
       
    else:
        print(df["service_domain"][i] , df_result["التصنيف"][i])
    
print(count)


# 55 sentiment 
# 24 service_domain
# 24 urgency

