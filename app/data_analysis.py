import pandas as pd

df = pd.read_excel("C:/Sentiment_analysis_app/Sentiment_analysis_project/Data/northern_borders_emirate_sentiment_prototype_dataset_100.xlsx")


df_train = pd.read_csv("Data/train_data.csv")
df_map= {"متابعة المعاملات والطلبات لدى الإمارة": "متابعة", 
         "المركز الشامل وخدمات الجمهور": "خدمات",
         "الشكاوى والملاحظات المحالة لجهات خدمية":"الشكاوى",
         "المحافظات والمراكز والقرى والهجر": "المحافظات",
         "القنوات الرقمية والنماذج الإلكترونية": "الإلكترونية",
         "الاستفسارات عن المتطلبات والإجراءات": "الاستفسارات",
         "اقتراحات تحسين تجربة المستفيد": "اقتراحات",
         "رضا وشكر": "شكر",
         "حالات عاجلة وحرجة":"عاجلة"
         
         }
df_train["service_domain_new"] = df_train["service_domain"].map(df_map)


df_train["service_domain_new"]
df_train.to_csv("./train_data.csv", sep=",")
service_domain= ['متابعة المعاملات والطلبات لدى الإمارة' ,'المركز الشامل وخدمات الجمهور',
 'الشكاوى والملاحظات المحالة لجهات خدمية',
 'المحافظات والمراكز والقرى والهجر', 'القنوات الرقمية والنماذج الإلكترونية',
 'الاستفسارات عن المتطلبات والإجراءات' ,'اقتراحات تحسين تجربة المستفيد',
 'رضا وشكر' ,'حالات عاجلة وحرجة']


# df3_train = pd.DataFrame()

# df3_test = pd.DataFrame()
# for service in service_domain:

#     filtered_df = df2[df2["service_domain"] == service]
    
#     if not filtered_df.empty:
       
#         df_row = filtered_df.iloc[:2,:]
#         df_row_test = filtered_df.iloc[2:,:]

#         df3_train = pd.concat(
#             [df3_train, df_row],
#             ignore_index=True
#         )
#         df3_test = pd.concat([df3_test, df_row_test], ignore_index = True)

# print(df3_train)


# df3_test.to_csv("./test_data.csv", sep=",")
# df3_train.to_csv("./train_data.csv", sep=",")


# df_test_input = df3_test["text_ar"]
# df_test_input.to_csv("./test_data_input.txt", index= False, header= False)
# request_type: شكوى       46
# اقتراح     21
# استفسار    14
# شكر        13
# ملاحظة      6

# sentiment: سسلبي      48
# محايد     38
# إيجابي    13
# مختلط      1

# urgency
# منخفض    47
# متوسط    40
# عالي      9
# حرج       4





# متابعة المعاملات والطلبات لدى الإمارة     18
# المركز الشامل وخدمات الجمهور              15
# الشكاوى والملاحظات المحالة لجهات خدمية    15
# المحافظات والمراكز والقرى والهجر          15
# القنوات الرقمية والنماذج الإلكترونية   
# الاستفسارات عن المتطلبات والإجراءات     8
# اقتراحات تحسين تجربة المستفيد           4
# القنوات الرقمية والنماذج الإلكترونية    3