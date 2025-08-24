import streamlit as st
from PIL import Image
import base64

# Carrega a imagem da logo
logo = Image.open('img/logo.png')

# Configurações da página, incluindo o ícone da aba do navegador
st.set_page_config(
    page_title="Victor Hugo de Paula - Portfólio",
    page_icon=logo,
    layout="wide"
)

def get_image_base64(path):
    with open(path, "rb") as img_file: return base64.b64encode(img_file.read()).decode()

# streamlit run Home.py / python -m streamlit run Home.py
def home_page():

    # Adiciona a logo na sidebar
    with st.sidebar:
        st.image(logo, width=30)

    col1, col2 = st.columns([1, 9])

    with col1:
        # Coloca a logo na primeira coluna
        st.image(logo, width=100)

    with col2:
        # Título
        st.title("Victor Hugo de Paula - Perfil Profissional")

    # Conteúdo da página Home
    st.divider()
    col1, col2, col3 = st.columns([8, 1, 4])

    with col1:
        st.header("Introdução Pessoal")
        st.markdown("""
        Tenho 19 anos. Estudante de **Engenharia de Software**  com forte interesse em tecnologia desde a infância.
        Possuo conhecimentos avançados em computação  e sou **autodidata** em:
        - **Design gráfico** (Photoshop)
        - **Produção musical** (FL Studio, Ableton Live)
        - **Edição de vídeo** (VEGAS, Davinci Resolve)

        Além da minha formação técnica, sou **fluente em inglês** e iniciante em francês. Minhas **habilidades interpessoais** foram desenvolvidas por meio da prática esportiva e trabalhos em grupo. Sou uma pessoa **determinada, criativa** e com **facilidade para aprender**.
        """)
    
    with col3:
        image_path = 'img/pfp.jpg' # Substitua 'sua_foto.jpg' pelo nome do seu arquivo
        image_base64 = get_image_base64(image_path)
        st.markdown(f"""
            <img src="data:image/png;base64,{image_base64}" 
                 style="border: 2px solid #FDEBE2; border-radius: 7px; width: 320px; height: auto;">
        """, unsafe_allow_html=True)

    st.header("Objetivo Profissional")
    st.markdown("""
    Busco minha primeira oportunidade profissional na área de tecnologia, com o objetivo de aplicar e expandir meus conhecimentos em desenvolvimento de software, design digital e computação em geral.
    """)

    # Adicionando o rodapé
    st.divider() # Adiciona uma linha horizontal para separar o conteúdo do rodapé
    st.markdown(f"""
        <div style="text-align: center;">
            <p>
                <b>Contato:</b><br>
                📞 Telefone: (11) 91032-7240  | 📧 E-mail: dipaula.victo@gmail.com  | 🔗 <a href="https://github.com/dipaula-victo">GitHub</a><br>
            </p>
                <b>© 2025</b>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    home_page()