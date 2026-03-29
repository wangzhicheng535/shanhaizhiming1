import streamlit as st
import requests
import re
from datetime import datetime, timedelta

# ====================== 浅绿色主题 ======================
st.markdown("""
<style>
.stApp { background-color: #f0f8f0; }
.css-1d391kg { background-color: #e6f5e6; }
.stButton>button { background-color: #4CAF50; color: white; border-radius:8px; }
.stButton>button:hover { background-color: #388E3C; }
h1,h2,h3 { color: #2e7d32; }
.comment-box { border:1px solid #ccc; padding:10px; margin:5px 0; border-radius:8px; background:white; }
.badges { color:#FF9800; font-weight:bold; }
.feedback-box { border-left:3px solid #4CAF50; padding:8px 12px; margin:6px 0; background:#f8fff8; }
</style>
""", unsafe_allow_html=True)

# ====================== AI 客服（离线 1000+ 条）======================
def ai_customer_service():
    st.markdown("### 🤖 AI客服")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    qa = {
        "你好":"你好呀，有什么可以帮你的？",
        "您好":"您好，很高兴为您服务",
        "在吗":"我在呢，你说",
        "在":"在的，随时为你服务",
        "谢谢":"不客气，能帮到你就好",
        "感谢":"不客气，有问题随时再来",
        "拜拜":"拜拜，下次见",
        "再见":"再见，祝你观影愉快",
        "早上好":"早上好，新的一天顺利",
        "晚上好":"晚上好，注意休息哦",
        "午安":"午安，好好休息",
        "晚安":"晚安，做个好梦",
        "哈哈":"开心就好啦",
        "嘿嘿":"嘻嘻",
        "呵呵":"哈哈",
        "厉害":"谢谢夸奖",
        "牛逼":"文明用语哦",
        "大佬":"不敢当，尽力帮你",
        "软件叫什么":"山海追剧",
        "这是什么软件":"山海追剧，免费解析视频",
        "软件干嘛的":"可以解析、播放、批量下载视频",
        "有什么功能":"批量解析、批量保存、在线播放、评论、反馈",
        "功能有哪些":"批量解析、保存、播放、去广告、评论、反馈",
        "怎么使用":"粘贴链接即可解析，支持一行一个批量",
        "使用教程":"首页粘贴链接，点解析就可以播放或下载",
        "教程在哪":"直接粘贴链接，系统自动解析",
        "怎么操作":"输入链接点解析即可",
        "步骤是什么":"1粘贴链接 2解析 3播放或保存",
        "解析是什么":"把加密链接转成可以直接播放的链接",
        "为什么解析":"原链接无法播放，解析后可以播放",
        "解析失败":"链接失效、网络问题、换个链接试试",
        "解析不了":"换链接、切网络、刷新重试",
        "解析不出来":"换个视频链接试试",
        "解析超时":"网络慢，切换4/5G或WiFi",
        "解析错误":"链接无效或平台限制",
        "解析黑屏":"视频源失效，换一个",
        "解析卡顿":"换线路、降低画质",
        "解析无声音":"视频源问题，换片源",
        "解析慢":"网络问题",
        "能解析什么":"抖音、快手、爱奇艺、腾讯、优酷等",
        "支持哪些平台":"主流短视频、影视平台都支持",
        "支持抖音吗":"支持",
        "支持快手吗":"支持",
        "支持B站吗":"支持",
        "支持爱奇艺吗":"支持",
        "支持腾讯吗":"支持",
        "支持优酷吗":"支持",
        "支持芒果吗":"支持",
        "支持西瓜吗":"支持",
        "批量怎么用":"一行一个链接粘贴到批量解析",
        "怎么批量下载":"粘贴多个链接，解析后保存",
        "批量保存":"在批量解析里粘贴多个链接",
        "一次多个":"批量解析支持一次粘贴多个",
        "批量解析失败":"部分链接失效，剔除无效链接重试",
        "批量没反应":"检查链接格式，一行一个不要空行",
        "批量保存失败":"网络问题或链接失效",
        "批量能下多少":"一次建议20个以内",
        "批量上限":"一次建议不超过30个",
        "怎么播放":"解析成功后点击播放按钮",
        "播放不了":"链接失效、换线路、换网络",
        "播放黑屏":"视频源已失效",
        "播放卡顿":"切换清晰度、切换网络",
        "播放没声音":"视频本身无音轨或失效",
        "播放慢":"网络问题",
        "倍速播放":"目前暂不支持倍速",
        "全屏":"点击视频右上角全屏",
        "横屏":"手机自动旋转即可",
        "怎么下载":"解析后复制链接用浏览器下载",
        "怎么保存":"输入直链，点保存视频",
        "保存失败":"网络中断或链接失效",
        "保存路径":"默认保存在软件同目录下",
        "保存位置":"和本程序同一个文件夹",
        "下载慢":"网络问题，换WiFi",
        "下载不了":"链接失效",
        "保存格式":"默认MP4",
        "能下高清吗":"支持高清，看原视频质量",
        "VIP是什么":"去广告、专属线路、高清",
        "VIP有什么用":"去广告、高清、优先解析",
        "怎么开VIP":"VIP页面扫码付款输订单号",
        "VIP多少钱":"9.9元一个月",
        "VIP价格":"月度9.9",
        "永久VIP吗":"可以联系管理员开通",
        "VIP到期":"到期后自动关闭去广告",
        "怎么续期":"重新开通即可",
        "有广告吗":"普通用户有广告，VIP无广告",
        "广告怎么去除":"开通VIP自动去广告",
        "去广告":"开通VIP",
        "为什么有广告":"免费版需要广告维持运营",
        "广告多怎么办":"开通VIP即可去除",
        "不开通有广告吗":"是的，免费版有广告",
        "微信支付":"在VIP页面扫码支付",
        "支付宝支付":"VIP页面支持支付宝",
        "付款了没开通":"输入订单号自动开通",
        "订单号是什么":"付款后账单里的订单编号",
        "在哪看订单号":"微信/支付宝账单详情",
        "付错了怎么办":"虚拟商品不退款",
        "能退款吗":"虚拟服务不支持退款",
        "支付失败":"换网络或重新扫码",
        "扫码没反应":"刷新重试",
        "怎么注册":"登录页点击注册",
        "怎么登录":"输入用户名密码登录",
        "忘记密码":"目前暂不支持找回",
        "密码忘了":"暂时无法找回，可重新注册",
        "账号异常":"退出重登",
        "账号被封":"违规被封，无法解封",
        "能改密码吗":"暂不支持",
        "注销账号":"联系管理员",
        "账号安全":"请勿泄露密码",
        "怎么评论":"进入评论区发表",
        "评论被删":"违规被管理员删除",
        "为什么删评论":"违规、辱骂、广告",
        "什么不能发":"广告、辱骂、政治、色情",
        "优质评论":"有意义的评论可获得奖状",
        "奖状是什么":"优质评论标记",
        "怎么得奖状":"发表有价值的评论",
        "奖状有什么用":"展示优质用户",
        "怎么反馈":"侧边栏点击我要反馈",
        "反馈有用吗":"管理员每天查看",
        "反馈多久回复":"一般1-2天",
        "反馈没回复":"管理员处理中",
        "BUG怎么反馈":"在反馈里选择问题报错",
        "建议怎么提":"反馈里选择功能建议",
        "管理员是谁":"admin",
        "怎么联系管理员":"通过反馈留言",
        "能加管理员微信":"暂不提供",
        "管理员能干嘛":"删评论、删用户、删反馈、开VIP",
        "能当管理员吗":"不能，仅官方",
        "不能发什么":"广告、辱骂、涉政、色情、暴力",
        "违规会怎样":"禁言、封号",
        "骂人会怎样":"删除评论并封号",
        "发广告会怎样":"直接封号",
        "闪退":"重启软件",
        "卡顿":"刷新或重启",
        "打不开":"重新运行",
        "报错":"截图反馈给管理员",
        "网络异常":"切换网络",
        "无网络":"检查WiFi或流量",
        "最新电影":"首页查看推荐",
        "电视剧能看吗":"可以",
        "动漫能看吗":"可以",
        "综艺能看吗":"可以",
        "短剧能看吗":"可以",
        "韩剧能看吗":"可以",
        "美剧能看吗":"可以",
        "a":"我在",
        "aa":"在的",
        "好":"好的",
        "好的":"嗯嗯",
        "行":"行",
        "可以":"可以",
        "哦":"哦",
        "嗯":"嗯",
        "额":"额",
        "唉":"怎么了",
        "哇":"哈哈",
        "哦豁":"咋啦",
        "没事":"没事就好",
        "哈喽":"哈喽",
        "嗨":"嗨",
        "加油":"加油",
        "辛苦":"不辛苦",
        "开心":"开心就好",
        "难过":"摸摸头",
        "累了":"休息一下",
        "饿了":"快去吃饭",
        "困了":"早点休息",
        "冷了":"多穿点",
        "热了":"吹吹空调",
        "下雨了":"记得带伞",
        "天晴了":"适合看剧",
        "上班":"上班加油",
        "下班":"下班快乐",
        "上学":"好好学习",
        "放假":"放假快乐",
        "新年快乐":"新年快乐",
        "生日快乐":"生日快乐",
        "国庆快乐":"国庆快乐",
        "端午安康":"端午安康",
        "中秋快乐":"中秋快乐",
        "马年大吉":"马年大吉",
        "恭喜发财":"恭喜发财",
        "身体健康":"祝你身体健康",
        "万事如意":"万事如意",
        "心想事成":"心想事成",
        "平安喜乐":"平安喜乐",
        "财源广进":"财源广进",
        "好运连连":"好运连连",
        "万事顺意":"万事顺意",
        "前程似锦":"前程似锦",
        "步步高升":"步步高升",
        "工作顺利":"工作顺利",
        "学习进步":"学习进步",
        "天天开心":"天天开心",
        "笑口常开":"笑口常开",
        "越来越帅":"谢谢",
        "越来越美":"谢谢",
        "越来越有钱":"一起发财",
        "暴富":"暴富",
        "暴瘦":"暴瘦",
        "脱单":"脱单",
        "中奖":"中奖",
        "好运":"好运",
        "福气":"福气满满",
        "发财":"发财",
        "顺利":"顺利",
        "平安":"平安",
        "健康":"健康",
        "快乐":"快乐",
        "幸福":"幸福",
        "美满":"美满",
        "甜蜜":"甜蜜",
        "温馨":"温馨",
        "浪漫":"浪漫",
        "悠闲":"悠闲",
        "自在":"自在",
        "轻松":"轻松",
        "舒服":"舒服",
        "惬意":"惬意",
        "爽":"爽",
        "赞":"赞",
        "顶":"顶",
        "支持":"支持",
        "喜欢":"喜欢就好",
        "爱你":"爱你哟",
        "比心":"比心",
        "抱抱":"抱抱",
        "亲亲":"亲亲",
        "么么哒":"么么哒",
        "mua":"mua",
        "哈哈哈哈":"哈哈哈哈",
        "嘿嘿嘿":"嘿嘿嘿",
        "嘻嘻":"嘻嘻",
        "啦啦啦":"啦啦啦",
        "略略略":"略略略",
        "呜呜呜":"摸摸头",
        "嘤嘤嘤":"不哭不哭",
        "555":"不哭",
        "666":"666",
        "888":"发发发",
        "999":"666",
        "牛逼啊":"文明用语哦",
        "绝了":"绝了",
        "无敌":"无敌",
        "最强":"最强",
        "第一":"第一",
        "优秀":"优秀",
        "棒":"棒",
        "完美":"完美",
        "给力":"给力",
        "靠谱":"靠谱",
        "稳":"稳",
        "牛":"牛",
        "强":"强",
        "飒":"飒",
        "酷":"酷",
        "萌":"萌",
        "帅":"帅",
        "美":"美",
        "甜":"甜",
        "软":"软",
        "暖":"暖",
        "治愈":"治愈",
        "温柔":"温柔",
        "霸气":"霸气",
        "可爱":"可爱",
        "好看":"好看",
        "好听":"好听",
        "好吃":"好吃",
        "好玩":"好玩",
        "好用":"好用",
        "方便":"方便",
        "实用":"实用",
        "简单":"简单",
        "容易":"容易",
        "快捷":"快捷",
        "高效":"高效",
        "清晰":"清晰",
        "流畅":"流畅",
        "稳定":"稳定",
        "安全":"安全",
        "放心":"放心",
        "靠谱":"靠谱",
        "良心":"良心",
        "好评":"好评",
        "推荐":"推荐",
        "安利":"安利",
        "种草":"种草",
        "收藏":"收藏",
        "转发":"转发",
        "分享":"分享",
        "关注":"关注",
        "点赞":"点赞",
        "评论":"评论",
        "留言":"留言",
        "互动":"互动",
        "交流":"交流",
        "聊天":"聊天",
        "唠嗑":"唠嗑",
        "扯家常":"扯家常",
        "讲故事":"讲故事",
        "说笑话":"说笑话",
        "唱歌":"唱歌",
        "跳舞":"跳舞",
        "画画":"画画",
        "写作":"写作",
        "读书":"读书",
        "学习":"学习",
        "运动":"运动",
        "健身":"健身",
        "旅游":"旅游",
        "逛街":"逛街",
        "购物":"购物",
        "美食":"美食",
        "电影":"电影",
        "电视剧":"电视剧",
        "动漫":"动漫",
        "综艺":"综艺",
        "短剧":"短剧",
        "音乐":"音乐",
        "游戏":"游戏",
        "追剧":"追剧",
        "看片":"看片",
        "躺平":"躺平",
        "摆烂":"摆烂",
        "内卷":"内卷",
        "摸鱼":"摸鱼",
        "划水":"划水",
        "加班":"加班辛苦",
        "熬夜":"别熬夜",
        "早起":"早起真棒",
        "早睡":"早睡身体好",
        "喝水":"多喝水",
        "吃饭":"好好吃饭",
        "睡觉":"好好睡觉",
        "养生":"养生真棒",
        "护肤":"护肤真棒",
        "化妆":"化妆真棒",
        "穿搭":"穿搭真棒",
        "发型":"发型真棒",
        "美甲":"美甲真棒",
        "纹身":"纹身真棒",
        "宠物":"宠物真可爱",
        "猫咪":"猫咪真可爱",
        "狗狗":"狗狗真可爱",
        "兔子":"兔子真可爱",
        "熊猫":"熊猫真可爱",
        "老虎":"老虎真霸气",
        "狮子":"狮子真霸气",
        "狼":"狼真霸气",
        "熊":"熊真壮",
        "鸟":"小鸟真可爱",
        "鱼":"小鱼真自由",
        "花":"花真漂亮",
        "草":"草真绿",
        "树":"树真高",
        "山":"山真高",
        "水":"水真清",
        "海":"海真大",
        "河":"河真长",
        "湖":"湖真美",
        "云":"云真白",
        "天":"天真蓝",
        "太阳":"太阳真暖",
        "月亮":"月亮真美",
        "星星":"星星真亮",
        "风":"风真凉",
        "雨":"雨真细",
        "雪":"雪真白",
        "雷":"雷真响",
        "电":"电真亮",
        "春":"春天真美",
        "夏":"夏天真热",
        "秋":"秋天真凉",
        "冬":"冬天真冷",
        "早上":"早上好",
        "中午":"中午好",
        "下午":"下午好",
        "晚上":"晚上好",
        "今天":"今天好",
        "明天":"明天好",
        "昨天":"昨天好",
        "现在":"现在好",
        "马上":"马上",
        "立刻":"立刻",
        "快点":"快点",
        "慢点":"慢点",
        "等等":"等等",
        "别急":"别急",
        "冷静":"冷静",
        "放松":"放松",
        "开心点":"开心点",
        "别难过":"别难过",
        "别生气":"别生气",
        "别担心":"别担心",
        "别害怕":"别害怕",
        "别放弃":"别放弃",
        "坚持住":"坚持住",
        "加油啊":"加油啊",
        "你可以":"你可以",
        "相信你":"相信你",
        "支持你":"支持你",
        "挺你":"挺你",
        "陪你":"陪你",
        "等你":"等你",
        "想你":"想你",
        "念你":"念你",
        "牵挂":"牵挂",
        "思念":"思念",
        "喜欢":"喜欢",
        "爱":"爱",
        "宠爱":"宠爱",
        "疼爱":"疼爱",
        "珍爱":"珍爱",
        "深爱":"深爱",
        "偏爱":"偏爱",
        "唯一":"唯一",
        "专属":"专属",
        "独家":"独家",
        "限量":"限量",
        "珍贵":"珍贵",
        "珍惜":"珍惜",
        "守护":"守护",
        "保护":"保护",
        "陪伴":"陪伴",
        "相守":"相守",
        "相依":"相依",
        "相伴":"相伴",
        "相随":"相随",
        "同行":"同行",
        "共进":"共进",
        "共赢":"共赢",
        "同心":"同心",
        "同德":"同德",
        "同道":"同道",
        "同志":"同志",
        "朋友":"朋友",
        "兄弟":"兄弟",
        "姐妹":"姐妹",
        "家人":"家人",
        "亲人":"亲人",
        "爱人":"爱人",
        "恋人":"恋人",
        "情侣":"情侣",
        "夫妻":"夫妻",
        "知己":"知己",
        "闺蜜":"闺蜜",
        "老铁":"老铁",
        "哥们":"哥们",
        "姐们":"姐们",
        "伙伴":"伙伴",
        "队友":"队友",
        "同事":"同事",
        "同学":"同学",
        "老师":"老师",
        "学生":"学生",
        "家长":"家长",
        "孩子":"孩子",
        "宝宝":"宝宝",
        "宝贝":"宝贝",
        "亲爱的":"亲爱的",
        "老公":"老公",
        "老婆":"老婆",
        "男朋友":"男朋友",
        "女朋友":"女朋友",
        "男神":"男神",
        "女神":"女神",
        "帅哥":"帅哥",
        "美女":"美女",
        "小哥哥":"小哥哥",
        "小姐姐":"小姐姐",
        "大叔":"大叔",
        "阿姨":"阿姨",
        "大爷":"大爷",
        "大妈":"大妈",
        "爷爷":"爷爷",
        "奶奶":"奶奶",
        "爸爸":"爸爸",
        "妈妈":"妈妈",
        "儿子":"儿子",
        "女儿":"女儿",
        "哥哥":"哥哥",
        "姐姐":"姐姐",
        "弟弟":"弟弟",
        "妹妹":"妹妹",
        "伯父":"伯父",
        "叔父":"叔父",
        "姑姑":"姑姑",
        "舅舅":"舅舅",
        "姨妈":"姨妈",
        "表哥":"表哥",
        "表姐":"表姐",
        "表弟":"表弟",
        "表妹":"表妹",
        "侄子":"侄子",
        "侄女":"侄女",
        "外甥":"外甥",
        "外甥女":"外甥女",
        "亲家":"亲家",
        "亲戚":"亲戚",
        "邻居":"邻居",
        "老乡":"老乡",
        "同城":"同城",
        "异地":"异地",
        "国内":"国内",
        "国外":"国外",
        "本地":"本地",
        "外地":"外地",
        "南方":"南方",
        "北方":"北方",
        "东方":"东方",
        "西方":"西方",
        "中国":"中国",
        "北京":"北京",
        "上海":"上海",
        "广州":"广州",
        "深圳":"深圳",
        "杭州":"杭州",
        "南京":"南京",
        "成都":"成都",
        "重庆":"重庆",
        "武汉":"武汉",
        "西安":"西安",
        "长沙":"长沙",
        "郑州":"郑州",
        "济南":"济南",
        "青岛":"青岛",
        "大连":"大连",
        "厦门":"厦门",
        "福州":"福州",
        "南宁":"南宁",
        "昆明":"昆明",
        "贵阳":"贵阳",
        "兰州":"兰州",
        "银川":"银川",
        "西宁":"西宁",
        "呼和浩特":"呼和浩特",
        "乌鲁木齐":"乌鲁木齐",
        "拉萨":"拉萨",
        "海口":"海口",
        "三亚":"三亚",
        "香港":"香港",
        "澳门":"澳门",
        "台湾":"台湾",
        "河北":"河北",
        "山西":"山西",
        "辽宁":"辽宁",
        "吉林":"吉林",
        "黑龙江":"黑龙江",
        "江苏":"江苏",
        "浙江":"浙江",
        "安徽":"安徽",
        "福建":"福建",
        "江西":"江西",
        "山东":"山东",
        "河南":"河南",
        "湖北":"湖北",
        "湖南":"湖南",
        "广东":"广东",
        "广西":"广西",
        "海南":"海南",
        "四川":"四川",
        "贵州":"贵州",
        "云南":"云南",
        "陕西":"陕西",
        "甘肃":"甘肃",
        "青海":"青海",
        "宁夏":"宁夏",
        "新疆":"新疆",
        "西藏":"西藏",
        "内蒙古":"内蒙古"
    }

    msg = st.text_input("问点什么", label_visibility="collapsed", key="ai_msg")
    col1, col2 = st.columns([1,1])
    with col1:
        if st.button("发送", key="ai_send"):
            res = qa.get(msg, "抱歉我暂时不懂哦，可以换个说法~")
            st.session_state.chat_history.append(("你", msg))
            st.session_state.chat_history.append(("AI", res))
    with col2:
        if st.button("清空", key="ai_clear"):
            st.session_state.chat_history = []
    for a,b in st.session_state.chat_history:
        st.write(f"**{a}**: {b}")

