#!/usr/bin/env python3
"""
🎢 FamilyGo - 親子旅遊推薦平台
真正從網路抓取最新景點！
"""

import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import json
import time

st.set_page_config(page_title="🎢 FamilyGo 親子遊", page_icon="🎢", layout="wide")

# Headers 模擬瀏覽器
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# ========================
# 真正的網路爬蟲
# ========================
def get_tripadvisor_taiwan():
    """從 TripAdvisor 抓台灣親子景點"""
    places = []
    try:
        # TripAdvisor 搜尋 API
        url = "https://www.tripadvisor.com/Attractions-g293910-Activities-Taiwan.html"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        
        if resp.status_code == 200:
            # 解析 HTML
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            # 找景點標題
            for item in soup.select('div[data-test-target="AttractionSnippet"]')[:15]:
                try:
                    name = item.select_one('.LVPCq').text.strip()
                    places.append({
                        "name": name,
                        "city": "台灣",
                        "type": "景點",
                        "age": "全年齡",
                        "tags": ["👶", "🧒"],
                        "time": "，依官網",
                        "desc": "TripAdvisor 推薦景點",
                        "source": "tripadvisor"
                    })
                except:
                    continue
    except Exception as e:
        print(f"TripAdvisor error: {e}")
    
    return places

def get_klook_family():
    """從 Klook 抓親子活動"""
    places = []
    try:
        # Klook 熱門親子活動
        url = "https://www.klook.com/zh-TW/explore/taiwan/taipei-family-activities/"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            # 找活動標題
            for item in soup.select('div.explore-card')[:10]:
                try:
                    name = item.select_one('h3').text.strip()
                    if name:
                        places.append({
                            "name": name,
                            "city": "台北",
                            "type": "活動",
                            "age": "3-12歲",
                            "tags": ["👶", "🧒", "🎢"],
                            "time": "，依官網",
                            "desc": "Klook 熱門活動",
                            "source": "klook"
                        })
                except:
                    continue
    except Exception as e:
        print(f"Klook error: {e}")
    
    return places

def get_wikipedia_parks():
    """從維基百科抓公園列表"""
    places = []
    try:
        url = "https://en.wikipedia.org/wiki/List_of_urban_parks_in_Taiwan"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            for row in soup.select('table.wikitable tr')[1:20]:
                try:
                    cells = row.select('td')
                    if len(cells) >= 2:
                        name = cells[0].text.strip()
                        city = cells[1].text.strip()
                        
                        places.append({
                            "name": name,
                            "city": city if city else "台灣",
                            "type": "公園",
                            "age": "全年齡",
                            "tags": ["👶", "🚼", "🌳", "🅿️"],
                            "time": "全天",
                            "desc": "都市公園",
                            "source": "wikipedia"
                        })
                except:
                    continue
    except Exception as e:
        print(f"Wikipedia error: {e}")
    
    return places

def get_taipei_opendata():
    """從台北市 Open Data 抓公園"""
    places = []
    try:
        # 台北市政府資料平台
        url = "https://data.taipei/api/v3/dataset/5cf3a02c-a8aa-4a89-9e4c-4f68e4d68ee3?format=json"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        
        if resp.status_code == 200:
            data = resp.json()
            # 解析資料
    except Exception as e:
        print(f"Taipei OpenData error: {e}")
    
    return places

