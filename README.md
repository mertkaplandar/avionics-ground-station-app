# Avionics Ground Station App

Bu uygulama, Teknofest Roket Yarışması'na katılan Atmaca Roket Takımı'nın roketi üzerindeki aviyonik sistemden yer istasyonuna gelen verilerin görselleştirilmesi ve HYI (Hakem Yer İstasyonu) ile paylaşılması amacıyla geliştirilmiştir.

## İçerik

- [Özellikler](#özellikler)
- [Kurulum](#kurulum)
- [Kullanım](#kullanım)
- [Dosya Açıklamaları](#dosya-açıklamaları)

## Özellikler

- Roket üzerindeki aviyonik sistemden gelen verilerin anlık olarak yer istasyonunda görselleştirilmesi.
- Verilerin JSON formatında alınması ve PyQt5 ile grafiksel arayüzde gösterilmesi.
- Harita üzerinde iki yer istasyonunun konumlarının görüntülenmesi.
- HYI ile verilerin paylaşılması için gerekli yapıların sağlanması.

## Kurulum

Bu projeyi yerel makinenize klonlamak ve çalıştırmak için aşağıdaki adımları takip edebilirsiniz:

1. Repoyu klonlayın:
    ```bash
    git clone https://github.com/mertkaplandar/avionics-ground-station-app.git
    ```
2. Gerekli Python paketlerini yükleyin:
    ```bash
    pip install -r requirements.txt
    ```

## Kullanım

Uygulamayı çalıştırmak için aşağıdaki komutu kullanabilirsiniz:
```bash
python ground-station-app.py
```

## Dosya Açıklamaları
### ground-station-app.py
- Veri Alımı: COM portu üzerinden JSON formatında gelen verilerin alınmasını sağlar.
- Veri Görselleştirme: PyQt5 kullanarak verilerin grafiksel arayüzde görselleştirilmesini sağlar.
- Harita Görselleştirme: Folium kullanarak iki yer istasyonunun konumlarının harita üzerinde gösterilmesini sağlar.
- Seri Port İletişimi: İki yer istasyonundan gelen ham mesajların ayrı sekmelerde görüntülenmesini sağlar.

### hyi-controller.py
- Veri Paylaşımı: Alınan verilerin HYI (Hakem Yer İstasyonu) ile paylaşılmasını sağlar.
- Bağlantı Yönetimi: HYI ile bağlantı kurma ve sonlandırma işlemlerini yönetir.
- Paket Oluşturma: HYI'ye gönderilecek verilerin belirli bir paket formatında oluşturulmasını sağlar.

## Katkıda Bulunma
Katkıda bulunmak isterseniz, lütfen bir pull request gönderin veya bir issue açın.