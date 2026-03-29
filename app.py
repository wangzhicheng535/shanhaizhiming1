import streamlit as st
from datetime import datetime, timedelta

# ====================== 全局浅绿色主题样式 ======================
st.markdown("""
<style>
/* 整体背景 */
.stApp {
    background-color: #f0f8f0;
}
/* 侧边栏 */
.css-1d391kg, .css-1lcbmhc {
    background-color: #e6f5e6;
}
/* 按钮 */
.stButton>button {
    background-color: #4CAF50;
    color: white;
    border-radius: 8px;
}
.stButton>button:hover {
    background-color: #45a049;
}
/* 标题颜色 */
h1,h2,h3 {
    color: #2e7d32;
}
</style>
""", unsafe_allow_html=True)

# ====================== 离线AI客服 ======================
def ai_customer_service():
    st.markdown("### 🤖 AI 智能客服")
    st.caption("播放、VIP、支付、广告、账号问题均可咨询")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    qa_dict = {
        "怎么注册": "在登录页点击注册，设置用户名密码即可。",
        "如何注册": "在登录页点击注册，设置用户名密码即可。",
        "怎么登录": "输入用户名和密码即可登录。",
        "忘记密码": "目前暂不支持找回密码，请牢记。",
        "vip怎么开": "进入VIP开通页，扫码付款后输入订单号自动开通。",
        "如何开通vip": "进入VIP开通页，扫码付款后输入订单号自动开通。",
        "vip多少钱": "月度VIP 9.9元。",
        "vip有什么用": "无广告、1080P高清、极速线路、无限观看。",
        "会员特权": "无广告、1080P高清、极速线路、无限观看。",
        "vip没到账": "检查订单号是否正确，或联系管理员。",
        "微信支付": "扫描微信收款码，付款后输入订单号。",
        "支付宝支付": "扫描支付宝收款码，付款后输入订单号。",
        "付了没开通": "输入正确订单号即可自动开通VIP。",
        "怎么退款": "虚拟服务一经开通，不支持退款。",
        "视频加载慢": "切换播放线路、降低清晰度或切换网络。",
        "播放卡顿": "降低清晰度，关闭后台应用。",
        "打不开视频": "刷新页面、切换线路、检查网络。",
        "广告太多": "开通VIP即可彻底去除所有广告。",
        "怎么去广告": "开通VIP自动屏蔽全部广告。",
        "求片": "留言影片名，管理员会尽快添加。",
        "人工": "请联系管理员处理。",
        "人工客服": "请联系管理员处理。",
        "谢谢": "不客气，祝你观影愉快！",
        "在吗": "我一直都在哦！",
        "你好": "你好！有什么可以帮助你的？",
        "推荐电影": "推荐：狂飙、孤注一掷、满江红、漫长的季节。",
    }

    def get_answer(text):
        t = text.strip().lower()
        for q, a in qa_dict.items():
            if q in t or t in q:
                return a
        return "抱歉我暂时不会，你可以发“人工”联系管理员。"

    st.markdown("---")
    st.markdown("#### 💬 聊天记录")
    for chat in st.session_state.chat_history:
        if chat["role"] == "user":
            st.markdown(f"**👤 你：** {chat['content']}")
        else:
            st.markdown(f"**🤖 客服：** {chat['content']}")

    st.markdown("---")
    user_input = st.text_input("输入问题", placeholder="例：vip怎么开、视频卡顿…")
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("发送"):
            if user_input:
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                ans = get_answer(user_input)
                st.session_state.chat_history.append({"role": "ai", "content": ans})
                st.rerun()
    with col2:
        if st.button("清空记录"):
            st.session_state.chat_history = []
            st.rerun()

# ====================== 页面配置 ======================
st.set_page_config(page_title="山海追剧", page_icon="📺", layout="wide")

# ====================== 侧边栏 ======================
with st.sidebar:
    st.title("山海追剧")
    page = st.radio("导航", ["首页", "播放解析", "VIP开通", "个人中心"])
    st.markdown("---")
    ai_customer_service()

# ====================== 解析接口 ======================
PARSE_APIS = {
    "主线路": "https://jx.xmflv.cc/?url=",
    "备用1": "https://www.jxhdzy.com/?url=",
    "备用2": "https://jx.aidouer.net/?url=",
}

# ====================== 用户数据 ======================
if "users" not in st.session_state:
    st.session_state.users = {
        "admin": {
            "pwd": "wangzhicheng535",
            "is_admin": True,
            "vip_expire": "2099-01-01"
        },
        "user1": {
            "pwd": "123456",
            "is_admin": False,
            "vip_expire": "2025-01-01"
        }
    }

if "current_user" not in st.session_state:
    st.session_state.current_user = None

