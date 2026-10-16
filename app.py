import streamlit as st
import datetime

# ==========================================
# 1. 頁面基本設定
# ==========================================
st.set_page_config(page_title="辦公室訂飲料系統", page_icon="🧋", layout="centered")

# ==========================================
# 2. 初始化 Session State (用來記憶頁面狀態與變數)
# ==========================================
# 預設停留在首頁 (home)
if "page" not in st.session_state:
    st.session_state.page = "home"

# 記憶日期與飲料店
if "order_date" not in st.session_state:
    st.session_state.order_date = datetime.date.today()
if "shop_name" not in st.session_state:
    st.session_state.shop_name = ""

# 切換頁面的函數
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
    
    st.write("") # 空行排版用
    
    # 變數 1：日期選擇
    selected_date = st.date_input("📅 選擇訂購日期", value=st.session_state.order_date)
    
    # 變數 2：飲料店選擇
    shop_options = [
        "請選擇...", "50嵐", "可不可熟成紅茶", "麻古茶坊", 
        "迷客夏", "得正", "清心福全", "茶湯會", "其他 (自行輸入)"
    ]
    selected_shop = st.selectbox("🏪 選擇飲料店", options=shop_options)
    
    # 如果選擇「其他」，自動彈出文字輸入框讓發起人自己打
    custom_shop = ""
    if selected_shop == "其他 (自行輸入)":
        custom_shop = st.text_input("✍️ 請輸入飲料店名稱：")
    
    st.write("") # 空行排版用
    
    # 進入下一步的按鈕
    if st.button("建立訂單，進入點餐畫面 ➡️", type="primary", use_container_width=True):
        # 檢查是否有選擇飲料店
        final_shop_name = custom_shop if selected_shop == "其他 (自行輸入)" else selected_shop
        
        if final_shop_name == "請選擇..." or final_shop_name.strip() == "":
            st.error("⚠️ 請選擇或輸入飲料店名稱喔！")
        else:
            # 將選擇的變數存入系統記憶中
            st.session_state.order_date = selected_date
            st.session_state.shop_name = final_shop_name
            # 切換到第二頁
            go_to_order_page()
            st.rerun()

# ==========================================
# 4. 畫面設計：第二頁 (大家填寫點餐明細的地方)
# ==========================================
elif st.session_state.page == "order":
    st.title(f"📝 {st.session_state.shop_name} - 點餐表")
    st.markdown(f"**📅 訂單日期：** {st.session_state.order_date.strftime('%Y-%m-%d')}")
    st.markdown("---")
    
    st.success("🎉 成功進入第二頁！我們接下來可以在這裡加入點餐的表格或輸入框。")
    
    # 這裡可以預留未來要寫的點餐表單 (姓名、品項、甜度、冰塊等)
    # ...
    # ...

    st.markdown("---")
    # 提供返回上一頁的按鈕 (方便主揪修改店家)
    if st.button("⬅️ 返回修改店家或日期"):
        go_to_home()
        st.rerun()