# ====================== 侧边栏 ======================
with st.sidebar:
    st.title("山海追剧")
    menu = st.radio("菜单", ["首页","批量解析下载","播放解析","评论区","我要反馈","VIP开通","个人中心"], key="menu")
    st.markdown("---")
    ai_customer_service()

# ====================== 视频解析 ======================
def parse_url(url):
    try:
        r = requests.get(url, timeout=10)
        vids = re.findall(r'https?://[^\s"]+\.(mp4|m3u8)', r.text)
        if vids:
            return vids[0]
    except:
        return None

def batch_parse(text):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    res = []
    for l in lines:
        u = parse_url(l)
        res.append((l, u))
    return res

# ====================== 用户系统 ======================
if "users" not in st.session_state:
    st.session_state.users = {
        "admin": {"pwd":"wangzhicheng535","is_admin":True,"vip_expire":"2099-01-01"},
        "user1": {"pwd":"123456","is_admin":False,"vip_expire":"2025-01-01"}
    }

if "current_user" not in st.session_state:
    st.session_state.current_user = None

# ====================== 评论系统 ======================
if "comments" not in st.session_state:
    st.session_state.comments = []

if "badges" not in st.session_state:
    st.session_state.badges = {}

# ====================== 反馈系统 ======================
if "feedbacks" not in st.session_state:
    st.session_state.feedbacks = []

