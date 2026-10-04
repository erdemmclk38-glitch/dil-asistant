import json
import os
import random
import streamlit as st

# Verilerin saklanacağı dosya
DATA_FILE = "vocab_data.json"

# Desteklenen diller
LANGUAGES = ["İspanyolca", "Rusça", "Almanca"]


def load_data():
  if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
      return json.load(f)
  # Başlangıçta her dil için boş sözlük oluşturalım
  return {lang: {} for lang in LANGUAGES}


def save_data(data):
  with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)


# Sayfa Ayarları
st.set_page_config(
    page_title="Çok Dilli Kelime Asistanı", page_icon="🌍", layout="centered"
)

st.title("🌍 3 Dilli Kelime Öğrenme Asistanı")
vocab_data = load_data()

# Kenar Çubuğu (Menü)
st.sidebar.header("Menü")
menu = st.sidebar.selectbox(
    "Git", ["Çalış / Test Modu", "Yeni Kelime Ekle", "Kelimelerim"]
)

# 1. Yeni Kelime Ekleme Sayfası
if menu == "Yeni Kelime Ekle":
  st.subheader("Yeni Kelime Ekle")

  selected_lang = st.selectbox("Hedef Dil Seçin", LANGUAGES)
  word = st.text_input(f"Kelime ({selected_lang}):")
  meaning = st.text_input("Anlamı (Türkçe):")

  if st.button("Kelimeyi Kaydet"):
    if word.strip() and meaning.strip():
      vocab_data[selected_lang][word.strip()] = meaning.strip()
      save_data(vocab_data)
      st.success(
          f"'{word}' başarıyla **{selected_lang}** sözlüğüne eklendi! 🎉"
      )
    else:
      st.warning("Lütfen her iki alanı da doldurun.")

# 2. Kayıtlı Kelimeler Sayfası
elif menu == "Kelimelerim":
  st.subheader("Kayıtlı Kelimeleriniz")
  selected_lang = st.selectbox("Görmek İstediğin Dil", LANGUAGES)

  lang_dict = vocab_data.get(selected_lang, {})
  if lang_dict:
    st.info(f"Toplam {len(lang_dict)} kelime kaydedilmiş.")
    for w, m in lang_dict.items():
      st.write(f"🔹 **{w}** : {m}")
  else:
    st.warning(f"**{selected_lang}** dilinde henüz kelime yok.")

# 3. Çalışma / Test Modu
elif menu == "Çalış / Test Modu":
  st.subheader("Flashcard / Test Modu")
  selected_lang = st.selectbox("Çalışılacak Dil", LANGUAGES)

  lang_dict = vocab_data.get(selected_lang, {})

  if lang_dict:
    words = list(lang_dict.keys())

    # Oturumda kelime yoksa veya dil değiştiyse rastgele bir kelime seç
    if (
        "current_word" not in st.session_state
        or st.session_state.get("active_lang") != selected_lang
    ):
      st.session_state.active_lang = selected_lang
      st.session_state.current_word = random.choice(words)
      st.session_state.show_answer = False

    curr_w = st.session_state.current_word

    st.markdown(f"### Soru ({selected_lang}): **{curr_w}**")

    if st.button("Anlamını Göster"):
      st.session_state.show_answer = True

    if st.session_state.show_answer:
      st.success(f"Türkçe Anlamı: **{lang_dict[curr_w]}**")

    if st.button("Sonraki Kelimeye Geç ➡️"):
      st.session_state.current_word = random.choice(words)
      st.session_state.show_answer = False
      st.rerun()
  else:
    st.warning(
        f"Önce **{selected_lang}** diline 'Yeni Kelime Ekle' menüsünden birkaç"
        " kelime eklemelisin!"
    )