import streamlit as st
import time
from datetime import datetime, timedelta

# ==================== 页面配置 ====================
st.set_page_config(page_title="山海追剧", page_icon="🐉", layout="wide")

# ==================== 解析接口 ====================
PARSE_APIS = {
    "主接口": "https://jx.xmflv.cc/?url=",
    "备用1": "https://www.jxhdzy.com/?url=",
    "备用2": "https://jx.aidouer.net/?url=",
}

# ==================== 账号 & 会员系统 ====================
if "users" not in st.session_state:
    st.session_state.users = {
        "admin": {
            "pwd": "wzc1105",
            "is_admin": True,
            "vip_expire": "2099-01-01"
        },
        "user1": {
            "pwd": "123456",
            "is_admin": False,
            "vip_expire": "2025-01-01"
        }
    }

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.session_state.is_admin = False

# ==================== 登录/注册界面（必须先登录） ====================
if not st.session_state.logged_in:
    st.title("🔐 山海追剧 - 登录")
    tab_login, tab_reg = st.tabs(["登录", "注册"])

    with tab_login:
        username = st.text_input("用户名")
        password = st.text_input("密码", type="password")
        if st.button("登录"):
            if username in st.session_state.users:
                if st.session_state.users[username]["pwd"] == password:
                    st.session_state.logged_in = True
                    st.session_state.current_user = username
                    st.session_state.is_admin = st.session_state.users[username]["is_admin"]
                    st.success("登录成功！")
                    st.rerun()
                else:
                    st.error("密码错误")
            else:
                st.error("用户不存在")

    with tab_reg:
        new_user = st.text_input("设置用户名")
        new_pwd = st.text_input("设置密码", type="password")
        if st.button("注册账号"):
            if new_user in st.session_state.users:
                st.warning("用户名已存在")
            elif len(new_user) < 2 or len(new_pwd) < 2:
                st.warning("用户名/密码不能太短")
            else:
                st.session_state.users[new_user] = {
                    "pwd": new_pwd,
                    "is_admin": False,
                    "vip_expire": "2025-01-01"
                }
                st.success("注册成功！请登录")
    st.stop()

# ==================== 已登录，进入主程序 ====================
user = st.session_state.current_user
is_admin = st.session_state.is_admin
vip_expire_str = st.session_state.users[user]["vip_expire"]
vip_expire = datetime.strptime(vip_expire_str, "%Y-%m-%d")
now = datetime.now()
is_vip = is_admin or (vip_expire > now)

st.markdown(f"👤 欢迎：**{user}**　｜　VIP到期：**{vip_expire_str}**")
if is_admin:
    st.success("✅ 管理员模式：自动免广告 + 免费会员")

# ==================== 样式 ====================
st.markdown("""
<style>
.stApp { background: #050a1a; color: #eef; }
.title { font-size: 46px; text-align:center; background: linear-gradient(90deg,#4facfe,#00f2fe);
         -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight:bold; }
.block { background:rgba(20,30,60,0.6); padding:15px; border-radius:10px; margin:10px 0; }
.ad-banner { background:#222; padding:10px; border-radius:8px; text-align:center; color:white; }
</style>
""", unsafe_allow_html=True)

# ==================== 顶部广告（非VIP显示） ====================
if not is_vip:
    st.markdown('<div class="ad-banner">【广告】免费用户需观看广告解锁播放 · 开通会员免广告</div>', unsafe_allow_html=True)

# ==================== 标题 ====================
st.markdown("<div class='title'>山海追剧</div>", unsafe_allow_html=True)
st.divider()

# ==================== 功能标签页 ====================
tab_names = ["🎬 单视频解析", "📋 批量播放", "📜 历史记录", "🤖 AI客服"]
if is_admin:
    tab_names.append("⚙️ 管理后台")
tabs = st.tabs(tab_names)

# 1. 单视频解析
with tabs[0]:
    st.markdown("<div class='block'>", unsafe_allow_html=True)
    url = st.text_input("输入视频链接", placeholder="https://...")
    api = st.selectbox("解析源", list(PARSE_APIS.keys()))
    if st.button("▶️ 立即播放"):
        if not url.startswith("http"):
            st.warning("请输入有效链接")
        else:
            if not is_vip:
                st.info("免费用户需观看广告解锁播放")
                time.sleep(1)
                st.success("广告已看完，正在播放")
            play_url = PARSE_APIS[api] + url
            st.markdown(f"👉 [点击播放]({play_url})")
    st.markdown("</div>", unsafe_allow_html=True)

