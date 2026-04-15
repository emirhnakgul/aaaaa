import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import io

st.set_page_config(page_title="Hazine Simülatörü PRO", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    /* Ana Arkaplan */
    .main { background-color: #0e1117; }
    
    /* Metrik Kartları Düzenleme */
    [data-testid="metric-container"] {
        background-color: #1e293b;
        border: 1px solid #334155;
        padding: 20px;
        border-radius: 12px;
        color: white;
    }
    
    /* Metrik Başlık ve Değer Renkleri */
    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-size: 16px !important;
    }
    
    [data-testid="stMetricValue"] {
        color: #f8fafc !important;
    }

    /* Tablo ve Sidebar Düzenlemeleri */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

if 'opps' not in st.session_state:
    st.session_state.opps = {
        "Gecelik Repo (TRY)": {"rate": 0.45, "tax": 0.05, "currency": "TRY", "tenor": 1},
        "Para Piyasası Fonu": {"rate": 0.43, "tax": 0.0, "currency": "TRY", "tenor": 1},
        "Eurobond (USD)": {"rate": 0.085, "tax": 0.10, "currency": "USD", "tenor": 30},
        "USD Mevduat": {"rate": 0.04, "tax": 0.25, "currency": "USD", "tenor": 30},
        "EUR Mevduat": {"rate": 0.025, "tax": 0.25, "currency": "EUR", "tenor": 30}
    }

st.sidebar.title("🏢 Kurumsal Giriş")
st.sidebar.subheader("Nakit Pozisyonları")
c_try = st.sidebar.number_input("Eldeki TRY", value=15000000)
c_usd = st.sidebar.number_input("Eldeki USD", value=2500000)
c_eur = st.sidebar.number_input("Eldeki EUR", value=500000)

st.sidebar.subheader("Piyasa Kur Verileri")
fx_usd = st.sidebar.number_input("USD/TRY", value=32.50, step=0.01)
fx_eur = st.sidebar.number_input("EUR/TRY", value=35.20, step=0.01)

st.sidebar.subheader("Senaryo Analizi")
shock = st.sidebar.slider("Kur Şoku Senaryosu (%)", 0, 50, 10) / 100

st.title("💼 Kurumsal Nakit Yönetimi ve Hazine Simülatörü")
st.info("Farklı para birimlerindeki nakit varlıkların optimizasyonu ve başabaş kur analizi.")

total_now_try = c_try + (c_usd * fx_usd) + (c_eur * fx_eur)
total_shock_try = c_try + (c_usd * fx_usd * (1+shock)) + (c_eur * fx_eur * (1+shock))

m1, m2, m3 = st.columns(3)
m1.metric("Toplam Nakit (TRY Karşılığı)", f"{total_now_try:,.0f} ₺")
m2.metric("Kur Şoku Sonrası Değer", f"{total_shock_try:,.0f} ₺", f"+{total_shock_try-total_now_try:,.0f} ₺")
m3.metric("Döviz Ağırlığı", f"{((c_usd*fx_usd + c_eur*fx_eur)/total_now_try)*100:.1f}%")

tab1, tab2 = st.tabs(["📊 Yatırım Analizi", "⚙️ Enstrüman Yönetimi"])

with tab1:
    try_net = st.session_state.opps["Gecelik Repo (TRY)"]["rate"] * (1 - st.session_state.opps["Gecelik Repo (TRY)"]["tax"])
    
    results = []
    for name, data in st.session_state.opps.items():
        net_rate = data['rate'] * (1 - data['tax'])
        breakeven = 0
        if data['currency'] != 'TRY':
            curr_rate = fx_usd if data['currency'] == 'USD' else fx_eur
            period_try = 1 + (try_net * (data['tenor']/365))
            period_fx = 1 + (net_rate * (data['tenor']/365))
            breakeven = curr_rate * (period_try / period_fx)

        results.append({
            "Enstrüman": name,
            "Para Birimi": data['currency'],
            "Net Yıllık %": round(net_rate * 100, 2),
            "Başabaş Kur": round(breakeven, 3) if breakeven > 0 else "N/A",
            "Vade": f"{data['tenor']} Gün"
        })

    df_res = pd.DataFrame(results).sort_values("Net Yıllık %", ascending=False)
    
    col_l, col_r = st.columns([2, 1])
    
    with col_l:
        st.subheader("Getiri ve Risk Tablosu")
        st.dataframe(df_res, use_container_width=True, hide_index=True)
        
        fig_bar = px.bar(df_res, x="Enstrüman", y="Net Yıllık %", color="Para Birimi",
                         title="Enstrüman Bazlı Net Getiri Karşılaştırması",
                         color_discrete_map={"TRY": "#10b981", "USD": "#3b82f6", "EUR": "#f59e0b"},
                         template="plotly_dark")
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_r:
        st.subheader("Hazine Karar Destek")
        best_try = df_res[df_res["Para Birimi"] == "TRY"].iloc[0]
        best_fx = df_res[df_res["Para Birimi"] != "TRY"].iloc[0]
        
        st.success(f"**TL Getiri Lideri:** {best_try['Enstrüman']} (%{best_try['Net Yıllık %']})")
        st.warning(f"**Döviz Getiri Lideri:** {best_fx['Enstrüman']} (%{best_fx['Net Yıllık %']})")
        
        st.write(f"---")
        st.write(f"**Kritik Eşik:** Eğer USD/TRY vade sonunda **{best_fx['Başabaş Kur']}** üzerine çıkacaksa dövizde kalmak daha kârlıdır.")

with tab2:
    st.subheader("Piyasa Getiri Oranlarını Güncelle")
    edited_df = st.data_editor(pd.DataFrame(st.session_state.opps).T, use_container_width=True)
    if st.button("Değişiklikleri Kaydet"):
        st.session_state.opps = edited_df.to_dict('index')
        st.rerun()

st.divider()
st.caption("© 2026 Kurumsal Nakit Yönetimi Simülatörü | Veriler simülasyon amaçlıdır.")