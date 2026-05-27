"""
Sentiment Analysis App - Streamlit Version
==========================================
A complete sentiment analysis application built with Streamlit.
Supports text input and file upload with Arabic RTL support.

Installation:
    pip install streamlit ollama python-dotenv

Run:
    streamlit run streamlit_app.py
"""

import streamlit as st
import ollama
import os
from dotenv import load_dotenv
from io import StringIO
import json
from datetime import datetime
from prompt import build_prompt, validate_and_map_category
import plotly.graph_objects as go
import plotly.express as px
import sqlite3
from datetime import datetime
from database import init_database, save_to_database, load_from_database, get_database_stats


# ============================================
# PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title="تحليل المشاعر",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load environment variables
load_dotenv()

# ============================================
# CUSTOM CSS FOR ARABIC RTL SUPPORT
# ============================================
st.markdown("""
    <style>
        /* RTL Support */
        body, .main, .stApp {
            direction: rtl;
            text-align: right;
        }
        
        /* Header styling */
        .header-content {
            width: 100%;
            text-align: right;
            padding: 15px 20px;
        }
        .title-wrapper {
            position: relative;
            margin-bottom: 30px;
        }

        .header-title {
            color: white;
            text-align: right;
            font-size: 2.5rem;
            font-weight: bold;
            margin: 0;
            padding: 0;
            position: relative;
            
        }
        
        .header-subtitle {
            color: white;
            text-align: right;
            font-size: 1.4rem;
            margin-bottom: 30px;
        }
            
        /*gradient horizantal bar*/
        
        
        .gradient-bar {
        height: auto;
            width: 100%;
            border-radius: 8px;
            background: linear-gradient(
                90deg,
                #0f7a22,   /* darker green */
                #0E543E   /*  main green */
            );
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            z-index: 1;
        }
        /* Card styling */
        .result-card {
            background-color: #f8f9fa;
            border-left: 4px solid #1B8B7F;
            padding: 20px;
            border-radius: 8px;
            margin: 10px 0;
        }
        
        .stat-card {
            background-color: white;
            border: 1px solid #e0e0e0;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }
        
        .stat-number {
            font-size: 2rem;
            font-weight: bold;
            color: #1B8B7F;
        }
        
        .stat-label {
            color: #666;
            font-size: 0.9rem;
            margin-top: 10px;
        }
        
        /* ===== TAB STYLING ===== */
      
        .stTabs {
            background-color: transparent;
        }

        /* Tab container - remove underline */
        .stTabs [data-baseweb="tab-list"] {
            background-color: #0E543E !important;
            gap: 0 !important;
            padding: 5px !important;
            border-radius: 8px !important;
            border-bottom: none !important;
            box-shadow: none !important;
             
            
        }

        /* Individual tab */
        .stTabs [data-baseweb="tab"] {
            background-color: #0E543E !important;
            color: white !important;
            padding: 12px 20px !important;
            font-size: 1.2rem !important;
            font-weight: 600 !important;
            border-radius: 6px !important;
            border: none !important;
            outline: none !important;
        }

        /* Tab text */
        .stTabs [data-baseweb="tab"] p {
            color: white !important;
            font-size: 1.2rem !important;
            font-weight: 600 !important;
        }

        /* Tab hover */
        .stTabs [data-baseweb="tab"]:hover {
            background-color: #0f7a22 !important;
            color: white !important;
        }

        .stTabs [data-baseweb="tab"]:hover p {
            color: white !important;
        }

        /* Active tab - NO UNDERLINE */
        .stTabs [aria-selected="true"] {
            background-color: #0E543E !important;
            color: white !important;
            border: none !important;
            border-bottom: none !important;
            outline: none !important;
            box-shadow: none !important;
        }

        .stTabs [aria-selected="true"] p {
            color: white !important;
        }

        /* Tab panel */
        .stTabs [data-baseweb="tab-panel"] {
            padding: 20px !important;
        }

        /* Remove underline from tab list */
        .stTabs [data-baseweb="tab-list"]::after {
            display: none !important;
        }

        div[role="tablist"] {
            border-bottom: none !important;
        }

        div[role="tab"] {
            border-bottom: none !important;
        }

        /* ===== COMPLETE TAB OVERRIDE ===== */
        .stTabs [data-baseweb="tab-list"] {
            background-color: #0E543E !important;
            gap: 0 !important;
            padding: 5px !important;
            border-radius: 8px !important;
            border: none !important;
            border-bottom: none !important;
            box-shadow: none !important;
            background-image: none !important;
            outline: none !important;
        }

        .stTabs [data-baseweb="tab-list"] * {
            border: none !important;
            border-bottom: none !important;
            outline: none !important;
        }

        .stTabs [data-baseweb="tab"] {
            background-color: #0E543E !important;
            color: white !important;
            padding: 12px 20px !important;
            font-size: 1.2rem !important;
            font-weight: 600 !important;
            border-radius: 6px !important;
            border: none !important;
            outline: none !important;
        }

        .stTabs [data-baseweb="tab"]:hover {
            background-color: #0f7a22 !important;
        }

        .stTabs [aria-selected="true"] {
            background-color: #0E543E !important;
            color: white !important;
            border: none !important;
            outline: none !important;
            
        }

        /* Button styling */
        .stButton > button {
        background-color: #0E543E !important;
        color: white !important;
        border: none !important;
        transition: all 0.3s ease !important;
        }

        .stButton > button:hover {
        background-color: #0f7a22 !important;
        color: white !important;
        transform: scale(1.02) !important;
        }

        .stButton > button:active {
        background-color: #0d5a3a !important;
        }
            
        /*Expander styling */
        div[data-testid="stExpander"] details summary p{
            font-size: 1rem;
            font-weight: bold;
        }
            
        /* Sentiment colors */
        .sentiment-positive {
            color: #28a745;
            font-weight: bold;
        }
        
        .sentiment-negative {
            color: #dc3545;
            font-weight: bold;
        }
        
        .sentiment-neutral {
            color: #ffc107;
            font-weight: bold;
        }
        
        /* Text area with label styling */
        .stTextArea {
            margin-bottom: 4px;
        }

        .stTextArea label {
            font-size: 2.1rem !important;
            font-weight: bold !important;
            color: #0E543E !important;
        }

        .stTextArea textarea {
            font-size: 1.2rem !important;
            font-weight: bold !important;
            padding: 12px !important;
            border-radius: 6px !important;
            border: 2px solid #0E543E !important;
        }


        /* Priority colors */
        .priority-high {
            background-color: #f8d7da;
            color: #721c24;
            padding: 8px 12px;
            border-radius: 4px;
            font-weight: bold;
        }
        
        .priority-medium {
            background-color: #fff3cd;
            color: #856404;
            padding: 8px 12px;
            border-radius: 4px;
            font-weight: bold;
        }
        
        .priority-low {
            background-color: #d4edda;
            color: #155724;
            padding: 8px 12px;
            border-radius: 4px;
            font-weight: bold;
        }
        
        /* Classification colors */
        .classification-badge {
            display: inline-block;
            padding: 8px 12px;
            border-radius: 20px;
            font-weight: bold;
            margin: 5px;
        }
        
       

    </style>
""", unsafe_allow_html=True)



    
    