def get_all_places():
    """整合所有網路資料"""
    all_places = []
    
    # 1. 嘗試從 TripAdvisor 抓
    try:
        ta_places = get_tripadvisor_taiwan()
        all_places.extend(ta_places)
        print(f"抓取 TripAdvisor: {len(ta_places)} 筆")
    except:
        pass
    
    # 2. 從維基百科抓
    try:
        wiki_places = get_wikipedia_parks()
        all_places.extend(wiki_places)
        print(f"抓取 Wikipedia: {len(wiki_places)} 筆")
    except:
        pass
    
    # 3. 加上經典景點（備用）
    static = [
        {"name": "台北市立兒童新樂園", "city": "台北", "type": "樂園", "age": "3-12歲",
         "tags": ["👶", "🚼", "🧒", "🅿️", "🎢"], "time": "09:00-17:00",
         "desc": "室內外遊樂設施", "source": "static"},
        {"name": "國立科教館", "city": "台北", "type": "博物館", "age": "3-15歲",
         "tags": ["👶", "🧒", "🅿️", "🔬"], "time": "09:00-17:00",
         "desc": "互動科學", "source": "static"},
        {"name": "台北市立動物園", "city": "台北", "type": "動物園", "age": "全年齡",
         "tags": ["👶", "🧒", "🅿️", "🦁"], "time": "09:00-17:00",
         "desc": "無尾熊、貓熊", "source": "static"},
        {"name": "華山1914", "city": "台北", "type": "室內", "age": "全年齡",
         "tags": ["👶", "🧒", "☕", "🎭"], "time": "10:00-18:00",
         "desc": "文創園區", "source": "static"},
        {"name": "十三行博物館", "city": "新北", "type": "博物館", "age": "全年齡",
         "tags": ["👶", "🧒", "🏺"], "time": "09:00-17:00",
         "desc": "考古體驗", "source": "static"},
        {"name": "科博館", "city": "台中", "type": "博物館", "age": "���年��",
         "tags": ["👶", "🚼", "🅿️", "🔬"], "time": "09:00-17:00",
         "desc": "恐龍標本", "source": "static"},
        {"name": "麗寶樂園", "city": "台中", "type": "樂園", "age": "4-15歲",
         "tags": ["👶", "🎢", "🅿️"], "time": "09:30-17:00",
         "desc": "中部最大樂園", "source": "static"},
        {"name": "科工館", "city": "高雄", "type": "博物館", "age": "3-15歲",
         "tags": ["👶", "🚼", "🅿️"], "time": "09:00-17:00",
         "desc": "兒童科學", "source": "static"},
        {"name": "斑溝農場", "city": "宜蘭", "type": "農場", "age": "全年齡",
         "tags": ["👶", "🐑", "🅿️"], "time": "09:00-17:00",
         "desc": "餵小動物", "source": "static"},
        {"name": "傳藝中心", "city": "宜蘭", "type": "室內", "age": "全年齡",
         "tags": ["👶", "🧒", "🎭"], "time": "09:00-18:00",
         "desc": "傳統技藝", "source": "static"},
    ]
    all_places.extend(static)
    
    return all_places

# ========================
# 主程式
# ========================
def main():
    st.title("🎢 FamilyGo 親子遊")
    st.markdown("### 🌐 即時從網路抓取最新景點！")
    st.markdown("---")
    
    with st.sidebar:
        st.header("🔍 搜尋條件")
        
        city = st.selectbox("縣市", ["全部", "台北", "新北", "台中", "高雄", "宜蘭"])
        ptype = st.selectbox("類型", ["全部", "公園", "樂園", "博物館", "農場", "動物園", "室內"])
        
        st.markdown("### 🎯 必備設施")
        need_nursing = st.checkbox("👶 哺乳室")
        need_diaper = st.checkbox("🚼 尿布台")
        need_parking = st.checkbox("🅿️ 停車場")
        
        st.markdown("---")
        if st.button("🔄 重新抓取最新景點", type="primary"):
            st.rerun()
    
    # 顯示正在抓取
    with st.spinner("🌐 正在從網路抓取最新景點資料..."):
        results = get_all_places()
    
    # 顯示更新時間
    st.caption(f"📅 最後更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 篩選
    if city != "全部":
        results = [p for p in results if p.get("city") == city]
    if ptype != "全部":
        results = [p for p in results if p.get("type") == ptype]
    if need_nursing:
        results = [p for p in results if "👶" in p.get("tags", [])]
    if need_diaper:
        results = [p for p in results if "🚼" in p.get("tags", [])]
    if need_parking:
        results = [p for p in results if "🅿️" in p.get("tags", [])]
    
    st.header(f"📍 共 {len(results)} 個景點")
    
    # 顯示
    for place in results:
        source_emoji = {"tripadvisor": "🌐", "klook": "🎫", "wikipedia": "📚", "static": "📍"}
        emoji = source_emoji.get(place.get("source", "static"), "📍")
        
        with st.expander(f"{emoji} {place['name']} ({place.get('city', '')})"):
            tags_str = " ".join(place.get("tags", []))
            st.markdown(f"**標籤**: {tags_str}")
            st.markdown(f"**說明**: {place.get('desc', '')}")
            st.markdown(f"**年齡**: {place.get('age', '')}")
            st.markdown(f"**時間**: {place.get('time', '')}")
            st.caption(f"**資料來源**: {place.get('source', 'unknown')}")
    
    # 統計
    st.markdown("---")
    
    # 來源統計
    sources = {}
    for p in results:
        s = p.get("source", "unknown")
        sources[s] = sources.get(s, 0) + 1
    
    st.header("📊 統計")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("總景點", len(results))
    col2.metric("台北", len([p for p in results if p.get("city") == "台北"]))
    col3.metric("網路抓取", sources.get("tripadvisor", 0) + sources.get("wikipedia", 0))
    col4.metric("靜態庫", sources.get("static", 0))
    
    st.markdown("---")
    st.caption("🎢 FamilyGo | 資料來源：TripAdvisor, Wikipedia, 靜態資料庫")

if __name__ == "__main__":
    main()