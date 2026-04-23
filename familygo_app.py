#!/usr/bin/env python3
"""
🎢 FamilyGo - 親子旅遊推薦平台
MVP Web 版本
"""

import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="🎢 FamilyGo 親子遊", page_icon="🎢", layout="wide")

# ========================
# 親子景點資料庫
# ========================
PLACES = [
    # 台北
    {"name": "台北市立兒童新樂園", "city": "台北", "type": "樂園", "age": "3-12歲",
     "tags": ["👶", "🚼", "🧒", "🅿️"], "time": "09:00-17:00",
     "desc": "室內外遊樂設施豐富，適合小童"},
    {"name": "科教館", "city": "台北", "type": "博物館", "age": "3-15歲",
     "tags": ["👶", "🧒", "🎠", "🅿️"], "time": "09:00-17:00",
     "desc": "互動科學體驗，孩子最愛"},
    {"name": "市立動物園", "city": "台北", "type": "動物園", "age": "全年齡",
     "tags": ["👶", "🧒", "🅿️", "🦁"], "time": "09:00-17:00",
     "desc": "無尾熊、貓熊超萌"},
    {"name": "華山文創", "city": "台北", "type": "室內", "age": "全年齡",
     "tags": ["👶", "🧒", "☕"], "time": "10:00-18:00",
     "desc": "文創園區，常有親子活動"},
    {"name": "大安森林公園", "city": "台北", "type": "公園", "age": "全年齡",
     "tags": ["👶", "🚼", "🧒", "🌳"], "time": "全天",
     "desc": "共融遊戲場，木屑鋪面"},
    
    # 新北
    {"name": "野柳海洋世界", "city": "新北", "type": "水族館", "age": "3-15歲",
     "tags": ["👶", "🐬", "🅿️"], "time": "09:00-17:00",
     "desc": "海豚表演秀"},
    {"name": "淡水兒福中心", "city": "新北", "type": "室內", "age": "0-12歲",
     "tags": ["👶", "🚼", "🧒", "🎠"], "time": "09:00-17:00",
     "desc": "免費室內遊戲室"},
    {"name": "八里十三行", "city": "新北", "type": "博物館", "age": "全年齡",
     "tags": ["👶", "🧒", "🏺"], "time": "09:00-17:00",
     "desc": "考古體驗，戶外溜滑梯"},
    
    # 台中
    {"name": "科博館", "city": "台中", "type": "博物館", "age": "全年齡",
     "tags": ["👶", "🚼", "🧒", "🅿️", "🔬"], "time": "09:00-17:00",
     "desc": "恐龍標本超震撼"},
    {"name": "麗寶樂園", "city": "台中", "type": "樂園", "age": "4-15歲",
     "tags": ["👶", "🎢", "🧒", "🅿️"], "time": "09:30-17:00",
     "desc": "中部最大樂園"},
    {"name": "921地震教育園區", "city": "台中", "type": "博物館", "age": "6-15歲",
     "tags": ["🧒", "🏺", "🅿️"], "time": "09:00-17:00",
     "desc": "地震體驗， 教育意義"},
    
    # 高雄
    {"name": "旗津海水浴場", "city": "高雄", "type": "海邊", "age": "全年齡",
     "tags": ["👶", "🏖️", "🧒", "🅿️"], "time": "全天",
     "desc": "沙灘、騎單車"},
    {"name": "科工館", "city": "高雄", "type": "博物館", "age": "3-15歲",
     "tags": ["👶", "🚼", "🧒", "🅿️"], "time": "09:00-17:00",
     "desc": "儿童科學天堂"},
    
    # 宜蘭
    {"name": "員山森林生態", "city": "宜蘭", "type": "農場", "age": "全年齡",
     "tags": ["👶", "🐑", "🧒", "🅿️"], "time": "09:00-17:00",
     "desc": "餵小鹿、梅花鼠"},
    {"name": "甲子湖休閒農場", "city": "宜蘭", "type": "農場", "age": "全年齡",
     "tags": ["👶", "🐰", "🧒", "🅿️"], "time": "09:00-17:00",
     "desc": "小兔子超可愛"},
    {"name": "傳藝中心", "city": "宜蘭", "type": "室內", "age": "全年齡",
     "tags": ["👶", "🧒", "🎭", "🅿️"], "time": "09:00-18:00",
     "desc": "傳統技藝體驗"},
]

