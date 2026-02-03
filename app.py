import streamlit as st
import numpy as np
import librosa
import tempfile
import os
import re
from basic_pitch.inference import predict
from basic_pitch import ICASSP_2022_MODEL_PATH

# --- Configurações da Página ---
st.set_page_config(
    page_title="Arquitetura da Música",
    page_icon="🎼",
    layout="wide"
)

# --- Estilo Customizado ---
st.markdown("""
<style>
    .stApp {
        background-color: #fcfcfc;
    }
    .title-text {
        color: #1a365d;
        text-align: center;
        font-family: 'Georgia', serif;
        font-weight: 900;
        margin-bottom: 0px;
    }
    .subtitle-text {
        color: #4a5568;
        text-align: center;
        margin-bottom: 30px;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

# --- Lógica de Apoio (Backend) ---

def split_syllables_pt(text):
    """
    Uma aproximação simples para separação silábica em Português.
    Considera sinalefas (junção de vogais entre palavras).
    """
    # Limpeza básica
    text = text.strip()
    # Identifica sinalefas: vogal no fim de palavra + vogal no início da próxima
    # Ex: "terra e" -> "terrae" (vira uma sílaba rítmica)
    text = re.sub(r'([aeiouáéíóúâêôãõ])\s+([aeiouáéíóúâêôãõ])', r'\1\2', text, flags=re.IGNORECASE)
    
    words = text.split()
    all_syllables = []
    
    for word in words:
        # Padrão básico de sílabas (consoante + vogal)
        # Nota: Esta é uma versão simplificada para a Fase 2.
        syllables = re.findall(r'[^aeiouáéíóúâêôãõ]*[aeiouáéíóúâêôãõ]+(?:n|s|r|l|m|z)?(?![aeiouáéíóúâêôãõ])|.+', word, re.IGNORECASE)
        all_syllables.extend(syllables)
    
    return [s.strip() for s in all_syllables if s.strip()]

def midi_to_rousseau(midi_note, key_note):
    """
    Converte nota MIDI para o número Rousseau (1-7) baseado no tom.
    """
    names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    key_index = names.index(key_note)
    
    # Distância em semitons do tom fundamental
    distance = (int(midi_note) - key_index) % 12
    
    # Mapeamento Graus (Simplificado: Maior)
    mapping = {
        0: "1",  # Tônica
        1: "1#",
        2: "2",  # Segunda
        3: "2#",
        4: "3",  # Terça
        5: "4",  # Quarta
        6: "4#",
        7: "5",  # Quinta
        8: "5#",
        9: "6",  # Sexta
        10: "6#",
        11: "7"   # Sétima
    }
    return mapping.get(distance, "?")

# --- Interface Principal ---

st.markdown('<h1 class="title-text">Arquitetura da Música</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">Análise Estrutural: Rousseau-Galin-Paris-Chevé</p>', unsafe_allow_html=True)

with st.sidebar:
    st.header("Configurações")
    notas = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    tonalidade = st.selectbox("Tom (Key):", notas)
    
    st.divider()
    st.info("O sistema utiliza `basic-pitch` para transcrição automática de áudio.")

col_main, col_preview = st.columns([2, 1])

with col_main:
    audio_file = st.file_uploader("Upload de Áudio (Voz/Instrumento):", type=["mp3", "wav"])
    letra_bruta = st.text_area("Letra da Música:", height=150, placeholder="Ex: Eu gostava tanto de você...")
    
    if st.button("Gerar Análise Completa", type="primary"):
        if audio_file and letra_bruta:
            with st.spinner("Analisando frequências e alinhando prosódia..."):
                # 1. Salvar áudio temporariamente para processar
                with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp:
                    tmp.write(audio_file.getvalue())
                    tmp_path = tmp.name

                try:
                    # 2. Extração de Pitch (Inference)
                    model_output, midi_data, note_events = predict(tmp_path)
                    
                    # Ordenar notas por tempo de início
                    notes = sorted(midi_data.instruments[0].notes, key=lambda x: x.start)
                    
                    # 3. Processamento de Letra
                    silabas = split_syllables_pt(letra_bruta)
                    
                    # 4. Alinhamento (Silaba -> Nota)
                    # Pegamos apenas as notas principais para alinhar com as sílabas
                    num_to_match = min(len(notes), len(silabas))
                    
                    output_data = []
                    for i in range(num_to_match):
                        note_val = notes[i].pitch
                        rousseau = midi_to_rousseau(note_val, tonalidade)
                        output_data.append({
                            "nota": rousseau,
                            "silaba": silabas[i]
                        })
                    
                    # 5. Visualização LaTeX
                    st.subheader("Resultado da Análise")
                    
                    # Construir strings para o LaTeX
                    melodia_str = " & ".join([fr"\mathbf{{{d['nota']}}}" for d in output_data])
                    silabas_str = " & ".join([fr"\text{{{d['silaba']}}}" for d in output_data])
                    
                    # Placeholder para harmonia vertical (Ex: I 5/3)
                    # Na fase posterior, isso virá de um motor de harmonia
                    harmonia_str = " & ".join([r"\text{I} \begin{smallmatrix} 5 \\ 3 \end{smallmatrix}" if i == 0 else r"\dots" for i in range(num_to_match)])

                    latex_code = fr"""
                    \begin{array}{l}
                    \text{{Melodia (Rousseau):}} & {melodia_str} \\
                    \text{{Prosódia (Sílabas):}} & {silabas_str} \\
                    \text{{Harmonia Híbrida:}} & {harmonia_str}
                    \end{array}
                    """
                    
                    st.latex(latex_code)
                    
                    st.success(f"Análise concluída: {num_to_match} unidades alinhadas.")
                    
                except Exception as e:
                    st.error(f"Erro no processamento: {e}")
                finally:
                    os.unlink(tmp_path)
        else:
            st.warning("Por favor, forneça o áudio e a letra.")

with col_preview:
    st.subheader("Referência de Sistema")
    st.markdown("""
    **Legenda Rousseau:**
    - 1: Dó (Tônica)
    - 2: Ré
    - 3: Mi
    - 4: Fá
    - 5: Sol
    - 6: Lá
    - 7: Si
    
    **Sinalefas:** 
    Identificadas automaticamente quando vogais se encontram entre palavras.
    """)
    
    if audio_file:
        st.audio(audio_file)


# --- Footer ---
st.markdown("---")
st.caption("Fase 1: Implementação de Interface e Coleta de Dados. | Desenvolvido para Prof. Rafael Rodrigues da Silva.")
