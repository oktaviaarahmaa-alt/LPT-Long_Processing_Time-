import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Production Scheduling · LPT Optimizer",
    page_icon="⏳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS (Soft Pastel — Mint · Sky · Peach Theme) ─────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

/* ── Base ── */
html, body, [class*="css"] { font-family: 'Nunito', sans-serif; }
.stApp { background: #FDF6F0; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #B2D8C8 0%, #C8D8E8 60%, #E8C4A8 100%) !important;
    border-right: 1px solid #D4C0B0;
}
[data-testid="stSidebar"] * { color: #5A4A42 !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #3D2E28 !important; }
[data-testid="stSidebar"] .stMarkdown p { color: #5A4A42 !important; }

/* ── Hero Banner ── */
.hero-banner {
    background: linear-gradient(135deg, #7FBFAD 0%, #A8C4D4 50%, #E8A882 100%);
    border-radius: 20px;
    padding: 38px 44px;
    margin-bottom: 28px;
    box-shadow: 0 4px 20px rgba(180,140,120,0.18);
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 180px; height: 180px;
    background: rgba(255,255,255,0.12);
    border-radius: 50%;
}
.hero-banner::after {
    content: '';
    position: absolute;
    bottom: -30px; left: 120px;
    width: 100px; height: 100px;
    background: rgba(255,255,255,0.08);
    border-radius: 50%;
}
.hero-title { font-size: 28px; font-weight: 700; color: #fff; margin: 0 0 8px; text-shadow: 0 1px 4px rgba(0,0,0,0.12); }
.hero-sub { font-size: 14px; color: rgba(255,255,255,0.88); margin: 0; font-weight: 400; }

/* ── Metric Cards ── */
.metric-card {
    background: #ffffff;
    border-radius: 16px;
    padding: 20px 22px;
    border: 1.5px solid #EDD8CC;
    box-shadow: 0 2px 10px rgba(200,160,130,0.10);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.metric-card:hover { transform: translateY(-2px); box-shadow: 0 6px 18px rgba(200,160,130,0.18); }
.metric-card.blue  { border-top: 4px solid #7FBFAD; }   /* sage mint  */
.metric-card.slate { border-top: 4px solid #A8C4D4; }   /* soft sky   */
.metric-card.coral { border-top: 4px solid #E8A882; }   /* warm peach */

.metric-label {
    font-size: 10px; font-weight: 700; color: #B08070;
    text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;
}
.metric-value {
    font-size: 26px; font-weight: 700;
    color: #5A3E35;
    font-family: 'DM Mono', monospace;
}
.metric-sub { font-size: 11px; color: #B08070; margin-top: 4px; }

/* ── Section Headers ── */
.section-header { display: flex; align-items: center; gap: 10px; margin: 28px 0 14px; }
.section-title {
    font-size: 15px; font-weight: 700; color: #5A3E35;
    padding-left: 10px;
    border-left: 3px solid #7FBFAD;
}

/* ── Info Box ── */
.info-box {
    background: linear-gradient(90deg, #E8F5F0 0%, #F5EEE8 100%);
    border-left: 4px solid #7FBFAD;
    border-radius: 0 12px 12px 0;
    padding: 14px 18px;
    margin-bottom: 20px;
    font-size: 13px;
    color: #5A4A42;
}

/* ── Divider ── */
hr { border-color: #EDD8CC !important; }

/* ── Button override ── */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #7FBFAD 0%, #A8C4D4 100%) !important;
    border: none !important;
    border-radius: 10px !important;
    color: white !important;
    font-weight: 600 !important;
    padding: 10px 28px !important;
    box-shadow: 0 3px 12px rgba(127,191,173,0.35) !important;
    transition: opacity 0.2s ease !important;
}
.stButton > button[kind="primary"]:hover { opacity: 0.88 !important; }

/* ── Dataframe tweaks ── */
[data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)

# ─── Sidebar Input ────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 20px 0 16px'>
        <div style='font-size:22px; font-weight:700; color:#3D2E28;'>⏳ LPT Scheduler</div>
        <div style='font-size:12px; color:#7A5A50; margin-top:3px'>Longest Processing Time Rule</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.write("⏳ **Aturan LPT:** Pekerjaan dengan waktu proses **terpanjang** akan dijadwalkan terlebih dahulu. Aturan ini sangat baik untuk mengidentifikasi beban kerja besar di awal atau mendistribusikan tugas pada beberapa mesin (Parallel Machines).")

# ─── Hero Banner ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">⏳ Longest Processing Time (LPT) Dashboard</div>
    <div class="hero-sub">Optimasi urutan penjadwalan job tunggal (Single Machine Scheduling) berdasarkan prioritas waktu terlama</div>
</div>
""", unsafe_allow_html=True)

# ─── Data Input Section ───────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-title">📂 Input Data Job (Pekerjaan)</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
    💡 <b>Petunjuk:</b> Isikan daftar pekerjaan, waktu proses (Processing Time), dan batas waktu penyelesaian (Due Date). 
    Anda bisa menambah baris baru di bagian bawah tabel. Aturan LPT akan otomatis mengurutkan dari waktu terlama.
</div>
""", unsafe_allow_html=True)

# Default baseline data
init_data = pd.DataFrame([
    {"Job_Name": "Job A", "Processing_Time": 5, "Due_Date": 10},
    {"Job_Name": "Job B", "Processing_Time": 2, "Due_Date": 6},
    {"Job_Name": "Job C", "Processing_Time": 8, "Due_Date": 15},
    {"Job_Name": "Job D", "Processing_Time": 3, "Due_Date": 8},
])

edited_df = st.data_editor(
    init_data,
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "Job_Name": st.column_config.TextColumn("Nama Job / Pekerjaan", required=True),
        "Processing_Time": st.column_config.NumberColumn("Processing Time (Jam/Hari)", min_value=1, step=1, format="%d"),
        "Due_Date": st.column_config.NumberColumn("Due Date (Batas Waktu)", min_value=1, step=1, format="%d")
    }
)

if st.button("▶ Hitung Penjadwalan LPT", type="primary"):
    if edited_df is not None and len(edited_df) > 0:
        df_jobs = edited_df.dropna().copy()
        
        # ─── LPT Calculation Logic (Ascending=False) ──────────────────────────
        df_lpt = df_jobs.sort_values(by="Processing_Time", ascending=False).reset_index(drop=True)
        
        start_times = []
        comp_times = []
        current_time = 0
        
        for idx, row in df_lpt.iterrows():
            start_times.append(current_time)
            current_time += int(row["Processing_Time"])
            comp_times.append(current_time)
            
        df_lpt["Start_Time"] = start_times
        df_lpt["Completion_Time"] = comp_times
        
        df_lpt["Lateness"] = df_lpt["Completion_Time"] - df_lpt["Due_Date"]
        df_lpt["Tardiness"] = df_lpt["Lateness"].apply(lambda x: max(0, x))
        
        # ─── Hitung Metrik Performa ───────────────────────────────────────────
        mean_flow_time = df_lpt["Completion_Time"].mean()
        max_tardiness = df_lpt["Tardiness"].max()
        mean_tardiness = df_lpt["Tardiness"].mean()
        num_tardy_jobs = sum(df_lpt["Tardiness"] > 0)
        
        # ─── METRIC CARDS ─────────────────────────────────────────────────────
        st.markdown("""<div class="section-header"><div class="section-title">📊 Performa Penjadwalan LPT</div></div>""", unsafe_allow_html=True)
        
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f"""<div class="metric-card blue"><div class="metric-label">Mean Flow Time</div><div class="metric-value">{mean_flow_time:.2f}</div><div class="metric-sub">Rata-rata waktu alir job</div></div>""", unsafe_allow_html=True)
        with m2:
            st.markdown(f"""<div class="metric-card slate"><div class="metric-label">Mean Tardiness</div><div class="metric-value">{mean_tardiness:.2f}</div><div class="metric-sub">Rata-rata keterlambatan</div></div>""", unsafe_allow_html=True)
        with m3:
            st.markdown(f"""<div class="metric-card coral"><div class="metric-label">Max Tardiness</div><div class="metric-value">{max_tardiness}</div><div class="metric-sub">Keterlambatan maksimal</div></div>""", unsafe_allow_html=True)
        with m4:
            st.markdown(f"""<div class="metric-card blue"><div class="metric-label">Tardy Jobs</div><div class="metric-value">{num_tardy_jobs} / {len(df_lpt)}</div><div class="metric-sub">Jumlah job yang terlambat</div></div>""", unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # ─── TABEL HASIL URUTAN LPT ───────────────────────────────────────────
        st.markdown("**Urutan Pengerjaan Hasil Optimasi LPT (Berdasarkan Waktu Terlama)**")
        
        df_lpt["Sequence"] = [f"Urutan {i+1}" for i in range(len(df_lpt))]
        df_display = df_lpt.set_index("Sequence")[["Job_Name", "Processing_Time", "Due_Date", "Start_Time", "Completion_Time", "Lateness", "Tardiness"]]
        
        st.dataframe(
            df_display.style
            .map(lambda x: "background-color: #E0F2FE; color: #0369A1;" if x > 0 else "", subset=["Processing_Time"])
            .map(lambda x: "color: #DC2626; font-weight: bold;" if x > 0 else "color: #16A34A;", subset=["Tardiness"]),
            use_container_width=True
        )
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # ─── VISUALISASI CHART ────────────────────────────────────────────────
        st.markdown("""<div class="section-header"><div class="section-title">📈 Visualisasi Penjadwalan</div></div>""", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2, gap="large")
        
        with c1:
            fig_gantt = go.Figure()
            for idx, row in df_lpt.iterrows():
                fig_gantt.add_trace(go.Bar(
                    x=[row["Processing_Time"]],
                    y=["Mesin Tunggal"],
                    base=[row["Start_Time"]],
                    orientation='h',
                    name=row["Job_Name"],
                    text=f"{row['Job_Name']} ({row['Processing_Time']})",
                    textposition='inside',
                    marker=dict(line=dict(color='white', width=1))
                ))
            
            fig_gantt.update_layout(
                title=dict(text="Gantt Chart Urutan Pengerjaan LPT (Timeline)", font=dict(family="Nunito", color="#5A3E35")),
                barmode='stack',
                height=300,
                plot_bgcolor="#FDF6F0",
                paper_bgcolor="white",
                showlegend=False,
                xaxis=dict(title="Waktu (Jam/Hari)", gridcolor="#EDD8CC", color="#B08070"),
                yaxis=dict(color="#B08070"),
                colorway=["#7FBFAD", "#A8C4D4", "#E8A882", "#C8A8B8", "#D4C4A0"]
            )
            st.plotly_chart(fig_gantt, use_container_width=True)
            
        with c2:
            fig_comp = go.Figure()
            fig_comp.add_bar(x=df_lpt["Job_Name"], y=df_lpt["Due_Date"], name="Due Date", marker_color="#C8D8E8")
            fig_comp.add_bar(x=df_lpt["Job_Name"], y=df_lpt["Completion_Time"], name="Completion Time", marker_color="#E8A882")
            
            fig_comp.update_layout(
                title=dict(text="Perbandingan Batas Waktu (Due Date) vs Waktu Selesai", font=dict(family="Nunito", color="#5A3E35")),
                barmode="group",
                height=300,
                plot_bgcolor="#FDF6F0",
                paper_bgcolor="white",
                xaxis=dict(gridcolor="#EDD8CC", color="#B08070"),
                yaxis=dict(gridcolor="#EDD8CC", color="#B08070"),
                legend=dict(font=dict(color="#5A3E35"))
            )
            st.plotly_chart(fig_comp, use_container_width=True)
            
    else:
        st.warning("Silakan masukkan data pekerjaan terlebih dahulu pada tabel.")
