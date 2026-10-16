import streamlit as st
import datetime

# ==========================================
# 1. 頁面基本設定
# ==========================================
st.set_page_config(page_title="辦公室訂飲料系統", page_icon="🧋", layout="centered")

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
    # 置中大標題
    st.markdown("<h1 style='text-align: center; font-size: 3.5rem;'>🧋 辦公室訂飲料系統</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #666; margin-bottom: 40px;'>請選擇您的點餐裝置</h3>", unsafe_allow_html=True)
    
    # 用 Columns 讓兩個按鈕並排、變大
    col1, col2 = st.columns(2)
    with col1:
        # 按下按鈕後，記錄裝置並跳轉到點餐頁面
        if st.button("💻 網頁版 (電腦)", use_container_width=True, type="primary"):
            st.session_state.device_type = "網頁版"
            st.session_state.page = "order"
            st.rerun()
            
    with col2:
        if st.button("📱 手機版", use_container_width=True, type="primary"):
            st.session_state.device_type = "手機版"
            st.session_state.page = "order"
            st.rerun()

# ==========================================
# 4. 第二頁：設定訂單與點餐區
# ==========================================
elif st.session_state.page == "order":
    # 頂部列：返回按鈕與目前模式提示
    col_back, col_title = st.columns([1, 4])
    with col_back:
        if st.button("⬅️ 返回首頁"):
            st.session_state.page = "home"
            st.rerun()
    with col_title:
        st.markdown(f"<div style='text-align: right; color: #888; padding-top: 10px;'>目前模式：{st.session_state.device_type}</div>", unsafe_allow_html=True)
        
    st.markdown("---")
    
    # 步驟 1：把原本的日期與店家選擇移來這裡
    st.markdown("### 📋 步驟 1：確認訂單資訊")
    col_date, col_shop = st.columns(2)
    with col_date:
        st.session_state.order_date = st.date_input("📅 選擇訂購日期", value=st.session_state.order_date)
        
    with col_shop:
        shop_options = ["請選擇...", "50嵐", "可不可熟成紅茶", "麻古茶坊", "迷客夏", "得正", "清心福全", "茶湯會", "其他 (自行輸入)"]
        selected_shop = st.selectbox("🏪 選擇飲料店", options=shop_options)
        
    # 如果選「其他」，跳出文字框自己打
    if selected_shop == "其他 (自行輸入)":
        custom_shop = st.text_input("✍️ 請輸入飲料店名稱：")
        st.session_state.shop_name = custom_shop
    else:
        st.session_state.shop_name = selected_shop if selected_shop != "請選擇..." else ""

    st.markdown("---")
    
    # 步驟 2：只有選好店家後，才解鎖下方的「點餐區」
    if st.session_state.shop_name == "":
        st.info("👆 請先在上方選擇飲料店，即可解鎖點餐區塊！")
    else:
        st.markdown(f"### 📝 步驟 2：開始點餐 ({st.session_state.shop_name})")
        
        # 這裡根據第一頁選的裝置，呈現不同排版的預留區塊
        if st.session_state.device_type == "手機版":
            st.warning("📱 【手機版排版區】接下來這裡會設計成適合手機螢幕、不用左右滑動的點餐卡片。")
        else:
            st.success("💻 【網頁版排版區】接下來這裡會設計成寬敞的點餐大表格。")