# 2. 批量播放
with tabs[1]:
    st.markdown("<div class='block'>", unsafe_allow_html=True)
    uploaded = st.file_uploader("上传txt链接列表", type="txt")
    api2 = st.selectbox("批量解析源", list(PARSE_APIS.keys()), key="batch")
    if st.button("▶️ 批量打开") and uploaded:
        lines = uploaded.read().decode("utf-8").splitlines()
        urls = [x.strip() for x in lines if x.strip().startswith("http")]
        for u in urls:
            st.markdown(f"✅ [播放]({PARSE_APIS[api2] + u})")
    st.markdown("</div>", unsafe_allow_html=True)

# 3. 历史记录
with tabs[2]:
    st.markdown("<div class='block'>", unsafe_allow_html=True)
    st.subheader("📜 播放历史")
    st.info("本地历史记录演示，如需云端可升级")
    if st.button("🧹 清空历史"):
        st.success("已清空")
    st.markdown("</div>", unsafe_allow_html=True)

# 4. AI客服
with tabs[3]:
    st.markdown("<div class='block'>", unsafe_allow_html=True)
    st.subheader("🤖 AI客服")
    q = st.text_input("输入问题", key="q")
    if st.button("发送问题"):
        st.success("客服已收到，管理员将尽快回复")
    st.markdown("</div>", unsafe_allow_html=True)

# 5. 管理员后台（仅管理员可见）
if is_admin:
    with tabs[4]:
        st.markdown("<div class='block'>", unsafe_allow_html=True)
        st.subheader("⚙️ 管理员后台")
        st.write(f"当前用户总数：**{len(st.session_state.users)}**")
        target_user = st.selectbox("选择用户", list(st.session_state.users.keys()))
        if target_user:
            user_info = st.session_state.users[target_user]
            st.write("密码：", user_info["pwd"])
            st.write("是否管理员：", user_info["is_admin"])
            st.write("VIP到期时间：", user_info["vip_expire"])

            days = st.number_input("开通VIP天数", 1, 365, 30)
            if st.button("设置VIP"):
                new_expire = (now + timedelta(days=days)).strftime("%Y-%m-%d")
                st.session_state.users[target_user]["vip_expire"] = new_expire
                st.success(f"已设置VIP至：{new_expire}")

            if target_user != "admin" and st.button("删除用户"):
                del st.session_state.users[target_user]
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ==================== 支付开通VIP（微信+支付宝收款码版） ====================
if not is_vip:
    st.markdown("<div class='block'>", unsafe_allow_html=True)
    st.subheader("💎 会员特权")
    st.write("✅ 无广告")
    st.write("✅ 1080P高清")
    st.write("✅ 不限次数播放")
    st.write("✅ 极速线路")
    st.markdown("## 💰 9.9 元 / 月")
    st.markdown("**付款后请在客服提交用户名+付款截图，管理员将在1分钟内为您开通VIP**")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 微信支付")
        try:
            st.image("wechat_pay.png", use_column_width=True)
        except:
            st.info("微信收款码加载中...")
        if st.button("✅ 我已付款，开通VIP", key="wechat_pay", use_container_width=True):
            st.info("请将付款截图和用户名发送给客服，管理员核实后将为您开通VIP")

    with col2:
        st.markdown("### 支付宝支付")
        try:
            st.image("alipay_pay.png", use_column_width=True)
        except:
            st.info("支付宝收款码加载中...")
        if st.button("✅ 我已付款，开通VIP", key="alipay_pay", use_container_width=True):
            st.info("请将付款截图和用户名发送给客服，管理员核实后将为您开通VIP")
    st.markdown("</div>", unsafe_allow_html=True)

# ==================== 底部广告 ====================
if not is_vip:
    st.markdown("""
    <div style="background:#111;padding:12px;text-align:center;color:#aaa;margin-top:20px;">
    【广告】山海追剧
    </div>
    """, unsafe_allow_html=True)

st.markdown("<p style='text-align:center;color:#666;margin-top:10px;'>山海追剧</p>", unsafe_allow_html=True)