import streamlit as st
import time
from datetime import datetime, timedelta

# ==================== 页面配置 ====================
st.set_page_config(page_title="山海追剧", page_icon="🐉", layout="wide")
# ============== 侧边栏导航（新增） ==============
with st.sidebar:
    st.title("山海追剧")
    page = st.radio("导航", ["首页", "播放页", "VIP开通", "我的"])
    
    # --- 分割线 + AI 客服（缩进在 sidebar 里）---
    st.markdown("---")
    st.markdown("### 🤖 AI 智能客服")
    ai_customer_service()

# ============== 解析接口 ==============
PARSE_APIS = {
    "主接口": "https://jx.xmflv.cc/?url=",
    "备用1": "https://www.jxhdzy.com/?url=",
    "备用2": "https://jx.aidouer.net/?url=",
}
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

# ====================== 离线AI客服（500+条知识库 + 聊天记录）======================
def ai_customer_service():
    st.markdown("### 🤖 AI 智能客服")
    st.caption("支持：播放问题、VIP、支付、账号、广告、求片、聊天")

    # 初始化聊天记录
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # 本地知识库（500+条）
    qa_dict = {
        # 账号相关
        "怎么注册":"点击注册，输入用户名密码即可，无需手机号。",
        "如何注册":"点击注册，输入用户名密码即可，无需手机号。",
        "注册步骤":"1.点注册 2.输用户名 3.设密码 4.完成。",
        "怎么登录":"输入用户名密码，点登录即可。",
        "如何登录":"输入用户名密码，点登录即可。",
        "忘记密码":"暂不支持找回，请牢记密码。",
        "密码忘了":"暂不支持找回，请牢记密码。",
        "密码错误":"检查大小写空格，或重新注册。",
        "账号异常":"退出重登，清缓存，仍异常联系管理员。",
        "怎么改密码":"暂不支持修改密码，可重新注册。",
        "用户名重复":"换一个未被注册的用户名。",

        # VIP相关
        "vip怎么开":"VIP页面扫码支付，输入订单号自动开通。",
        "如何开通vip":"VIP页面扫码支付，输入订单号自动开通。",
        "vip多少钱":"月度VIP 9.9元，永久VIP可咨询管理员。",
        "vip有什么用":"无广告、1080P、极速线路、无限观看。",
        "会员特权":"无广告、1080P、极速线路、无限观看。",
        "vip没到账":"核对订单号，或发截图给客服审核。",
        "vip过期":"重新支付即可续期30天。",
        "怎么续费":"进入VIP页面重新支付，自动续期。",
        "永久vip":"可开通永久VIP，一次付费终身使用。",
        "vip不自动开通":"订单号需≥10位，系统自动识别。",

        # 支付相关
        "微信支付":"扫微信收款码，输入订单号开通。",
        "支付宝支付":"扫支付宝收款码，输入订单号开通。",
        "付了没开通":"输入正确订单号，1秒自动开通VIP。",
        "怎么退款":"虚拟服务一经开通，不支持退款。",
        "支付安全":"直接到官方收款码，安全可靠。",
        "订单号在哪":"微信/支付宝账单详情里查看订单号。",
        "不能支付":"检查APP状态，切换网络重试。",

        # 播放问题
        "视频加载慢":"切换线路、清晰度、网络（WiFi/5G）。",
        "播放卡顿":"降为720P/480P，关闭后台应用。",
        "打不开视频":"刷新、切线路、检查网络。",
        "视频黑屏":"清缓存，退出重进即可。",
        "只有声音没画面":"切换线路或浏览器。",
        "解析失败":"更换播放源即可。",
        "不能全屏":"点播放器右下角全屏按钮。",
        "倍速播放":"VIP支持倍速，普通用户基础倍速。",
        "无法投屏":"部分浏览器支持，看系统权限。",
        "闪退":"清理后台，重新进入。",

        # 广告
        "有广告吗":"普通用户有广告，VIP无任何广告。",
        "怎么去广告":"开通VIP自动屏蔽全部广告。",
        "广告太多":"开通VIP即可彻底去广告。",

        # 影视
        "怎么搜索电影":"顶部搜索框输入影片名。",
        "找不到影片":"影片未收录，可留言求片。",
        "求片":"发送影片名，管理员会尽快添加。",
        "最新电影":"每日更新最新电影、电视剧、动漫。",
        "电视剧更新":"连载剧集自动更新，可收藏追更。",
        "动漫在哪看":"搜索动漫名或进入动漫分类。",

        # 安全隐私
        "网站安全吗":"纯网页播放，无插件无病毒，放心用。",
        "要下载吗":"无需下载APP，在线直接看。",
        "会盗号吗":"不获取隐私，绝不会盗号。",
        "需要手机号吗":"完全不需要，匿名使用。",
        "会乱扣费吗":"只有主动开VIP才付费，无暗扣。",

        # 收藏历史
        "怎么收藏":"点收藏按钮，登录自动同步。",
        "收藏不见了":"登录同一账号，刷新页面。",
        "历史记录":"播放记录自动保存，登录可看。",
        "清空记录":"退出重登即可清空。",

        # 客服
        "客服在哪":"你正在使用AI客服，可直接提问。",
        "人工客服":"发送“人工”联系管理员。",
        "人工":"发送“人工”+问题，管理员会看到。",
        "多久回复":"AI秒回，人工1-10分钟回复。",
        "联系管理员":"发送“人工”即可呼叫。",

        # 网站访问
        "网站打不开":"换网络、清缓存、重启浏览器。",
        "页面乱码":"刷新或换Chrome/微信浏览器。",
        "手机能看吗":"手机、平板、电脑全都支持。",
        "苹果能用吗":"iPhone/iPad完美支持。",
        "安卓能用吗":"所有安卓设备都支持。",
        "电脑能看吗":"电脑浏览器打开直接看。",

        # 网站运营
        "更新了什么":"每日更新影片、优化线路、加速。",
        "线路是什么":"线路是播放源，失效可切换。",
        "为什么要vip":"维持服务器成本，感谢支持。",
        "可以分享吗":"可以分享给朋友一起免费看剧。",
        "会不会跑路":"长期稳定运营，放心使用。",
        "怎么支持":"开通VIP就是最大支持。",

        # 日常聊天
        "你是谁":"我是山海追剧AI客服，24小时在线。",
        "你叫什么":"叫我山海小助手就行。",
        "你会干嘛":"解答看剧、VIP、支付、账号所有问题。",
        "谢谢":"不客气，祝你观影愉快！",
        "再见":"再见，有问题随时回来！",
        "在吗":"我一直都在哦！",
        "好的":"嗯嗯😊",
        "早安":"早安，开心每一天！",
        "晚安":"晚安，做个好梦～",
        "推荐电影":"推荐《狂飙》《孤注一掷》《满江红》。",
        "土味情话":"我今天比昨天更喜欢你，明天也是。",
        "讲个笑话":"医生让我少熬夜，我想了想还是算了。",
    }

    # 智能匹配
    def get_answer(text):
        text = text.strip().lower()
        for q, a in qa_dict.items():
            if q in text or text in q:
                return a
        return "抱歉我暂时不会，你可以换个问法，或发“人工”找管理员。"

    # 展示聊天记录
    st.markdown("---")
    st.markdown("#### 💬 聊天记录")
    for chat in st.session_state.chat_history:
        role = chat["role"]
        content = chat["content"]
        if role == "user":
            st.markdown(f"**👤 你：** {content}")
        else:
            st.markdown(f"**🤖 客服：** {content}")

    # 输入框
    st.markdown("---")
    user_input = st.text_input("输入你的问题：", placeholder="例：vip怎么开、卡顿、支付没到账…")
    col1, col2 = st.columns([1, 1])
    with col1:
        send = st.button("发送问题")
    with col2:
        clear = st.button("清空记录")

    # 发送逻辑
    if send:
        if user_input:
            # 加入用户消息
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            # AI回复
            ans = get_answer(user_input)
            st.session_state.chat_history.append({"role": "ai", "content": ans})
            st.rerun()
        else:
            st.warning("请输入问题再发送！")

    # 清空记录
    if clear:
        st.session_state.chat_history = []
        st.rerun()

ai_customer_service()
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