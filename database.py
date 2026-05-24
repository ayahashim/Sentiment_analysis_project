import sqlite3
from datetime import datetime
import streamlit as st

def init_database():
    """Initialize SQLite database for storing analysis results"""
    conn = sqlite3.connect('sentiment_analysis.db')
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analysis_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input_text TEXT NOT NULL,
            classification TEXT,
            sentiment TEXT,
            priority TEXT,
            summary TEXT,
            response_time TEXT,
            analysis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()



def save_to_database(analysis_result: dict):
    """Save analysis result to SQLite database"""
    try:
        conn = sqlite3.connect('sentiment_analysis.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO analysis_history 
            (input_text, classification, sentiment, priority, summary, response_time, analysis_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            analysis_result.get('input', ''),
            analysis_result.get('التصنيف', ''),
            analysis_result.get('المشاعر', ''),
            analysis_result.get('درجة_الأولوية', ''),
            analysis_result.get('الملخص', ''),
            analysis_result.get('وقت_الاستجابة', ''),
            analysis_result.get('الوقت', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        ))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"خطأ في حفظ البيانات: {str(e)}")
        return False

def load_from_database() -> list:
    """Load all analysis results from SQLite database"""
    try:
        conn = sqlite3.connect('sentiment_analysis.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT input_text, classification, sentiment, priority, summary, response_time, analysis_date
            FROM analysis_history
            ORDER BY analysis_date DESC
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        # Convert to list of dictionaries
        results = []
        for row in rows:
            results.append({
                'input': row[0],
                'التصنيف': row[1],
                'المشاعر': row[2],
                'درجة_الأولوية': row[3],
                'الملخص': row[4],
                'وقت_الاستجابة': row[5],
                'الوقت': row[6]
            })
        
        return results
    except Exception as e:
        st.error(f"خطأ في تحميل البيانات: {str(e)}")
        return []

def get_database_stats() -> dict:
    """Get statistics from database"""
    try:
        conn = sqlite3.connect('sentiment_analysis.db')
        cursor = conn.cursor()
        
        # Total analyses
        cursor.execute('SELECT COUNT(*) FROM analysis_history')
        total = cursor.fetchone()[0]
        
        # Count by sentiment
        cursor.execute('SELECT sentiment, COUNT(*) FROM analysis_history GROUP BY sentiment')
        sentiment_counts = dict(cursor.fetchall())
        
        # Count by classification
        cursor.execute('SELECT classification, COUNT(*) FROM analysis_history GROUP BY classification')
        classification_counts = dict(cursor.fetchall())
        
        conn.close()
        
        return {
            'total': total,
            'sentiment': sentiment_counts,
            'classification': classification_counts
        }
    except Exception as e:
        st.error(f"خطأ في الحصول على الإحصائيات: {str(e)}")
        return {}
