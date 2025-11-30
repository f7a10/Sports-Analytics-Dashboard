import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# إعداد الصفحة
st.set_page_config(page_title="Sports Data Analysis", layout="wide")
st.title("🏆 Sports Analytics Dashboard")

# --- 1. تحميل وتجهيز البيانات (نفس منطق النوت بوك الجديد) ---
@st.cache_data
def load_data():
    # قراءة الملف
    try:
        df = pd.read_csv('which_sport_is_best.csv')
    except FileNotFoundError:
        st.error("ملف 'which_sport_is_best.csv' غير موجود. تأكد من وضعه في نفس المجلد.")
        return pd.DataFrame()

    # تنظيف
    if 'Unnamed: 0' in df.columns:
        df = df.drop('Unnamed: 0', axis=1)
    
    # قاموس الشعبية الجديد (من الكود الخاص بك)
    popularity_index = {
        "Boxing": 500, "Ice Hockey": 520, "Football": 1000, "Basketball": 850,
        "Wrestling": 300, "Martial Arts": 480, "Tennis": 750, "Gymnastics": 420,
        "Baseball/Softball": 600, "Soccer": 1000, "Skiing: Alpine": 350, "Water Polo": 260,
        "Rugby": 540, "Lacrosse": 200, "Rodeo: Steer Wrestling": 170, "Track and Field: Pole Vault": 330,
        "Field Hockey": 700, "Speed Skating": 320, "Figure Skating": 360, "Cycling: Distance": 430,
        "Volleyball": 650, "Racquetball/Squash": 240, "Surfing": 230, "Fencing": 220,
        "Skiing: Freestyle": 320, "Team Handball": 280, "Cycling: Sprints": 360, "Bobsledding/Luge": 210,
        "Ski Jumping": 310, "Badminton": 430, "Skiing: Nordic": 330, "Auto Racing": 560,
        "Track and Field: High Jump": 340, "Track and Field: Long, Triple jumps": 360, "Diving": 300,
        "Swimming (all strokes): Distance": 380, "Skateboarding": 230, "Track and Field: Sprints": 400,
        "Rowing": 260, "Rodeo: Calf Roping": 170, "Track and Field: Distance": 380,
        "Rodeo: Bull/Bareback/Bronc Riding": 190, "Track and Field: Middle Distance": 370,
        "Weight-Lifting": 250, "Swimming (all strokes): Sprints": 380, "Water Skiing": 210,
        "Table Tennis": 640, "Track and Field: Weights": 330, "Canoe/Kayak": 240,
        "Horse Racing": 340, "Golf": 580, "Cheerleading": 190, "Roller Skating": 180,
        "Equestrian": 260, "Archery": 230, "Curling": 230, "Bowling": 240,
        "Shooting": 220, "Billiards": 260, "Fishing": 260
    }

    pop_df = pd.DataFrame([
        {"sport": sport, "popularity_index": idx}
        for sport, idx in popularity_index.items()
    ])

    # الدمج
    merged_df = df.merge(pop_df, on="sport", how="left")
    
    # ملء القيم المفقودة بمتوسط الشعبية (تحسين إضافي)
    merged_df['popularity_index'] = merged_df['popularity_index'].fillna(merged_df['popularity_index'].mean())

    return merged_df

df = load_data()

