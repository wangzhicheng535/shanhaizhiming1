import streamlit as st
import requests
import json
import time
from urllib.parse import quote

# ==================== 配置 ====================
st.set_page_config(page_title="山海追剧", page_icon="🐉", layout="wide")

PARSE_APIS = {
    "主接口": "https://jx.xmflv.cc/?url=",
    "备用1": "https://www.jxhdzy.com/?url=",
    "备用2": "https://jx.aidouer.net/?url=",
}

# ==================== 会员系统 ====================
if "is_vip" not in st.session_state:
    st.session_state.is_vip = False

# ==================== 样式 ====================
st.markdown("""
<style>
.stApp { background: #050a1a; color: #eef; }
.title { font-size: 50px; text-align:center; background: linear-gradient(90deg,#4facfe,#00f2fe);
         -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.subtitle { text-align:center; font-size:20px; color:#a78bff; }
.block { background:rgba(20,30,60,0.6); padding:15px; border-radius:10px; margin:10px 0; }
.ad-top { background:#222; padding:10px; border-radius:8px; text-align:center; color:white; }
.ad-bottom { position:fixed; bottom:0; left:0; width:100%; background:#111; padding:10px; text-align:center; color:#aaa; }
</style>
""", unsafe_allow_html=True)

# ==================== 广告（非会员显示） ====================
if not st.session_state.is_vip:
    st.markdown('<div class="ad-top">【广告】开通会员免广告 · 1080P高清</div>', unsafe_allow_html=True)

# ==================== 标题 ====================
st.markdown("<div class='title'>山海</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>破解追剧</div>", unsafe_allow_html=True)
st.divider()

# ==================== 分页 ====================
tab1, tab2, tab3, tab4 = st.tabs(["🎬 单视频解析", "📋 批量播放", "📜 历史记录", "🤖 AI客服"])

# ==================== 1. 单视频解析 ====================
with tab1:
    st.markdown("<div class='block'>", unsafe_allow_html=True)
    st.subheader("播放解析")
    url = st.text_input("输入视频链接", placeholder="https://...")
    api = st.selectbox("解析源", list(PARSE_APIS.keys()))
    if st.button("▶️ 立即播放"):
        if not url.startswith("http"):
            st.warning("请输入有效链接")
        else:
            if not st.session_state.is_vip:
                st.info("免费用户需观看广告解锁播放")
                time.sleep(1)
                st.success("广告已看完，正在播放")
            play = PARSE_APIS[api] + url
            st.markdown(f"👉 [点击播放]({play})")
    st.markdown("</div>", unsafe_allow_html=True)

# ==================== 2. 批量播放 ====================
with tab2:
    st.markdown("<div class='block'>", unsafe_allow_html=True)
    st.subheader("批量解析")
    uploaded = st.file_uploader("上传txt链接列表", type="txt")
    api2 = st.selectbox("批量解析源", list(PARSE_APIS.keys()), key="batch")
    if st.button("▶️ 批量打开") and uploaded:
        lines = uploaded.read().decode("utf-8").splitlines()
        urls = [x.strip() for x in lines if x.strip().startswith("http")]
        for u in urls:
            st.markdown(f"✅ [播放]({PARSE_APIS[api2] + u})")
    st.markdown("</div>", unsafe_allow_html=True)

# ==================== 3. 历史记录 ====================
with tab3:
    st.markdown("<div class='block'>", unsafe_allow_html=True)
    st.subheader("播放历史")
    st.info("本地历史记录功能已保留（如需保存到云端可升级）")
    if st.button("🧹 清空历史"):
        st.success("已清空")
    st.markdown("</div>", unsafe_allow_html=True)

# ==================== 4. AI客服 ====================
with tab4:
    st.markdown("<div class='block'>", unsafe_allow_html=True)
    st.subheader("AI客服")
    q = st.text_input("输入问题", key="q")
    if st.button("发送"):
        st.success("AI回复：功能正在升级，敬请期待")
    st.markdown("</div>", unsafe_allow_html=True)

# ==================== 会员开通 ====================
st.markdown("<div class='block'>", unsafe_allow_html=True)
st.subheader("💎 会员特权")
st.write("✅ 无广告")
st.write("✅ 1080P高清")
st.write("✅ 批量不限次数")
st.write("✅ 极速播放")

if st.button("9.9元开通月度会员"):
    st.session_state.is_vip = True
    st.success("已成功开通会员！")
st.markdown("</div>", unsafe_allow_html=True)

# ==================== 底部广告 ====================
if not st.session_state.is_vip:
    st.markdown('<div class="ad-bottom">【广告】影视会员 | 设备推荐</div>', unsafe_allow_html=True)

st.markdown("<p style='text-align:center;color:#666;margin:20px 0;'>山海追剧 · 仅供学习</p>", unsafe_allow_html=True)