# Initialize database on app start
init_database()

# ============================================
# SESSION STATE INITIALIZATION
# ============================================
if "analysis_history" not in st.session_state:
    # Load from database on first load
    st.session_state.analysis_history = load_from_database()

if "current_result" not in st.session_state:
    st.session_state.current_result = None

# ============================================
# HELPER FUNCTIONS
# ============================================

def get_sentiment_color(sentiment: str) -> str:
    """Return HTML class for sentiment color"""
    if "إيجابي" in sentiment:
        return "sentiment-positive"
    elif "سلبي" in sentiment:
        return "sentiment-negative"
    else:
        return "sentiment-neutral"

def get_priority_color(priority: str) -> str:
    """Return HTML class for priority color"""
    if "عالي" in priority or "حرج" in priority or "عاجلة" in priority or "عاجل" in priority:
        return "priority-high"

    elif "متوسط" in priority:
        return "priority-medium"
    else:
        return "priority-low"

def get_classification_color(classification: str) -> str:
    """Return color for classification badge"""
    colors = {
        "متابعة المعاملات والطلبات لدى الإمارة":  "#1B8B7F", 
"المركز الشامل وخدمات الجمهور" : "#00BCD4",
 "الشكاوى والملاحظات المحالة لجهات خدمية" : "#9E9E9E",
"المحافظات والمراكز والقرى والهجر" : "#5C36F4", 
"القنوات الرقمية والنماذج الإلكترونية" : "#9C27B0",
"الاستفسارات عن المتطلبات والإجراءات" : "#4CAF50", 
"اقتراحات تحسين تجربة المستفيد": "#FF9800",
"رضا وشكر": "#3CFF00", 
"حالات عاجلة وحرجة" : "#FF1900"
    }
    
     
    for key, color in colors.items():
        if key in classification:
            return color
    return "#1B8B7F"

