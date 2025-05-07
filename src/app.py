import streamlit as st
from gemini_functions import GeminiChat
import time
import base64
from streamlit.components.v1 import html

# Configuração da página
st.set_page_config(
    page_title="Dxrager Gaming",
    page_icon="🎮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS personalizado
def set_custom_style():
    st.markdown(f"""
    <style>
        :root {{
            --primary: #00d4ff;
            --secondary: #6e00ff;
            --dark: #0a0a1a;
            --light: #f0f2f6;
        }}
        
        /* Layout principal */
        .main {{
            background-color: #000000;
            color: white;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        
        /* Container do produto */
        .product-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 2rem;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(110, 0, 255, 0.2);
            max-width: 600px;
            margin: 0 auto;
        }}
        
        /* Título */
        .product-title {{
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            background: linear-gradient(90deg, #00d4ff 0%, #6e00ff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
        }}
        
        /* Subtítulo */
        .product-subtitle {{
            font-size: 1rem;
            color: #a0a0a0;
            margin-bottom: 2rem;
            text-align: center;
        }}
        
        /* Opções */
        .option-group {{
            width: 100%;
            margin-bottom: 1.5rem;
        }}
        
        .option-title {{
            font-size: 1rem;
            font-weight: 600;
            color: #00d4ff;
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
        }}
        
        .option-title:before {{
            content: "•";
            margin-right: 8px;
            color: #6e00ff;
        }}
        
        /* Botões */
        .stButton>button {{
            width: 100%;
            border: none;
            background: linear-gradient(90deg, #6e00ff 0%, #00d4ff 100%);
            color: white;
            padding: 12px;
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.3s ease;
        }}
        
        .stButton>button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(110, 0, 255, 0.4);
        }}
    </style>
    """, unsafe_allow_html=True)

set_custom_style()

# Inicialização do chat
if "gemini_chat" not in st.session_state:
    st.session_state.gemini_chat = GeminiChat()
    
if "messages" not in st.session_state:
    st.session_state.messages = []

# Container principal
with st.container():
    # Logo no topo
    st.image("imagens/AstraMind_logo.png", width=500, use_container_width=True)
    
    # Histórico de mensagens
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message["role"] == "user":
                st.markdown(f"<div class='glass-effect' style='color: #00d4ff;'>{message['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='glass-effect'>{message['content']}</div>", unsafe_allow_html=True)

# Rodapé fixo
with st.container():
    st.markdown('<div class="footer-container">', unsafe_allow_html=True)
    
    # Input de mensagem
    if prompt := st.chat_input("Digite sua mensagem..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(f"<div class='glass-effect' style='color: #00d4ff;'>{prompt}</div>", unsafe_allow_html=True)
        
        with st.chat_message("assistant"):
            with st.spinner("Processando..."):
                response = st.session_state.gemini_chat.send_message(prompt)
            
            if response.startswith(("⚠️", "⛔")):
                st.markdown(
                    f"""<div class='error-effect'>⚠️ {response}</div>""",
                    unsafe_allow_html=True
                )
            else:
                message_placeholder = st.empty()
                full_response = ""
                
                for chunk in response.split(" "):
                    full_response += chunk + " "
                    time.sleep(0.05)
                    message_placeholder.markdown(f"""
                    <div class='glass-effect'>
                        {full_response}<span style='color: #00d4ff;'>▌</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                message_placeholder.markdown(f"""
                <div class='glass-effect'>
                    {full_response}
                </div>
                """, unsafe_allow_html=True)
            
            st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Botão de limpar
    if st.button("Limpar Conversa", key="clear_chat", use_container_width=True, type="primary"):
        st.session_state.gemini_chat.clear_history()
        st.session_state.messages = []
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)