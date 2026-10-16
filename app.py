import streamlit as st
import datetime

# ==========================================
# 1. 頁面基本設定與視覺風格
# ==========================================
st.set_page_config(page_title="辦公室訂飲料系統", page_icon="🧋", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@700;900&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Zen Maru Gothic', sans-serif !important;
        font-weight: 700 !important;
    }
    .main-title {
        text-align: center;
        font-size: clamp(2rem, 8vw, 3.5rem); 
        font-weight: 900;
        color: #5A544B; 
        margin-bottom: 10px;
    }
    .sub-title {
        text-align: center;
        color: #8B9A92; 
        font-size: clamp(1.1rem, 4vw, 1.5rem);
        margin-bottom: 40px;
    }
    div[data-testid="stButton"] > button {
        background-color: #A3B19B !important; 
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 16px !important; 
        height: 70px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05) !important;
        transition: all 0.3s ease !important;
    }
    div[data-testid="stButton"] > button:hover {
        background-color: #8F9E87 !important; 
        transform: translateY(-3px); 
        box-shadow: 0 6px 12px rgba(0,0,0,0.1) !important;
    }
    div[data-testid="stButton"] > button p {
        font-size: 1.3rem !important;
        font-weight: 900 !important;
        letter-spacing: 2px;
    }
    header[data-testid="stHeader"] { display: none !important; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 飲料店菜單資料庫 (Dictionary 架構)
# ==========================================
# 之後你要新增品項，只要照著這個格式打字加進去就可以了！
SHOP_MENUS = {
    "50嵐": ["波霸奶茶", "珍珠奶茶", "四季春青茶", "黃金烏龍", "冰淇淋紅茶", "旺來紅", "燕麥紅茶拿鐵"],
    "可不可熟成紅茶": ["熟成紅茶", "春芽綠茶", "胭脂紅茶", "熟成歐蕾", "白玉歐蕾", "春梅冰茶", "冷露歐蕾"],
    "麻古茶坊": ["楊枝甘露2.0", "芝芝芒果果粒", "香橙果粒茶", "葡萄柚果粒蜜茶", "高山金萱茶", "波霸紅茶拿鐵"],
    "迷客夏": ["珍珠紅茶拿鐵", "柳丁綠茶", "蜜桃烏龍", "大正紅茶拿鐵", "芋頭鮮奶", "手炒黑糖鮮奶"],
    "得正": ["紅茶", "綠茶", "春烏龍", "輕烏龍", "焙烏龍", "檸檬春烏龍", "芝士奶蓋春烏龍"],
    "清心福全": ["烏龍綠茶", "特級綠茶", "珍珠奶茶", "優多綠茶", "隱藏版(珍珠蜂蜜鮮奶普洱)", "冰淇淋紅茶"],
    "茶湯會": ["蜜香紅茶", "鐵觀音拿鐵", "翡翠檸檬", "碳烤鐵觀音", "觀音拿鐵/珍珠", "黃金蕎麥"],
    "其他 (自行輸入)": ["請手動輸入飲料名稱"] 
}

# 共通的甜度與冰塊選項
SUGAR_OPTIONS = ["正常糖", "少糖(7分)", "半糖(5分)", "微糖(3分)", "一分糖", "無糖"]
ICE_OPTIONS = ["正常冰", "少冰", "微冰", "去冰", "完全去冰", "常溫", "溫", "熱"]

# ==========================================
# 3. 初始化 Session State
# ==========================================
if "page" not in st.session_state:
    st.session_state.page = "home"
if "order_date" not in st.session_state:
    st.session_state.order_date = datetime.date.today()
if "shop_name" not in st.session_state:
    st.session_state.shop_name = ""
if "device_type" not in st.session_state:
    st.session_state.device_type = ""
if "orders" not in st.session_state:
    st.session_state.orders = [] # 用來存大家點的飲料

# ==========================================
# 4. 第一頁：極簡首頁 (只選裝置)
# ==========================================
if st.session_state.page == "home":
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
# 5. 第二頁：設定訂單與點餐區
# ==========================================
elif st.session_state.page == "order":
    col_back, col_title = st.columns([1, 4])
    with col_back:
        if st.button("⬅️ 返回首頁"):
            st.session_state.page = "home"
            st.rerun()
    with col_title:
        st.markdown(f"<div style='text-align: right; color: #8B9A92; padding-top: 20px;'>模式：{st.session_state.device_type}</div>", unsafe_allow_html=True)
        
    st.markdown("---")
    
    st.markdown("### 📋 步驟 1：確認訂單資訊")
    col_date, col_shop = st.columns(2)
    with col_date:
        st.session_state.order_date = st.date_input("📅 選擇訂購日期", value=st.session_state.order_date)
        
    with col_shop:
        # 這裡的選項自動抓取字典裡面的 key (也就是店家名稱)
        shop_options = ["請選擇..."] + list(SHOP_MENUS.keys())
        selected_shop = st.selectbox("🏪 選擇飲料店", options=shop_options)
        
    if selected_shop == "其他 (自行輸入)":
        custom_shop = st.text_input("✍️ 請輸入飲料店名稱：")
        st.session_state.shop_name = custom_shop
    else:
        st.session_state.shop_name = selected_shop if selected_shop != "請選擇..." else ""

    st.markdown("---")
    
    # 步驟 2：點餐表單區塊
    if st.session_state.shop_name == "":
        st.info("👆 請先在上方選擇飲料店，即可解鎖點餐區塊！")
    else:
        st.markdown(f"### 📝 步驟 2：開始點餐 ({st.session_state.shop_name})")
        
        # 決定要顯示的菜單清單
        # 如果是手動輸入的店，就提供一個手動輸入的框框
        current_menu = SHOP_MENUS.get(selected_shop, [])
        
        with st.container(border=True):
            col_name, col_drink = st.columns(2)
            with col_name:
                user_name = st.text_input("👤 您的姓名 (必填)")
            
            with col_drink:
                if selected_shop == "其他 (自行輸入)":
                    drink_item = st.text_input("🥤 請輸入飲料名稱 (必填)")
                else:
                    drink_item = st.selectbox("🥤 選擇飲料", options=current_menu)
            
            col_sugar, col_ice, col_note = st.columns([1, 1, 2])
            with col_sugar:
                sugar_level = st.selectbox("🍬 甜度", options=SUGAR_OPTIONS, index=2) # 預設半糖
            with col_ice:
                ice_level = st.selectbox("🧊 冰塊", options=ICE_OPTIONS, index=3) # 預設去冰
            with col_note:
                notes = st.text_input("📝 備註 (加料/尺寸大小/其他要求)")

            # 送出訂單按鈕
            if st.button("✅ 確認送出我的點餐", use_container_width=True):
                if user_name.strip() == "" or drink_item.strip() == "":
                    st.error("⚠️ 姓名和飲料名稱一定要填寫喔！")
                else:
                    # 將這筆訂單存入系統記憶中
                    new_order = {
                        "姓名": user_name,
                        "飲料品項": drink_item,
                        "甜度": sugar_level,
                        "冰塊": ice_level,
                        "備註": notes
                    }
                    st.session_state.orders.append(
