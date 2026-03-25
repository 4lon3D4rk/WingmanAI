import streamlit as st
from google import genai

st.set_page_config(page_title="Wingman AI", page_icon="✈️")

try:
    API_KEY = st.secrets["API"]
    client = genai.Client(api_key=API_KEY)
except Exception:
    st.error("Lütfen Streamlit Secrets kısmına 'GEMINI_API_KEY' ekleyin.")
    st.stop()

MODELS_TO_TRY = ["gemini-3.1-flash-lite-preview",
                "gemma-3-27b-it",
                "gemini-2.0-flash",
                "gemini-2.5-pro",
                "gemini-2.5-flash",
                "gemini-3-pro-preview",
                "gemini-3.1-pro-preview"]

st.title("✈️ Wingman AI")
st.subheader("Cevapsızlık derdine Son!")

gelen_mesaj = st.text_area("Gelen mesajı buraya yapıştır:", placeholder="Akşam dışarı çıkmaya ne dersin?")

col1, col2 , col3 = st.columns(3)

with col1:
    iliski = st.selectbox("Aranızdaki durum ne?", ["💖Flört", "🤗Kanka", "💔Eski Sevgili", "👋Yeni Biri", "💞Sevgili"])
with col2:
    mood = st.selectbox("Cevap enerjisi nasıl olsun?", ["🥰Cana Yakın", "😝Heyecanlı", "🙂Normal", "😪Üzgün", "🥶Soğuk", "😡Küs"])
with col3:
    kısaltma_btn = st.checkbox("Kısaltma Kullan")

extra_not = st.text_area("Ekstra Öneri Notu (İsteğe bağlı):", placeholder="Örn: Küfürlü konuş ve kısa cevaplar yaz")

result_container = st.container()

if st.button("Cevapları Listele ✨"):
    if not gelen_mesaj:
        st.error("Lütfen bir mesaj gir!")
    else:
        if kısaltma_btn: kısaltma = "Evet"
        else: kısaltma = "Hayır"

        with result_container:
            success = False
            prompt = f"""
            Gelen Mesaj: "{gelen_mesaj}"
            İlişki Durumu: {iliski}
            Cevap Enerjisi: {mood}
            Kısaltma Kullanılsın mı? : {kısaltma}
            Ekstra Not: {extra_not if extra_not else "Yok"}
            GÖREV: Sadece 3 farklı, kısa ve doğal cevap önerisi yaz. 
            KURAL 1: Hiçbir açıklama yapma, sadece madde işaretli liste ver.
            KURAL 2: Eğer kısaltma kullanılcaksa bunun gibi kısaltmalar kullan (Kısaltma Kullanılmıcaksa bu kuralı unut.);
                - ok : tamam
                - bb : görüşürüz
                - tm : tamam
                - yk : yok
                - evt : evet
                - nbr : naber?
                - ii : iyi
                - eyw : eyvallah
                - tşk : teşekkürler
            """

            for model_name in MODELS_TO_TRY:
                try:
                    with st.spinner(f'Wingman düşünüyor... ({model_name})'):
                        response = client.models.generate_content(model=model_name, contents=prompt)
                        
                        st.markdown("---")
                        st.success(f"İşte senin için öneriler:")
                        st.write(response.text)
                        
                        st.info("💡 **Unutma:** Mesajı kendi tarzına göre ufakça düzenlemeyi ihmal etme!")
                        
                        success = True
                        break 
                except Exception as e:
                    continue
            
            if not success:
                st.error("Şu an tüm zekalar meşgul, lütfen saniyeler sonra tekrar dene.")