def get_category_distribution() -> dict:
    """Calculate percentage of each category from analysis history"""
    if not st.session_state.analysis_history:
        return {}
    
    categories = {
       "متابعة المعاملات والطلبات لدى الإمارة": 0.0, 
"المركز الشامل وخدمات الجمهور" : 0.0, 
 "الشكاوى والملاحظات المحالة لجهات خدمية" : 0.0,
"المحافظات والمراكز والقرى والهجر" : 0.0, 
"القنوات الرقمية والنماذج الإلكترونية" : 0.0,
"الاستفسارات عن المتطلبات والإجراءات" : 0.0, 
"اقتراحات تحسين تجربة المستفيد": 0.0,
"رضا وشكر": 0.0, 
"حالات عاجلة وحرجة" : 0.0
    }
    
    # Count each category
    for analysis in st.session_state.analysis_history:
        classification = analysis.get("التصنيف", "")
        if classification is None:
            classification = ""
        
        # Convert to string if it's not already
        classification = str(classification)

        for category in categories.keys():
            if category in classification:
                categories[category] += 1
                break
    
    return categories
def clean_json_keys(json_str):
    """Remove leading/trailing spaces from JSON keys"""
    data = json_str
    try:
        
        cleaned = {}
        for key, value in data.items():
            # Strip spaces from key
            clean_key = key.strip()
            # Also strip value if it's a string
            clean_value = value.strip() if isinstance(value, str) else value
            cleaned[clean_key] = clean_value
        return cleaned
    except:
        return data
    
def analyze_text(text: str, use_ollama: bool = True) -> dict:
    """
    Analyze text and return sentiment analysis with response time
    
    Args:
        text: Text to analyze
        use_ollama: Whether to use Ollama (True) or mock response (False)
    
    Returns:
        Dictionary with analysis results including response time
    """
    if not text or not text.strip():
        st.error("يرجى إدخال نص للتحليل")
        return None
    
    import time
    start_time = time.time()  # Track start time
    
    try:
        with st.spinner("جاري التحليل..."):
            if use_ollama:
                try:
                    response = ollama.chat(
                        model="qwen3:1.7b",
                        messages=[{"role": "user", "content": f"حلل المشاعر في هذا النص: {build_prompt(text)}"}]
                    )
                    analysis_text = response["message"]["content"]
                    analysis_text = json.loads(analysis_text)
                    analysis_text = clean_json_keys(analysis_text)  
                    # Calculate response time
                    response_time = time.time() - start_time
                    category, is_valid, error = validate_and_map_category(
                    analysis_text.get("التصنيف", ""),
                    strict=False
                             )
            
                    
                    if not is_valid:
                            print(f"Warning: {error}")
                    
                    
                    analysis_text.update({ "التصنيف": category, 
                        "النص": text,
                        "الوقت": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "وقت_الاستجابة": f"{response_time:.2f}s"  # Add response time
                    })
                    
                    
                    st.session_state.analysis_history.append(analysis_text)
                    st.session_state.current_result = analysis_text
                    # Save to database
                    save_to_database(analysis_text)

                    # st.rerun()
                    return analysis_text
                    
                except Exception as e:
                    st.warning(f"تعذر الاتصال بـ Ollama: {str(e)}")
                    analysis_text = f"تحليل النص: {text[:100]}..."
            else:
                analysis_text = f"تحليل النص: {text[:100]}..."
            
            # Calculate response time
            response_time = time.time() - start_time
            
            result = {
                "النص": text,
                "التصنيف": "غير متاح",
                "المشاعر": "غير متاح",
                "درجة_الأولوية": "غير متاح",
                "الملخص": analysis_text,
                "الوقت": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "وقت_الاستجابة": f"{response_time:.2f}s"  # Add response time
            }
            
            st.session_state.analysis_history.append(result)
            st.session_state.current_result = result
            # FORCE RERUN TO UPDATE SIDEBAR
            # st.rerun()
            return result
    
    except Exception as e:
        st.error(f"خطأ في التحليل: {str(e)}")
        return None
    
