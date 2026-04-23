#!/usr/bin/env python3
"""
🎢 FamilyGo - 親子旅遊推薦平台
自動關鍵字搜尋
"""

import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="🎢 FamilyGo 親子遊", page_icon="🎢", layout="wide")

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) Chrome/120'}

# ========================
# 自動關鍵字搜尋
# ========================
AUTO_KEYWORDS = [
    '台北 親子景點 ptt',
    '台灣 親子公園推薦',
    '台北 親子餐廳 ptt',
    '新北 親子景點 2024',
    '中部 親子樂園推薦',
    '宜蘭 親子農場 評價',
    '高雄 親子景點 推薦',
]

def auto_search():
    """自動搜尋多個關鍵字"""
    all_results = []
    
    for query in AUTO_KEYWORDS:
        try:
            # Try direct URL first (simpler)
            url = f'https://www.google.com/search?q={query.replace(\" \", \"+\")}&hl=zh-TW'
            resp = requests.get(url, headers=HEADERS, timeout=8)
            
            if resp.status_code == 200:
                # Simple check - if we got content with the keyword
                if query.split()[0] in resp.text[:5000]:
                    all_results.append({
                        'name': f'{query}',
                        'city': query.split()[0],
                        'type': '搜尋結果',
                        'age': '全年齡',
                        'tags': ['👶', '🧒'],
                        'time': '依官網',
                        'desc': f'關鍵字: {query}',
                        'source': 'google'
                    })
        except:
            pass
    
    return all_results

def search_static():
    """靜態景點庫"""
    return [
        # 台北
        {'name': '台北市立兒童新樂園', 'city': '台北', 'type': '樂園', 'age': '3-12歲',
         'tags': ['👶', '🚼', '🧒', '🅿️', '🎢'], 'time': '09:00-17:00',
         'desc': '室內外遊樂設施，超多遊戲', 'source': 'static'},
        
        {'name': '國立科教館', 'city': '台北', 'type': '博物館', 'age': '3-15歲',
         'tags': ['👶', '🧒', '🅿️', '🔬'], 'time': '09:00-17:00',
         'desc': '恐龍標本、科學實驗', 'source': 'static'},
        
        {'name': '台北市立動物園', 'city': '台北', 'type': '動物園', 'age': '全年齡',
         'tags': ['👶', '🧒', '🅿️', '🦁'], 'time': '09:00-17:00',
         'desc': '無尾熊、貓熊超萌', 'source': 'static'},
        
        {'name': '華山1914文創園區', 'city': '台北', 'type': '室內', 'age': '全年齡',
         'tags': ['👶', '🧒', '☕', '🎭'], 'time': '10:00-18:00',
         'desc': '文創活動、常設展', 'source': 'static'},
        
        {'name': '大安森林公園', 'city': '台北', 'type': '公園', 'age': '全年齡',
         'tags': ['👶', '🚼', '🌳', '🅿️'], 'time': '全天',
         'desc': '共融遊戲場、溜滑梯', 'source': 'static'},
        
        {'name': '青年公園', 'city': '台北', 'type': '公園', 'age': '全年齡',
         'tags': ['👶', '🚼', '🧒', '🅿️'], 'time': '全天',
         'desc': '遊戲設施、戲水池', 'source': 'static'},
        
        # 新北
        {'name': '十三行博物館', 'city': '新北', 'type': '博物館', 'age': '全年齡',
         'tags': ['👶', '🧒', '🏺'], 'time': '09:00-17:00',
         'desc': '考古體驗、VR互動', 'source': 'static'},
        
        {'name': '野柳海洋世界', 'city': '新北', 'type': '水族館', 'age': '3-15歲',
         'tags': ['👶', '🐬', '🅿️'], 'time': '09:00-17:00',
         'desc': '海豚表演秀', 'source': 'static'},
        
        {'name': '淡水兒福中心', 'city': '新北', 'type': '室內', 'age': '0-12歲',
         'tags': ['👶', '🚼', '🧒', '🎠'], 'time': '09:00-17:00',
         'desc': '免費室內遊戲室', 'source': 'static'},
        
        # 台中
        {'name': '科教館', 'city': '台中', 'type': '博物館', 'age': '全年齡',
         'tags': ['👶', '🚼', '🅿️', '🔬'], 'time': '09:00-17:00',
         'desc': '恐龍標本、全 台最大', 'source': 'static'},
        
        {'name': '麗寶樂園', 'city': '台中', 'type': '樂園', 'age': '4-15歲',
         'tags': ['👶', '🎢', '🅿️'], 'time': '09:30-17:00',
         'desc': '中部最大主題樂園', 'source': 'static'},
        
        # 高雄
        {'name': '科工館', 'city': '高雄', 'type': '博物館', 'age': '3-15歲',
         'tags': ['👶', '🚼', '🅿️'], 'time': '09:00-17:00',
         'desc': '兒童科學.gz樂園', 'source': 'static'},
        
        {'name': '旗津海水浴場', 'city': '高雄', 'type': '海邊', 'age': '全年齡',
         'tags': ['👶', '🏖️', '🧒', '🅿️'], 'time': '全天',
         'desc': '沙灘、騎單車', 'source': 'static'},
        
        # 宜蘭
        {'name': '斑溝休閒農場', 'city': '宜蘭', 'type': '農場', 'age': '全年齡',
         'tags': ['👶', '🐑', '🅿️'], 'time': '09:00-17:00',
         'desc': '餵小鹿、梅花鼠', 'source': 'static'},
        
        {'name': '傳統藝術中心', 'city': '宜蘭', 'type': '室內', 'age': '全年齡',
         'tags': ['👶', '🧒', '🎭'], 'time': '09:00-18:00',
         'desc': '傳統技藝DIY', 'source': 'static'},
        
        {'name': '甲子湖休閒農場', 'city': '宜蘭', 'type': '農場', 'age': '全年齡',
         'tags': ['👶', '🐰', '🅿️'], 'time': '09:00-17:00',
         'desc': '小兔子、小羊', 'source': 'static'},
    ]

