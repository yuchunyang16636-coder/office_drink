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
    
    /* 價格顯示的特別樣式 */
    .price-tag {
        font-size: 1.5rem;
        color: #d9534f;
        font-weight: 900;
        background: #fdf2f2;
        padding: 5px 15px;
        border-radius: 10px;
        display: inline-block;
        margin-top: 10px;
        border: 2px dashed #d9534f;
    }
    
    header[data-testid="stHeader"] { display: none !important; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 飲料店菜單資料庫 (加入價格與尺寸)
# ==========================================
# 格式說明: "飲料名稱": {"尺寸": 價格}
SHOP_MENUS = {
    "50嵐": {
        "茉莉綠茶": {"M": 30, "L": 35},
        "四季春青茶": {"M": 30, "L": 35},
        "波霸奶茶": {"M": 40, "L": 55},
        "紅茶拿鐵": {"M": 50, "L": 65},
        "8冰綠": {"M": 40, "L": 55},
        "冰淇淋紅茶": {"M": 40, "L": 55}
    },
    "可不可熟成紅茶": {
        "熟成紅茶": {"M": 30, "L": 35},
        "春芽綠茶": {"M": 30, "L": 35},
        "熟成歐蕾": {"M": 55, "L": 65},
        "白玉歐蕾": {"M": 60, "L": 70},
        "胭脂紅茶": {"M": 40, "L": 45},
        "春梅冰茶": {"M": 45, "L": 55}
    },
    "得正": {
        "紅茶": {"M": 25, "L": 30},
        "春烏龍": {"M": 30, "L": 35},
        "焙烏龍": {"M": 30, "L": 35},
        "奶茶": {"M": 45, "L": 50},
        "芝士奶蓋春烏龍": {"M": 50, "L": 60},
        "檸檬春烏龍": {"M": 55, "L": 65}
    },
    "迷客夏": {
        "大正紅茶拿鐵": {"M": 50, "L": 60},
        "珍珠紅茶拿鐵": {"M": 60, "L": 70},
        "芋頭鮮奶": {"M": 65, "L": 85},
        "娜杯紅茶": {"L": 40},
        "柳丁綠茶": {"L": 65},
        "蜜桃烏龍": {"L": 70}
    },
    "麻古茶坊": {
        "高山金萱茶": {"L": 30},
        "波霸紅茶拿鐵": {"L": 65},
        "香橙果粒茶": {"L": 75},
        "葡萄柚果粒蜜茶": {"L": 70},
        "芝芝芒果果粒": {"L": 95},
        "楊枝甘露2.0": {"L": 85}
    },
    "清心福全": {
        "烏龍綠茶": {"M": 30, "L": 35},
        "珍珠奶茶": {"M": 45, "L": 55},
        "冰淇淋紅茶": {"M": 45, "L": 55},
        "梅子綠茶": {"M": 40, "L": 50},
        "優多綠茶": {"L": 50},
        "隱藏版(珍珠蜂蜜鮮奶普洱)": {"M": 50, "L": 70}
    },
    "茶湯會": {
        "蜜香紅茶": {"預設尺寸": 35},
        "碳烤鐵觀音": {"預設尺寸": 40},
        "翡翠檸檬": {"預設尺寸": 65},
        "觀音拿鐵": {"預設尺寸": 70},
        "粉粿蕎麥四季春": {"預設尺寸": 60},
        "觀音雙Q拿鐵": {"預設尺寸": 75}
    },
    "其他 (自行輸入)": {} 
}

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
    st.session_state.orders = [] 

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
        
        with st.container(border=True):
            col_name, col_drink = st.columns(2)
            with col_name:
                user_name = st.text_input("👤 您的姓名 (必填)")
            
            with col_drink:
                # 處理飲料選擇與連動價格
                if selected_shop == "其他 (自行輸入)":
                    drink_item = st.text_input("🥤 請輸入飲料名稱 (必填)")
                else:
                    current_menu = list(SHOP_MENUS[selected_shop].keys())
                    drink_item = st.selectbox("🥤 選擇飲料", options=current_menu)
            
            col_size, col_sugar, col_ice = st.columns([1, 1, 1])
            with col_size:
                if selected_shop == "其他 (自行輸入)":
                    selected_size = st.selectbox("📏 尺寸", options=["M", "L", "預設"])
                    # 手動輸入價格
                    price = st.number_input("💰 自訂價格 (元)", min_value=0, value=50)
                else:
                    # 抓取該飲料有的尺寸與價格
                    available_sizes = SHOP_MENUS[selected_shop][drink_item]
                    selected_size = st.selectbox("📏 尺寸", options=list(available_sizes.keys()))
                    price = available_sizes[selected_size]
                    
            with col_sugar:
                sugar_level = st.selectbox("🍬 甜度", options=SUGAR_OPTIONS, index=2)
            with col_ice:
                ice_level = st.selectbox("🧊 冰塊", options=ICE_OPTIONS, index=3)
                
            notes = st.text_input("📝 備註 (加料/其他要求，若有加料請將金額加在下方自訂價格中)")
            
            # 顯示連動計算好的價格
            if selected_shop != "其他 (自行輸入)":
                st.markdown(f'<div class="price-tag">總計： NT$ {price}</div>', unsafe_allow_html=True)

            # 送出訂單按鈕
            if st.button("✅ 確認送出我的點餐", use_container_width=True):
                if user_name.strip() == "" or drink_item.strip() == "":
                    st.error("⚠️ 姓名和飲料名稱一定要填寫喔！")
                else:
                    new_order = {
                        "姓名": user_name,
                        "飲料品項": drink_item,
                        "尺寸": selected_size,
                        "甜度": sugar_level,
                        "冰塊": ice_level,
                        "金額": price,
                        "備註": notes
                    }
                    st.session_state.orders.append(new_order)
                    st.success(f"🎉 點餐成功！已將 {user_name} 的 {drink_item} 加入清單。")
