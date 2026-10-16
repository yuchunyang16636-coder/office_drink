import streamlit as st
import datetime

# ==========================================
# 1. 頁面基本設定
# ==========================================
st.set_page_config(page_title="辦公室訂飲料系統", page_icon="🧋", layout="centered")

# ==========================================
# 🎨 視覺風格設定 (字體、按鈕、響應式標題)
# ==========================================
st.markdown("""
    <style>
    /* 匯入可愛的圓潤粗體字型 (Zen Maru Gothic) */
    @import url('https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@700;900&display=swap');
    
    /* 全域套用字型與粗體 */
    html, body, [class*="st-"] {
        font-family: 'Zen Maru Gothic', sans-serif !important;
        font-weight: 700 !important;
    }
    
    /* 改善手機版標題分行：使用 clamp 函數動態調整文字大小 */
    .main-title {
        text-align: center;
        /* 字體大小：最小 2rem，彈性 8vw，最大 3.5rem */
        font-size: clamp(2rem, 8vw, 3.5rem); 
        font-weight: 900;
        color: #5A544B; /* 日系文青深棕色 */
        margin-bottom: 10px;
    }
    .sub-title {
        text-align: center;
        color: #8B9A92; /* 日系低飽和灰綠色 */
        font-size: clamp(1.1rem, 4vw, 1.5rem);
        margin-bottom: 40px;
    }
    
    /* 統一按鈕風格為日系文青風 (低飽和抹茶綠) */
    div[data-testid="stButton"] > button {
        background-color: #A3B19B !important; 
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 16px !important; /* 增加圓角讓它更可愛 */
        height: 70px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05) !important;
        transition: all 0.3s ease !important;
    }
    div[data-testid="stButton"] > button:hover {
        background-color: #8F9E87 !important; /* 游標懸停時稍微變深 */
        transform: translateY(-3px); /* 懸停時稍微往上浮起 */
        box-shadow: 0 6px 12px rgba(0,0,0,0.1) !important;
    }
    div[data-testid="stButton"] > button p {
        font-size: 1.3rem !important;
        font-weight: 900 !important;
        letter-spacing: 2px;
    }
    
    /* 隱藏右上角的 Deploy 按鈕與選單 */
    header[data-testid="stHeader"] { display: none !important; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 初始化 Session State
# ==========================================
if "page" not in st.session_state:
    st.session_state.page = "home"
if "order_date" not in st.session_state:
    st.session_state.order_date = datetime.date.today()
if "shop_name" not in st.session_state:
    st.session_state.shop_name = ""
if "device_type" not in st.session_state:
    st.session_state.device_type = ""

# ==========================================
# 3. 第一頁：極簡首頁 (只選裝置)
# ==========================================
if st.session_state.page == "home":
    # 使用我們剛剛寫好 CSS 的響應式標題
    st.markdown('<div class="main-title">🧋 辦公室訂飲料系統</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">請選擇您的點餐裝置</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💻 電腦版", use_container_width=True):
            st.session_state.device_type = "網頁版"
            st.session_state.page = "order"
            st.rerun()
            
    with col2:
        if st.button("📱 手機版", use_container_width=True):
            st.session_state.device_type = "手機版"
            st.session_state.page = "order"
            st.rerun()

# ==========================================
# 4. 第二頁：設定訂單與點餐區
# ==========================================
elif st.session_state.page == "order":
    col_back, col_title = st.columns([1, 4])
    with col_back:
        if st.button("⬅️ 返回首頁"):
            st.session_state.page = "home"
            st.rerun()
    with col_title:
        st.markdown(f"<div style='text-align: right; color: #8B9A92; padding-top: 20px;'>目前模式：{st.session_state.device_type}</div>", unsafe_allow_html=True)
        
    st.markdown("---")
    
    st.markdown("### 📋 步驟 1：確認訂單資訊")
    col_date, col_shop = st.columns(2)
    with col_date:
        st.session_state.order_date = st.date_input("📅 選擇訂購日期", value=st.session_state.order_date)
        
    with col_shop:
        shop_options = ["請選擇...", "50嵐", "可不可熟成紅茶", "麻古茶坊", "迷客夏", "得正", "清心福全", "茶湯會", "其他 (自行輸入)"]
        selected_shop = st.selectbox("🏪 選擇飲料店", options=shop_options)
        
    if selected_shop == "其他 (自行輸入)":
        custom_shop = st.text_input("✍️ 請輸入飲料店名稱：")
        st.session_state.shop_name = custom_shop
    else:
        st.session_state.shop_name = selected_shop if selected_shop != "請選擇..." else ""

    st.markdown("---")
    
    if st.session_state.shop_name == "":
        st.info("👆 請先在上方選擇飲料店，即可解鎖點餐區塊！")
    else:
        st.markdown(f"### 📝 步驟 2：開始點餐 ({st.session_state.shop_name})")
        
        if st.session_state.device_type == "手機版":
            st.warning("📱 【手機版排版區】接下來這裡會設計成適合手機螢幕的點餐卡片。")
        else:
            st.success("💻 【網頁版排版區】接下來這裡會設計成寬敞的點餐大表格。")
