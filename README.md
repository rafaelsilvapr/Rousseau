# Arquitetura da Música - Sistema Rousseau

Este projeto é uma ferramenta de transcrição e análise musical baseada no sistema **Rousseau-Galin-Paris-Chevé**, desenvolvida para o **Prof. Dr. Rafael**. O objetivo é converter áudio e letra em uma partitura funcional que utilize a notação numérica de Rousseau e um sistema de harmonia híbrida autoral.

## 🚀 Funcionalidades Atuais (Fase 1 & 2)

- **Transcrição de Pitch:** Utiliza o motor `basic-pitch` da Spotify para extrair notas de arquivos de áudio (.mp3, .wav).
- **Sistema Rousseau:** Conversão automática de frequências para o sistema de numeração musical (1-7), adaptado à tonalidade (Key) selecionada.
- **Análise Prosódica:** Motor de separação silábica em Português com suporte automático para **Sinalefas e Elisões** (junção rítmica de vogais).
- **Visualização LaTeX:** Geração de output visual alinhando verticalmente Melodia, Letra e estrutura Harmônica.

## 🛠️ Instalação e Uso Local

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/rafaelsilvapr/Rousseau.git
   cd Rousseau
   ```

2. **Crie um ambiente virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Mac/Linux
   # No Windows: venv\Scripts\activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute o App:**
   ```bash
   streamlit run app.py
   ```

## ☁️ Deployment

Este app foi projetado para rodar no **Streamlit Community Cloud**. Para mais detalhes sobre a arquitetura da música e o sistema Rousseau, entre em contato com o Prof. Rafael.

---
*Desenvolvido com foco em Tecnologia Musical e Engenharia de Software.*
