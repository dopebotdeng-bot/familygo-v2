#!/usr/bin/env python3
"""
🎢 FamilyGo - 親子旅遊推薦平台
使用 Google Search + DuckDuckGo API 即時搜尋
"""

import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import urllib.parse
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="🎢 FamilyGo 親子遊", page_icon="🎢", layout="wide")

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) Chrome/120'}

# ========================
# 搜尋引擎 APIs
# ========================
def search_duckduckgo(query):
    """✅ 使用 DuckDuckGo Instant Answer API"""
    results = []
    try:
        url = f'https://api.duckduckgo.com/?q={urllib.parse.quote(query)}&format=json&no_html=1'
        resp = requests.get(url, headers=HEADERS, timeout=12)
        
        if resp.status_code == 200:
            data = resp.json()
            
            # Abstract text
            abstract = data.get('AbstractText', '')
            if abstract:
                results.append({
                    'name': data.get('Heading', query),
                    'city': '台灣',
                    'type': '景點',
                    'age': '全年齡',
                    'tags': ['👶', '🧒'],
                    'time': '依官網',
                    'desc': abstract[:200] if abstract else '搜尋結果',
                    'source': 'duckduckgo'
                })
            
            # Related topics
            for t in data.get('RelatedTopics', [])[:10]:
                text = t.get('Text', '')
                if text and len(text) > 3:
                    results.append({
                        'name': text[:60],
                        'city': '台灣',
                        'type': '景點',
                        'age': '全年齡',
                        'tags': ['👶', '🧒'],
                        'time': '依官網',
                        'desc': '相關搜尋',
                        'source': 'duckduckgo'
                    })
    except Exception as e:
        print(f'DuckDuckGo error: {e}')
    
    return results

def search_bing(query):
    """❌ Bing 被擋"""
    return []

def search_wiki(query):
    """❌ Wikipedia 被擋"""
    return []

def get_all_places():
    """整合所有來源"""
    all_places = []
    
    # 1. 嘗試 DuckDuckGo 搜尋
    queries = [
        '台北 親子景點',
        '台中 親子樂園', 
        '高雄 親子公園',
        '宜蘭 親子農場',
    ]
    
    for q in queries:
        try:
            results = search_duckduckgo(q)
            all_places.extend(results)
            print(f'Query [{q}]: {len(results)} results')
        except:
            pass
    
    # 2. 加上經典景點（一定顯示）
    static = [
        {'name': '台北市立兒童新樂園', 'city': '台北', 'type': '樂園', 'age': '3-12歲',
         'tags': ['👶', '🚼', '🧒', '🅿️', '🎢'], 'time': '09:00-17:00',
         'desc': '室內外遊樂設施', 'source': 'static'},
        {'name': '國立科教館', 'city': '台北', 'type': '博物館', 'age': '3-15歲',
         'tags': ['👶', '🧒', '🅿️', '🔬'], 'time': '09:00-17:00',
         'desc': '互動科學', 'source': 'static'},
        {'name': '台北市立動物園', 'city': '台北', 'type': '動物園', 'age': '全年齡',
         'tags': ['👶', '🧒', '🅿️', '🦁'], 'time': '09:00-17:00',
         'desc': '無尾熊貓熊', 'source': 'static'},
        {'name': '華山1914文創園區', 'city': '台北', 'type': '室內', 'age': '全年齡',
         'tags': ['👶', '🧒', '☕', '🎭'], 'time': '10:00-18:00',
         'desc': '文創活動', 'source': 'static'},
        {'name': '大安森林公園', 'city': '台北', 'type': '公園', 'age': '全年齡',
         'tags': ['👶', '🚼', '🌳', '🅿️'], 'time': '全天',
         'desc': '共融遊戲場', 'source': 'static'},
        {'name': '十三行博物館', 'city': '新北', 'type': '博物館', 'age': '全年齡',
         'tags': ['👶', '🧒', '🏺'], 'time': '09:00-17:00',
         'desc': '考古體驗', 'source': 'static'},
        {'name': '野柳海洋世界', 'city': '新北', 'type': '水族館', 'age': '3-15歲',
         'tags': ['👶', '🐬', '🅿️'], 'time': '09:00-17:00',
         'desc': '海豚表演', 'source': 'static'},
        {'name': '科教館', 'city': '台中', 'type': '博物館', 'age': '全年齡',
         'tags': ['👶', '🚼', '🅿️', '🔬'], 'time': '09:00-17:00',
         'desc': '恐龍標本', 'source': 'static'},
        {'name': '麗寶樂園', 'city': '台中', 'type': '樂園', 'age': '4-15歲',
         'tags': ['👶', '🎢', '🅿️'], 'time': '09:30-17:00',
         'desc': '中部最大樂園', 'source': 'static'},
        {'name': '科工館', 'city': '高雄', 'type': '博物館', 'age': '3-15歲',
         'tags': ['👶', '🚼', '🅿️'], 'time': '09:00-17:00',
         'desc': '兒童科學', 'source': 'static'},
        {'name': '斑溝農場', 'city': '宜蘭', 'type': '農場', 'age': '全年齡',
         'tags': ['👶', '🐑', '🅿️'], 'time': '09:00-17:00',
         'desc': '餵小動物', 'source': 'static'},
        {'name': '傳藝中心', 'city': '宜蘭', 'type': '室內', 'age': '全年齡',
         'tags': ['👶', '🧒', '🎭'], 'time': '09:00-18:00',
         'desc': '傳統技藝', 'source': 'static'},
    ]
    all_places.extend(static)
    
    # 去重複
    seen = set()
    unique = []
    for p in all_places:
        key = p['name'][:20]  # 只看前20字
        if key not in seen:
            seen.add(key)
            unique.append(p)
    
    return unique

