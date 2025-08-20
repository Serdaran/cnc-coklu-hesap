# coklu_hesap_app.py
import math
import streamlit as st

# ---------- 1) Sayfa ayarı ----------
st.set_page_config(page_title="CNC Çoklu Hesap", page_icon="🧰", layout="centered")

# ---------- 2) Başlık & açıklama ----------
st.title("🧰 CNC Çoklu Hesap")
st.caption("Devir (n), Tabla Hızı (Vc) ve İlerleme (Vf) için üç ayrı mod. Birimleri doğru gir: Vc: m/dak, D: mm, n: rpm, fz: mm/diş, z: diş sayısı.")

with st.expander("Formüller"):
    st.latex(r"n = \frac{1000 \cdot V_c}{\pi \cdot D} \quad (rpm)")
    st.latex(r"V_c = \frac{\pi \cdot D \cdot n}{1000} \quad (m/dak)")
    st.latex(r"V_f = f_z \cdot z \cdot n \quad (mm/dak)")

# ---------- 3) Yardımcılar ----------
def to_float(txt: str) -> float:
    """Virgülü noktaya çevirerek güvenli float dönüşümü."""
    return float(txt.strip().replace(",", "."))

def check_positive(name: str, value: float, allow_zero: bool = False) -> bool:
    if allow_zero and value == 0:
        return True
    if value <= 0:
        st.error(f"**{name}** sıfırdan büyük olmalı.")
        return False
    return True

# ---------- 4) Mod seçimi ----------
mod = st.radio(
    "Mod Seç",
    ["Devir (n) Hesapla", "Tabla Hızı (Vc) Hesapla", "İlerleme (Vf) Hesapla"],
    horizontal=True,
)

# ---------- 5) Ortak ayarlar ----------
ondalik = st.slider("Ondalık basamak", 0, 6, 2)

# ---------- 6) Mod 1: Devir (n) ----------
if mod == "Devir (n) Hesapla":
    col1, col2 = st.columns(2)
    with col1:
        vc_in = st.text_input("Kesme Hızı Vc (m/dak)", "150")
    with col2:
        d_in  = st.text_input("Parça Çapı D (mm)", "26")

    if st.button("HESAPLA (n)"):
        try:
            vc = to_float(vc_in)
            D  = to_float(d_in)
            ok = True
            ok &= check_positive("Vc (m/dak)", vc)
            ok &= check_positive("D (mm)", D)
            if ok:
                n = (1000 * vc) / (math.pi * D)
                st.success(f"Devir (n): **{round(n, ondalik)} rpm**")
                st.write(f"(Ham: {n:.6f} rpm)")
        except ValueError:
            st.error("Lütfen sayısal değer gir (örn. 150 veya 26.5).")

# ---------- 7) Mod 2: Tabla Hızı (Vc) ----------
elif mod == "Tabla Hızı (Vc) Hesapla":
    col1, col2 = st.columns(2)
    with col1:
        n_in = st.text_input("Devir n (rpm)", "1837")
    with col2:
        d_in = st.text_input("Parça Çapı D (mm)", "26")

    if st.button("HESAPLA (Vc)"):
        try:
            n = to_float(n_in)
            D = to_float(d_in)
            ok = True
            ok &= check_positive("n (rpm)", n)
            ok &= check_positive("D (mm)", D)
            if ok:
                vc = (math.pi * D * n) / 1000
                st.success(f"Tabla Hızı (Vc): **{round(vc, ondalik)} m/dak**")
                st.write(f"(Ham: {vc:.6f} m/dak)")
        except ValueError:
            st.error("Lütfen sayısal değer gir (örn. 1800 veya 26.5).")

# ---------- 8) Mod 3: İlerleme (Vf) ----------
else:  # "İlerleme (Vf) Hesapla"
    col1, col2, col3 = st.columns(3)
    with col1:
        fz_in = st.text_input("Diş Başına İlerleme fz (mm/diş)", "0.1")
    with col2:
        z_in  = st.text_input("Diş Sayısı z", "4")
    with col3:
        n_in  = st.text_input("Devir n (rpm)", "2000")

    if st.button("HESAPLA (Vf)"):
        try:
            fz = to_float(fz_in)
            z  = to_float(z_in)
            n  = to_float(n_in)
            ok = True
            ok &= check_positive("fz (mm/diş)", fz)
            ok &= check_positive("z (diş sayısı)", z)
            ok &= check_positive("n (rpm)", n)
            if ok:
                vf = fz * z * n  # mm/dak
                st.success(f"İlerleme (Vf): **{round(vf, ondalik)} mm/dak**")
                st.write(f"(Ham: {vf:.6f} mm/dak)")
        except ValueError:
            st.error("Lütfen sayısal değer gir (örn. 0.08, 4, 2000).")

# ---------- 9) Yan panel ----------
with st.sidebar:
    st.header("Birimler & Notlar")
    st.markdown(
        "- **Vc (m/dak)**: Kesme hızı\n"
        "- **D (mm)**: Parça veya takım çapı\n"
        "- **n (rpm)**: Devir\n"
        "- **fz (mm/diş)**: Diş başına ilerleme\n"
        "- **z**: Diş sayısı\n"
        "- **Vf (mm/dak)**: İlerleme hızı\n\n"
        "Hatalı girişlerde üstte **kırmızı uyarı** görürsün. Virgül girersen otomatik nokta kabul edilir."
    )
    st.divider()
    st.caption("© SANTEK MÜHENDİSLİK • prototip")