def analyze_multiple_complaints(complaints: list) -> list:
    """
    Analyze multiple complaints from a list
    
    Args:
        complaints: List of complaint dictionaries
    
    Returns:
        List of analysis results
    """
    if not complaints:
        st.error("لا توجد شكاوى للتحليل")
        return []
    
    import time
    results = []
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    
    for idx, complaint in enumerate(complaints):
        # Update progress
        progress = (idx + 1) / len(complaints)
        progress_bar.progress(progress)
        status_text.text(f"جاري تحليل الشكوى {idx + 1} من {len(complaints)}...")
        
        # Extract complaint text
        complaint_text = complaint.get("input", "")
        
        if not complaint_text.strip():
            continue
        
        start_time = time.time()
        
        try:
            # Analyze using Ollama
            response = ollama.chat(
                model="qwen3:1.7b",
                messages=[{"role": "user", "content": f"حلل المشاعر والتصنيف والأولوية: {build_prompt(complaint_text)}"}]
            )
            

            
            analysis_text = response["message"]["content"]
            analysis_result = json.loads(analysis_text)
            analysis_result = clean_json_keys(analysis_result)  

            category, is_valid, error = validate_and_map_category(
                    analysis_result.get("التصنيف", ""),
                    strict=False
                             )
            
                    
            if not is_valid:
                    print(f"Warning: {error}")
            
            response_time = time.time() - start_time
            
            # Add metadata
            analysis_result.update({ "التصنيف": category,
                "النص": complaint_text,
                "الوقت": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "وقت_الاستجابة": f"{response_time:.2f}s"
            })
            st.write(analysis_result)
            results.append(analysis_result)
            st.session_state.analysis_history.append(analysis_result)
            st.session_state.current_result = analysis_result

            # Save to database
            save_to_database(analysis_result)
            # st.rerun()
        except Exception as e:
            st.warning(f"خطأ في تحليل الشكوى {idx + 1}: {str(e)}")
            results.append({
                "النص": complaint_text,
                "التصنيف": "غير متاح",
                "المشاعر": "غير متاح",
                "درجة_الأولوية": "غير متاح",
                "الملخص": f"خطأ: {str(e)}",
                "الوقت": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "وقت_الاستجابة": "0.00s"
            })
    
    # Clear progress indicators
    progress_bar.empty()
    status_text.empty()
    
    
    return results

def calculate_average_response_time() -> str:
    """Calculate average response time from analysis history"""
    if not st.session_state.analysis_history:
        return "0.00s"
    
    total_time = 0
    count = 0
    
    for analysis in st.session_state.analysis_history:
        if "وقت_الاستجابة" in analysis:
            # Extract numeric value from "X.XXs" format
            time_str = analysis["وقت_الاستجابة"].replace("s", "")
            try:
                total_time += float(time_str)
                count += 1
            except ValueError:
                continue
    
    if count == 0:
        return "0.00s"
    
    average = total_time / count
    return f"{average:.2f}s"

def read_file(uploaded_file) -> str:
    """Read content from uploaded file"""
    try:
        if uploaded_file.type == "text/plain":

            content = uploaded_file.getvalue().decode("utf-8")
            
            # Check if file contains multiple lines
            lines = content.strip().split('\n')
            if len(lines) >1:
                complaints = []
                for line in lines:
                    # line = line.strip()
                    if line:  # Skip empty lines
                        complaints.append({"input": line})
                return complaints
            else:
                return content

        elif uploaded_file.type == "application/pdf":
            st.warning("ملفات PDF تتطلب مكتبة إضافية. يرجى استخدام ملفات نصية.")
            return None
        elif "wordprocessingml" in uploaded_file.type:
            st.warning("ملفات Word تتطلب مكتبة إضافية. يرجى استخدام ملفات نصية.")
            return None
        else:
            st.error("نوع الملف غير مدعوم")
            return None
    except Exception as e:
        st.error(f"خطأ في قراءة الملف: {str(e)}")
        return None