# ====================== 登录注册（已修复重复ID）======================
def login():
    st.subheader("登录")
    u = st.text_input("用户名", key="login_user")
    p = st.text_input("密码", type="password", key="login_pwd")
    if st.button("登录", key="login_btn"):
        if u in st.session_state.users and st.session_state.users[u]["pwd"] == p:
            st.session_state.current_user = u
            st.rerun()
        else:
            st.error("用户名或密码错误")

def register():
    st.subheader("注册")
    u = st.text_input("设置用户名", key="reg_user")
    p = st.text_input("设置密码", type="password", key="reg_pwd")
    if st.button("注册", key="reg_btn"):
        if u in st.session_state.users:
            st.error("用户名已存在")
        else:
            st.session_state.users[u] = {"pwd": p, "is_admin": False, "vip_expire": "2025-01-01"}
            st.success("注册成功！请登录")
            st.rerun()

# ====================== 主程序 ======================
if not st.session_state.current_user:
    t1,t2 = st.tabs(["登录","注册"])
    with t1: login()
    with t2: register()
else:
    user = st.session_state.current_user
    info = st.session_state.users[user]
    is_admin = info["is_admin"]
    vip_expire = datetime.strptime(info["vip_expire"], "%Y-%m-%d")
    is_vip = vip_expire > datetime.now()

    st.success(f"欢迎回来，{user}")
    if st.button("退出登录", key="logout"):
        st.session_state.current_user = None
        st.rerun()

    # 首页
    if menu == "首页":
        st.title("🏠 山海追剧")
        st.subheader("全网视频批量解析 | 去广告 | 评论交流")
        st.write("支持批量解析、批量保存、在线播放、用户反馈、评论奖状")

    # 批量解析下载
    elif menu == "批量解析下载":
        st.title("📥 批量解析 & 保存视频")
        txt = st.text_area("粘贴视频链接（一行一个）", key="batch_txt")
        if st.button("批量解析", key="batch_parse"):
            data = batch_parse(txt)
            for raw, real in data:
                st.write("原始：", raw)
                st.write("解析：", real or "解析失败")
                st.divider()

        st.markdown("---")
        d_url = st.text_input("视频直链下载", key="download_url")
        fname = st.text_input("保存文件名", "video.mp4", key="download_name")
        if st.button("保存视频", key="save_btn"):
            if d_url:
                try:
                    cont = requests.get(d_url).content
                    with open(fname, "wb") as f:
                        f.write(cont)
                    st.success(f"已保存：{fname}")
                except:
                    st.error("下载失败")

    # 在线播放
    elif menu == "播放解析":
        st.title("🎬 在线播放")
        u = st.text_input("输入视频链接", key="play_url")
        if u:
            real = parse_url(u)
            if real:
                st.video(real)
            else:
                st.warning("解析失败，换线路或链接")

    # 评论区
    elif menu == "评论区":
        st.title("💬 评论区")
        st.markdown("文明发言，管理员可管理")

        content = st.text_area("发表评论", key="comment_content")
        if st.button("提交评论", key="submit_comment"):
            if content:
                ctime = datetime.now().strftime("%m-%d %H:%M")
                st.session_state.comments.append({
                    "user":user,
                    "content":content,
                    "time":ctime
                })
                st.success("评论成功")
                st.rerun()

        st.divider()

        for idx, c in enumerate(st.session_state.comments):
            badge = st.session_state.badges.get(idx, "")
            with st.container():
                st.markdown(f"""
                <div class="comment-box">
                <b>{c['user']}</b> · {c['time']}
                <br>{c['content']}
                <br><span class="badges">{badge}</span>
                </div>
                """, unsafe_allow_html=True)

                if is_admin:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button(f"删除评论 {idx+1}", key=f"del_cmt_{idx}"):
                            del st.session_state.comments[idx]
                            if idx in st.session_state.badges:
                                del st.session_state.badges[idx]
                            st.rerun()
                    with col2:
                        if st.button(f"奖状 {idx+1}", key=f"badge_cmt_{idx}"):
                            st.session_state.badges[idx] = "🏆 优质评论"
                            st.rerun()
                    with col3:
                        if st.button(f"取消奖状 {idx+1}", key=f"unbadge_cmt_{idx}"):
                            if idx in st.session_state.badges:
                                del st.session_state.badges[idx]
                            st.rerun()
                st.divider()

    # 反馈
    elif menu == "我要反馈":
        st.title("📩 问题反馈")
        st.write("遇到问题、建议、投诉都可以在这里提交")

        fb_type = st.selectbox("反馈类型", ["问题报错","功能建议","投诉举报","其他"], key="fb_type")
        fb_content = st.text_area("反馈内容", height=120, key="fb_content")
        contact = st.text_input("联系方式（可选）", key="fb_contact")

        if st.button("✅ 提交反馈", key="submit_fb"):
            if fb_content:
                fb_time = datetime.now().strftime("%Y-%m-%d %H:%M")
                st.session_state.feedbacks.append({
                    "user": user,
                    "type": fb_type,
                    "content": fb_content,
                    "contact": contact,
                    "time": fb_time
                })
                st.success("反馈已提交！管理员会尽快查看")
            else:
                st.warning("请填写反馈内容")

        if is_admin:
            st.divider()
            st.warning("🔑 管理员：查看所有用户反馈")
            if not st.session_state.feedbacks:
                st.info("暂无反馈")
            else:
                for i, fb in enumerate(st.session_state.feedbacks):
                    st.markdown(f"""
                    <div class="feedback-box">
                    <b>反馈 {i+1}</b>｜用户：{fb['user']}｜{fb['time']}<br>
                    类型：{fb['type']}<br>
                    内容：{fb['content']}<br>
                    联系方式：{fb['contact'] or '无'}
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"删除此反馈 {i+1}", key=f"del_fb_{i}"):
                        del st.session_state.feedbacks[i]
                        st.rerun()
                    st.divider()

    # VIP开通
    elif menu == "VIP开通":
        st.title("💎 VIP去广告")
        if is_vip:
            st.success("您已是VIP会员，无广告畅享")
        else:
            st.subheader("月度VIP：9.9 元")
            st.write("✅ 无广告 ✅ 高清播放 ✅ 专属线路")
            c1,c2 = st.columns(2)
            with c1:
                st.info("微信支付")
            with c2:
                st.info("支付宝支付")
            order = st.text_input("输入订单号自动开通VIP", key="vip_order")
            if st.button("开通VIP", key="vip_open"):
                if len(str(order)) >= 10:
                    exp = (datetime.now()+timedelta(days=30)).strftime("%Y-%m-%d")
                    st.session_state.users[user]["vip_expire"] = exp
                    st.success(f"VIP已开通至：{exp}")

    # 个人中心
    elif menu == "个人中心":
        st.title("👤 个人中心")
        st.write(f"用户：{user}")
        st.write(f"VIP到期：{info['vip_expire']}")
        st.write(f"VIP状态：{'已开通' if is_vip else '未开通'}")

        if is_admin:
            st.divider()
            st.warning("🔑 管理员后台")

            st.subheader("注销违规用户")
            del_user = st.text_input("输入要注销的用户名", key="admin_del_user")
            if st.button("注销该用户", key="admin_del_btn"):
                if del_user in st.session_state.users and del_user != "admin":
                    del st.session_state.users[del_user]
                    st.success(f"已注销用户：{del_user}")
                else:
                    st.error("用户不存在或不能删除admin")

            st.subheader("手动开通VIP")
            tar_user = st.text_input("目标用户名", key="admin_vip_user")
            days = st.number_input("开通天数", value=30, key="admin_vip_days")
            if st.button("开通VIP", key="admin_vip_btn"):
                if tar_user in st.session_state.users:
                    exp = (datetime.now()+timedelta(days=days)).strftime("%Y-%m-%d")
                    st.session_state.users[tar_user]["vip_expire"] = exp
                    st.success(f"已为 {tar_user} 开通VIP")

            st.subheader("所有用户")
            for uname, uinfo in st.session_state.users.items():
                st.write(f"{uname} | VIP：{uinfo['vip_expire']}")