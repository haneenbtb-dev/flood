import datetime
import textwrap
import streamlit as st
import folium
from folium import plugins
from streamlit_folium import st_folium

# -----------------------------------------------------------------------------
# 1. إعدادات الصفحة والتصميم (واجهة مركز قيادة العمليات الذكية - دعم كامل للعربية و RTL)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="نظام مراقبة تجمعات السيول والملاحة الذكية",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تخصيص الواجهة بتنسيق عصري داكن وخطوط عربية احترافية مع دعم اتجاه النص من اليمين لليسار (RTL)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Alexandria:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600;700&display=swap');

    html, body, [class*="css"], .stMarkdown, .stButton, .stSelectbox, .stSlider, .stNumberInput {
        font-family: 'Alexandria', -apple-system, BlinkMacSystemFont, sans-serif !important;
        direction: rtl;
        text-align: right;
    }
    
    .stApp {
        background-color: #0b0f19;
        color: #e2e8f0;
    }

    /* الشريط العلوي لمركز القيادة */
    .command-header {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.9) 100%);
        border: 1px solid rgba(59, 130, 246, 0.25);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 14px;
        padding: 1.25rem 1.75rem;
        margin-bottom: 1.25rem;
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        align-items: center;
        gap: 1rem;
        direction: rtl;
    }

    .header-title-container {
        display: flex;
        align-items: center;
        gap: 14px;
    }

    .header-icon {
        font-size: 2.2rem;
        background: linear-gradient(135deg, #0ea5e9, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: inline-block;
    }

    .header-title {
        font-size: 1.45rem;
        font-weight: 800;
        letter-spacing: -0.01em;
        color: #f8fafc;
        margin: 0;
        line-height: 1.3;
    }

    .header-subtitle {
        font-size: 0.88rem;
        color: #94a3b8;
        margin: 0;
        font-weight: 500;
    }

    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid rgba(16, 185, 129, 0.4);
        padding: 6px 14px;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 700;
        color: #34d399;
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.2);
    }

    .status-pulse {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #10b981;
        box-shadow: 0 0 8px #10b981;
        animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.4; transform: scale(1.3); }
    }

    .time-badge {
        font-family: 'JetBrains Mono', 'Alexandria', monospace;
        font-size: 0.88rem;
        color: #cbd5e1;
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(148, 163, 184, 0.2);
        padding: 6px 12px;
        border-radius: 8px;
        direction: ltr;
        text-align: center;
    }

    /* بطاقات المؤشرات الرقمية */
    .metric-card {
        background: linear-gradient(145deg, rgba(17, 24, 39, 0.9) 0%, rgba(31, 41, 55, 0.8) 100%);
        border: 1px solid rgba(75, 85, 99, 0.3);
        border-radius: 12px;
        padding: 1.1rem 1.25rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
        transition: transform 0.2s ease, border-color 0.2s ease;
        text-align: right;
    }
    .metric-card:hover {
        border-color: rgba(59, 130, 246, 0.5);
        transform: translateY(-2px);
    }

    .metric-label {
        font-size: 0.85rem;
        color: #94a3b8;
        font-weight: 700;
        margin-bottom: 0.4rem;
    }

    .metric-value {
        font-size: 1.75rem;
        font-weight: 900;
        font-family: 'Alexandria', 'JetBrains Mono', sans-serif;
        color: #f8fafc;
        display: flex;
        align-items: baseline;
        justify-content: flex-start;
        gap: 6px;
    }

    .metric-unit {
        font-size: 0.9rem;
        color: #64748b;
        font-weight: 600;
    }

    .metric-sub {
        font-size: 0.78rem;
        margin-top: 0.4rem;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* بطاقات مصفوفة عبور المركبات */
    .vehicle-card {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(51, 65, 85, 0.6);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.75rem;
        position: relative;
        overflow: hidden;
        text-align: right;
    }

    .vehicle-card.status-safe {
        border-right: 4px solid #10b981;
        background: linear-gradient(270deg, rgba(16, 185, 129, 0.08) 0%, rgba(15, 23, 42, 0.8) 100%);
    }

    .vehicle-card.status-caution {
        border-right: 4px solid #f59e0b;
        background: linear-gradient(270deg, rgba(245, 158, 11, 0.08) 0%, rgba(15, 23, 42, 0.8) 100%);
    }

    .vehicle-card.status-danger {
        border-right: 4px solid #ef4444;
        background: linear-gradient(270deg, rgba(239, 68, 68, 0.12) 0%, rgba(15, 23, 42, 0.8) 100%);
    }

    .vehicle-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
    }

    .vehicle-title {
        font-weight: 800;
        font-size: 0.98rem;
        color: #f1f5f9;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .badge-pill {
        font-size: 0.76rem;
        font-weight: 800;
        padding: 3px 10px;
        border-radius: 9999px;
    }

    .badge-safe {
        background: rgba(16, 185, 129, 0.2);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.4);
    }

    .badge-caution {
        background: rgba(245, 158, 11, 0.2);
        color: #fbbf24;
        border: 1px solid rgba(245, 158, 11, 0.4);
    }

    .badge-danger {
        background: rgba(239, 68, 68, 0.2);
        color: #f87171;
        border: 1px solid rgba(239, 68, 68, 0.4);
        box-shadow: 0 0 10px rgba(239, 68, 68, 0.2);
    }

    /* شريط نسبة الخطر والارتفاع */
    .clearance-track {
        background: rgba(51, 65, 85, 0.4);
        height: 7px;
        border-radius: 9999px;
        overflow: hidden;
        margin-top: 8px;
    }

    .clearance-fill {
        height: 100%;
        border-radius: 9999px;
        transition: width 0.4s ease;
    }

    /* لافتة الطوارئ الحمراء */
    .emergency-banner {
        background: linear-gradient(90deg, #b91c1c 0%, #dc2626 50%, #991b1b 100%);
        color: #ffffff;
        padding: 12px 18px;
        border-radius: 10px;
        margin-bottom: 1.25rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        font-weight: 800;
        box-shadow: 0 0 25px rgba(220, 38, 38, 0.4);
        animation: emergency-glow 1.8s infinite alternate;
        direction: rtl;
    }

    @keyframes emergency-glow {
        from { box-shadow: 0 0 10px rgba(220, 38, 38, 0.3); }
        to { box-shadow: 0 0 25px rgba(220, 38, 38, 0.7); }
    }

    /* بطاقة سجل الأحداث */
    .log-container {
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(51, 65, 85, 0.5);
        border-radius: 12px;
        padding: 0.75rem 1rem;
        direction: rtl;
        display: flex;
        flex-direction: column;
        gap: 8px;
    }

    .log-item {
        font-size: 0.85rem;
        padding: 8px 12px;
        background: rgba(30, 41, 59, 0.4);
        border-radius: 8px;
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .log-time {
        font-family: 'JetBrains Mono', monospace;
        color: #94a3b8;
        min-width: 85px;
        direction: ltr;
        text-align: center;
        font-size: 0.8rem;
    }

    .log-tag {
        font-weight: 800;
        font-size: 0.75rem;
        padding: 2px 8px;
        border-radius: 6px;
        min-width: 80px;
        text-align: center;
    }

    .tag-critical { background: rgba(239, 68, 68, 0.25); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.4); }
    .tag-warning { background: rgba(245, 158, 11, 0.25); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.4); }
    .tag-info { background: rgba(59, 130, 246, 0.25); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.4); }
    .tag-action { background: rgba(16, 185, 129, 0.25); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.4); }

    .log-message {
        color: #cbd5e1;
        flex: 1;
        font-weight: 500;
    }

    section[data-testid="stSidebar"] {
        direction: rtl;
        text-align: right;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 2. لوحة التحكم الجانبية ومحاكاة البيانات الحية (Sidebar)
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown(textwrap.dedent("""
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:15px;">
            <span style="font-size:1.8rem;">🎛️</span>
            <div>
                <h3 style="margin:0; color:#f8fafc; font-size:1.15rem; font-weight:800;">محاكي الحساسات الحية</h3>
                <span style="color:#64748b; font-size:0.75rem;">بيانات إنترنت الأشياء (IoT) والتحكم الميداني</span>
            </div>
        </div>
    """), unsafe_allow_html=True)

    preset = st.selectbox(
        "⚡ سيناريوهات العرض السريع",
        options=[
            "تحكم يدوي مخصص",
            "سيناريو 1: أجواء مستقرة وطريق آمن",
            "سيناريو 2: هطول مفاجئ وتحذير سيول (حذر)",
            "سيناريو 3: غمر كامل وسيول جارفة (إغلاق الطريق)"
        ],
        index=0
    )

    if preset == "سيناريو 1: أجواء مستقرة وطريق آمن":
        default_depth = 5
    elif preset == "سيناريو 2: هطول مفاجئ وتحذير سيول (حذر)":
        default_depth = 18
    elif preset == "سيناريو 3: غمر كامل وسيول جارفة (إغلاق الطريق)":
        default_depth = 34
    else:
        default_depth = 22

    water_depth = st.slider(
        "🌊 منسوب عمق المياه في الطريق (سم)",
        min_value=0,
        max_value=50,
        value=default_depth,
        step=1,
        help="محاكاة قراءات حساسات الرادار والألتراسونيك في نفق طريق الملك فهد الحيوي."
    )

    st.markdown("---")
    st.markdown("##### ⚙️ القياسات البيئية المرافقة")
    
    if water_depth < 12:
        rain_label = "أمطار خفيفة (4 ملم/س)"
        rate_val = round(water_depth * 0.08 + 0.2, 1)
        rain_class = "خفيف"
        status_state = "GREEN"
    elif 12 <= water_depth < 25:
        rain_label = "هطول رعدي متوسط (18 ملم/س)"
        rate_val = round(water_depth * 0.15 + 0.8, 1)
        rain_class = "متوسط"
        status_state = "ORANGE"
    else:
        rain_label = "عاصفة مطرية شديدة وسيول (45 ملم/س)"
        rate_val = round(water_depth * 0.22 + 1.6, 1)
        rain_class = "شديد / غزير جداً"
        status_state = "RED"

    rain_intensity = st.selectbox(
        "🌧️ بث رادار قياس كثافة الأمطار",
        options=["أمطار خفيفة (4 ملم/س)", "هطول رعدي متوسط (18 ملم/س)", "عاصفة مطرية شديدة وسيول (45 ملم/س)"],
        index=0 if rain_class == "خفيف" else (1 if rain_class == "متوسط" else 2)
    )

    accumulation_rate = st.number_input(
        "📈 معدل تدفق وتراكم المياه (سم/دقيقة)",
        min_value=0.0,
        max_value=10.0,
        value=rate_val,
        step=0.1
    )

    st.markdown("---")
    st.markdown("##### 🚨 إجراءات الاستجابة الآلية الذكية")
    drainage_pumps = st.toggle("⚡ تفعيل مضخات التصريف الهيدروليكية العملاقة", value=(water_depth >= 15))
    sms_broadcast = st.toggle("📡 إرسال رسائل التحذير العامة (SMS Broadcast)", value=(water_depth >= 25))
    variable_signs = st.toggle("🪧 تفعيل لوحات الرسائل المتغيرة على الطرق (VMS)", value=(water_depth >= 12))

    st.markdown(textwrap.dedent("""
        <div style="background:rgba(30,41,59,0.5); padding:10px; border-radius:8px; margin-top:20px; font-size:0.75rem; color:#94a3b8; border:1px solid rgba(75,85,99,0.2);">
            <b>معرّف شبكة الحساسات:</b> SG-RIYADH-402<br>
            <b>معدل التحديث:</b> كل 1 ثانية<br>
            <b>العقدة الميدانية:</b> نفق القطاع الشمالي
        </div>
    """), unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 3. الشريط العلوي وحساب حالة الطريق
# -----------------------------------------------------------------------------
now_str = datetime.datetime.now().strftime("%Y-%m-%d | %H:%M:%S")

if water_depth < 12:
    status_label = "الطريق آمن وسالك تماماً"
    status_color = "#10b981"
    status_bg = "rgba(16, 185, 129, 0.2)"
    road_polyline_color = "#10b981"
    status_icon = "🟢"
    status_level = "آمن (أخضر)"
elif 12 <= water_depth < 25:
    status_label = "تحذير: تجمع مياه - القيادة بحذر"
    status_color = "#f59e0b"
    status_bg = "rgba(245, 158, 11, 0.2)"
    road_polyline_color = "#f59e0b"
    status_icon = "🟡"
    status_level = "تنبيه (برتقالي)"
else:
    status_label = "الطريق مغمور ومغلق - تم تفعيل المسار البديل"
    status_color = "#ef4444"
    status_bg = "rgba(239, 68, 68, 0.25)"
    road_polyline_color = "#ef4444"
    status_icon = "🔴"
    status_level = "خطر وسيول (أحمر)"

st.markdown(textwrap.dedent(f"""
    <div class="command-header">
        <div class="header-title-container">
            <span class="header-icon">🛡️</span>
            <div>
                <h1 class="header-title">نظام مراقبة تجمعات السيول والملاحة الذكية</h1>
                <p class="header-subtitle">مركز التحكم وإدارة طوارئ المدينة الذكية • رصد مباشر للمستشعرات الميدانية</p>
            </div>
        </div>
        <div style="display:flex; align-items:center; gap:12px; flex-wrap:wrap;">
            <div class="status-badge">
                <span class="status-pulse"></span>
                النظام نشط - الحساسات متصلة بالكامل
            </div>
            <div class="time-badge">🕒 {now_str}</div>
        </div>
    </div>
"""), unsafe_allow_html=True)

if "أحمر" in status_level:
    st.markdown(textwrap.dedent(f"""
        <div class="emergency-banner">
            <div style="display:flex; align-items:center; gap:14px;">
                <span style="font-size:1.8rem;">⚠️</span>
                <div>
                    <div style="font-size:1.1rem; letter-spacing:0.01em;">إنذار طوارئ: غمر مائي حرج - تم إغلاق الطريق الرئيسي بالكامل</div>
                    <div style="font-size:0.85rem; font-weight:500; opacity:0.95;">تجاوز عمق المياه الحد الآمن ({water_depth} سم ≥ 25 سم). تم توجيه حركة المرور تلقائياً نحو الطريق الدائري العلوي البديل.</div>
                </div>
            </div>
            <div style="background:rgba(0,0,0,0.3); padding:6px 14px; border-radius:8px; font-size:0.85rem; font-weight:800;">
                كود الإنذار: FLOOD-LVL-3
            </div>
        </div>
    """), unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 4. بطاقات المؤشرات المباشرة
# -----------------------------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    depth_delta_color = "#34d399" if water_depth < 12 else ("#fbbf24" if water_depth < 25 else "#f87171")
    st.markdown(textwrap.dedent(f"""
        <div class="metric-card">
            <div class="metric-label">🌊 منسوب المياه المباشر</div>
            <div class="metric-value" style="color:{depth_delta_color};">
                {water_depth} <span class="metric-unit">سم</span>
            </div>
            <div class="metric-sub" style="color:{depth_delta_color};">
                <span>الحد الآمن: أقل من 12 سم</span> • <span>الأقصى: 50 سم</span>
            </div>
        </div>
    """), unsafe_allow_html=True)

with col2:
    rain_color = "#38bdf8" if "خفيف" in rain_class else ("#facc15" if "متوسط" in rain_class else "#f87171")
    st.markdown(textwrap.dedent(f"""
        <div class="metric-card">
            <div class="metric-label">🌧️ كثافة هطول الأمطار</div>
            <div class="metric-value" style="font-size:1.45rem; color:{rain_color};">
                {rain_class}
            </div>
            <div class="metric-sub" style="color:#94a3b8;">
                <span>رادار الدوبلر الميداني</span>
            </div>
        </div>
    """), unsafe_allow_html=True)

with col3:
    rate_color = "#34d399" if accumulation_rate < 1.0 else ("#fbbf24" if accumulation_rate < 3.0 else "#f87171")
    st.markdown(textwrap.dedent(f"""
        <div class="metric-card">
            <div class="metric-label">⚡ معدل تدفق وتراكم المياه</div>
            <div class="metric-value" style="color:{rate_color};">
                +{accumulation_rate} <span class="metric-unit">سم/دقيقة</span>
            </div>
            <div class="metric-sub" style="color:#94a3b8;">
                <span>الجريان السطحي والسيول</span>
            </div>
        </div>
    """), unsafe_allow_html=True)

with col4:
    st.markdown(textwrap.dedent(f"""
        <div class="metric-card" style="border-right: 4px solid {status_color};">
            <div class="metric-label">🚦 حالة الشريان المروري الرئيسي</div>
            <div class="metric-value" style="font-size:1.25rem; color:{status_color}; font-weight:900;">
                {status_icon} {status_level}
            </div>
            <div class="metric-sub" style="color:{status_color}; font-weight:700;">
                <span>{status_label}</span>
            </div>
        </div>
    """), unsafe_allow_html=True)

st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 5. الخريطة التفاعلية ومصفوفة أمان عبور المركبات
# -----------------------------------------------------------------------------
map_col, vehicle_col = st.columns([1.65, 1.0])

CITY_CENTER = [24.7136, 46.6753]

main_road_coords = [
    [24.7080, 46.6700],
    [24.7105, 46.6725],
    [24.7128, 46.6748],
    [24.7145, 46.6765],
    [24.7168, 46.6788],
    [24.7195, 46.6815]
]

sensor_location = [24.7136, 46.6756]

detour_route_coords = [
    [24.7080, 46.6700],
    [24.7065, 46.6740],
    [24.7090, 46.6810],
    [24.7140, 46.6850],
    [24.7180, 46.6840],
    [24.7195, 46.6815]
]

with map_col:
    st.markdown("### 🗺️ الخريطة الجغرافية الحية والتوجيه الملاحي الذكي")
    
    m = folium.Map(
        location=CITY_CENTER,
        zoom_start=15,
        tiles="CartoDB dark_matter",
        control_scale=True
    )

    road_tooltip_msg = f"<b>طريق الملك فهد الرئيسي (قطاع النفق)</b><br>منسوب المياه الحالي: {water_depth} سم<br>الحالة: {status_label}"
    
    folium.PolyLine(
        locations=main_road_coords,
        color=road_polyline_color,
        weight=8,
        opacity=0.9,
        tooltip=folium.Tooltip(road_tooltip_msg),
        popup=folium.Popup(f"""
            <div style="font-family:'Alexandria', 'Readex Pro', sans-serif; direction:rtl; text-align:right; min-width:190px;">
                <h4 style="margin:0 0 5px 0; color:#0f172a;">نفق المحور الرئيسي</h4>
                <b>عمق المياه:</b> {water_depth} سم<br>
                <b>الحالة المرورية:</b> <span style="color:{status_color}; font-weight:bold;">{status_level}</span><br>
                <b>مضخات الطوارئ:</b> {'تعمل بأقصى طاقة' if drainage_pumps else 'في وضع الاستعداد'}
            </div>
        """, max_width=320)
    ).add_to(m)

    sensor_icon_color = "green" if water_depth < 12 else ("orange" if water_depth < 25 else "red")
    
    folium.Marker(
        location=sensor_location,
        popup=folium.Popup(f"""
            <div style="font-family:'Alexandria', 'Readex Pro', sans-serif; direction:rtl; text-align:right; min-width:210px;">
                <h4 style="margin:0 0 4px 0; color:#1e293b;">📡 محطة الحساس الميداني #SG-402</h4>
                <hr style="margin:4px 0;">
                <b>نوع الحساس:</b> رادار ليزري + ألتراسونيك<br>
                <b>العمق المسجل:</b> <b style="color:{status_color}; font-size:1.1rem;">{water_depth} سم</b><br>
                <b>معدل التدفق:</b> +{accumulation_rate} سم/دقيقة<br>
                <b>وقت القراءة:</b> {now_str}
            </div>
        """, max_width=340),
        tooltip="محطة استشعار السيول SG-402",
        icon=folium.Icon(color=sensor_icon_color, icon="tint", prefix="fa")
    ).add_to(m)

    if water_depth >= 12:
        warning_icon = "exclamation-triangle" if water_depth < 25 else "ban"
        folium.Marker(
            location=[24.7145, 46.6765],
            popup=folium.Popup(f"""
                <div style="font-family:'Alexandria', 'Readex Pro', sans-serif; direction:rtl; text-align:right; min-width:220px;">
                    <h4 style="margin:0 0 4px 0; color:{status_color};">🚨 إنذار خطر تجمع سيول</h4>
                    <p style="margin:4px 0; font-size:13px;"><b>القياس الدقيق:</b> {water_depth} سم مياه راكدة</p>
                    <p style="margin:4px 0; font-size:13px;"><b>حالة الطريق:</b> {status_label}</p>
                    <p style="margin:4px 0; font-size:13px;"><b>التوجيه:</b> {'يمنع عبور سيارات السيدان' if water_depth < 25 else 'إغلاق شامل - اسلك المسار الأزرق البديل'}</p>
                </div>
            """, max_width=340),
            tooltip=f"⚠️ تحذير ميداني: تجمع مياه بعمق {water_depth} سم",
            icon=folium.Icon(color="red" if water_depth >= 25 else "orange", icon=warning_icon, prefix="fa")
        ).add_to(m)

    if water_depth >= 25:
        folium.PolyLine(
            locations=detour_route_coords,
            color="#38bdf8",
            weight=6,
            dash_array="10, 10",
            opacity=0.95,
            tooltip="<b>المسار البديل الآمن الموصى به:</b> الطريق الدائري العلوي المرتفع",
            popup=folium.Popup("""
                <div style="font-family:'Alexandria', 'Readex Pro', sans-serif; direction:rtl; text-align:right; min-width:210px;">
                    <h4 style="margin:0 0 4px 0; color:#0284c7;">↪️ مسار التحويلة الملاحية الآمنة</h4>
                    <b>الاسم:</b> الطريق الدائري العلوي المرتفع<br>
                    <b>حالة المسار:</b> جاف وآمن بنسبة 100%<br>
                    <b>السرعة القصوى:</b> 80 كم/س<br>
                    <b>المزامنة الملاحية:</b> تم التعميم على تطبيقات الـ GPS
                </div>
            """, max_width=320)
        ).add_to(m)

        folium.Marker(
            location=detour_route_coords[1],
            tooltip="نقطة الدخول للمسار البديل (جسر علوي)",
            icon=folium.Icon(color="blue", icon="share", prefix="fa")
        ).add_to(m)

        folium.Marker(
            location=detour_route_coords[4],
            tooltip="نقطة العودة للمسار الرئيسي بعد تجاوز منطقة الخطر",
            icon=folium.Icon(color="blue", icon="check", prefix="fa")
        ).add_to(m)

    plugins.Fullscreen(position="topleft").add_to(m)
    
    st_folium(m, width="100%", height=490, returned_objects=[])

    st.markdown(textwrap.dedent("""
        <div style="display:flex; justify-content:space-around; background:rgba(15,23,42,0.7); padding:8px 12px; border-radius:8px; border:1px solid rgba(51,65,85,0.4); font-size:0.8rem; margin-top:8px;">
            <div style="display:flex; align-items:center; gap:6px;"><span style="display:inline-block; width:12px; height:12px; background:#10b981; border-radius:2px;"></span> أخضر: آمن (< 12 سم)</div>
            <div style="display:flex; align-items:center; gap:6px;"><span style="display:inline-block; width:12px; height:12px; background:#f59e0b; border-radius:2px;"></span> برتقالي: حذر (12-24 سم)</div>
            <div style="display:flex; align-items:center; gap:6px;"><span style="display:inline-block; width:12px; height:12px; background:#ef4444; border-radius:2px;"></span> أحمر: مغلق وسيول (≥ 25 سم)</div>
            <div style="display:flex; align-items:center; gap:6px;"><span style="display:inline-block; width:16px; height:3px; background:#38bdf8; border-top:2px dashed #38bdf8;"></span> خط أزرق متقطع: مسار بديل</div>
        </div>
    """), unsafe_allow_html=True)


with vehicle_col:
    st.markdown("### 🚘 مصفوفة أمان وعبور المركبات")

    # 1. سيارات السيدان والمركبات الصغيرة
    if water_depth < 12:
        sedan_status = "✅ آمن للعبور"
        sedan_class = "status-safe"
        sedan_badge_class = "badge-safe"
        sedan_fill_color = "#10b981"
        sedan_desc = "الارتفاع كافٍ تماماً. لا توجد أي خطورة على محرك السيارة."
        sedan_pct = max(5, int((water_depth / 18) * 100))
    elif 12 <= water_depth <= 18:
        sedan_status = "⚠️ تحذير - سرعة بطيئة"
        sedan_class = "status-caution"
        sedan_badge_class = "badge-caution"
        sedan_fill_color = "#f59e0b"
        sedan_desc = "المياه تلامس أسفل الشاسيه. يجب القيادة بسرعة منخفضة جداً وبحذر."
        sedan_pct = int((water_depth / 18) * 100)
    else:
        sedan_status = "⛔ ممنوع العبور / خطر غرق"
        sedan_class = "status-danger"
        sedan_badge_class = "badge-danger"
        sedan_fill_color = "#ef4444"
        sedan_desc = "خطر دخول المياه لمحرك السيارة (Hydro-lock) وانجراف المركبة."
        sedan_pct = 100

    # 2. سيارات الدفع الرباعي
    if water_depth < 25:
        suv_status = "✅ آمن للعبور"
        suv_class = "status-safe"
        suv_badge_class = "badge-safe"
        suv_fill_color = "#10b981"
        suv_desc = "الخلوص الأرضي كافٍ (أكثر من 200 ملم). تماسك تام للإطارات."
        suv_pct = max(5, int((water_depth / 35) * 100))
    elif 25 <= water_depth <= 35:
        suv_status = "⚠️ حذر - منسوب مرتفع"
        suv_class = "status-caution"
        suv_badge_class = "badge-caution"
        suv_fill_color = "#f59e0b"
        suv_desc = "اقتراب المياه من المحاور. يوصى بتفعيل وضع الدفع الرباعي 4WD."
        suv_pct = int((water_depth / 35) * 100)
    else:
        suv_status = "⛔ خطر شديد / مسار مقطوع"
        suv_class = "status-danger"
        suv_badge_class = "badge-danger"
        suv_fill_color = "#ef4444"
        suv_desc = "خطر فقدان التحكم والطفو بسبب شدة منسوب المياه."
        suv_pct = 100

    # 3. الشاحنات وفرق الطوارئ
    if water_depth <= 40:
        truck_status = "✅ مسار مسموح للطوارئ"
        truck_class = "status-safe"
        truck_badge_class = "badge-safe"
        truck_fill_color = "#10b981"
        truck_desc = "مدخل هواء المحرك مرتفع. ممر آمن لقوافل الدعم والإسعاف."
        truck_pct = max(5, int((water_depth / 48) * 100))
    elif 40 < water_depth <= 48:
        truck_status = "⚠️ حذر - رتل طوارئ فقط"
        truck_class = "status-caution"
        truck_badge_class = "badge-caution"
        truck_fill_color = "#f59e0b"
        truck_desc = "منسوب المياه قريب من جنوط الشاحنات الكبيرة."
        truck_pct = int((water_depth / 48) * 100)
    else:
        truck_status = "⛔ خطر سيول جارفة"
        truck_class = "status-danger"
        truck_badge_class = "badge-danger"
        truck_fill_color = "#ef4444"
        truck_desc = "تيارات السيول تجاوزت قدرة التحمل لجميع المركبات الثقيلة."
        truck_pct = 100

    st.markdown(textwrap.dedent(f"""
        <div class="vehicle-card {sedan_class}">
            <div class="vehicle-header">
                <span class="vehicle-title">🚗 سيارات السيدان والصغيرة</span>
                <span class="badge-pill {sedan_badge_class}">{sedan_status}</span>
            </div>
            <div style="font-size:0.83rem; color:#cbd5e1; line-height:1.4;">{sedan_desc}</div>
            <div style="display:flex; justify-content:space-between; font-size:0.75rem; color:#94a3b8; margin-top:8px;">
                <span>الحد الأقصى للتحمل: 18 سم</span>
                <span>العمق الحالي: {water_depth} سم</span>
            </div>
            <div class="clearance-track">
                <div class="clearance-fill" style="width:{sedan_pct}%; background-color:{sedan_fill_color};"></div>
            </div>
        </div>
    """), unsafe_allow_html=True)

    st.markdown(textwrap.dedent(f"""
        <div class="vehicle-card {suv_class}">
            <div class="vehicle-header">
                <span class="vehicle-title">🚙 سيارات الدفع الرباعي والـ SUV</span>
                <span class="badge-pill {suv_badge_class}">{suv_status}</span>
            </div>
            <div style="font-size:0.83rem; color:#cbd5e1; line-height:1.4;">{suv_desc}</div>
            <div style="display:flex; justify-content:space-between; font-size:0.75rem; color:#94a3b8; margin-top:8px;">
                <span>الحد الأقصى للتحمل: 35 سم</span>
                <span>العمق الحالي: {water_depth} سم</span>
            </div>
            <div class="clearance-track">
                <div class="clearance-fill" style="width:{suv_pct}%; background-color:{suv_fill_color};"></div>
            </div>
        </div>
    """), unsafe_allow_html=True)

    st.markdown(textwrap.dedent(f"""
        <div class="vehicle-card {truck_class}">
            <div class="vehicle-header">
                <span class="vehicle-title">🚚 الشاحنات وآليات الدفاع المدني</span>
                <span class="badge-pill {truck_badge_class}">{truck_status}</span>
            </div>
            <div style="font-size:0.83rem; color:#cbd5e1; line-height:1.4;">{truck_desc}</div>
            <div style="display:flex; justify-content:space-between; font-size:0.75rem; color:#94a3b8; margin-top:8px;">
                <span>الحد الأقصى للتحمل: 48 سم</span>
                <span>العمق الحالي: {water_depth} سم</span>
            </div>
            <div class="clearance-track">
                <div class="clearance-fill" style="width:{truck_pct}%; background-color:{truck_fill_color};"></div>
            </div>
        </div>
    """), unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 6. سجل الأحداث والإنذارات المباشر لغرفة العمليات
# -----------------------------------------------------------------------------
st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
st.markdown("### 📋 سجل الأحداث المباشر وتنبيهات غرفة العمليات")

base_time = datetime.datetime.now()
logs = []

if water_depth >= 25:
    logs.append({
        "time": (base_time - datetime.timedelta(minutes=1)).strftime("%I:%M %p"),
        "tag": "طوارئ قصوى",
        "tag_class": "tag-critical",
        "msg": f"تصعيد حالة الطريق إلى (أحمر خطر). العمق المسجل {water_depth} سم. إغلاق بوابات النفق الرئيسية آلياً."
    })
    logs.append({
        "time": (base_time - datetime.timedelta(minutes=2)).strftime("%I:%M %p"),
        "tag": "إجراء ذكي",
        "tag_class": "tag-action",
        "msg": "تفعيل مسار التحويلة الآمنة عبر الطريق الدائري العلوي ومزامنة الخرائط الملاحية."
    })
    if sms_broadcast:
        logs.append({
            "time": (base_time - datetime.timedelta(minutes=3)).strftime("%I:%M %p"),
            "tag": "إنذار عام",
            "tag_class": "tag-critical",
            "msg": "بث رسائل تحذير SMS جغرافية عاجلة لجميع الهواتف المتواجدة في نطاق القطاع الرابع."
        })

if water_depth >= 12:
    logs.append({
        "time": (base_time - datetime.timedelta(minutes=5)).strftime("%I:%M %p"),
        "tag": "تحذير مياه",
        "tag_class": "tag-warning",
        "msg": f"تجاوز الحد الآمن: منسوب المياه وصل إلى {water_depth} سم. توجيه سيارات السيدان بتجنب النفق."
    })
    if variable_signs:
        logs.append({
            "time": (base_time - datetime.timedelta(minutes=7)).strftime("%I:%M %p"),
            "tag": "إجراء ذكي",
            "tag_class": "tag-action",
            "msg": "تحديث لوحات الطرق الإرشادية (VMS-101, VMS-102) برسالة: 'تجمع سيول أمامك - خفف السرعة'."
        })

if drainage_pumps:
    logs.append({
        "time": (base_time - datetime.timedelta(minutes=8)).strftime("%I:%M %p"),
        "tag": "تشغيل ميداني",
        "tag_class": "tag-action",
        "msg": "بدء عمل محطة ضخ التصريف الهيدروليكية رقم 4 بطاقة 85% (12,000 لتر/دقيقة)."
    })

logs.append({
    "time": (base_time - datetime.timedelta(minutes=12)).strftime("%I:%M %p"),
    "tag": "بيانات بيئية",
    "tag_class": "tag-info",
    "msg": f"تحديث رادار الأمطار: {rain_intensity}. معدل الجريان السطحي الحالي +{accumulation_rate} سم/دقيقة."
})

logs.append({
    "time": (base_time - datetime.timedelta(minutes=18)).strftime("%I:%M %p"),
    "tag": "حالة النظام",
    "tag_class": "tag-info",
    "msg": "معايرة حساسات الرادار والألتراسونيك SG-402 بنجاح، ومعدل إرسال البيانات كل ثانية واحدة."
})

# بناء جدول السجل الأنيق بدون مسافات بادئة تسبب مشاكل كود الماركداون
log_items_html = ""
for log in logs:
    log_items_html += f'<div class="log-item"><span class="log-time">{log["time"]}</span><span class="log-tag {log["tag_class"]}">{log["tag"]}</span><span class="log-message">{log["msg"]}</span></div>'

log_wrapper_html = f'<div class="log-container">{log_items_html}</div>'

st.markdown(log_wrapper_html, unsafe_allow_html=True)