# ============================================
# HEADER SECTION
# ============================================
# st.markdown('<div class="gradient-bar"></div>', unsafe_allow_html=True)
# st.markdown("""<div class = "title-wrapper"> <div class="header-title">📊 تحليل المشاعر</div>
#             <div class="gradient-bar"></div> </div>""", unsafe_allow_html=True)

st.markdown("""
    <div class="title-wrapper">
        <div class="gradient-bar">
            <div class="header-content">
                <div class="header-title">تحليل المشاعر</div>
                <div class="header-subtitle">حلل المشاعر والعواطف في نصك</div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# st.markdown('<div class="header-subtitle">حلل المشاعر والعواطف في نصك</div>', unsafe_allow_html=True)

# Top divider
st.markdown("---")



# ============================================
# MAIN CONTENT - TABS
# ============================================


st.markdown('<div class="gradient-bar">', unsafe_allow_html=True)
tab1, tab2, tab3 = st.tabs(["📝 إدخال النص", "📁 تحميل ملف", "📊 الإحصائيات"])
st.markdown('</div>', unsafe_allow_html=True)
# ============================================
# TAB 1: TEXT INPUT
# ============================================
with tab1:
    # st.markdown(" أدخل نصك للتحليل")
    label = " أدخل نصك للتحليل"
    s = f"<p style='font-size:20px; font-weight: bold;'>{label}</p>"
    st.markdown(s, unsafe_allow_html=True)  
    # Text area
    input_text = st.text_area(
      "",
        placeholder="أدخل النص الذي تريد تحليل مشاعره...",
        height=200,
        key="text_input"
    )
    
    # Buttons
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("🔍 تحليل النص", use_container_width=True):
            result = analyze_text(input_text, use_ollama=True)
    
    with col2:
        if st.button("🗑️ مسح", use_container_width=True):
            st.session_state.current_result = None
            st.rerun()
    
    # Display results
    if st.session_state.current_result:
        st.markdown("---")
        st.markdown("### 📋 نتائج التحليل")
        
        result = st.session_state.current_result
        
        # Create columns for results
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
                <div class="result-card">
                    <h4>المشاعر</h4>
                    <p class="{get_sentiment_color(result['المشاعر'])}">{result['المشاعر']}</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class="result-card">
                    <h4>درجة الأولوية</h4>
                    <div class="{get_priority_color(result['درجة_الأولوية'])}">{result['درجة_الأولوية']}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div class="result-card">
                    <h4>التصنيف</h4>
                    <p style="color: {get_classification_color(result['التصنيف'])}; font-weight: bold;">
                        {result['التصنيف']}
                    </p>
                </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
                <div class="result-card">
                    <h4>⏱️ وقت الاستجابة</h4>
                    <p style="color: #0E543E; font-weight: bold; font-size: 1.3rem;">
                        {result.get('وقت_الاستجابة', 'غير متاح')}
                    </p>
                </div>
            """, unsafe_allow_html=True)
        
        # Summary
        st.markdown("#### الملخص")
        st.info(result.get('الملخص',""))
        
        # Download results as JSON
        st.download_button(
            label="📥 تحميل النتائج (JSON)",
            data=json.dumps(result, ensure_ascii=False, indent=2),
            file_name=f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

# ============================================
# TAB 2: FILE UPLOAD
# ============================================
with tab2:
    st.markdown("### تحميل ملف للتحليل")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "اختر ملف نصي (.txt)",
        type=["txt"],
        help = "يمكنك تحميل ملف نصي يحتوي على شكوى في كل سطر. الحد الأقصى: 5 ميجابايت"
       
    )
    
    if uploaded_file is not None:
        # Check file size
        if uploaded_file.size > 5 * 1024 * 1024:
            st.error("حجم الملف كبير جداً (الحد الأقصى 5 ميجابايت)")
        else:
            # # Display file info
            # col1, col2, col3= st.columns(3)
            # with col1:
            #     st.metric("اسم الملف", uploaded_file.name)
            # with col2:
            #     st.metric("حجم الملف", f"{uploaded_file.size / 1024:.2f} KB")
            # with col3:
            #     st.metric("نوع الملف", uploaded_file.type)
            
            # Read file
            file_content = read_file(uploaded_file)
            
            if len(file_content) > 1:
                complaints = file_content
                st.markdown(f" تم العثور على **{len(complaints)}** شكوى")
            
                # Show preview of complaints
                # Wrapper div with class
                st.markdown('<div>', unsafe_allow_html=True)
                with st.expander("معاينة الشكاوى"):
                    for idx, complaint in enumerate(complaints, 1):
                        st.markdown(f"**الشكوى {idx}:**")
                        st.write(complaint.get("input", "بدون نص"))
                        st.divider()
                st.markdown("</div>", unsafe_allow_html=True)
                if st.button("🔍 تحليل جميع الشكاوى", key="analyze_multiple"):
                    results = analyze_multiple_complaints(complaints)
                    
                    
                    if results:
                        
                        

                        st.success(f"✅ تم تحليل **{len(results)}** شكوى بنجاح")
                        
                        # Display results in expandable sections
                        st.markdown("---")
                        st.markdown("### 📋 نتائج التحليل")
                        
                        for idx, result in enumerate(results, 1):
                            with st.expander(f"الشكوى {idx}: {result.get('التصنيف', 'غير متاح')} - {result.get('المشاعر', 'غير متاح')}"):
                                col1, col2, col3, col4 = st.columns(4)
                                
                                with col1:
                                    st.markdown(f"""
                                        <div class="result-card">
                                            <h4>المشاعر</h4>
                                            <p class="{get_sentiment_color(result.get('المشاعر', ''))}">{result.get('المشاعر', 'غير متاح')}</p>
                                        </div>
                                    """, unsafe_allow_html=True)
                                with col2:
                                    st.markdown(f"""
                                        <div class="result-card">
                                            <h4>درجة الأولوية</h4>
                                            <div class="{get_priority_color(result.get('درجة_الأولوية', ''))}">{result.get('درجة_الأولوية', 'غير متاح')}</div>
                                        </div>
                                    """, unsafe_allow_html=True)
                                
                                with col3:
                                    st.markdown(f"""
                                        <div class="result-card">
                                            <h4>التصنيف</h4>
                                            <p style="color: {get_classification_color(result.get('التصنيف', ''))}; font-weight: bold;">
                                                {result.get('التصنيف', 'غير متاح')}
                                            </p>
                                        </div>
                                    """, unsafe_allow_html=True)
                                with col4:
                                    st.markdown(f"""
                                        <div class="result-card">
                                            <h4>⏱️ وقت الاستجابة</h4>
                                            <p style="color: #0E543E; font-weight: bold; font-size: 1.3rem;">
                                                {result.get('وقت_الاستجابة', 'غير متاح')}
                                            </p>
                                        </div>
                                    """, unsafe_allow_html=True)

                                st.markdown(f"**الملخص:** {result.get('الملخص', 'غير متاح')}")
                                st.markdown(f"**النص الأصلي:** {result.get('النص', 'بدون نص')}")
                        st.markdown("---")
                        st.markdown("### 📥 تحميل النتائج")
                        
                        # col_json = st.columns(1)
                        
                        # with col_json:
                        json_results = json.dumps(results, ensure_ascii=False, indent=2)
                        st.download_button(
                                label="📥 تحميل كـ JSON",
                                data=json_results,
                                file_name=f"analysis_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                                mime="application/json",
                                key="download_json"
                            )
                            


            else:
                st.markdown("---")
                st.markdown("#### محتوى الملف:")
                st.text_area("", value=file_content[:500], height=150, disabled=True)
                # Analyze button
                if st.button(" تحليل محتوى الملف", use_container_width=True):
                    result = analyze_text(file_content, use_ollama=True)
                
                
                    # Display results if available
                    
                    if st.session_state.current_result:
                        st.markdown("---")
                        st.markdown("### 📋 نتائج التحليل")
                        
                        result = st.session_state.current_result
                        
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.markdown(f"""
                                <div class="result-card">
                                    <h4>المشاعر</h4>
                                    <p class="{get_sentiment_color(result['المشاعر'])}">{result['المشاعر']}</p>
                                </div>
                            """, unsafe_allow_html=True)
                        
                        with col2:
                            st.markdown(f"""
                                <div class="result-card">
                                    <h4>درجة الأولوية</h4>
                                    <div class="{get_priority_color(result['درجة_الأولوية'])}">{result['درجة_الأولوية']}</div>
                                </div>
                            """, unsafe_allow_html=True)
                        
                        with col3:
                            st.markdown(f"""
                                <div class="result-card">
                                    <h4>التصنيف</h4>
                                    <p style="color: {get_classification_color(result['التصنيف'])}; font-weight: bold;">
                                        {result['التصنيف']}
                                    </p>
                                </div>
                            """, unsafe_allow_html=True)
                        
                        st.markdown("#### الملخص")
                        st.info(result.get('الملخص',""))


                        with col4:
                            st.markdown(f"""
                                <div class="result-card">
                                    <h4>⏱️ وقت الاستجابة</h4>
                                    <p style="color: #0E543E; font-weight: bold; font-size: 1.3rem;">
                                        {result.get('وقت_الاستجابة', 'غير متاح')}
                                    </p>
                                </div>
                            """, unsafe_allow_html=True)

                 

