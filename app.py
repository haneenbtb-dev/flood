import datetime
import random
import textwrap
import streamlit as st
import folium
from folium import plugins
from streamlit_folium import st_folium

# -----------------------------------------------------------------------------
# 1. إعدادات الصفحة والتصميم الهندسي لمركز قيادة العمليات (Command Center)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="مرصاد",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# تخصيص الواجهة بتصميم داكن احترافي عالي الكثافة (Operations Dashboard)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Alexandria:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;700&display=swap');

    html, body, [class*="css"], .stMarkdown, .stButton, .stSelectbox, .stSlider, .stNumberInput {
        font-family: 'Alexandria', -apple-system, BlinkMacSystemFont, sans-serif !important;
        direction: rtl;
        text-align: right;
    }
    
    .stApp {
        background-color: #070b14;
        color: #e2e8f0;
    }

    /* الشريط الرئيسي العلوي لمركز العمليات */
    .ops-header {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(17, 24, 39, 0.98) 100%);
        border: 1px solid rgba(59, 130, 246, 0.2);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        border-radius: 12px;
        padding: 0.9rem 1.4rem;
        margin-bottom: 0.9rem;
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        align-items: center;
        gap: 0.8rem;
        direction: rtl;
    }

    .ops-title-group {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .ops-logo {
        font-size: 1.9rem;
        background: linear-gradient(135deg, #38bdf8, #2563eb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .ops-title {
        font-size: 1.28rem;
        font-weight: 800;
        color: #f8fafc;
        margin: 0;
        line-height: 1.25;
    }

    .ops-subtitle {
        font-size: 0.78rem;
        color: #94a3b8;
        margin: 0;
        font-weight: 500;
    }

    .badge-live-pulse {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        background: rgba(16, 185, 129, 0.12);
        border: 1px solid rgba(16, 185, 129, 0.35);
        padding: 5px 12px;
        border-radius: 9999px;
        font-size: 0.76rem;
        font-weight: 700;
        color: #34d399;
    }

    .pulse-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background-color: #10b981;
        box-shadow: 0 0 8px #10b981;
        animation: live-pulse 1.8s infinite;
    }

    @keyframes live-pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.3; transform: scale(1.3); }
    }

    .time-chip {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.82rem;
        color: #cbd5e1;
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(148, 163, 184, 0.2);
        padding: 5px 12px;
        border-radius: 8px;
        direction: ltr;
    }

    /* بطاقات الإحصائيات العلوية KPI */
    .kpi-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
        gap: 10px;
        margin-bottom: 0.9rem;
        direction: rtl;
    }

    .kpi-card {
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.75) 100%);
        border: 1px solid rgba(75, 85, 99, 0.3);
        border-radius: 10px;
        padding: 0.75rem 0.9rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
        text-align: right;
        position: relative;
        overflow: hidden;
    }

    .kpi-card.kpi-total { border-right: 3px solid #38bdf8; }
    .kpi-card.kpi-safe { border-right: 3px solid #10b981; }
    .kpi-card.kpi-moderate { border-right: 3px solid #facc15; }
    .kpi-card.kpi-high { border-right: 3px solid #f97316; }
    .kpi-card.kpi-critical { border-right: 3px solid #ef4444; background: linear-gradient(145deg, rgba(239, 68, 68, 0.12) 0%, rgba(30, 41, 59, 0.85) 100%); }
    .kpi-card.kpi-sensors { border-right: 3px solid #6366f1; }
    .kpi-card.kpi-alerts { border-right: 3px solid #ec4899; }

    .kpi-label {
        font-size: 0.72rem;
        color: #94a3b8;
        font-weight: 600;
        margin-bottom: 0.2rem;
        white-space: nowrap;
    }

    .kpi-val {
        font-size: 1.45rem;
        font-weight: 800;
        font-family: 'Alexandria', 'JetBrains Mono', sans-serif;
        color: #f8fafc;
        line-height: 1.2;
    }

    .kpi-sub {
        font-size: 0.65rem;
        color: #64748b;
        margin-top: 0.2rem;
    }

    /* لافتة الإنذار العاجل لغرفة العمليات */
    .critical-alert-banner {
        background: linear-gradient(90deg, #7f1d1d 0%, #991b1b 50%, #b91c1c 100%);
        border: 1px solid #ef4444;
        color: #ffffff;
        padding: 10px 16px;
        border-radius: 9px;
        margin-bottom: 0.9rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        font-weight: 700;
        box-shadow: 0 0 20px rgba(220, 38, 38, 0.35);
        animation: pulse-red 2s infinite alternate;
        direction: rtl;
    }

    @keyframes pulse-red {
        from { box-shadow: 0 0 10px rgba(220, 38, 38, 0.25); }
        to { box-shadow: 0 0 22px rgba(220, 38, 38, 0.6); }
    }

    /* جدول بيانات الشوارع الموحد */
    .streets-table-container {
        background: rgba(15, 23, 42, 0.9);
        border: 1px solid rgba(51, 65, 85, 0.6);
        border-radius: 11px;
        padding: 0.8rem 1rem;
        margin-top: 0.9rem;
        direction: rtl;
    }

    .table-title-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.6rem;
    }

    .custom-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.82rem;
        text-align: right;
    }

    .custom-table th {
        background: rgba(30, 41, 59, 0.8);
        color: #94a3b8;
        padding: 8px 12px;
        font-weight: 700;
        border-bottom: 1px solid rgba(75, 85, 99, 0.4);
        white-space: nowrap;
    }

    .custom-table td {
        padding: 9px 12px;
        border-bottom: 1px solid rgba(51, 65, 85, 0.3);
        color: #e2e8f0;
        vertical-align: middle;
    }

    .custom-table tr:hover {
        background: rgba(51, 65, 85, 0.25);
    }

    .status-pill {
        display: inline-block;
        padding: 3px 9px;
        border-radius: 9999px;
        font-size: 0.72rem;
        font-weight: 700;
        white-space: nowrap;
    }

    .pill-safe { background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.35); }
    .pill-moderate { background: rgba(250, 204, 21, 0.15); color: #facc15; border: 1px solid rgba(250, 204, 21, 0.35); }
    .pill-high { background: rgba(249, 115, 22, 0.18); color: #fb923c; border: 1px solid rgba(249, 115, 22, 0.4); }
    .pill-critical { background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.45); font-weight: 800; animation: blink-text 1.5s infinite; }

    @keyframes blink-text {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.65; }
    }

    .sensor-online {
        color: #34d399;
        font-weight: 700;
        display: inline-flex;
        align-items: center;
        gap: 5px;
    }

    .mini-progress-bg {
        background: rgba(51, 65, 85, 0.5);
        height: 6px;
        width: 75px;
        border-radius: 9999px;
        overflow: hidden;
        display: inline-block;
        vertical-align: middle;
        margin-right: 6px;
    }

    .mini-progress-bar {
        height: 100%;
        border-radius: 9999px;
    }

    /* وسائل التحكم البسيطة */
    .controls-strip {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(51, 65, 85, 0.4);
        border-radius: 8px;
        padding: 6px 12px;
        margin-bottom: 0.6rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 10px;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 2. تعريف شبكة شوارع المدينة الحقيقية (10 شوارع متصلة ومترابطة في الرياض)
# -----------------------------------------------------------------------------
# قاعدة بيانات الشوارع العشرة مع إحداثيات المسارات المتصلة ونقاط الحساسات
BASE_STREETS = [
    {
        "id": "ST-01",
        "name": "طريق الملك فهد (قطاع النفق المركزي)",
        "coords": [[24.6980, 46.6800], [24.7060, 46.6825], [24.7145, 46.6850], [24.7230, 46.6875], [24.7310, 46.6900]],
        "sensor_loc": [24.7145, 46.6850],
        "base_depth": 34,
        "base_pct": 92,
        "status": "حرج / معرض للغرق",
        "status_color": "#ef4444",
        "pill_class": "pill-critical",
        "sensor_status": "متصل (رادار مزدوج)",
        "sensor_color": "#34d399",
        "drainage": "4 مضخات غاطسة تعمل بأقصى طاقة",
        "closure": "مغلق بقرار الدفاع المدني (تحويل إلى الدائري)",
        "last_seen_sec": 4
    },
    {
        "id": "ST-02",
        "name": "طريق مكة المكرمة (خريص - تقاطع العليا)",
        "coords": [[24.7080, 46.6580], [24.7100, 46.6720], [24.7120, 46.6860], [24.7140, 46.7000], [24.7160, 46.7140]],
        "sensor_loc": [24.7120, 46.6860],
        "base_depth": 21,
        "base_pct": 68,
        "status": "ارتفاع مرتفع",
        "status_color": "#f97316",
        "pill_class": "pill-high",
        "sensor_status": "متصل (ألتراسونيك)",
        "sensor_color": "#34d399",
        "drainage": "مضختان قيد التشغيل",
        "closure": "مسار الشاحنات فقط - تنبيه للسيدان",
        "last_seen_sec": 8
    },
    {
        "id": "ST-03",
        "name": "طريق التخصصي (منخفض وادي حنيفة)",
        "coords": [[24.6850, 46.6620], [24.6980, 46.6670], [24.7110, 46.6720], [24.7240, 46.6770], [24.7370, 46.6820]],
        "sensor_loc": [24.7110, 46.6720],
        "base_depth": 11,
        "base_pct": 36,
        "status": "ارتفاع متوسط",
        "status_color": "#facc15",
        "pill_class": "pill-moderate",
        "sensor_status": "متصل (هيدروليكي)",
        "sensor_color": "#34d399",
        "drainage": "تصريف طبيعي مستمر",
        "closure": "سالك مع تخفيف السرعة",
        "last_seen_sec": 11
    },
    {
        "id": "ST-04",
        "name": "طريق العروبة (نفق تقاطع التخصصي)",
        "coords": [[24.7200, 46.6600], [24.7215, 46.6730], [24.7230, 46.6860], [24.7245, 46.6990], [24.7260, 46.7120]],
        "sensor_loc": [24.7215, 46.6730],
        "base_depth": 28,
        "base_pct": 86,
        "status": "حرج / معرض للغرق",
        "status_color": "#ef4444",
        "pill_class": "pill-critical",
        "sensor_status": "متصل (رادار ليزري)",
        "sensor_color": "#34d399",
        "drainage": "3 مضخات طوارئ تعمل",
        "closure": "إغلاق جزئي لحارات النفق السفلية",
        "last_seen_sec": 3
    },
    {
        "id": "ST-05",
        "name": "طريق الملك عبدالله (المسار السطحي والخدمة)",
        "coords": [[24.7350, 46.6500], [24.7370, 46.6680], [24.7390, 46.6860], [24.7410, 46.7040], [24.7430, 46.7220]],
        "sensor_loc": [24.7390, 46.6860],
        "base_depth": 4,
        "base_pct": 14,
        "status": "طبيعي",
        "status_color": "#10b981",
        "pill_class": "pill-safe",
        "sensor_status": "متصل (رادار)",
        "sensor_color": "#34d399",
        "drainage": "جاهزية الاستعداد",
        "closure": "سالك ومفتوح بالكامل",
        "last_seen_sec": 14
    },
    {
        "id": "ST-06",
        "name": "طريق الإمام سعود بن عبدالعزيز بن محمد",
        "coords": [[24.7550, 46.6550], [24.7570, 46.6720], [24.7590, 46.6890], [24.7610, 46.7060], [24.7630, 46.7230]],
        "sensor_loc": [24.7590, 46.6890],
        "base_depth": 2,
        "base_pct": 8,
        "status": "طبيعي",
        "status_color": "#10b981",
        "pill_class": "pill-safe",
        "sensor_status": "متصل (ألتراسونيك)",
        "sensor_color": "#34d399",
        "drainage": "تصريف طبيعي",
        "closure": "سالك ومفتوح بالكامل",
        "last_seen_sec": 18
    },
    {
        "id": "ST-07",
        "name": "طريق الأمير تركي بن عبدالعزيز الأول",
        "coords": [[24.7000, 46.6450], [24.7150, 46.6480], [24.7300, 46.6510], [24.7450, 46.6540], [24.7600, 46.6570]],
        "sensor_loc": [24.7300, 46.6510],
        "base_depth": 17,
        "base_pct": 54,
        "status": "ارتفاع مرتفع",
        "status_color": "#f97316",
        "pill_class": "pill-high",
        "sensor_status": "متصل (مسبار ضغط)",
        "sensor_color": "#34d399",
        "drainage": "مضخة هيدروليكية تعمل",
        "closure": "تحذير من تجمعات مياه جانبية",
        "last_seen_sec": 6
    },
    {
        "id": "ST-08",
        "name": "طريق أبي بكر الصديق (تقاطع مخرج 6)",
        "coords": [[24.7300, 46.7020], [24.7450, 46.7060], [24.7600, 46.7100], [24.7750, 46.7140], [24.7900, 46.7180]],
        "sensor_loc": [24.7600, 46.7100],
        "base_depth": 8,
        "base_pct": 26,
        "status": "ارتفاع متوسط",
        "status_color": "#facc15",
        "pill_class": "pill-moderate",
        "sensor_status": "متصل (ألتراسونيك)",
        "sensor_color": "#34d399",
        "drainage": "قنوات السيول سالكة",
        "closure": "سالك مع تنبيه مروري",
        "last_seen_sec": 9
    },
    {
        "id": "ST-09",
        "name": "طريق الملك عبدالعزيز (نفق تقاطع العروبة)",
        "coords": [[24.7050, 46.7050], [24.7200, 46.7080], [24.7350, 46.7110], [24.7500, 46.7140], [24.7650, 46.7170]],
        "sensor_loc": [24.7200, 46.7080],
        "base_depth": 3,
        "base_pct": 10,
        "status": "طبيعي",
        "status_color": "#10b981",
        "pill_class": "pill-safe",
        "sensor_status": "متصل (رادار)",
        "sensor_color": "#34d399",
        "drainage": "تصريف طبيعي",
        "closure": "سالك ومفتوح بالكامل",
        "last_seen_sec": 22
    },
    {
        "id": "ST-10",
        "name": "طريق عثمان بن عفان (المخرج الشمالي)",
        "coords": [[24.7320, 46.7200], [24.7470, 46.7240], [24.7620, 46.7280], [24.7770, 46.7320], [24.7920, 46.7360]],
        "sensor_loc": [24.7620, 46.7280],
        "base_depth": 1,
        "base_pct": 4,
        "status": "طبيعي",
        "status_color": "#10b981",
        "pill_class": "pill-safe",
        "sensor_status": "متصل (رادار ليزري)",
        "sensor_color": "#34d399",
        "drainage": "تصريف طبيعي",
        "closure": "سالك ومفتوح بالكامل",
        "last_seen_sec": 15
    }
]


# -----------------------------------------------------------------------------
# 3. محاكاة بيانات حية متغيرة طفيفاً (Live Telemetry Stream)
# -----------------------------------------------------------------------------
# إضافة تقلب طفيف عشوائي ±1-2 سم لإظهار تدفق البيانات الحية لحظياً
streets_data = []
random.seed(int(datetime.datetime.now().minute * 60 + datetime.datetime.now().second // 10))

for st_info in BASE_STREETS:
    delta = random.randint(-1, 1)
    current_depth = max(0, min(50, st_info["base_depth"] + delta))
    
    # حساب نسبة مستوى المياه بناءً على عمق 35 سم كحد أقصى للغمر
    current_pct = min(100, int((current_depth / 35.0) * 100))
    
    # تحديد الحالة بدقة
    if current_depth < 7:
        status_text = "طبيعي"
        status_color = "#10b981"
        pill_class = "pill-safe"
    elif 7 <= current_depth <= 15:
        status_text = "ارتفاع متوسط"
        status_color = "#facc15"
        pill_class = "pill-moderate"
    elif 16 <= current_depth <= 24:
        status_text = "ارتفاع مرتفع"
        status_color = "#f97316"
        pill_class = "pill-high"
    else:
        status_text = "حرج / معرض للغرق"
        status_color = "#ef4444"
        pill_class = "pill-critical"

    updated_sec = random.randint(3, 20)

    streets_data.append({
        **st_info,
        "depth": current_depth,
        "pct": current_pct,
        "status": status_text,
        "status_color": status_color,
        "pill_class": pill_class,
        "last_seen": f"قبل {updated_sec} ثوانٍ"
    })

# حساب الإحصائيات الإجمالية
total_streets = len(streets_data)
safe_count = sum(1 for s in streets_data if s["status"] == "طبيعي")
moderate_count = sum(1 for s in streets_data if s["status"] == "ارتفاع متوسط")
high_count = sum(1 for s in streets_data if s["status"] == "ارتفاع مرتفع")
critical_count = sum(1 for s in streets_data if "حرج" in s["status"])
connected_sensors = sum(1 for s in streets_data if "متصل" in s["sensor_status"])
active_alerts = high_count + critical_count
critical_streets = [s for s in streets_data if "حرج" in s["status"]]

# -----------------------------------------------------------------------------
# 4. الشريط الرئاسي العلوي (Operations Command Header)
# -----------------------------------------------------------------------------
now_time = datetime.datetime.now().strftime("%Y-%m-%d | %H:%M:%S")

st.markdown(textwrap.dedent(f"""
    <div class="ops-header">
        <div class="ops-title-group">
            <span class="ops-logo">🛡️</span>
            <div>
                <h1 class="ops-title">مِـرْصَـاد</h1>
                <p class="ops-subtitle">غرفة القيادة والتحكم الموحدة • رصد شبكة الطرق الحضرية الذكية (10 شوارع رئيسية متصلة)</p>
            </div>
        </div>
        <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
            <div class="badge-live-pulse">
                <span class="pulse-dot"></span>
                بث حي مباشر للحساسات الميدانية (Active Grid)
            </div>
            <div class="time-chip">🕒 {now_time}</div>
        </div>
    </div>
"""), unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 5. شريط الإحصائيات الشامل (KPI Summary Cards)
# -----------------------------------------------------------------------------
st.markdown(textwrap.dedent(f"""
    <div class="kpi-container">
        <div class="kpi-card kpi-total">
            <div class="kpi-label">🛣️ إجمالي الشوارع المراقبة</div>
            <div class="kpi-val" style="color:#38bdf8;">{total_streets}</div>
            <div class="kpi-sub">شبكة محاور رئيسية متصلة</div>
        </div>
        <div class="kpi-card kpi-safe">
            <div class="kpi-label">🟢 الشوارع الطبيعية</div>
            <div class="kpi-val" style="color:#10b981;">{safe_count}</div>
            <div class="kpi-sub">لا توجد مياه راكدة ({int((safe_count/total_streets)*100)}%)</div>
        </div>
        <div class="kpi-card kpi-moderate">
            <div class="kpi-label">🟡 ارتفاع متوسط</div>
            <div class="kpi-val" style="color:#facc15;">{moderate_count}</div>
            <div class="kpi-sub">منسوب 7 - 15 سم</div>
        </div>
        <div class="kpi-card kpi-high">
            <div class="kpi-label">🟠 ارتفاع مرتفع (خطورة)</div>
            <div class="kpi-val" style="color:#fb923c;">{high_count}</div>
            <div class="kpi-sub">منسوب 16 - 24 سم</div>
        </div>
        <div class="kpi-card kpi-critical">
            <div class="kpi-label">🔴 شوارع حرجة / غمر</div>
            <div class="kpi-val" style="color:#f87171;">{critical_count}</div>
            <div class="kpi-sub">منسوب ≥ 25 سم (تدخل عاجل)</div>
        </div>
        <div class="kpi-card kpi-sensors">
            <div class="kpi-label">📡 الحساسات المتصلة</div>
            <div class="kpi-val" style="color:#818cf8;">{connected_sensors}/{total_streets}</div>
            <div class="kpi-sub">تغطية شبكية بنسبة 100%</div>
        </div>
        <div class="kpi-card kpi-alerts">
            <div class="kpi-label">🚨 التنبيهات النشطة</div>
            <div class="kpi-val" style="color:#f472b6;">{active_alerts}</div>
            <div class="kpi-sub">تستدعي تدخل الفرق الميدانية</div>
        </div>
    </div>
"""), unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 6. لافتة الإنذار العاجل لغرفة العمليات عند وجود شوارع حرجة
# -----------------------------------------------------------------------------
if critical_count > 0:
    critical_names = " • ".join([f"<b>{s['name']}</b> ({s['depth']} سم - {s['pct']}%)" for s in critical_streets])
    st.markdown(textwrap.dedent(f"""
        <div class="critical-alert-banner">
            <div style="display:flex; align-items:center; gap:12px;">
                <span style="font-size:1.6rem;">⚠️</span>
                <div>
                    <div style="font-size:1.02rem; letter-spacing:0.01em;">إنذار أمني طارئ: تم رصد {critical_count} شوارع في مرحلة الغمر الحرج</div>
                    <div style="font-size:0.83rem; font-weight:500; opacity:0.95; margin-top:2px;">الشوارع المتأثرة: {critical_names} — يتطلب تدخلاً فورياً، تشغيل مضخات الطوارئ وتفعيل خطة التحويل المروري.</div>
                </div>
            </div>
            <div style="background:rgba(0,0,0,0.35); padding:5px 14px; border-radius:6px; font-size:0.8rem; font-family:'JetBrains Mono'; white-space:nowrap;">
                CIVIL-DEFENSE ALERT-LVL-4
            </div>
        </div>
    """), unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 7. الخريطة التفاعلية المركزية الكبرى (Unified Real City Connected Map)
# -----------------------------------------------------------------------------
# مركز المدينة (الرياض - شبكة المحاور الرئيسية)
CITY_MAP_CENTER = [24.7350, 46.6850]

# إنشاء خريطة Folium واقعية عالية الدقة بنمط داكن يناسب غرف العمليات
m = folium.Map(
    location=CITY_MAP_CENTER,
    zoom_start=12.8,
    tiles="CartoDB dark_matter",
    control_scale=True,
    prefer_canvas=True
)

# رسم جميع الشوارع العشرة المتصلة وإضافة الحساسات الميدانية
for st_item in streets_data:
    # 1. رسم مسار الشارع بلونه الموحد الدال على حالته
    is_critical = "حرج" in st_item["status"]
    line_weight = 7 if is_critical else 5
    line_opacity = 0.95 if is_critical else 0.85
    
    # تلميح يظهر عند تمرير الفأرة على مسار الشارع
    tooltip_content = f"""
        <div style="font-family:'Alexandria', sans-serif; direction:rtl; text-align:right; font-size:12px;">
            <b>{st_item['name']}</b><br>
            الحالة: <span style="color:{st_item['status_color']}; font-weight:bold;">{st_item['status']}</span><br>
            العمق: <b>{st_item['depth']} سم</b> ({st_item['pct']}%)<br>
            الحساس: {st_item['sensor_status']}
        </div>
    """

    folium.PolyLine(
        locations=st_item["coords"],
        color=st_item["status_color"],
        weight=line_weight,
        opacity=line_opacity,
        tooltip=folium.Tooltip(tooltip_content),
        popup=folium.Popup(f"""
            <div style="font-family:'Alexandria', sans-serif; direction:rtl; text-align:right; min-width:210px;">
                <h4 style="margin:0 0 5px 0; color:#0f172a; font-size:14px; font-weight:800;">{st_item['name']}</h4>
                <hr style="margin:4px 0; border:0; border-top:1px solid #cbd5e1;">
                <b>معرّف المسار:</b> {st_item['id']}<br>
                <b>الحالة الميدانية:</b> <span style="color:{st_item['status_color']}; font-weight:bold;">{st_item['status']}</span><br>
                <b>منسوب عمق المياه:</b> <b style="font-size:14px; color:{st_item['status_color']};">{st_item['depth']} سم</b> ({st_item['pct']}%)<br>
                <b>جاهزية التصريف:</b> {st_item['drainage']}<br>
                <b>الإجراء المروري:</b> <span style="color:#b91c1c; font-weight:bold;">{st_item['closure']}</span><br>
                <b>آخر قراءة:</b> {st_item['last_seen']}
            </div>
        """, max_width=330)
    ).add_to(m)

    # 2. إضافة علامة نقطة الحساس الذكي (Sensor Node) على الشارع
    # اختيار لون وأيقونة الحساس حسب الخطورة
    if "طبيعي" in st_item["status"]:
        icon_name = "tint"
        marker_color = "green"
    elif "متوسط" in st_item["status"]:
        icon_name = "info-circle"
        marker_color = "cadetblue"
    elif "مرتفع" in st_item["status"]:
        icon_name = "exclamation-circle"
        marker_color = "orange"
    else:
        icon_name = "exclamation-triangle"
        marker_color = "red"

    folium.Marker(
        location=st_item["sensor_loc"],
        popup=folium.Popup(f"""
            <div style="font-family:'Alexandria', sans-serif; direction:rtl; text-align:right; min-width:200px;">
                <h4 style="margin:0 0 4px 0; color:{st_item['status_color']}; font-size:13px; font-weight:800;">📡 محطة الحساس: {st_item['id']}</h4>
                <b>الموقع:</b> {st_item['name']}<br>
                <b>العمق اللحظي:</b> <b style="color:{st_item['status_color']}; font-size:15px;">{st_item['depth']} سم</b> ({st_item['pct']}%)<br>
                <b>حالة الحساس:</b> <span style="color:#10b981; font-weight:bold;">{st_item['sensor_status']}</span><br>
                <b>حالة الشارع:</b> {st_item['status']}<br>
                <b>التحديث:</b> {st_item['last_seen']}
            </div>
        """, max_width=320),
        tooltip=f"حساس {st_item['id']} - {st_item['name']} ({st_item['depth']} سم)",
        icon=folium.Icon(color=marker_color, icon=icon_name, prefix="fa")
    ).add_to(m)

# إضافة أداة ملء الشاشة وطبقات الخريطة
plugins.Fullscreen(position="topleft").add_to(m)

# عرض الخريطة كأكبر عنصر في الصفحة
st_folium(m, width="100%", height=560, returned_objects=[])

# دليل الألوان والحالات أسفل الخريطة مباشرة
st.markdown(textwrap.dedent("""
    <div style="display:flex; justify-content:space-around; align-items:center; background:rgba(15,23,42,0.85); padding:8px 14px; border-radius:8px; border:1px solid rgba(51,65,85,0.4); font-size:0.78rem; margin-top:6px; flex-wrap:wrap; gap:8px;">
        <div style="display:flex; align-items:center; gap:6px;">
            <span style="display:inline-block; width:14px; height:14px; background:#10b981; border-radius:3px;"></span>
            <b>أخضر:</b> طبيعي — لا توجد مياه (< 7 سم)
        </div>
        <div style="display:flex; align-items:center; gap:6px;">
            <span style="display:inline-block; width:14px; height:14px; background:#facc15; border-radius:3px;"></span>
            <b>أصفر:</b> ارتفاع متوسط (7 - 15 سم)
        </div>
        <div style="display:flex; align-items:center; gap:6px;">
            <span style="display:inline-block; width:14px; height:14px; background:#f97316; border-radius:3px;"></span>
            <b>برتقالي:</b> ارتفاع مرتفع — خطورة (16 - 24 سم)
        </div>
        <div style="display:flex; align-items:center; gap:6px;">
            <span style="display:inline-block; width:14px; height:14px; background:#ef4444; border-radius:3px; animation:blink-text 1.5s infinite;"></span>
            <b>أحمر:</b> حرج / معرض للغرق (≥ 25 سم — إغلاق وتدخل)
        </div>
        <div style="display:flex; align-items:center; gap:6px; color:#94a3b8;">
            <span>📡 اضغط على أي شارع أو حساس لعرض القياسات اللحظية والتفاصيل الميدانية</span>
        </div>
    </div>
"""), unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 8. جدول بيانات الشوارع الموحد (Unified Operations Matrix Table)
# -----------------------------------------------------------------------------
table_rows_html = ""

for s in streets_data:
    bar_color = s["status_color"]
    pct_val = s["pct"]
    depth_val = s["depth"]
    s_id = s["id"]
    s_name = s["name"]
    s_status = s["status"]
    s_sensor = s["sensor_status"]
    s_drainage = s["drainage"]
    s_closure = s["closure"]
    s_seen = s["last_seen"]
    pill_c = s["pill_class"]

    pct_bar = f"<div style='display:inline-flex; align-items:center;'><div class='mini-progress-bg'><div class='mini-progress-bar' style='width:{pct_val}%; background-color:{bar_color};'></div></div><span style='font-family:JetBrains Mono; font-weight:700; font-size:0.75rem; color:{bar_color};'>{pct_val}%</span></div>"
    depth_str = f"<b style='font-family:JetBrains Mono; color:{bar_color};'>{depth_val} سم</b>"
    status_badge = f"<span class='status-pill {pill_c}'>{s_status}</span>"
    sensor_badge = f"<span class='sensor-online'>🟢 {s_sensor}</span>"
    closure_color = '#f87171' if 'مغلق' in s_closure else '#cbd5e1'
    closure_weight = '800' if 'مغلق' in s_closure else '500'
    
    table_rows_html += (
        f"<tr>"
        f"<td style='font-weight:700;'><span style='color:#94a3b8; font-size:0.75rem; font-family:JetBrains Mono; margin-left:6px;'>{s_id}</span>{s_name}</td>"
        f"<td>{pct_bar}</td>"
        f"<td>{depth_str}</td>"
        f"<td>{status_badge}</td>"
        f"<td>{sensor_badge}</td>"
        f"<td style='font-size:0.75rem; color:#94a3b8;'>{s_drainage}</td>"
        f"<td style='font-size:0.75rem; color:{closure_color}; font-weight:{closure_weight};'>{s_closure}</td>"
        f"<td style='font-family:JetBrains Mono; font-size:0.74rem; color:#64748b; direction:ltr; text-align:right;'>{s_seen}</td>"
        f"</tr>"
    )

table_wrapper_html = (
    f"<div class='streets-table-container'>"
    f"<div class='table-title-row'>"
    f"<div style='display:flex; align-items:center; gap:8px;'>"
    f"<span style='font-size:1.2rem;'>📊</span>"
    f"<h3 style='margin:0; font-size:1.05rem; font-weight:800; color:#f8fafc;'>جدول الرصد الميداني الشامل</h3>"
    f"</div>"
    f"<div style='font-size:0.76rem; color:#94a3b8;'>تحديث حي ومباشر لكافة العقد الهيدرولوجية</div>"
    f"</div>"
    f"<div style='overflow-x:auto;'>"
    f"<table class='custom-table'>"
    f"<thead><tr>"
    f"<th>اسم الشارع والمحور الميداني</th><th>مستوى المياه %</th><th>عمق المياه</th><th>حالة الشارع</th><th>حالة الحساس</th><th>مضخات التصريف</th><th>الإجراء المروري والتدخل</th><th>آخر تحديث</th>"
    f"</tr></thead>"
    f"<tbody>{table_rows_html}</tbody>"
    f"</table></div></div>"
)

st.markdown(table_wrapper_html, unsafe_allow_html=True)