if not df.empty:
    # --- القائمة الجانبية ---
    st.sidebar.header("⚙️ Dashboard Settings")
    st.sidebar.info("Use the tabs on the right to navigate different analyses.")

    # --- التصميم الرئيسي (Tabs) ---
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Dataset Overview", 
        "🔥 Heatmap & Correlation", 
        "💪 Skill Relationships", 
        "⭐ Popularity Analysis", 
        "🆚 Head-to-Head"
    ])

    # 1. Dataset Overview
    with tab1:
        st.subheader("Raw Data Preview")
        st.dataframe(df)
        st.write(f"**Shape:** {df.shape[0]} rows, {df.shape[1]} columns")

    # 2. Heatmap (Correlation)
    with tab2:
        st.subheader("Correlation Between Sports Skills")
        st.write("This heatmap shows how different athletic skills are related.")
        
        # الكود من خليتك رقم 8
        # نستخدم الأعمدة الرقمية للمهارات (عادة من العمود 1 إلى 11 حسب ملفك)
        # تأكدنا من الأعمدة عبر df.columns في الكود السابق
        try:
            # نختار الأعمدة الرقمية فقط للارتباط
            skills_df = df.iloc[:, 1:11] 
            corr_matrix = skills_df.corr()
            
            fig, ax = plt.subplots(figsize=(10, 8))
            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Error generating heatmap: {e}")

    # 3. Skill Relationships (Scatter Plots)
    with tab3:
        st.subheader("Skill Relationships")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Strength vs Power")
            # الكود من خليتك رقم 12
            fig1, ax1 = plt.subplots(figsize=(6, 5))
            if 'str' in df.columns and 'pwr' in df.columns:
                ax1.scatter(df['str'], df['pwr'], color='blue', alpha=0.7)
                ax1.set_xlabel("Strength (str)")
                ax1.set_ylabel("Power (pwr)")
                ax1.set_title("Strength vs Power")
                ax1.grid(True)
                st.pyplot(fig1)
            else:
                st.warning("Columns 'str' or 'pwr' not found.")

        with col2:
            st.markdown("#### Strength vs Hand-Eye Coordination")
            # الكود من خليتك رقم 13
            fig2, ax2 = plt.subplots(figsize=(6, 5))
            if 'str' in df.columns and 'han' in df.columns:
                ax2.scatter(df['str'], df['han'], color='red', alpha=0.7)
                ax2.set_xlabel("Strength (str)")
                ax2.set_ylabel("Handling (han)")
                ax2.set_title("Strength vs Handling")
                ax2.grid(True)
                st.pyplot(fig2)
            else:
                st.warning("Columns 'str' or 'han' not found.")

    # 4. Popularity Analysis
    with tab4:
        st.subheader("What makes a sport popular?")
        
        # Scatter: Total Score vs Popularity (Cell 15)
        st.markdown("#### Total Skill Score vs Popularity Index")
        fig3, ax3 = plt.subplots(figsize=(10, 6))
        ax3.scatter(df["total"], df["popularity_index"], color='green', s=100, alpha=0.6)
        ax3.set_xlabel("Total Skill Score")
        ax3.set_ylabel("Popularity Index")
        ax3.set_title("Sport Total Score vs Popularity")
        ax3.grid(True)
        st.pyplot(fig3)

        st.divider()

        # Bar Plot: Correlation with Popularity (Cell 16)
        st.markdown("#### Which specific skill correlates most with Popularity?")
        # حساب الارتباط
        features = df[['end', 'str', 'pwr', 'spd', 'agi', 'flx', 'ner', 'dur', 'han', 'ana']]
        correlations = features.corrwith(df['popularity_index']).sort_values(ascending=True)
        
        fig4, ax4 = plt.subplots(figsize=(10, 6))
        sns.barplot(x=correlations.index, y=correlations.values, palette='coolwarm', ax=ax4)
        ax4.set_title('Feature Correlation with Popularity')
        ax4.set_xlabel("Attributes")
        ax4.set_ylabel('Correlation Coefficient')
        st.pyplot(fig4)

    # 5. Head-to-Head Comparison
    with tab5:
        st.subheader("Compare Two Sports")
        st.write("Compare the attribute profile of any two sports.")
        
        # قوائم اختيار للمستخدم (تحديث: جعلناها تفاعلية بدلاً من تثبيتها على كرة القدم والسلة فقط)
        sports_list = df['sport'].unique()
        c1, c2 = st.columns(2)
        sport1 = c1.selectbox("Select Sport 1", sports_list, index=list(sports_list).index("Football") if "Football" in sports_list else 0)
        sport2 = c2.selectbox("Select Sport 2", sports_list, index=list(sports_list).index("Basketball") if "Basketball" in sports_list else 1)

        if sport1 and sport2:
            comparison = df[df['sport'].isin([sport1, sport2])]
            # تجهيز البيانات للرسم (Cell 11 logic)
            # نحتاج لاستبعاد الأعمدة غير الرقمية مثل 'sport', 'rank', 'total', 'popularity_index' للرسم
            plot_df = comparison.set_index('sport')
            # نختار فقط أعمدة المهارات العشرة
            skills_cols = ['end', 'str', 'pwr', 'spd', 'agi', 'flx', 'ner', 'dur', 'han', 'ana']
            plot_df = plot_df[skills_cols].T

            # الرسم
            fig5, ax5 = plt.subplots(figsize=(12, 6))
            x = np.arange(len(plot_df.index))
            width = 0.35
            
            val1 = plot_df[sport1]
            val2 = plot_df[sport2]

            ax5.bar(x - width/2, val1, width, label=sport1)
            ax5.bar(x + width/2, val2, width, label=sport2)

            ax5.set_xticks(x)
            ax5.set_xticklabels(plot_df.index)
            ax5.set_xlabel("Attributes")
            ax5.set_ylabel("Score")
            ax5.set_title(f"{sport1} vs {sport2} – Attribute Comparison")
            ax5.legend()
            st.pyplot(fig5)