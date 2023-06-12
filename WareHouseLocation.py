import urllib.request
import numpy as np

url = "https://raw.githubusercontent.com/merttfazli/Warehouse-Location-Problem/main/wl_16_1"
response = urllib.request.urlopen(url)
data = response.read().decode('utf-8')

lines = data.split('\n')
depo_sayisi = int(lines[0].split()[0])
musteri_sayisi = int(lines[0].split()[1])

depo_kapasiteleri = []
depo_maliyetleri = []
musteri_talepleri = []
musteri_depo_maliyetleri = []

for i in range(1, depo_sayisi + 1):
    depo_verileri = lines[i].split()
    depo_kapasitesi = int(depo_verileri[0])
    depo_maliyeti = float(depo_verileri[1])

    depo_kapasiteleri.append(depo_kapasitesi)
    depo_maliyetleri.append(depo_maliyeti)

musteri_talepleri_verisi = lines[depo_sayisi + 1:]
musteri_talepleri_verisi = [line.strip() for line in musteri_talepleri_verisi if line.strip() != '']

for i in range(0, len(musteri_talepleri_verisi), 2):
    talep = int(musteri_talepleri_verisi[i])
    musteri_talepleri.append(talep)
    
    depo_maliyeti = [float(x) for x in musteri_talepleri_verisi[i+1].split()]
    musteri_depo_maliyetleri.append(depo_maliyeti)

# Tüm müşteri-depo kombinasyonlarını oluşturma
kombinasyonlar = [(musteri_idx, depo_idx) for musteri_idx in range(musteri_sayisi) for depo_idx in range(depo_sayisi)]

# Optimizasyon işlemi için değişkenlerin tanımlanması
depo_atamalari = np.zeros((musteri_sayisi, depo_sayisi), dtype=int)
optimal_maliyet = 0

# Müşteri taleplerini karşılamak için en uygun depoların seçilmesi
for musteri_idx in range(musteri_sayisi):
    musteri_talebi = musteri_talepleri[musteri_idx]
    en_uygun_depo = None
    en_dusuk_maliyet = np.inf
    for depo_idx in range(depo_sayisi):
        depo_kapasitesi = depo_kapasiteleri[depo_idx]
        depo_maliyeti = depo_maliyetleri[depo_idx]
        musteri_depo_maliyeti = musteri_depo_maliyetleri[musteri_idx][depo_idx]
        if musteri_talebi <= depo_kapasitesi and musteri_depo_maliyeti < en_dusuk_maliyet:
            en_uygun_depo = depo_idx
            en_dusuk_maliyet = musteri_depo_maliyeti
    if en_uygun_depo is not None:
        depo_atamalari[musteri_idx][en_uygun_depo] = 1
        optimal_maliyet += en_dusuk_maliyet

# Sonuçların yazdırılması
print("Optimal Maliyet:", optimal_maliyet)
print("Müşterilere Atanan Depolar:")
for musteri_idx in range(musteri_sayisi):
    atanan_depo = [depo_idx for depo_idx in range(depo_sayisi) if depo_atamalari[musteri_idx][depo_idx] == 1]
    atanan_depo_str = ' '.join(str(x) for x in atanan_depo)
    print(atanan_depo_str, end=' ')
print()
