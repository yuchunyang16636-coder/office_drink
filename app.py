import streamlit as st
import datetime
import pandas as pd

# ==========================================
# 1. 頁面基本設定
# ==========================================
st.set_page_config(page_title="辦公室訂飲料系統", page_icon="🧋", layout="centered")

# ==========================================
# 2. 初始化 Session State (用來記憶頁面狀態與變數)
# ==========================================
if "page" not in st.session_state:
    st.session_state.page = "home"
if "order_date" not in st.session_state:
    st.session_state.order_date = datetime.date.today()
if "shop_name" not in st.session_state:
    st.session_state.shop_name = ""
if "device_type" not in st.session_state:
    st.session_state.device_type = "網頁版 (電腦)"

def go_to_order_page():
    st.session_state.page = "order"

def go_to_home():
    st.session_state.page = "home"

# ==========================================
# 3. 畫面設計：第一頁 (設定表單)
# ==========================================
if st.session_state.page == "home":
    st.title("🧋 辦公室下午茶訂購系統")
    st.markdown("### 📋 第一步：請先設定今天的訂單資訊")
    
    st.write("") 
    
    # 變數 1：觀看裝置選擇 (影響後續排版)
    device_options = ["網頁版 (電腦)", "手機版"]
    selected_device = st.radio("📱 請選擇您的觀看裝置", options=device_options, horizontal=True)
    
    # 變數 2：日期選擇
    selected_date = st.date_input("📅 選擇訂購日期", value=st.session_state.order_date)
    
    # 變數 3：飲料店選擇
    shop_options = [
        "請選擇...", "50嵐", "可不可熟成紅茶", "麻古茶坊", 
        "迷客夏", "得正", "清心福全", "茶湯會", "其他 (自行輸入)"
    ]
    selected_shop = st.selectbox("🏪 選擇飲料店", options=shop_options)
    
    custom_shop = ""
    if selected_shop == "其他 (自行輸入)":
        custom_shop = st.text_input("✍️ 請輸入飲料店名稱：")
    
    st.write("") 
    
    # 進入下一步的按鈕
    if st.button("建立訂單，進入點餐畫面 ➡️", type="primary", use_container_width=True):
        final_shop_name = custom_shop if selected_shop == "其他 (自行輸入)" else selected_shop
        
        if final_shop_name == "請選擇..." or final_shop_name.strip() == "":
            st.error("⚠️ 請選擇或輸入飲料店名稱喔！")
        else:
            st.session_state.order_date = selected_date
            st.session_state.shop_name = final_shop_name
            st.session_state.device_type = selected_device
            go_to_order_page()
            st.rerun()

# ==========================================
# 4. 畫面設計：第二頁 (大家填寫點餐明細的地方)
# ==========================================
elif st.session_state.page == "order":
    st.title(f"📝 {st.session_state.shop_name} - 點餐表")
    
    # 顯示目前設定狀態
    st.markdown(f"**📅 日期：** {st.session_state.order_date.strftime('%Y-%m-%d')} | **🖥️ 模式：** {st.session_state.device_type}")
    st.markdown("---")
    
    # 根據不同裝置，顯示不同的排版提示 (這裡我們先做排版區隔的測試)
    if st.session_state.device_type == "手機版":
        st.info("📱 目前為【手機版】模式。未來的飲料清單會以「垂直卡片」的方式往下排列，方便單手滑動觀看！")
        # 手機版排版預留區
    else:
        st.success("💻 目前為【網頁版】模式。未來的飲料清單會以「滿版大表格」呈現，方便一眼看清楚所有人點了什麼！")
        # 網頁版排版預留區

    st.markdown("---")
    if st.button("⬅️ 返回修改設定"):
        go_to_home()
        st.rerun()
