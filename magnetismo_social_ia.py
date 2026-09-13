import streamlit as st
from groq import Groq
from datetime import datetime
import json
import re

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="MAGNETISMO SOCIAL IA", layout="wide")

# --- ESTILO CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    .stApp { background-color:#F8F9FA; font-family:'Inter',sans-serif; }
    [data-testid="stSidebar"] { display:none; }

    .stTextInput>div>div>input, .stTextArea>div>textarea,
    .stSelectbox>div>div>div, .stNumberInput>div>div>input {
        background-color:#FFFFFF !important; color:#1A1A2E !important;
        border:1px solid #CED4DA !important; font-family:'Inter',sans-serif !important;
    }

    .stButton>button {
        width:100%; border-radius:10px; height:3.2em;
        background:linear-gradient(135deg,#495057,#343A40) !important; color:white !important;
        font-weight:600; border:none; box-shadow:2px 2px 8px rgba(0,0,0,0.1);
        font-family:'Inter',sans-serif !important; transition:all 0.2s ease;
    }
    .stButton>button:hover { background:linear-gradient(135deg,#343A40,#212529) !important; transform:translateY(-1px); }
    .stApp .stButton>button, .stApp .stButton>button p,
    .stApp .stButton>button span, .stApp .stButton>button div { color:white !important; }

    .stApp h1, .stApp h2, .stApp h3 { color:#1A1A2E !important; font-family:'Inter',sans-serif !important; font-weight:700 !important; }

    .card { background:linear-gradient(135deg,#F1F3F5,#E9ECEF); padding:20px; border-radius:14px; border:1px solid #CED4DA; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card, .stApp .card p, .stApp .card span, .stApp .card div, .stApp .card strong, .stApp .card em { color:#1A1A2E !important; }

    .card-dark { background:linear-gradient(135deg,#E9ECEF,#DEE2E6); padding:20px; border-radius:14px; border:1px solid #ADB5BD; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-dark, .stApp .card-dark p, .stApp .card-dark span, .stApp .card-dark div, .stApp .card-dark strong { color:#1A1A2E !important; }

    .card-green { background:linear-gradient(135deg,#F0FDF4,#DCFCE7); padding:20px; border-radius:14px; border:1px solid #86EFAC; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-green, .stApp .card-green p, .stApp .card-green span, .stApp .card-green div { color:#14532D !important; }

    .card-blue { background:linear-gradient(135deg,#EFF6FF,#DBEAFE); padding:20px; border-radius:14px; border:1px solid #93C5FD; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-blue, .stApp .card-blue p, .stApp .card-blue span, .stApp .card-blue div { color:#1E3A8A !important; }

    .card-red { background:linear-gradient(135deg,#FFF5F5,#FEE2E2); padding:20px; border-radius:14px; border:1px solid #FECACA; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-red, .stApp .card-red p, .stApp .card-red span, .stApp .card-red div { color:#7F1D1D !important; }

    .card-yellow { background:linear-gradient(135deg,#FFFBEB,#FEF3C7); padding:18px; border-radius:12px; border:1px solid #FCD34D; margin-bottom:12px; white-space:normal; word-wrap:break-word; }
    .stApp .card-yellow, .stApp .card-yellow p, .stApp .card-yellow span, .stApp .card-yellow div { color:#78350F !important; }

    .stat-box { background:#FFFFFF; border-radius:12px; padding:16px; text-align:center; border:1px solid #CED4DA; }
    .stApp .stat-box div, .stApp .stat-box span, .stApp .stat-box p { color:#1A1A2E !important; }
    .stApp .stat-numero, .stat-numero { font-size:2em; font-weight:700; color:#495057 !important; }

    .hist-item { background:#FFFFFF; border-radius:10px; padding:12px 16px; margin-bottom:8px; border-left:4px solid #CED4DA; }
    .stApp .hist-item, .stApp .hist-item p, .stApp .hist-item span, .stApp .hist-item div, .stApp .hist-item small { color:#1A1A2E !important; }

    .badge { background:#495057; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-verde { background:#059669; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-amarelo { background:#B45309; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-azul { background:#1D4ED8; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-roxo { background:#6D28D9; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }

    .divider { border:none; height:1px; background:linear-gradient(to right,transparent,#CED4DA,transparent); margin:18px 0; }

    .chat-user { background:#FFFFFF; border:1px solid #CED4DA; border-radius:12px 12px 4px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-user, .stApp .chat-user p, .stApp .chat-user span, .stApp .chat-user div { color:#1A1A2E !important; }

    .chat-persona { background:#F8F9FA; border:1px solid #CED4DA; border-radius:4px 12px 12px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-persona, .stApp .chat-persona p, .stApp .chat-persona span, .stApp .chat-persona div { color:#1A1A2E !important; }

    .questao-box { background:#FFFFFF; border:2px solid #CED4DA; border-radius:12px; padding:18px; margin-bottom:14px; }
    .stApp .questao-box, .stApp .questao-box p, .stApp .questao-box span, .stApp .questao-box div { color:#1A1A2E !important; }

    .avaliacao-box { background:#FFFFFF; border:2px solid #CED4DA; border-radius:14px; padding:18px; margin-bottom:12px; }
    .stApp .avaliacao-box, .stApp .avaliacao-box p, .stApp .avaliacao-box span, .stApp .avaliacao-box div { color:#1A1A2E !important; }

    .meta-box { background:#FFFFFF; border:2px solid #CED4DA; border-radius:12px; padding:16px; text-align:center; margin:10px 0; }
    .stApp .meta-box, .stApp .meta-box div, .stApp .meta-box span { color:#1A1A2E !important; }
    .stApp .meta-numero { font-size:2em; font-weight:700; color:#495057 !important; }

    .chat-scroll-container { max-height:40vh; overflow-y:auto; display:flex; flex-direction:column; scroll-behavior:smooth; padding-bottom:4px; }
    .chat-scroll-container > * { flex-shrink:0; }
    

    </style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CACHE
# ─────────────────────────────────────────────
@st.cache_resource
def get_cache_magnetismo():
    return {"perfis": {}}

_cache = get_cache_magnetismo()

# ─────────────────────────────────────────────
# PERSISTÊNCIA LOCAL (JSON)
# ─────────────────────────────────────────────
CHAVES_SALVAR = ['usuario', 'historico_consultas', 'consultas_salvas', 'contexto_padrao']

def gerar_json_sessao() -> str:
    dados = {k: st.session_state.get(k) for k in CHAVES_SALVAR}
    dados['salvo_em'] = datetime.now().strftime('%d/%m/%Y %H:%M')
    return json.dumps(dados, ensure_ascii=False, indent=2, default=str)

def carregar_json_sessao(dados):
    _bloq = {'api_key','etapa','nome_login','chave_login','upload_login','btn_entrar_login'}
    _pref = (
        'btn_','sel_','ul_','dl_','cad_','_sub','_sm','_tab','_bsc',
        'ativo_','rem_','sel_pet_','ev_','prof_','hig_','prev_',
        'vac_','sint_','comp_','trad_','subs_','amb_','viag_','chat_',
        'duvida_','emerg_','peso_','data_','obs_','tipo_','vet_','desc_',
        'local_','prox_','alim','sit_emerg_','tc_','oraf','siau','agmag',
        'lv','mv','pt','pi','sh','wc','rv','rp','rc',
    )
    import re as _re
    for k, v in dados.items():
        if k in _bloq: continue
        if any(k.startswith(p) for p in _pref): continue
        if _re.match(r'.+_\d+$', k): continue
        st.session_state[k] = v

def salvar_perfil_cache(usuario: str):
    _cache["perfis"][usuario] = {k: st.session_state.get(k) for k in CHAVES_SALVAR}

def perfis_salvos() -> list:
    return list(_cache["perfis"].keys())

def carregar_perfil_cache(usuario: str) -> dict | None:
    return _cache["perfis"].get(usuario)

def salvar_consulta(modulo: str, tema: str, conteudo: str):
    st.session_state.historico_consultas.append({
        'data': datetime.now().strftime('%d/%m %H:%M'), 'modulo': modulo, 'tema': tema, 'conteudo': conteudo,
    })

# --- INICIALIZAÇÃO DE ESTADO ---
defaults = {
    'etapa': "Login", 'usuario': "", 'api_key': "", 'pagina': "Home",
    'historico_consultas': [], 'consultas_salvas': [], 'contexto_padrao': "",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# --- PRINCÍPIO ÉTICO — compartilhado em todo prompt ---
PRINCIPIO_ETICO = """
PRINCÍPIO OBRIGATÓRIO — siga isso em TODA resposta:
- Você é um estrategista de comunicação e conexão humana — seu objetivo é ajudar a pessoa a se comunicar melhor,
  com autenticidade, e a construir relações saudáveis. Você NUNCA ensina técnicas de manipulação, pressão psicológica,
  gatilhos de persuasão para forçar interesse, ou qualquer tática que desrespeite a autonomia da outra pessoa
- O consentimento e o conforto da outra pessoa SEMPRE vêm antes de "ter sucesso" na interação. Se um conselho só
  funciona ignorando sinais de desconforto da outra pessoa, esse conselho está errado e você não deve dá-lo
- Para Leitura de Interesse, Perfil da Pessoa e Análise de Conversa envolvendo uma terceira pessoa real: trate tudo
  como HIPÓTESES para reflexão do usuário, nunca como certeza. Mensagens de texto carregam pouquíssimo contexto
  (tom de voz, expressão, situação) e interpretações à distância erram com frequência. Quando relevante, lembre que
  perguntar diretamente para a pessoa é sempre mais confiável do que tentar decifrar sinais indiretos
- Para Sinais de Atenção: trate com seriedade real. Se a descrição do usuário sugerir padrões de controle, ciúme
  excessivo, desrespeito a limites, insistência após recusa clara, ou isolamento da pessoa de amigos/família, nomeie
  isso claramente como sinal de alerta e não minimize — mas também não diagnostique a outra pessoa, fale em termos
  de padrões observados e o que fazer a respeito
- Você ajuda com qualquer tipo de conexão humana — amizades, networking profissional, relações familiares, e também
  interesse romântico/afetivo — sem assumir orientação, gênero ou contexto que o usuário não tenha informado
- Tom: caloroso, prático e direto — like um bom amigo que entende de pessoas e quer genuinamente que a pessoa se
  conecte melhor, não um manual de sedução
- Português do Brasil
"""

DISCLAIMER_PADRAO = """
<div class="disclaimer">
⚠️ <strong>Lembrete:</strong> isso é uma reflexão de apoio, não uma fórmula garantida — pessoas reais são mais
complexas do que qualquer padrão. Comunicação genuína e respeito mútuo valem mais que qualquer técnica.
</div>
"""

DISCLAIMER_LEITURA = """
<div class="disclaimer-leitura">
🔍 <strong>Sobre esta leitura de sinais:</strong> nenhum sinal isolado confirma interesse, desinteresse ou qualquer
intenção — mensagens de texto carregam muito pouco contexto. A forma mais confiável de saber o que alguém sente é
perguntar diretamente. Use isso como reflexão, não como certeza.
</div>
"""

# --- MOTOR DE IA ---
def magnetismo_ia(prompt: str, system_extra: str = "") -> str:
    try:
        client = Groq(api_key=st.session_state.api_key)
        system = f"""Você é um estrategista de comunicação e conexão humana, especialista em ajudar pessoas a se
expressarem com mais autenticidade e confiança em qualquer tipo de relação.
Usuário: {st.session_state.usuario}. Contexto atual: {st.session_state.contexto_padrao or 'não informado'}.
{PRINCIPIO_ETICO}
{system_extra}"""
        response = client.chat.completions.create(
            messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
            model="openai/gpt-oss-120b",
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Erro na API: {e}"

# --- BARRA DE SALVAR ---
def barra_salvar():
    salvar_perfil_cache(st.session_state.usuario)
    nome_usuario = st.session_state.usuario.lower().replace(' ', '_') or 'minha_sessao'
    total = len(st.session_state.historico_consultas)
    salvos = len(st.session_state.consultas_salvas)

    col_info, col_btn = st.columns([4, 2])
    with col_info:
        st.markdown(
            f"<div style='background:#FDF2F8;border:1px solid #BE185D;border-radius:10px;"
            f"padding:10px 14px;font-size:0.84em;color:#1A1A2E;line-height:1.6;'>"
            f"💾 <strong>Antes de sair, salve seus dados no computador.</strong><br>"
            f"<span style='color:#888;font-size:0.88em;'>{total} consultas geradas · {salvos} salvas</span>"
            f"</div>", unsafe_allow_html=True
        )
    with col_btn:
        st.download_button("💾 SALVAR MEUS DADOS (.json)", data=gerar_json_sessao(),
            file_name=f"magnetismo_social_{nome_usuario}.json", mime="application/json", use_container_width=True, key="dl_magnet_1")
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("""<style>
    .dica-nav{font-size:0.72em;color:#94A3B8;text-align:center;padding:2px 0 6px;}
    .dica-mobile{display:none;}
    .dica-desktop{display:block;}
    @media(max-width:768px){.dica-mobile{display:block;}.dica-desktop{display:none;}}
    </style>
    <div class='dica-nav dica-mobile'>👆 Deslize o dedo para navegar entre as abas</div>
    <div class='dica-nav dica-desktop'>📋 Clique no ícone acima para abrir o menu completo</div>
    """, unsafe_allow_html=True)

# ============================================================
# TELA: LOGIN
# ============================================================
if 'consultas_salvas' not in st.session_state: st.session_state['consultas_salvas'] = []
if 'contexto_padrao' not in st.session_state: st.session_state['contexto_padrao'] = None
if 'historico_consultas' not in st.session_state: st.session_state['historico_consultas'] = []

def chamar_ia(prompt, sistema="Você é um assistente inteligente. Responda em português do Brasil."):
    try:
        from groq import Groq as _GrCI
        client = _GrCI(api_key=st.session_state.api_key)
        resp = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role":"system","content":sistema},{"role":"user","content":prompt}],
            max_tokens=2048
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"Erro na IA: {e}"

if st.session_state.etapa == "Login":
    st.markdown("# 🤖 MAGNETISMO SOCIAL IA")
    st.markdown("<div class=\'card\'><b>🔒 ACESSO RESTRITO A CLIENTES DO QUIZ COM PRÊMIOS</b><br>🔗 <a href='https://quizcompremios.com.br' target='_blank' style='color:#4F46E5;font-weight:700;text-decoration:underline;'>quizcompremios.com.br</a></div>", unsafe_allow_html=True)
    st.info("💻 **Dica:** Pela complexidade dos agentes, no computador a experiência é mais agradável.")
    with st.container():
        nome  = st.text_input("Seu Nome:", key="nome_login")
        chave = st.text_input("🔑 Sua Chave API da Groq:", type="password", key="chave_login")
        arq_j = st.file_uploader("📂 Carregar dados salvos (.json):", type=["json"], key="upload_login")
        dados_login = json.load(arq_j) if arq_j else None
        if st.button("✨ ENTRAR", key="btn_entrar_login"):
            if len(nome.strip()) < 2:
                st.warning("Digite um nome com pelo menos 2 caracteres.")
            elif chave.strip():
                st.session_state.usuario = nome.strip()
                st.session_state.api_key = chave
                if dados_login: carregar_json_sessao(dados_login)
                st.session_state.etapa = "App"
                st.rerun()
            else:
                st.warning("Preencha nome e chave API.")

elif st.session_state.etapa == "App":



    # TABS
    _tab_Home, _tab_Impressao, _tab_PerfilPessoa, _tab_Leitura, _tab_Resposta, _tab_Assuntos, _tab_Simulador, _tab_Analise, _tab_Alerta, _tab_Psicologia, _tab_Academia, _tab_Mentor = st.tabs(['🏠 Painel Principal', '💬 Primeira Impressão', '🧠 Perfil da Pessoa', '🎯 Leitura de Interes', '💬2 Melhor Resposta', '🧩 Assuntos Infinitos', '🎭 Simulador de Conve', '📈 Análise da Convers', '🚩 Sinais de Atenção', '🧠2 Psicologia da Atra', '🎓 Academia Social', '🤖 Mentor 24h'])

    # ── BARRA SALVAR — aparece em todas as abas ──
    with st.expander("💾 Salvar / Carregar meus dados", expanded=False):
        _bsc1, _bsc2 = st.columns(2)
        with _bsc1:
            import json as _jsv
            _dsv = {k: st.session_state.get(k) for k in list(st.session_state.keys()) if not k.startswith('_') and k not in ('api_key',)}
            st.download_button("💾 Baixar meus dados (.json)",
                data=_jsv.dumps(_dsv, ensure_ascii=False, indent=2, default=str),
                file_name=f"dados_{st.session_state.get('usuario','user')}.json",
                mime="application/json", key="dl_barra_sv_magnetis")
        with _bsc2:
            _fupsv = st.file_uploader("📂 Carregar dados salvos:", type=["json"], key="ul_barra_sv_magnetis", label_visibility="collapsed")
            if _fupsv:
                try:
                    import json as _jld
                    for _k2,_v2 in _jld.loads(_fupsv.read().decode()).items():
                        if _k2 not in ('api_key','etapa'): st.session_state[_k2] = _v2
                    st.success("✅ Dados restaurados!"); st.rerun()
                except: st.error("Arquivo inválido.")


    with _tab_Home:
        col_u, col_r = st.columns([3, 1])
        with col_u:
            st.title(f"Olá, {st.session_state.usuario}! 🧲")
            st.markdown("<span class='badge'>Conexão Autêntica</span>", unsafe_allow_html=True)
        with col_r:
            if st.button("🚪 Sair", key="magnetis3"):
                for k in list(st.session_state.keys()):
                    del st.session_state[k]
                st.rerun()

        if len(st.session_state.historico_consultas) == 0:
            st.markdown("""<div style="background:#FEF3C7;border:2px solid #F59E0B;border-radius:12px;
            padding:12px 18px;margin-bottom:4px;color:#000;font-size:0.9em;font-weight:600;">
            ⚠️ Seus dados não estão mais no servidor.
            </div>""", unsafe_allow_html=True)
            arq_home = st.file_uploader("Carregar meus dados salvos (.json):", type=["json"], key="upload_home")
            if arq_home is not None:
                try:
                    dados_home = json.load(arq_home)
                    carregar_json_sessao(dados_home)
                    salvar_perfil_cache(st.session_state.usuario)
                    st.success("✅ Dados recuperados!")
                    st.rerun()
                except Exception:
                    st.error("Arquivo inválido.")

        st.session_state.contexto_padrao = st.text_input("🎯 Contexto atual (opcional):",
            value=st.session_state.contexto_padrao, placeholder="ex: conhecendo alguém novo, networking profissional, reconectando com um amigo...", key="magnetis7")


        modulos_count = {}
        for c in st.session_state.historico_consultas:
            modulos_count[c['modulo']] = modulos_count.get(c['modulo'], 0) + 1

        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f"<div class='stat-box'><div class='stat-numero'>{len(st.session_state.historico_consultas)}</div><div>Consultas geradas</div></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='stat-box'><div class='stat-numero'>{len(st.session_state.consultas_salvas)}</div><div>Salvas</div></div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='stat-box'><div class='stat-numero'>{len(modulos_count)}</div><div>Áreas exploradas</div></div>", unsafe_allow_html=True)
        c4.markdown(f"<div class='stat-box'><div class='stat-numero'>{modulos_count.get('Simulador',0)}</div><div>Simulações treinadas</div></div>", unsafe_allow_html=True)

        st.markdown("<div class='card'>💡 <em>'As pessoas mais magnéticas não são as que mais falam — são as que fazem você se sentir genuinamente ouvido.'</em></div>", unsafe_allow_html=True)

        st.markdown("### 🗺️ O que cada módulo faz")
        guia = {
            "💬 Primeira Impressão": "Como iniciar uma conversa naturalmente, sem parecer forçado",
            "🧠 Perfil da Pessoa": "Sugestões de comunicação com base no jeito da pessoa — racional, emocional, tímida...",
            "🎯 Leitura de Interesse": "Sinais possíveis de interesse ou desinteresse — sempre como hipótese",
            "💬 Melhor Resposta": "Cole uma conversa e receba opções de resposta em 5 tons diferentes",
            "🧩 Assuntos Infinitos": "Temas de conversa por idade, profissão, hobbies e contexto",
            "🎭 Simulador de Conversa": "Treine antes de mandar a mensagem real",
            "📈 Análise da Conversa": "Onde houve conexão, onde houve excesso, pontos fortes",
            "🚩 Sinais de Atenção": "Identifica desinteresse, falta de reciprocidade e possível manipulação",
            "🧠 Psicologia da Atração": "Reciprocidade, escuta ativa, autenticidade e mais — explicado de verdade",
            "🎓 Academia Social": "Minicurso de confiança, carisma e comunicação",
            "🤖 Mentor 24h": "Converse livremente sobre qualquer situação social",
        }
        for aba, desc in guia.items():
            st.markdown(f"**{aba}** — {desc}")

        st.header("💬 Primeira Impressão")
        st.markdown("Como iniciar bem qualquer conversa, sem parecer forçado.")

        col1, col2 = st.columns(2)
        with col1:
            situacao_impr = st.selectbox("Situação:", ["Conhecendo alguém presencialmente","Mensagem de abertura (app/redes)","Evento de networking","Reconectando depois de um tempo","Outro"], key="magnetis4")
        with col2:
            contexto_impr = st.text_input("Contexto específico (opcional):", placeholder="ex: amigo em comum, evento da empresa, app de relacionamento...", key="magnetis5")

        if st.button("💬 GERAR ORIENTAÇÃO", key="magnetis6"):
            with st.spinner("Pensando na melhor abordagem..."):
                prompt = (
                    f"Crie orientação prática para uma primeira impressão.\n"
                    f"Situação: {situacao_impr}. Contexto: {contexto_impr or 'não informado'}\n\n"
                    f"FORMATO:\n\n"
                    f"💬 PRIMEIRA IMPRESSÃO — {situacao_impr.upper()}\n\n"
                    f"🎯 COMO INICIAR NATURALMENTE:\n[2-3 formas concretas de abrir a conversa, com exemplos de frase]\n\n"
                    f"❌ O QUE EVITAR NOS PRIMEIROS MINUTOS:\n[erros comuns que afastam ou soam forçados]\n\n"
                    f"✨ COMO GERAR CURIOSIDADE SEM FORÇAR:\n[técnica genuína — não manipulação, autenticidade interessante]\n\n"
                    f"💡 EXEMPLO PRÁTICO:\n[1 mini-diálogo de exemplo mostrando a abordagem funcionando bem]"
                )
                res = magnetismo_ia(prompt)
                salvar_consulta("Impressao", situacao_impr, res)
                st.session_state['impr_temp'] = res

        if st.session_state.get('impr_temp'):
            st.markdown(f"<div class='card'>{st.session_state['impr_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['impr_temp'], file_name="primeira_impressao.txt", mime="text/plain", use_container_width=True, key="dl_magnet_3")
            with col_sv:
                if st.button("❤️ Salvar", key="sv_impr", use_container_width=True):
                    st.session_state.consultas_salvas.append({'modulo':'Impressao','tema':situacao_impr if 'situacao_impr' in dir() else '','conteudo':st.session_state['impr_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

        # ========================
        # PERFIL DA PESSOA
        # ========================

        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        st.markdown("### 💾 Salvar e Carregar Dados")
        _csl1, _csl2 = st.columns(2)
        with _csl1:
            import json as _json_sv
            _dados_sv = {k: st.session_state.get(k) for k in list(st.session_state.keys()) if not k.startswith('_')}
            st.download_button("💾 Salvar dados (.json)",
                data=_json_sv.dumps(_dados_sv, ensure_ascii=False, indent=2, default=str),
                file_name=f"dados_{st.session_state.get('usuario','user')}.json",
                mime="application/json", key="dl_sv_magnetis")
        with _csl2:
            _arq_sv = st.file_uploader("📂 Carregar dados:", type=["json"], key="ul_sv_magnetis")
            if _arq_sv:
                try:
                    import json as _json_ld
                    for _k, _v in _json_ld.loads(_arq_sv.read().decode()).items():
                        st.session_state[_k] = _v
                    st.success("✅ Dados carregados!")
                    st.rerun()
                except: st.error("Arquivo inválido.")

    with _tab_Impressao:
        st.header("Impressao")
        st.markdown("Descreva o contexto para análise:")
        prompt_impressao = st.text_area("", height=150, key="ta_impressao1", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="btn_impressao1", use_container_width=True):
            if prompt_impressao.strip():
                with st.spinner("Analisando..."):
                    try:
                        resp = chamar_ia(prompt_impressao)
                        if resp: st.session_state['res_impressao_magnet1'] = resp
                        st.markdown(f"<div class='card'>{resp}</div>", unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Erro: {e}")
            else:
                st.warning("Preencha o campo.")

    with _tab_PerfilPessoa:
        st.header("🧠 Perfil da Pessoa")
        st.markdown(DISCLAIMER_LEITURA, unsafe_allow_html=True)

        descricao_perfil = st.text_area("📝 Descreva o jeito da pessoa (personalidade, forma de falar, reações):", height=150,
            placeholder="ex: Ela fala pouco no início, responde com frases curtas, mas faz perguntas bem pensadas quando se interessa por um assunto...", key="magnetis6_d2")

        if st.button("🧠 ANALISAR PERFIL", key="magnetis7_d2"):
            if descricao_perfil.strip():
                with st.spinner("Analisando..."):
                    prompt = (
                        f"Analise este perfil de comunicação e sugira a melhor abordagem.\n"
                        f"Descrição: {descricao_perfil}\n\n"
                        f"FORMATO:\n\n"
                        f"🧠 PERFIL IDENTIFICADO (hipótese)\n\n"
                        f"📊 TENDÊNCIA PRINCIPAL: [Mais racional / Mais emocional / Mais tímida / Mais extrovertida / Mix]\n"
                        f"[justificativa breve com base no que foi descrito]\n\n"
                        f"💬 COMO ESSA PESSOA PROVAVELMENTE PREFERE SE COMUNICAR:\n[estilo de linguagem, ritmo, profundidade]\n\n"
                        f"✅ O QUE FUNCIONA BEM COM ESSE PERFIL:\n[abordagens que tendem a criar conexão]\n\n"
                        f"❌ O QUE EVITAR COM ESSE PERFIL:\n[abordagens que tendem a afastar esse tipo de pessoa]\n\n"
                        f"💡 DICA ESPECÍFICA PARA SUA SITUAÇÃO:\n[1 sugestão prática e imediata]"
                    )
                    res = magnetismo_ia(prompt)
                    salvar_consulta("PerfilPessoa", descricao_perfil[:60], res)
                    st.session_state['perfilp_temp'] = res
            else:
                st.warning("Descreva o jeito da pessoa.")

        if st.session_state.get('perfilp_temp'):
            st.markdown(f"<div class='card-purple'>{st.session_state['perfilp_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['perfilp_temp'], file_name="perfil_pessoa.txt", mime="text/plain", use_container_width=True, key="dl_magnet_4")
            with col_sv:
                if st.button("❤️ Salvar", key="sv_perfilp", use_container_width=True):
                    st.session_state.consultas_salvas.append({'modulo':'PerfilPessoa','tema':descricao_perfil[:60] if 'descricao_perfil' in dir() else '','conteudo':st.session_state['perfilp_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

        # ========================
        # LEITURA DE INTERESSE
        # ========================

    with _tab_Leitura:
        st.header("🎯 Leitura de Interesse")
        st.markdown(DISCLAIMER_LEITURA, unsafe_allow_html=True)

        sinais_leitura = st.text_area("📝 Descreva os sinais/comportamentos que você notou:", height=180,
            placeholder="ex: Ela responde rápido às minhas mensagens, mas as respostas são curtas. Ontem ela curtiu meu story...", key="magnetis5_d2")

        if st.button("🎯 ANALISAR SINAIS", key="magnetis8"):
            if sinais_leitura.strip():
                with st.spinner("Analisando os sinais..."):
                    prompt = (
                        f"Analise estes sinais com cautela, sem tirar conclusões definitivas.\n"
                        f"Sinais: {sinais_leitura}\n\n"
                        f"FORMATO:\n\n"
                        f"🎯 ANÁLISE DE SINAIS\n\n"
                        f"✅ SINAIS QUE PODEM INDICAR INTERESSE:\n[liste, sempre com 'pode indicar', nunca 'significa']\n\n"
                        f"⚠️ SINAIS QUE PODEM INDICAR NEUTRALIDADE OU DESINTERESSE:\n[liste com a mesma cautela]\n\n"
                        f"🔄 SINAIS AMBÍGUOS (podem significar várias coisas):\n[explique a ambiguidade]\n\n"
                        f"🧩 LEITURA GERAL (hipótese, não certeza):\n[síntese honesta — incluindo se a leitura geral for inconclusiva]\n\n"
                        f"💡 O QUE FAZER COM ESSA INCERTEZA:\n[sugestão prática — geralmente: agir de forma autêntica e, se possível, perguntar ou observar mais diretamente em vez de só analisar à distância]"
                    )
                    res = magnetismo_ia(prompt)
                    salvar_consulta("Leitura", sinais_leitura[:60], res)
                    st.session_state['leitura_temp'] = res
            else:
                st.warning("Descreva os sinais.")

        if st.session_state.get('leitura_temp'):
            st.markdown(f"<div class='card-blue'>{st.session_state['leitura_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['leitura_temp'], file_name="leitura_interesse.txt", mime="text/plain", use_container_width=True, key="dl_magnet_5")
            with col_sv:
                if st.button("❤️ Salvar", key="sv_leitura", use_container_width=True):
                    st.session_state.consultas_salvas.append({'modulo':'Leitura','tema':sinais_leitura[:60] if 'sinais_leitura' in dir() else '','conteudo':st.session_state['leitura_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

        # ========================
        # MELHOR RESPOSTA
        # ========================

    with _tab_Resposta:
        st.header("💬 Melhor Resposta")
        st.markdown("Cole a conversa e receba opções de resposta em diferentes tons.")

        conversa_resp = st.text_area("📝 Cole a conversa (ou a última mensagem que você recebeu):", height=150,
            placeholder="ex: Ela disse: 'kkkk hoje foi um dia bem cansativo, trabalhei até tarde'...", key="magnetis4_d2")

        if st.button("💬 GERAR OPÇÕES DE RESPOSTA", key="magnetis9"):
            if conversa_resp.strip():
                with st.spinner("Criando opções..."):
                    prompt = (
                        f"Crie 5 opções de resposta para esta conversa, em tons diferentes.\n"
                        f"Conversa: {conversa_resp}\n\n"
                        f"FORMATO:\n\n"
                        f"💬 OPÇÕES DE RESPOSTA\n\n"
                        f"😌 LEVE:\n[resposta casual e tranquila]\n\n"
                        f"😄 DIVERTIDA:\n[resposta com humor genuíno, não forçado]\n\n"
                        f"🎩 ELEGANTE:\n[resposta mais cuidada e gentil]\n\n"
                        f"🎯 DIRETA:\n[resposta clara e objetiva]\n\n"
                        f"🌙 MISTERIOSA:\n[resposta que gera curiosidade sem ser evasiva ou fria]\n\n"
                        f"💡 QUAL ESCOLHER:\n[1 linha sugerindo qual opção combina melhor com o tom da conversa, mas deixando a decisão para o usuário]"
                    )
                    res = magnetismo_ia(prompt)
                    salvar_consulta("Resposta", conversa_resp[:60], res)
                    st.session_state['resp_temp'] = res
            else:
                st.warning("Cole a conversa.")

        if st.session_state.get('resp_temp'):
            st.markdown(f"<div class='card'>{st.session_state['resp_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['resp_temp'], file_name="opcoes_resposta.txt", mime="text/plain", use_container_width=True, key="dl_magnet_6")
            with col_sv:
                if st.button("❤️ Salvar", key="sv_resp", use_container_width=True):
                    st.session_state.consultas_salvas.append({'modulo':'Resposta','tema':conversa_resp[:60] if 'conversa_resp' in dir() else '','conteudo':st.session_state['resp_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

        # ========================
        # ASSUNTOS INFINITOS
        # ========================

    with _tab_Assuntos:
        st.header("🧩 Assuntos Infinitos")
        st.markdown("Nunca mais fique sem assunto.")

        col1, col2 = st.columns(2)
        with col1:
            idade_assunto = st.text_input("Idade aproximada da pessoa:", placeholder="ex: 28 anos", key="magnetis10")
            profissao_assunto = st.text_input("Profissão (opcional):", placeholder="ex: designer, médica, estudante...", key="magnetis11")
        with col2:
            hobbies_assunto = st.text_input("Hobbies/interesses conhecidos:", placeholder="ex: viagens, séries, esportes...", key="magnetis12")
            contexto_assunto = st.text_input("Contexto da relação:", placeholder="ex: colega de trabalho, conhecemos há pouco...", key="magnetis13")

        if st.button("🧩 GERAR TEMAS DE CONVERSA", key="magnetis14"):
            with st.spinner("Gerando temas..."):
                prompt = (
                    f"Gere temas de conversa interessantes para esta pessoa.\n"
                    f"Idade: {idade_assunto or 'não informada'}. Profissão: {profissao_assunto or 'não informada'}.\n"
                    f"Hobbies: {hobbies_assunto or 'não informados'}. Contexto: {contexto_assunto or 'não informado'}\n\n"
                    f"FORMATO:\n\n"
                    f"🧩 TEMAS DE CONVERSA SUGERIDOS\n\n"
                    f"🎯 TEMAS DIRETAMENTE LIGADOS AOS INTERESSES DELA:\n[5 temas específicos, com 1 pergunta de abertura para cada]\n\n"
                    f"🌍 TEMAS UNIVERSAIS QUE GERAM BOA CONVERSA:\n[3 temas que funcionam quase sempre, com pergunta de abertura]\n\n"
                    f"💡 PERGUNTAS QUE APROFUNDAM (não só perguntas de superfície):\n[2-3 perguntas que vão além do raso]\n\n"
                    f"⚠️ TEMAS A EVITAR NESSE CONTEXTO:\n[se aplicável, algo a não tocar ainda]"
                )
                res = magnetismo_ia(prompt)
                salvar_consulta("Assuntos", f"{profissao_assunto} {hobbies_assunto}", res)
                st.session_state['assunto_temp'] = res

        if st.session_state.get('assunto_temp'):
            st.markdown(f"<div class='card-teal'>{st.session_state['assunto_temp']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar (.txt)", data=st.session_state['assunto_temp'], file_name="assuntos.txt", mime="text/plain", key="dl_magnet_7")

        # ========================
        # SIMULADOR DE CONVERSA
        # ========================

    with _tab_Simulador:
        st.header("🎭 Simulador de Conversa")
        st.markdown("Treine a conversa antes de mandar a mensagem real.")

        if 'chat_simulador' not in st.session_state:
            st.session_state.chat_simulador = []
        if 'simulador_key' not in st.session_state:
            st.session_state.simulador_key = 0
        if 'simulador_perfil' not in st.session_state:
            st.session_state.simulador_perfil = ""

        if not st.session_state.chat_simulador:
            st.markdown("#### Configure quem a IA vai interpretar:")
            perfil_sim = st.text_area("Descreva o perfil/personalidade da pessoa a ser simulada:", height=100,
                placeholder="ex: Uma pessoa extrovertida, bem-humorada, que gosta de viagens e responde com humor...", key="magnetis3_d2")
            if st.button("🎭 INICIAR SIMULAÇÃO", key="magnetis15"):
                if perfil_sim.strip():
                    st.session_state.simulador_perfil = perfil_sim
                    st.rerun()
                else:
                    st.warning("Descreva o perfil a ser simulado.")
        else:
            st.markdown(f"<div class='disclaimer'>🎭 Simulando: {st.session_state.simulador_perfil[:100]}</div>", unsafe_allow_html=True)
            for msg in st.session_state.chat_simulador:
                if msg['role'] == 'user':
                    st.markdown(f"<div style='background:#FDF2F8;border:1px solid #BE185D;border-radius:12px 12px 4px 12px;padding:12px 16px;margin:8px 0;'><b>Você:</b> {msg['content']}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='card-dark' style='margin:8px 0;'><b>🎭 Simulação:</b><br>{msg['content']}</div>", unsafe_allow_html=True)

            mensagem_sim = st.text_input("Sua mensagem:", key=f"sim_input_{st.session_state.simulador_key}")
            col_env, col_limpar = st.columns([3,1])
            with col_env:
                if st.button("📤 ENVIAR", key="magnetis16"):
                    if mensagem_sim.strip():
                        with st.spinner("..."):
                            resp = magnetismo_ia(
                                mensagem_sim,
                                f"MODO SIMULAÇÃO: Interprete uma pessoa fictícia com este perfil: {st.session_state.simulador_perfil}. "
                                f"Responda como essa pessoa responderia nesta conversa, de forma realista e consistente com o perfil. "
                                f"NÃO saia do personagem, não dê conselhos meta sobre a conversa — apenas responda como a pessoa simulada responderia."
                            )
                        st.session_state.chat_simulador.append({"role": "user", "content": mensagem_sim})
                        st.session_state.chat_simulador.append({"role": "assistant", "content": resp})
                        st.session_state.simulador_key += 1
                        st.rerun()
            with col_limpar:
                if st.button("🔄 Nova simulação", key="magnetis17"):
                    st.session_state.chat_simulador = []
                    st.session_state.simulador_perfil = ""
                    st.rerun()

            if st.session_state.chat_simulador and st.button("📈 Analisar esta simulação", key="magnetis18"):
                with st.spinner("Analisando..."):
                    historico_sim = "\n".join([f"{'Você' if m['role']=='user' else 'Simulação'}: {m['content']}" for m in st.session_state.chat_simulador])
                    prompt = (
                        f"Analise esta conversa simulada de treino.\n"
                        f"Conversa: {historico_sim}\n\n"
                        f"FORMATO:\n\n"
                        f"📈 ANÁLISE DA SIMULAÇÃO\n\n"
                        f"✅ PONTOS FORTES:\n[o que funcionou bem na sua abordagem]\n\n"
                        f"⚠️ PONTOS A MELHORAR:\n[onde poderia ser mais natural ou eficaz]\n\n"
                        f"💡 SUGESTÃO PARA A CONVERSA REAL:\n[1-2 ajustes práticos para quando for conversar de verdade]"
                    )
                    res = magnetismo_ia(prompt)
                    salvar_consulta("Simulador", "Simulação de conversa", res)
                    st.session_state['sim_analise_temp'] = res

            if st.session_state.get('sim_analise_temp'):
                st.markdown(f"<div class='card-green'>{st.session_state['sim_analise_temp']}</div>", unsafe_allow_html=True)

        # ========================
        # ANÁLISE DA CONVERSA
        # ========================

    with _tab_Analise:
        st.header("📈 Análise da Conversa")
        st.markdown(DISCLAIMER_LEITURA, unsafe_allow_html=True)

        conversa_analise = st.text_area("📝 Cole a conversa completa que você quer analisar:", height=200,
            placeholder="Cole aqui a conversa, identificando quem disse cada parte...", key="magnetis2")

        if st.button("📈 ANALISAR CONVERSA", key="magnetis19"):
            if conversa_analise.strip():
                with st.spinner("Analisando..."):
                    prompt = (
                        f"Analise esta conversa identificando dinâmica de conexão.\n"
                        f"Conversa: {conversa_analise}\n\n"
                        f"FORMATO:\n\n"
                        f"📈 ANÁLISE DA CONVERSA\n\n"
                        f"✅ ONDE HOUVE CONEXÃO:\n[momentos que pareceram fluir bem]\n\n"
                        f"⚠️ ONDE HOUVE EXCESSO:\n[se algo pareceu insistente, longo demais, ou desequilibrado]\n\n"
                        f"📊 ONDE PODERIA MELHORAR:\n[oportunidades perdidas ou abordagens que poderiam ser mais eficazes]\n\n"
                        f"⭐ PONTOS FORTES DA SUA COMUNICAÇÃO:\n[o que você já faz bem]\n\n"
                        f"💡 PRÓXIMO PASSO SUGERIDO:\n[1 sugestão prática para a continuidade]"
                    )
                    res = magnetismo_ia(prompt)
                    salvar_consulta("Analise", conversa_analise[:60], res)
                    st.session_state['analise_temp'] = res
            else:
                st.warning("Cole a conversa.")

        if st.session_state.get('analise_temp'):
            st.markdown(f"<div class='card-purple'>{st.session_state['analise_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['analise_temp'], file_name="analise_conversa.txt", mime="text/plain", use_container_width=True, key="dl_magnet_10")
            with col_sv:
                if st.button("❤️ Salvar", key="sv_analise", use_container_width=True):
                    st.session_state.consultas_salvas.append({'modulo':'Analise','tema':conversa_analise[:60] if 'conversa_analise' in dir() else '','conteudo':st.session_state['analise_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

        # ========================
        # SINAIS DE ATENÇÃO
        # ========================

    with _tab_Alerta:
        st.header("🚩 Sinais de Atenção")
        st.markdown("Identifica padrões que merecem atenção — para relações mais saudáveis.")

        comportamento_alerta = st.text_area("📝 Descreva o comportamento que está te preocupando:", height=180,
            placeholder="ex: Ele fica bravo quando eu saio com amigas, sempre quer saber onde estou, e diz que se eu não respondo rápido é porque não me importo...", key="magnetis1")

        if st.button("🚩 ANALISAR", key="magnetis20"):
            if comportamento_alerta.strip():
                with st.spinner("Analisando com cuidado..."):
                    prompt = (
                        f"Analise este comportamento com seriedade, identificando padrões de atenção.\n"
                        f"Comportamento: {comportamento_alerta}\n\n"
                        f"FORMATO:\n\n"
                        f"🚩 ANÁLISE DE SINAIS\n\n"
                        f"📊 PADRÕES IDENTIFICADOS:\n[nomeie claramente os padrões — desinteresse, falta de reciprocidade, controle, "
                        f"ciúme excessivo, desrespeito a limites, etc — o que se aplicar com base na descrição]\n\n"
                        f"⚠️ NÍVEL DE ATENÇÃO RECOMENDADO: [Baixo / Moderado / Alto]\n"
                        f"[se houver sinais de controle, isolamento ou desrespeito a recusas, seja direto sobre a gravidade]\n\n"
                        f"💭 ISSO PODE SER NORMAL OU PASSAGEIRO SE:\n[contextos onde o comportamento descrito teria explicação benigna]\n\n"
                        f"🚨 ISSO MERECE MAIS ATENÇÃO SE:\n[sinais de que o padrão é estrutural e não um caso isolado]\n\n"
                        f"💡 O QUE FAZER:\n[passos práticos e saudáveis — conversar diretamente, estabelecer limites, buscar apoio de "
                        f"amigos/família, ou buscar ajuda profissional se a situação envolver controle ou desrespeito sério]"
                    )
                    res = magnetismo_ia(prompt, "Trate isso com seriedade real. Não minimize padrões de controle ou desrespeito, mas também não diagnostique a outra pessoa — fale em termos de padrões e o que fazer.")
                    salvar_caso_nome = "Alerta"
                    salvar_consulta("Alerta", comportamento_alerta[:60], res)
                    st.session_state['alerta_temp'] = res
            else:
                st.warning("Descreva o comportamento.")

        if st.session_state.get('alerta_temp'):
            st.markdown(f"<div class='card-red'>{st.session_state['alerta_temp']}</div>", unsafe_allow_html=True)
            st.markdown("""<div class="disclaimer-alerta">
            🚨 Se você se sente em risco ou inseguro(a) em uma relação, busque apoio: Central de Atendimento à Mulher
            (Disque 180), conversa com pessoas de confiança, ou um profissional de saúde mental. Você não está sozinho(a).
            </div>""", unsafe_allow_html=True)
            st.download_button("📋 Baixar (.txt)", data=st.session_state['alerta_temp'], file_name="sinais_atencao.txt", mime="text/plain", key="dl_magnet_11")

        # ========================
        # PSICOLOGIA DA ATRAÇÃO
        # ========================

    with _tab_Psicologia:
        st.header("🧠 Psicologia da Atração")

        conceito_psico = st.selectbox("Conceito:", [
            "Reciprocidade", "Escuta ativa", "Autenticidade", "Linguagem corporal",
            "Efeito da primeira impressão", "Influência do contexto", "Vulnerabilidade e conexão",
            "Validação social", "Princípio da familiaridade",
        ], key="select_conceito_psico")

        if st.button("🧠 EXPLICAR", key="magnetis21"):
            with st.spinner("Preparando explicação..."):
                prompt = (
                    f"Explique de forma profunda e prática: {conceito_psico}, no contexto de conexão humana e atração interpessoal.\n\n"
                    f"FORMATO:\n\n"
                    f"🧠 {conceito_psico.upper()}\n\n"
                    f"📖 O QUE É:\n[explicação clara do conceito psicológico]\n\n"
                    f"🔬 POR QUE FUNCIONA:\n[a base psicológica/comportamental por trás]\n\n"
                    f"💬 EXEMPLO PRÁTICO:\n[situação concreta mostrando o conceito em ação]\n\n"
                    f"✅ COMO APLICAR DE FORMA AUTÊNTICA:\n[como usar isso sem parecer manipulador ou ensaiado]\n\n"
                    f"❌ COMO ISSO É USADO DE FORMA MANIPULADORA (para você reconhecer):\n[o lado sombrio do conceito quando usado contra alguém, para que você também saiba identificar quando está sendo feito com você]"
                )
                res = magnetismo_ia(prompt)
                salvar_consulta("Psicologia", conceito_psico, res)
                st.session_state['psico_temp'] = res

        if st.session_state.get('psico_temp'):
            st.markdown(f"<div class='card-blue'>{st.session_state['psico_temp']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar (.txt)", data=st.session_state['psico_temp'], file_name="psicologia_atracao.txt", mime="text/plain", key="dl_magnet_13")

        # ========================
        # ACADEMIA SOCIAL
        # ========================

    with _tab_Academia:
        st.header("🎓 Academia Social")
        st.markdown("Minicurso de comunicação, confiança e carisma.")

        aulas_social = [
            "Como gerar confiança", "Como ser mais interessante", "Como manter conversas fluindo",
            "Como perder o medo de conversar", "Como fazer perguntas que aprofundam o diálogo",
            "Como lidar com rejeição de forma saudável", "Como desenvolver carisma",
            "Como ler o ambiente social", "Como se recuperar de um silêncio constrangedor",
            "Como equilibrar fazer perguntas e falar de si",
        ]
        aula_social_escolhida = st.selectbox("Escolha a aula:", aulas_social, key="select_aula_social")

        if st.button("🎓 INICIAR AULA", key="magnetis22"):
            with st.spinner("Preparando uma aula rica em conteúdo..."):
                prompt = (
                    f"Crie uma aula completa e aprofundada para a Academia Social sobre: {aula_social_escolhida}\n\n"
                    f"EXIGÊNCIAS: nada de clichês vazios — cada ponto deve ter exemplo concreto e aplicável. "
                    f"Mostre o raciocínio e o mecanismo, não apenas a conclusão.\n\n"
                    f"FORMATO:\n\n"
                    f"🎓 {aula_social_escolhida.upper()}\n\n"
                    f"📖 POR QUE ISSO IMPORTA:\n[conexão real com situações do dia a dia]\n\n"
                    f"💡 OS PRINCÍPIOS FUNDAMENTAIS:\n[2-4 princípios centrais, cada um explicado com exemplo]\n\n"
                    f"🎬 EXEMPLO PRÁTICO NARRADO:\n[uma situação detalhada mostrando o princípio em ação, com diálogo de exemplo]\n\n"
                    f"⚙️ COMO APLICAR PASSO A PASSO:\n[instruções concretas e replicáveis]\n\n"
                    f"⚠️ ERROS COMUNS:\n[o que as pessoas fazem errado tentando aplicar isso]\n\n"
                    f"🏋️ EXERCÍCIO PARA PRATICAR:\n[1 exercício real para aplicar essa semana]"
                )
                res = magnetismo_ia(prompt, "Escreva com profundidade real — a pessoa que está lendo é inteligente e vai notar superficialidade.")
                salvar_consulta("Academia", aula_social_escolhida, res)
                st.session_state['aula_social_temp'] = res

        if st.session_state.get('aula_social_temp'):
            st.markdown(f"<div class='card'>{st.session_state['aula_social_temp']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar aula (.txt)", data=st.session_state['aula_social_temp'], file_name="aula_academia_social.txt", mime="text/plain", key="dl_magnet_16")

        # ========================
        # MENTOR 24H
        # ========================

    with _tab_Mentor:
        st.header("🤖 Mentor 24h")
        st.markdown("Converse livremente sobre qualquer situação social.")

        if 'chat_mentor' not in st.session_state:
            st.session_state.chat_mentor = []
        if 'mentor_key' not in st.session_state:
            st.session_state.mentor_key = 0

        if st.session_state.chat_mentor:
            for msg in st.session_state.chat_mentor:
                if msg['role'] == 'user':
                    st.markdown(f"<div style='background:#FDF2F8;border:1px solid #BE185D;border-radius:12px 12px 4px 12px;padding:12px 16px;margin:8px 0;'><b>Você:</b> {msg['content']}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='card-dark' style='margin:8px 0;'><b>🧲 Mentor:</b><br>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown("""<div style="background:#FDF2F8;border:1px dashed #BE185D;border-radius:12px;padding:16px;text-align:center;">
            🤖 <strong>Pergunte qualquer coisa!</strong> Ex: "Como eu poderia ter respondido melhor nessa situação?",
            "Como recuperar uma conversa que ficou estranha?"
            </div>""", unsafe_allow_html=True)

        pergunta_mentor = st.text_input("Sua pergunta:", key=f"mentor_input_{st.session_state.mentor_key}", placeholder="Conte a situação...")

        col_env, col_limpar = st.columns([3, 1])
        with col_env:
            if st.button("📤 PERGUNTAR", key="magnetis23"):
                if pergunta_mentor.strip():
                    with st.spinner("Pensando..."):
                        resp = magnetismo_ia(pergunta_mentor, "Responda como um mentor caloroso e experiente em conexão humana, direto e prático.")
                    st.session_state.chat_mentor.append({"role": "user", "content": pergunta_mentor})
                    st.session_state.chat_mentor.append({"role": "assistant", "content": resp})
                    st.session_state.mentor_key += 1
                    salvar_consulta("Mentor", pergunta_mentor[:60], resp)
                    st.rerun()
                else:
                    st.warning("Digite sua pergunta.")
        with col_limpar:
            if st.button("🗑️ Limpar", key="magnetis24"):
                st.session_state.chat_mentor = []
                st.rerun()

        # ========================
        # BIBLIOTECA
        # ========================

# --- RODAPÉ ---
st.markdown(
    "<div style='text-align:center;color:#999;font-size:0.8em;margin-top:60px;'>"
    "© 2026 Magnetismo Social — Estrategista de Comunicação com IA · Quiz Com Prêmios"
    "</div>", unsafe_allow_html=True
)