# ============================================
# TAB 3: STATISTICS
# ============================================
with tab3:
    st.markdown("### 📊 إحصائيات التطبيق")

    # Get stats from database
    db_stats = get_database_stats()
    
    # Statistics
    col1, col2= st.columns(2)
    # len(st.session_state.analysis_history)
    with col1:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{db_stats.get('total', 0)}</div>
                <div class="stat-label">عدد التحليلات</div>
            </div>
        """, unsafe_allow_html=True)
    
    
    with col2:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{calculate_average_response_time()}</div>
                <div class="stat-label">متوسط وقت الاستجابة</div>
            </div>
        """, unsafe_allow_html=True)
    
    col1, col2= st.columns(2)
    with col1:
        # Analysis history chart
        if st.session_state.analysis_history:
            st.markdown("---")
            st.markdown("### 📈 سجل التحليلات")
            
            # Count sentiments
            sentiments = {}
            for analysis in st.session_state.analysis_history:
                sentiment = analysis['المشاعر']
                sentiments[sentiment] = sentiments.get(sentiment, 0) + 1
            
            # Display as bar chart
            import pandas as pd
            df = pd.DataFrame(list(sentiments.items()), columns=['المشاعر', 'العدد'])
            st.bar_chart(df.set_index('المشاعر'))
        else:
            st.markdown("---")
            st.markdown("### 📈 سجل التحليلات")
            st.info("لا توجد بيانات حتى الآن")




        
    # Pie chart for categories
    with col2:
        st.markdown("---")
        st.markdown("### 📈 توزيع الفئات")
        
        category_dist = get_category_distribution()
        
        if category_dist and sum(category_dist.values()) > 0:
            # Filter out zero values for cleaner chart
            filtered_categories = {k: v for k, v in category_dist.items() if v > 0}
            
            # Create pie chart
            fig = go.Figure(data=[go.Pie(
                labels=list(filtered_categories.keys()),
                values=list(filtered_categories.values()),
                hovertemplate='<b>%{label}</b> العدد: %{value} النسبة: %{percent}<extra></extra>',
                textposition='inside',
                textinfo='label+percent',
                marker=dict(
                    colors=['#1B8B7F', '#00BCD4', '#9E9E9E', '#F44336', '#9C27B0', '#4CAF50', '#FF9800']
                )
            )])
            
            fig.update_layout(
                height=400,
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=1.05
                ),
                margin=dict(l=0, r=200, t=0, b=0)
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("لا توجد بيانات كافية لعرض الرسم البياني. قم بتحليل بعض الشكاوى أولاً.")

    
    # Display table
    st.markdown("---")
    st.markdown("#### تفاصيل التحليلات:")

    # if st.session_state.analysis_history:
    #     history_df = pd.DataFrame(st.session_state.analysis_history)

    #     st.dataframe(
    #         history_df[['النص','المشاعر', 'درجة_الأولوية', 'التصنيف', 'الوقت']],
    #         use_container_width=True
    #     )


    if st.session_state.analysis_history:
        # Create DataFrame with all columns
        history_df = pd.DataFrame(st.session_state.analysis_history)
        
        # Display columns (what user sees in table)
        display_columns = ['الوقت', 'النص', 'المشاعر', 'درجة_الأولوية', 'التصنيف']
        
        # FIX: Prepare FULL export with correct column order
        export_columns = ['الوقت', 'النص', 'التصنيف', 'المشاعر', 'درجة_الأولوية', 'الملخص', 'وقت_الاستجابة']
        
        # Create export DataFrame with all columns
        export_df = history_df[[col for col in export_columns if col in history_df.columns]].copy()
        
        # # Fill missing columns
        # for col in export_columns:
        #     if col not in export_df.columns:
        #         export_df[col] = "غير متاح"
        
        # # Fill NaN values
        # export_df = export_df.fillna("غير متاح")
        
        # # Reorder columns
        # export_df = export_df[export_columns]
        
        # Convert to CSV
        csv_data = export_df.to_csv(index=False, encoding='utf-8-sig')
        
        # Display table (without using built-in download)
        st.dataframe(
            history_df[display_columns],
            use_container_width=True,
            hide_index=True
        )
        
        # ADD CUSTOM DOWNLOAD BUTTON (replaces dataframe's button)
        st.markdown("---")
        st.download_button(
            label="📥 تحميل التقرير الكامل (CSV)",
            data=csv_data,
            file_name=f"sentiment_analysis_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv",
            mime="text/csv;charset=utf-8",
            key="download_csv_full"
        )


    else:
        st.info("لا توجد بيانات تحليل حتى الآن")

