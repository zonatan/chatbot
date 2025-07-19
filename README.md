# Zobot: Chatbot Cerdas Berbasis NLP dan BERT 🤖

![Zobot Logo](https://png.pngtree.com/png-vector/20220718/ourmid/pngtree-chat-bot-icon-vector-png-image_5569903.png)  
**Zobot** adalah chatbot interaktif berbasis Python yang memanfaatkan **Natural Language Processing (NLP)** dan model **BERT** untuk memahami maksud pengguna dan memberikan respons cerdas. Zobot mendukung percakapan dalam **bahasa Indonesia** dan **Inggris**, dengan kemampuan pelatihan manual melalui perintah `/train`. Data disimpan dalam **SQLite** dan file **JSON** untuk fleksibilitas maksimal.

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python)](https://www.python.org/)  
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)  
[![GitHub Issues](https://img.shields.io/github/issues/zonatan/chatbot)](https://github.com/zonatan/chatbot/issues)

---

## 🚀 Fitur Unggulan

- **Pemahaman Intent**  
  Menggunakan **spaCy** untuk deteksi intent dasar dan **BERT** untuk klasifikasi intent yang lebih akurat.
- **Pelatihan Interaktif**  
  Latih bot secara langsung dengan perintah `/train <input> | <response> | <intent>`.
- **Pencocokan Fuzzy**  
  Tangani variasi input pengguna dengan `fuzzywuzzy` (case-insensitive).
- **Manajemen Data**  
  Simpan riwayat percakapan dan data pelatihan di **SQLite** dan **JSON**.
- **Analisis Sentimen**  
  Deteksi emosi pengguna dengan **TextBlob**.
- **Perintah Interaktif**  
  Dukungan untuk `/help`, `/history`, `/clear`, `/rate`, dan `/train`.

---

## 📋 Prasyarat

- **Python**: Versi 3.8 atau lebih tinggi
- **Virtual Environment**: Direkomendasikan
- **Dependensi**:
  ```bash
  pip install transformers torch accelerate fuzzywuzzy python-Levenshtein spacy textblob python-decouple scikit-learn
  python -m spacy download en_core_web_sm
  ```

---

## 🛠️ Instalasi

1. **Clone Repository** (jika tersedia):
   ```bash
   git clone https://github.com/zonatan/chatbot.git
   cd chatbot
   ```

2. **Buat Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   .\venv\Scripts\activate   # Windows
   ```

3. **Instal Dependensi**:
   ```bash
   pip install --upgrade pip
   pip install transformers[torch] accelerate fuzzywuzzy python-Levenshtein spacy textblob python-decouple scikit-learn
   python -m spacy download en_core_web_sm
   ```

4. **Konfigurasi `.env`** (opsional):
   ```plaintext
   USER_ID=user1
   ```

5. **Jalankan Zobot**:
   ```bash
   python chatbot.py
   ```

---

## 🎮 Cara Menggunakan

1. **Jalankan Bot**:
   ```bash
   python chatbot.py
   ```
   Bot akan menampilkan pesan:  
   `Zobot Enhanced started! Type /help for commands or /quit to exit.`

2. **Perintah yang Tersedia**:
   | Perintah | Deskripsi |
   |----------|-----------|
   | `/help` | Menampilkan daftar perintah |
   | `/history` | Menampilkan riwayat percakapan |
   | `/clear` | Menghapus konteks percakapan |
   | `/train <input> | <response> | <intent>` | Melatih bot dengan input, respons, dan intent |
   | `/rate <score>` | Memberi rating (1-5) untuk respons terakhir |
   | `/quit` | Keluar dari bot |

3. **Contoh Interaksi**:
   ```plaintext
   You: /train Halo | Halo, apa kabar? | greeting
   Bot: Trained: Intent 'greeting' with input 'halo' and response 'Halo, apa kabar?'
   You: halo
   Bot: Halo, apa kabar?
   You: apa kabar?
   Bot: Saya baik, terima kasih!
   ```

---

## 📂 Struktur Proyek

```plaintext
chatbot/
├── chatbot.py          # Logika utama chatbot
├── train.py            # Pelatihan model BERT
├── nlp_utils.py        # Pemrosesan NLP dan respons
├── database.py         # Manajemen database SQLite
├── responses.json      # Penyimpanan respons default dan terlatih
├── chatbot.db          # Database SQLite untuk riwayat dan pelatihan
├── .env                # Konfigurasi environment (opsional)
└── README.md           # Dokumentasi proyek
```

---

## 🔍 Cara Kerja

1. **Inisialisasi**: Memuat model **spaCy** (`en_core_web_sm`), **BERT** (`bert-base-uncased`), dan respons dari `responses.json`.
2. **Pemrosesan Input**: Fungsi `process_input` di `nlp_utils.py` mengenali intent menggunakan spaCy dan BERT.
3. **Pencocokan Respons**: `fuzzywuzzy` mencocokkan input pengguna dengan respons di `responses.json`.
4. **Pelatihan**: Perintah `/train` menyimpan data ke `chatbot.db` dan `responses.json`, lalu melatih ulang model BERT.
5. **Penyimpanan**: Riwayat percakapan dan rating disimpan di `chatbot.db`.

---

## 🤝 Kontribusi

Kami sangat menghargai kontribusi untuk meningkatkan Zobot! Langkah-langkah:
1. Fork repository ini.
2. Buat branch baru: `git checkout -b fitur-baru`.
3. Commit perubahan: `git commit -m "Menambahkan fitur baru"`.
4. Push ke branch: `git push origin fitur-baru`.
5. Buat Pull Request di GitHub.

---

## 🌟 Rencana Pengembangan

- **Pelatihan Otomatis**: Integrasi dataset eksternal untuk pelatihan tanpa `/train`.
- **Bahasa Indonesia**: Dukungan penuh dengan model seperti **IndoBERT**.
- **Antarmuka Web**: Tambahkan UI berbasis **Flask** atau **FastAPI**.
- **Analisis Sentimen Lanjutan**: Tingkatkan deteksi sentimen dengan model khusus.

---

## 📜 Lisensi

Dilisensikan di bawah [MIT License](LICENSE).

---

## 📬 Kontak

Ada pertanyaan atau saran? Hubungi kami di [zonatan.sh03@gmail.com](mailto:zonatan.sh03@gmail.com) atau buka issue di [GitHub](https://github.com/zonatan/chatbot/issues).