# Kurumsal Nakit Yönetimi ve Hazine Simülatörü

Bu proje, kurumsal hazine departmanlarının nakit pozisyonlarını optimize etmek, farklı para birimlerindeki yatırım araçlarını karşılaştırmak ve döviz riskini yönetmek için kullandığı stratejik bir karar destek simülatörüdür.

## 🚀 Canlı Uygulama
Uygulamayı tarayıcı üzerinden deneyimlemek için:
[**Hazine Simülatörü - Live App**](https://hazinesimulator.streamlit.app)

## 🛠️ Temel Özellikler

- **Çoklu Para Birimi Konsolidasyonu:** TRY, USD ve EUR varlıklarını anlık kurlar üzerinden tek bir ana para birimi (TRY) değerine dönüştürür.
- **Net Getiri Optimizasyonu:** Farklı yatırım araçlarını (Gecelik Repo, Eurobond, Mevduat, Para Piyasası Fonları) stopaj ve vergi etkilerini düşerek "Net Getiri" bazında karşılaştırır.
- **Başabaş Kur (Breakeven FX) Analizi:** TL ve Döviz bazlı yatırımların kafa kafaya geldiği kritik döviz eşiğini hesaplayarak "Hedge mi, TL Getirisi mi?" kararını rasyonelleştirir.
- **Senaryo Analizi & Stres Testi:** Döviz kurlarında yaşanabilecek ani şokların (%10, %20 vb.) toplam portföy değeri üzerindeki etkisini simüle eder.
- **Dinamik Veri Yönetimi:** Piyasadaki faiz ve vergi oranlarını anlık olarak güncelleyip simülasyona dahil etme imkanı sunar.

## 📊 Metodoloji

### Başabaş Kur Hesaplaması
Simülatör, bir döviz yatırımının (Örn: Eurobond) TL yatırımına (Örn: Repo) karşı avantajlı hale gelmesi için gereken minimum kur seviyesini şu formülle belirler:

$$Başabaş Kur = Mevcut Kur \times \frac{1 + (Net TL Faizi \times \frac{Vade}{365})}{1 + (Net Döviz Faizi \times \frac{Vade}{365})}$$

## 💻 Kullanılan Teknolojiler

- **Python:** Finansal modelleme ve veri işleme.
- **Streamlit:** Modern ve interaktif web arayüzü.
- **Plotly:** Getiri karşılaştırmaları ve görselleştirme.
- **Pandas:** Portföy yönetimi ve veri manipülasyonu.

