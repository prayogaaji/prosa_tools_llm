"""
Install the Google AI Python SDK

$ pip install google-generativeai
"""

import os
from dotenv import load_dotenv

import google.generativeai as genai
import pandas as pd
import regex as re

load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)
    
# mengambil data dari excel
df = pd.read_excel('prosa.xlsx', engine='openpyxl')
df['combined'] = df['Title'] + '\n' + df['Content']

data_result = {
    'classification_match': [],  
    'support': [],
    'oppose': [],
    'unrelated': [],
    'topic': [],
    'subtopic': []
}

# Membuat DataFrame baru
df_result = pd.DataFrame(data_result)

chat_session = model.start_chat(
  history=[]
)

for index, row in df.iterrows():
    try:
        article = row['combined']

        chat = f'''
        kamu adalah asisten yang sangat membantu. lakukan :
        1. "klasifikasi artikel" terhadap artikel yang diberikan ke dalam kategori Hoax atau Fakta. berikan jawaban singkat, maksimal 1 kata, akhiri dengan ".". 
        2. buatlah 1 "paragraf pendukung" untuk mendukung topik yang diberikan, akhiri dengan "."
        3. buatlah 1 "paragraf berlawanan" untuk kontra terhadap topik yang diberikan, akhiri dengan "."
        4. buatlah 1 "paragraf tidak berelasi" terkait topik yang diberikan , akhiri dengan "."
        5. pilih salah satu "topik" yang sesuai dengan artikel : (Dampak krisis iklim, Strategi mitigasi, Kebijakan dan pemerintahan, Edukasi dan kesadaran, Keadilan dan kesetaraan lingkungan, Konservasi lingkungan, Risiko kesehatan). akhiri dengan "."
        6. tentukan "subtopik" yang sesuai dengan artikel : (Ekosistem, Pertanian dan keamanan pangan, Pola cuaca yang berubah, Bencana alam, Inisiatif energi terbarukan, Perencanaan kota, Perjanjian internasional, Peran pemerintah lokal, Program literasi, Kampanye publik, Perspektif masyarakat adat tentang krisis iklim, Mengatasi dampak yang tidak proporsional, Ketahanan komunitas, Pelestarian habitat, Penyakit yang ditularkan oleh vektor, Polusi udara). akhiri dengan "."
        berikan judul dengan delimiter : "## " untuk setiap perintah

        ARTIKEL :
        {article}
        '''
        response = chat_session.send_message(chat)
        text = response.text.lower()

        # Parsing dengan regex untuk setiap bagian
        classification_match = re.search(r'## klasifikasi artikel\n*(.*)', text)
        support_match = re.search(r'## paragraf pendukung\n(.*?)(?=\n## paragraf berlawanan)', text, re.DOTALL)
        oppose_match = re.search(r'## paragraf berlawanan\n(.*?)(?=\n## paragraf tidak berelasi)', text, re.DOTALL)
        unrelated_match = re.search(r'## paragraf tidak berelasi\n(.*?)(?=\n## topik)', text, re.DOTALL)
        topic_match = re.search(r'## topik\n(.*?)(?=\n## subtopik)', text, re.DOTALL)
        subtopic_match = re.search(r'## subtopik\n(.*)', text)
        print(classification_match)
        # Ekstrak nilai yang ditemukan
        classification = classification_match.group(1) if classification_match else ''
        support = support_match.group(1).strip() if support_match else ''
        oppose = oppose_match.group(1).strip() if oppose_match else ''
        unrelated = unrelated_match.group(1).strip() if unrelated_match else ''
        topic = topic_match.group(1).strip() if topic_match else ''
        subtopic = subtopic_match.group(1) if subtopic_match else ''

        # Menambahkan teks menggunakan append
        df_result = df_result._append({
            'classification_match': classification, 
            'support' : support,
            'oppose': oppose,
            'unrelated': unrelated,
            'topic': topic,
            'subtopic': subtopic
            }, ignore_index=True)
        print(text)
    except Exception as e:
        print(f"Error terjadi: {e}. Menghentikan loop.")
        break
    
df_result.to_excel('prosa_result.xlsx', index=False)
