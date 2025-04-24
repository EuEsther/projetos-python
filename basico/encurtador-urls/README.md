# 🔗 Encurtador de URLs

Um serviço web que transforma URLs longas em links curtos e rastreáveis, com opção de personalização.

## 🔧 Funcionalidades
- Encurtamento de URLs com código aleatório (ex: `http://localhost:5000/XLMp`)
- Customização de slugs (ex: `http://localhost:5000/meu-link`)
- Estatísticas básicas de acesso (contagem de cliques)
- Banco de dados SQLite integrado

## 🛠️ Tecnologias
- **Flask**: Framework web.
- **SQLAlchemy**: ORM para banco de dados.
- **Hashids**: Geração de códigos curtos únicos.
- **Python-dotenv**: Gerenciamento de variáveis de ambiente.

## 🚀 Como Usar

### Pré-requisitos
- Python 3.8 ou superior.
- Git (opcional, para clonar o repositório).

### Passos para Executar

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/seu-usuario/projetos-python.git
   cd projetos-python/basico/encurtador-urls
2. Ative o ambiente virtual:
   ```bash
   source venv/bin/activate  # Linux/Mac
   # OU
   venv\Scripts\activate    # Windows
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
4. Execute o projeto:
   ```bash
   python app.py
5. Acesse: `http://localhost:5000`