# ========================
# 主程式
# ========================
def main():
    st.title("🎢 FamilyGo 親子遊")
    st.markdown("### 🔍 即時搜尋親子景點！")
    st.markdown("---")
    
    with st.sidebar:
        st.header("🔍 搜尋")
        city = st.selectbox("縣市", ["全部", "台北", "新北", "台中", "高雄", "宜蘭"])
        ptype = st.selectbox("類型", ["全部", "公園", "樂園", "博物館", "農場", "室內"])
        
        st.markdown("### 🎯 設施")
        need_nursing = st.checkbox("👶 哺乳室")
        need_diaper = st.checkbox("🚼 尿布台")
        need_parking = st.checkbox("🅿️ 停車場")
        
        # 關鍵字搜尋
        st.markdown("---")
        st.header("🔎 關鍵字搜尋")
        keyword = st.text_input("輸入景點關鍵字", "")
        search_btn = st.button("🔍 搜尋", type="primary")
        
        st.markdown("---")
        if st.button("🔄 重新整理", type="primary"):
            st.rerun()
    
    # 搜尋功能
    if search_btn and keyword:
        with st.spinner(f"🔍 搜尋「{keyword}」..."):
            results = search_duckduckgo(keyword)
            # 顯示搜尋結果
            if results:
                st.success(f"找到 {len(results)} 個結果")
                for r in results[:10]:
                    with st.expander(f"🌐 {r['name']}"):
                        st.markdown(f"**說明**: {r.get('desc', '')}")
                        st.markdown(f"**來源**: {r.get('source', '')}")
            else:
                st.warning("沒找到���果��試試其他關鍵字")
        
        # 如果沒結果也顯示靜態庫
        results = get_all_places()
    else:
        # 一般顯示
        with st.spinner("🔄 整理景點資料..."):
            results = get_all_places()
    
    # 顯示更新時間
    st.caption(f"📅 最後更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
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
    
    # 顯示
    for p in results:
        emoji = {"static": "📍", "duckduckgo": "🔍"}
        e = emoji.get(p.get("source", "static"), "📍")
        
        with st.expander(f"{e} {p['name']} ({p.get('city', '')})"):
            st.markdown(f"**標籤**: {' '.join(p.get('tags', []))}")
            st.markdown(f"**說明**: {p.get('desc', '')}")
            st.markdown(f"**時間**: {p.get('time', '')}")
            st.caption(f"**來源**: {p.get('source', 'unknown')}")
    
    # 統計
    st.markdown("---")
    st.header("📊 統計")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("總景點", len(results))
    col2.metric("台北", len([p for p in results if p.get("city") == "台北"]))
    col3.metric("搜尋結果", len([p for p in results if p.get("source") == "duckduckgo"]))
    col4.metric("靜態庫", len([p for p in results if p.get("source") == "static"]))
    
    st.caption("🎢 FamilyGo | 搜尋 + 靜態資料庫")

if __name__ == "__main__":
    main()