# ====================== 登录 ======================
def login():
    st.subheader("登录")
    username = st.text_input("用户名")
    pwd = st.text_input("密码", type="password")
    if st.button("登录"):
        if username in st.session_state.users and st.session_state.users[username]["pwd"] == pwd:
            st.session_state.current_user = username
            st.success("登录成功")
            st.rerun()
        else:
            st.error("用户名或密码错误")

# ====================== 注册 ======================
def register():
    st.subheader("注册")
    username = st.text_input("设置用户名")
    pwd = st.text_input("设置密码", type="password")
    if st.button("注册"):
        if username in st.session_state.users:
            st.error("用户名已存在")
        else:
            st.session_state.users[username] = {
                "pwd": pwd,
                "is_admin": False,
                "vip_expire": "2025-01-01"
            }
            st.success("注册成功！请登录")
            st.rerun()

# ====================== 主程序 ======================
if not st.session_state.current_user:
    tab1, tab2 = st.tabs(["登录", "注册"])
    with tab1:
        login()
    with tab2:
        register()
else:
    current_user = st.session_state.current_user
    user_info = st.session_state.users[current_user]
    is_admin = user_info["is_admin"]
    vip_expire = datetime.strptime(user_info["vip_expire"], "%Y-%m-%d")
    is_vip = vip_expire > datetime.now()

    st.success(f"欢迎回来，{current_user}")
    if st.button("退出登录"):
        st.session_state.current_user = None
        st.rerun()

    # -------------------- 首页 --------------------
    if page == "首页":
        st.title("🏠 山海追剧")
        st.subheader("热门影视推荐")
        st.write("• 狂飙")
        st.write("• 孤注一掷")
        st.write("• 满江红")
        st.write("• 漫长的季节")
        st.write("• 流浪地球2")

    # -------------------- 播放解析 --------------------
    elif page == "播放解析":
        st.title("🎬 在线播放")
        video_url = st.text_input("输入视频链接")
        if video_url:
            line = st.radio("选择播放线路", list(PARSE_APIS.keys()))
            real_url = PARSE_APIS[line] + video_url
            st.components.v1.iframe(real_url, height=550)

    # -------------------- VIP开通（微信+支付宝+自动开通） --------------------
    elif page == "VIP开通":
        st.title("💎 VIP会员开通")
        if is_vip:
            st.success("🎉 您已是VIP会员，畅享无广告观影！")
        else:
            st.subheader("月度VIP：9.9 元")
            st.write("✅ 无广告干扰")
            st.write("✅ 1080P高清播放")
            st.write("✅ 专属极速线路")
            st.write("✅ 无限次观看")

            st.markdown("---")
            st.subheader("💳 选择支付方式")

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### 微信支付")
                try:
                    st.image("wechat_pay.png", caption="微信扫码付款", use_column_width=True)
                except:
                    st.info("请放入图片：wechat_pay.png")

            with col2:
                st.markdown("### 支付宝支付")
                try:
                    st.image("alipay_pay.png", caption="支付宝扫码付款", use_column_width=True)
                except:
                    st.info("请放入图片：alipay_pay.png")

            st.markdown("---")
            order_id = st.text_input("付款后输入订单号自动开通VIP", placeholder="请输入10位以上订单号")
            if st.button("开通VIP（自动）"):
                if len(str(order_id)) >= 10:
                    new_expire = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
                    st.session_state.users[current_user]["vip_expire"] = new_expire
                    st.success(f"✅ VIP开通成功！有效期至：{new_expire}")
                    st.rerun()
                else:
                    st.error("❌ 订单号格式不正确")

    # -------------------- 个人中心 + 管理员手动VIP --------------------
    elif page == "个人中心":
        st.title("👤 个人中心")
        st.write(f"用户名：{current_user}")
        st.write(f"管理员权限：{is_admin}")
        st.write(f"VIP到期时间：{user_info['vip_expire']}")
        st.write(f"当前VIP状态：{'已生效' if is_vip else '未开通'}")

        if is_admin:
            st.markdown("---")
            st.warning("🔑 管理员控制面板")

            st.subheader("手动开通VIP")
            target_user = st.text_input("目标用户名")
            add_days = st.number_input("开通天数", value=30, min_value=1)
            if st.button("手动开通VIP"):
                if target_user in st.session_state.users:
                    new_exp = (datetime.now() + timedelta(days=add_days)).strftime("%Y-%m-%d")
                    st.session_state.users[target_user]["vip_expire"] = new_exp
                    st.success(f"已为【{target_user}】开通VIP {add_days}天")
                    st.rerun()
                else:
                    st.error("用户不存在")

            st.markdown("---")
            st.subheader("所有用户列表")
            for username, info in st.session_state.users.items():
                st.write(f"用户：{username} | VIP到期：{info['vip_expire']}")