def get_all():
    """整合"""
    # 嘗試自動搜尋
    results = []
    try:
        results = auto_search()
    except:
        pass
    
    # 加入靜態庫
    results.extend(search_static())
    
    # 去重
    seen = set()
    unique = []
    for p in results:
        if p['name'] not in seen:
            seen.add(p['name'])
            unique.append(p)
    
    return unique

# ========================
# 主程式
# ========================
def main():
    st.title("🎢 FamilyGo 親子遊")
    st.markdown("### 🌐 自動搜尋 + 經典景點庫")
    st.markdown("---")
    
    with st.sidebar:
        st.header("🔍 篩選")
        city = st.selectbox("縣市", ["全部", "台北", "新北", "台中", "高雄", "宜蘭"])
        ptype = st.selectbox("類型", ["全部", "公園", "樂園", "博物館", "農場", "室內", "海邊"])
        
        st.markdown("### 🎯 設施")
        need_nursing = st.checkbox("👶 哺乳室")
        need_diaper = st.checkbox("🚼 尿布台")
        need_parking = st.checkbox("🅿️ 停車場")
        
        st.markdown("---")
        if st.button("🔄 重新整理", type="primary"):
            st.rerun()
    
    # 自動載入
    with st.spinner("🔄 載入景點..."):
        results = get_all()
    
    # 篩選
    if city != "全部":
        results = [p for p in results if p.get("city") == city]
    if ptype != "全部":
        results = [p for p in results if ptype in p.get("type", "")]
    if need_nursing:
        results = [p for p in results if "👶" in p.get("tags", [])]
    if need_diaper:
        results = [p for p in results if "🚼" in p.get("tags", [])]
    if need_parking:
        results = [p for p in results if "🅿️" in p.get("tags", [])]
    
    st.header(f"📍 共 {len(results)} 個景點")
    
    for p in results:
        e = "🌐" if p.get("source") != "static" else "📍"
        with st.expander(f"{e} {p['name']} ({p.get('city', '')})"):
            st.markdown(f"**標籤**: {' '.join(p.get('tags', []))}")
            st.markdown(f"**說明**: {p.get('desc', '')}")
            st.markdown(f"**時間**: {p.get('time', '')}")
            st.markdown(f"**類型**: {p.get('type', '')}")
            st.caption(f"**來源**: {p.get('source', '')}")
    
    # 統計
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("總", len(results))
    col2.metric("台北", len([p for p in results if p.get("city") == "台北"]))
    col3.metric("宜蘭", len([p for p in results if p.get("city") == "宜蘭"]))
    col4.metric("台中", len([p for p in results if p.get("city") == "台中"]))
    
    st.caption(f"📅 更新: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

if __name__ == "__main__":
    main()