# ============================================
# SIDEBAR - SETTINGS & HISTORY
# ============================================
with st.sidebar:
    # st.markdown("### ⚙️ الإعدادات")
    
    # # Use Ollama toggle
    # use_ollama = st.checkbox(
    #     "استخدام Ollama للتحليل",
    #     value=True,
    #     help="إذا كان Ollama مثبتاً ومشغلاً، سيتم استخدامه للتحليل"
    # )
    
    # # API Key input (optional)
    # api_key = st.text_input(
    #     "مفتاح API (اختياري)",
    #     type="password",
    #     help="إذا كنت تستخدم خادم خارجي"
    # )
    
    # st.markdown("---")
    
    
    # Analysis History
    st.markdown("### 📜 سجل التحليلات")
    
    if st.session_state.analysis_history:
        st.write(f"عدد التحليلات: {len(st.session_state.analysis_history)}")


        if st.button("🗑️ حذف جميع البيانات"):
       
            try:
                conn = sqlite3.connect('sentiment_analysis.db')
                cursor = conn.cursor()
                cursor.execute('DELETE FROM analysis_history')
                conn.commit()
                conn.close()
                st.session_state.analysis_history = []
                st.success("تم حذف جميع البيانات")
                st.rerun()
            except Exception as e:
                st.error(f"خطأ: {str(e)}")
        
        # if st.button("🗑️ مسح السجل"):
        #     st.session_state.analysis_history = []
        #     st.session_state.current_result = None
        #     st.rerun()
        
        # Show recent analyses
        st.markdown("#### التحليلات الأخيرة:")
        for i, analysis in enumerate(reversed(st.session_state.analysis_history)):
            with st.expander(f"التحليل {len(st.session_state.analysis_history) - i}"):
                st.write(f"**الملخص:** {analysis.get('الملخص', 'النص')[:100]}...")
                st.write(f"**المشاعر:** {analysis['المشاعر']}")
                st.write(f"**الوقت:** {analysis['الوقت']}")
    else:
        st.info("لا توجد تحليلات بعد")



# ============================================
# FOOTER
# ============================================
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #999; font-size: 0.9rem; margin-top: 30px;">
        <p>© 2024 تطبيق تحليل المشاعر | جميع الحقوق محفوظة</p>
        
    </div>
""", unsafe_allow_html=True)