# ========================
# 特色標籤說明
# ========================
TAGS = {
    "👶": "哺乳室",
    "🚼": "親子廁所/尿布台",
    "🍼": "奶粉/沖泡區",
    "🧒": "兒童椅/孩童設施",
    "🅿️": "停車場",
    "🎢": "溜滑梯",
    "🎠": "旋轉木馬",
    "🏖️": "沙灘",
    "🐬": "海洋生物",
    "🦁": "動物",
    "🐑": "綿羊/山羊",
    "🐰": "兔子",
    "🌳": "戶外公園",
    "☕": "家長休息區",
    "🔬": "科學體驗",
    "🏺": "文化教育",
    "🎭": "表演藝術",
}

# ========================
# 主程式
# ========================
def main():
    st.title("🎢 FamilyGo 親子遊")
    st.markdown("### 找不到地方帶孩子玩？這裡幫你整理好了！")
    st.markdown("---")
    
    # 側邊欄
    with st.sidebar:
        st.header("🔍 搜尋條件")
        
        # 縣市
        city = st.selectbox("縣市", ["全部", "台北", "新北", "台中", "高雄", "宜蘭", "台南", "桃園"])
        
        # 類型
        ptype = st.selectbox("類型", ["全部", "公園", "樂園", "博物館", "農場", "動物園", "海邊", "室內"])
        
        # 年齡
        age = st.select_slider("兒童年齡", options=["全部", "0-3歲", "3-6歲", "6-12歲", "12歲以上"])
        
        # 設施篩選
        st.markdown("### 🎯 必備設施")
        need_nursing = st.checkbox("👶 哺乳室")
        need_diaper = st.checkbox("🚼 尿布台")
        need_parking = st.checkbox("🅿️ 停車場")
        
        # 收藏
        st.markdown("---")
        if "favorites" not in st.session_state:
            st.session_state.favorites = []
        
        st.header("❤️ 收藏清單")
        if st.session_state.favorites:
            for fav in st.session_state.favorites:
                st.markdown(f"- {fav}")
        else:
            st.info("還沒收藏任何景點")
    
    # 搜尋結果
    results = PLACES.copy()
    
    # 篩選
    if city != "全部":
        results = [p for p in results if p["city"] == city]
    if ptype != "全部":
        results = [p for p in results if p["type"] == ptype]
    
    # 設施篩選
    if need_nursing:
        results = [p for p in results if "👶" in p["tags"]]
    if need_diaper:
        results = [p for p in results if "🚼" in p["tags"]]
    if need_parking:
        results = [p for p in results if "🅿️" in p["tags"]]
    
    # 顯示結果
    st.header(f"📍 找到 {len(results)} 個景點")
    
    for place in results:
        with st.expander(f"{place['name']} ({place['city']})", expanded=False):
            # 標籤
            tags_str = " ".join(place["tags"])
            st.markdown(f"**標籤**: {tags_str}")
            
            # 說明
            st.markdown(f"**說明**: {place['desc']}")
            st.markdown(f"**年齡**: {place['age']}")
            st.markdown(f"**時間**: {place['time']}")
            
            # 收藏按鈕
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"❤️ 收藏", key=f"fav_{place['name']}"):
                    if place["name"] not in st.session_state.favorites:
                        st.session_state.favorites.append(place["name"])
                        st.rerun()
            with col2:
                st.markdown(f"**類型**: {place['type']}")
    
    # 統計
    st.markdown("---")
    st.header("📊 景點統計")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("總景點", len(PLACES))
    col2.metric("台北", len([p for p in PLACES if p["city"] == "台北"]))
    col3.metric("有哺乳室", len([p for p in PLACES if "👶" in p["tags"]]))
    col4.metric("有停車場", len([p for p in PLACES if "🅿️" in p["tags"]]))
    
    # 標籤說明
    st.markdown("---")
    st.header("🏷️ 標籤說明")
    
    tags_df = pd.DataFrame([{"標籤": k, "說明": v} for k, v in TAGS.items()])
    st.dataframe(tags_df, hide_index=True, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.caption("🎢 FamilyGo 親子遊 | 幫爸爸媽媽解決帶孩子去哪玩的問題！")

if __name__ == "__main__":
    main()