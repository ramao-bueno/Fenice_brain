# Avisa Api Integration - Design Specification

**Data**: 2026-06-09  
**Status**: Em Design (aguardando aprovação)  
**Objetivo**: Substituir integração Botpress por Avisa Api com arquitetura extensível  

---

## 1. Visão Geral

Refatorar o sistema atual para usar um **padrão Provider/Plugin** que desacopla a lógica de processamento de mensagens do provedor específico (Botpress, Avisa, etc). Isso permite:

- ✅ Migrar de Botpress → Avisa mantendo código limpo
- ✅ Suportar múltiplos canais no futuro sem duplicação
- ✅ Testar Avisa em paralelo com Botpress
- ✅ Reutilizar lógica de negócio (criação de clientes, casos, respostas com Claude)

---

## 2. Arquitetura Geral

### 2.1 Estrutura de Pastas

```
backend-python/src/
├── providers/                          # ← NOVO: abstração de provedores
│   ├── __init__.py
│   ├── base.py                         # Interface abstrata (BaseMessageProvider)
│   ├── botpress_provider.py            # Implementação Botpress (existente, refatorada)
│   └── avisa_provider.py               # Implementação Avisa (NOVO)
├── services/
│   ├── message_service.py              # ← NOVO: orquestra mensagens (agnóstico de provider)
│   ├── botpress_service.py             # Manter por enquanto (deprecar depois)
│   ├── document_service.py
│   ├── email_service.py
│   └── __init__.py
├── routes/
│   ├── webhooks.py                     # ← NOVO: rota genérica /webhook/{provider}
│   ├── botpress.py                     # Manter para compatibilidade
│   ├── documents.py
│   └── __init__.py
├── models/
│   ├── client.py
│   ├── case.py                         # Adicionar campo avisa_case_id
│   ├── interaction.py
│   ├── document.py
│   └── __init__.py
├── integrations/
│   ├── claude_ai.py
│   ├── email_provider.py
│   └── __init__.py
├── schemas/
│   ├── botpress_schemas.py
│   ├── provider_schemas.py             # ← NOVO: ProviderMessage e schemas neutros
│   └── __init__.py
├── config.py                           # Adicionar AVISA_API_TOKEN, AVISA_API_URL
├── database.py
└── main.py
```

### 2.2 Fluxo de Requisição

```
Avisa Api webhook → /webhook/avisa
    ↓
Route Handler identifica provider = "avisa"
    ↓
Instancia AvisaProvider(token)
    ↓
provider.parse_webhook(payload) → ProviderMessage neutro
    ↓
MessageService.process_message(message, provider)
    ├── Get/create Client
    ├── Enrich client com dados de Avisa
    ├── Detect request type
    ├── Auto-create Case
    ├── Sync case para Avisa
    ├── Generate response com Claude
    └── Log interaction
    ↓
provider.send_response(conversation_id, response_text)
    ↓
HTTP 200 OK com resultado
```

---

## 3. Padrão Provider - Interface Abstrata

### 3.1 ProviderMessage (formato neutro)

```python
# src/schemas/provider_schemas.py

from pydantic import BaseModel
from typing import Optional, Dict, Any

class ProviderMessage(BaseModel):
    """Formato neutro de mensagem (independente de provider)"""
    conversation_id: str
    user_id: str
    user_name: str
    user_email: Optional[str] = None
    text: str
    timestamp: str
    metadata: Dict[str, Any] = {}  # Provider-specific data
```

### 3.2 BaseMessageProvider (interface)

```python
# src/providers/base.py

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from src.schemas.provider_schemas import ProviderMessage
from src.models.case import Case

class BaseMessageProvider(ABC):
    """Interface que todo provider deve implementar"""
    
    @abstractmethod
    async def parse_webhook(self, payload: dict) -> ProviderMessage:
        """Converter payload do webhook → ProviderMessage neutro"""
        pass
    
    @abstractmethod
    async def send_response(self, conversation_id: str, response_text: str) -> bool:
        """Enviar resposta de volta para o usuário via provider"""
        pass
    
    @abstractmethod
    async def get_client_info(self, user_id: str) -> Dict[str, Any]:
        """Buscar dados do cliente da API do provider"""
        pass
    
    @abstractmethod
    async def create_case_in_provider(self, case: Case) -> bool:
        """Criar caso/ticket no provider para sincronização"""
        pass
```

---

## 4. Implementações Específicas

### 4.1 BotpressProvider

```python
# src/providers/botpress_provider.py

from src.providers.base import BaseMessageProvider
from src.schemas.provider_schemas import ProviderMessage
from src.models.case import Case
from typing import Optional, Dict, Any

class BotpressProvider(BaseMessageProvider):
    
    async def parse_webhook(self, payload: dict) -> ProviderMessage:
        """Converte webhook Botpress → ProviderMessage"""
        event = payload.get("events", [{}])[0]
        data = event.get("data", {})
        profile = data.get("userProfile", {})
        
        return ProviderMessage(
            conversation_id=data.get("conversationId"),
            user_id=data.get("userId"),
            user_name=profile.get("name", "Unknown"),
            user_email=profile.get("email"),
            text=data.get("text"),
            timestamp=data.get("timestamp"),
            metadata={"botpress_message_id": data.get("messageId")}
        )
    
    async def send_response(self, conversation_id: str, response_text: str) -> bool:
        """Enviar resposta de volta ao Botpress"""
        # Implementação específica do Botpress
        # Por enquanto, apenas retorna True (Botpress não requer resposta HTTP)
        return True
    
    async def get_client_info(self, user_id: str) -> Dict[str, Any]:
        """Botpress não oferece API para buscar info do cliente"""
        return {}
    
    async def create_case_in_provider(self, case: Case) -> bool:
        """Botpress não oferece API para criar casos"""
        return True  # Não faz nada, mas não falha
```

### 4.2 AvisaProvider

```python
# src/providers/avisa_provider.py

import httpx
from src.providers.base import BaseMessageProvider
from src.schemas.provider_schemas import ProviderMessage
from src.models.case import Case
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class AvisaProvider(BaseMessageProvider):
    
    def __init__(self, api_token: str, api_url: str = "https://api.avisa.com.br/v1"):
        self.api_token = api_token
        self.api_url = api_url
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
    
    async def parse_webhook(self, payload: dict) -> ProviderMessage:
        """Converte webhook Avisa → ProviderMessage"""
        return ProviderMessage(
            conversation_id=payload.get("conversation_id"),
            user_id=payload.get("from_user_id"),
            user_name=payload.get("from_user_name"),
            user_email=payload.get("from_user_email"),
            text=payload.get("message_text"),
            timestamp=payload.get("timestamp"),
            metadata={"avisa_message_id": payload.get("message_id")}
        )
    
    async def send_response(self, conversation_id: str, response_text: str) -> bool:
        """Enviar resposta via API Avisa"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/messages/send",
                    json={
                        "conversation_id": conversation_id,
                        "text": response_text
                    },
                    headers=self.headers,
                    timeout=10
                )
            
            if response.status_code == 200:
                logger.info(f"Response sent to Avisa conversation {conversation_id}")
                return True
            else:
                logger.error(f"Failed to send response: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"Error sending response: {str(e)}")
            return False
    
    async def get_client_info(self, user_id: str) -> Dict[str, Any]:
        """Buscar dados do cliente na API Avisa"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.api_url}/users/{user_id}",
                    headers=self.headers,
                    timeout=10
                )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.warning(f"Could not fetch client info: {response.status_code}")
                return {}
        except Exception as e:
            logger.error(f"Error fetching client info: {str(e)}")
            return {}
    
    async def create_case_in_provider(self, case: Case) -> bool:
        """Criar ticket/issue no Avisa para sincronização"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/cases",
                    json={
                        "title": case.title,
                        "description": case.description,
                        "type": case.case_type.value,
                        "client_id": case.client_id,
                        "external_id": case.id
                    },
                    headers=self.headers,
                    timeout=10
                )
            
            if response.status_code == 201:
                avisa_case_id = response.json().get("id")
                logger.info(f"Case synced to Avisa: {avisa_case_id}")
                # Case.avisa_case_id será salvo em MessageService
                return True
            else:
                logger.error(f"Failed to create case in Avisa: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"Error creating case in Avisa: {str(e)}")
            return False
```

---

## 5. MessageService - Orquestração Agnóstica

```python
# src/services/message_service.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, Dict, Any
import logging

from src.models.client import Client, ClientType
from src.models.case import Case, CaseStatus, CaseType
from src.models.interaction import Interaction, InteractionType
from src.schemas.provider_schemas import ProviderMessage
from src.providers.base import BaseMessageProvider
from src.integrations.claude_ai import ClaudeAIClient

logger = logging.getLogger(__name__)

class MessageService:
    """Serviço agnóstico de processamento de mensagens"""
    
    def __init__(self, db_session: AsyncSession, claude_client: Optional[ClaudeAIClient] = None):
        self.db = db_session
        self.claude = claude_client or ClaudeAIClient()
    
    async def process_message(
        self,
        message: ProviderMessage,
        provider: BaseMessageProvider
    ) -> Dict[str, Any]:
        """Processar mensagem de qualquer provider"""
        try:
            # 1. Get or create client
            client = await self._get_or_create_client(message)
            logger.info(f"Processing message for client: {client.id}")
            
            # 1.5 Enrich client com dados do provider
            provider_data = await provider.get_client_info(message.user_id)
            if provider_data:
                client = await self._enrich_client(client, provider_data)
            
            # 2. Detect request type
            request_type = self._detect_request_type(message.text)
            logger.info(f"Detected request type: {request_type}")
            
            # 3. Auto-create case
            case = None
            if request_type in ["document_request", "legal_opinion", "contract_review"]:
                case = await self._create_case(client.id, request_type, message)
                logger.info(f"Created case: {case.id}")
                
                # 3.5 Sync case para provider
                await provider.create_case_in_provider(case)
            
            # 4. Generate response
            response = await self._generate_response(client, case, message, request_type)
            logger.info(f"Generated response: {len(response)} chars")
            
            # 5. Log interaction
            interaction = await self._log_interaction(
                client.id,
                case.id if case else None,
                message,
                response
            )
            logger.info(f"Logged interaction: {interaction.id}")
            
            return {
                "status": "success",
                "client_id": client.id,
                "case_id": case.id if case else None,
                "interaction_id": interaction.id,
                "conversation_id": message.conversation_id,
                "response": response
            }
        
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}", exc_info=True)
            raise
    
    async def _get_or_create_client(self, message: ProviderMessage) -> Client:
        """Get or create client from message"""
        # Try to find by email
        if message.user_email:
            result = await self.db.execute(
                select(Client).where(Client.email == message.user_email)
            )
            existing = result.scalar_one_or_none()
            if existing:
                return existing
        
        # Create new client
        new_client = Client(
            name=message.user_name,
            email=message.user_email,
            client_type=ClientType.INDIVIDUAL
        )
        
        self.db.add(new_client)
        await self.db.flush()
        await self.db.refresh(new_client)
        
        return new_client
    
    async def _enrich_client(self, client: Client, provider_data: Dict[str, Any]) -> Client:
        """Enrich client com dados do provider (ex: histórico, tags)"""
        # Implementação específica por provider
        # Por enquanto, apenas retorna o client sem mudanças
        return client
    
    def _detect_request_type(self, text: str) -> str:
        """Detectar tipo de requisição (igual ao existente em botpress_service.py)"""
        import re
        
        text_lower = text.lower()
        
        opinion_keywords = [
            r'\bparecer\b', r'\bopinião\b', r'\banálise jurídica\b',
            r'\bconsulta jurídica\b'
        ]
        for keyword in opinion_keywords:
            if re.search(keyword, text_lower):
                return "legal_opinion"
        
        review_keywords = [
            r'\brevisão\b', r'\brevissar\b', r'\brevisar\b',
            r'\bcheck\b'
        ]
        for keyword in review_keywords:
            if re.search(keyword, text_lower):
                return "contract_review"
        
        document_keywords = [
            r'\bcontrato\b', r'\bnda\b', r'\bprestação de serviços\b',
            r'\bdocumento\b', r'\belaborar\b', r'\bgerar\b'
        ]
        for keyword in document_keywords:
            if re.search(keyword, text_lower):
                return "document_request"
        
        return "consultation"
    
    async def _create_case(
        self,
        client_id: int,
        request_type: str,
        message: ProviderMessage
    ) -> Case:
        """Create case for document/legal requests"""
        case_type_map = {
            "document_request": CaseType.DOCUMENT_REQUEST,
            "legal_opinion": CaseType.CONSULTATION,
            "contract_review": CaseType.CONTRACT_REVIEW,
            "consultation": CaseType.LEGAL_ISSUE
        }
        
        case_type = case_type_map.get(request_type, CaseType.OTHER)
        title = message.text[:100] if len(message.text) > 100 else message.text
        
        case = Case(
            client_id=client_id,
            title=title,
            description=message.text,
            case_type=case_type,
            status=CaseStatus.OPEN
        )
        
        self.db.add(case)
        await self.db.flush()
        await self.db.refresh(case)
        
        return case
    
    async def _generate_response(
        self,
        client: Client,
        case: Optional[Case],
        message: ProviderMessage,
        request_type: str
    ) -> str:
        """Generate response using Claude"""
        system_prompt = self._build_system_prompt(request_type, client)
        user_message = self._build_user_message(message, request_type, case)
        
        response = self.claude.generate_text(
            system_prompt=system_prompt,
            user_message=user_message,
            max_tokens=1024,
            temperature=0.7
        )
        
        return response
    
    def _build_system_prompt(self, request_type: str, client: Client) -> str:
        """Build system prompt for Claude"""
        base = f"""You are a helpful legal assistant for {client.name}.
Professional, empathetic, knowledgeable about Brazilian law.
Always respond in Portuguese (Brazilian Portuguese).
Keep responses concise but informative."""
        
        type_specific = {
            "document_request": "Confirm document type, ask clarifying questions, explain we'll prepare a draft.",
            "legal_opinion": "Acknowledge issue, provide guidance, ask clarifying questions.",
            "contract_review": "Ask them to describe or upload contract, explain what we review.",
            "consultation": "Answer clearly, provide relevant info, suggest consulting a lawyer."
        }
        
        return base + "\n\n" + type_specific.get(request_type, "")
    
    def _build_user_message(
        self,
        message: ProviderMessage,
        request_type: str,
        case: Optional[Case]
    ) -> str:
        """Build user message context for Claude"""
        case_context = f"\n[Case ID: {case.id}, Type: {case.case_type.value}]" if case else ""
        return f"Client Message: {message.text}{case_context}\n\nPlease respond to the client's request."
    
    async def _log_interaction(
        self,
        client_id: int,
        case_id: Optional[int],
        message: ProviderMessage,
        response: str
    ) -> Interaction:
        """Log interaction to database"""
        client_interaction = Interaction(
            client_id=client_id,
            case_id=case_id,
            interaction_type=InteractionType.BOTPRESS_MESSAGE,
            message=message.text,
            botpress_conversation_id=message.conversation_id,
            is_from_client=True
        )
        
        self.db.add(client_interaction)
        await self.db.flush()
        
        bot_interaction = Interaction(
            client_id=client_id,
            case_id=case_id,
            interaction_type=InteractionType.BOTPRESS_MESSAGE,
            message=response,
            botpress_conversation_id=message.conversation_id,
            is_from_client=False
        )
        
        self.db.add(bot_interaction)
        await self.db.flush()
        await self.db.refresh(client_interaction)
        
        return client_interaction
```

---

## 6. Routes - Handler Genérico

```python
# src/routes/webhooks.py

from fastapi import APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import settings
from src.providers.avisa_provider import AvisaProvider
from src.providers.botpress_provider import BotpressProvider
from src.services.message_service import MessageService
from src.integrations.claude_ai import ClaudeAIClient

router = APIRouter()

@router.post("/webhook/{provider}")
async def handle_webhook(provider: str, payload: dict, db: AsyncSession):
    """Rota genérica para qualquer provider"""
    
    # Mapear providers disponíveis
    providers_map = {
        "avisa": lambda: AvisaProvider(
            api_token=settings.avisa_api_token,
            api_url=settings.avisa_api_url
        ),
        "botpress": lambda: BotpressProvider()
    }
    
    if provider not in providers_map:
        raise HTTPException(status_code=400, detail=f"Unknown provider: {provider}")
    
    # Instanciar provider
    provider_instance = providers_map[provider]()
    
    # Parse mensagem
    message = await provider_instance.parse_webhook(payload)
    
    # Processar com MessageService
    message_service = MessageService(db, ClaudeAIClient())
    result = await message_service.process_message(message, provider_instance)
    
    # Enviar resposta
    await provider_instance.send_response(
        result["conversation_id"],
        result["response"]
    )
    
    return result
```

---

## 7. Configuração e Variáveis de Ambiente

### 7.1 .env

```bash
# Database
DATABASE_URL=postgresql://user:pass@host:5432/legaltech

# Claude API
ANTHROPIC_API_KEY=sk-ant-xxxxx

# Email
SENDGRID_API_KEY=SG.xxxxx
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=seu-email@gmail.com
SMTP_PASSWORD=sua-senha

# Botpress (legacy)
BOTPRESS_WEBHOOK_SECRET=xxxxx

# Avisa Api (NEW)
AVISA_API_TOKEN=<definido em .env — não commitar o valor real>
AVISA_API_URL=https://api.avisa.com.br/v1

# Server
ENVIRONMENT=production
DEBUG=False
```

### 7.2 config.py

```python
from pydantic_settings import BaseSettings
from typing import Literal

class Settings(BaseSettings):
    # Database
    database_url: str
    
    # Claude
    anthropic_api_key: str
    
    # Email
    sendgrid_api_key: str | None = None
    sendgrid_from_address: str | None = "noreply@legaltech.com"
    smtp_host: str | None = None
    smtp_port: int = 587
    smtp_user: str | None = None
    smtp_password: str | None = None
    
    # Botpress (legacy)
    botpress_webhook_secret: str | None = None
    
    # Avisa Api (NEW)
    avisa_api_token: str
    avisa_api_url: str = "https://api.avisa.com.br/v1"
    
    # Server
    environment: Literal["development", "staging", "production"] = "development"
    debug: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
```

---

## 8. Alterações no Modelo

### 8.1 case.py - Adicionar campo Avisa

```python
# src/models/case.py

from datetime import datetime
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

class Case(Base):
    __tablename__ = "cases"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"))
    title: Mapped[str]
    description: Mapped[str]
    case_type: Mapped[CaseType]
    status: Mapped[CaseStatus]
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
    
    # NEW: Track externo para Avisa
    avisa_case_id: Mapped[int | None] = None
    last_synced_at: Mapped[datetime | None] = None
```

---

## 9. Testes e Validação

### 9.1 Teste 1: Health Check

```bash
curl https://fenice.ia.br/health
# Response: {"status":"ok"}
```

### 9.2 Teste 2: Webhook Avisa (simulado)

```bash
curl -X POST https://fenice.ia.br/webhook/avisa \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": "avisa-conv-123",
    "from_user_id": "user-456",
    "from_user_name": "João Silva",
    "from_user_email": "joao@example.com",
    "message_text": "Preciso de um contrato de NDA",
    "timestamp": "2026-06-09T10:00:00Z",
    "message_id": "msg-789"
  }'
```

**Esperado:**
```json
{
  "status": "success",
  "client_id": 1,
  "case_id": 1,
  "interaction_id": 1,
  "conversation_id": "avisa-conv-123",
  "response": "[resposta gerada por Claude]"
}
```

### 9.3 Teste 3: Verificar dados no banco

```sql
SELECT * FROM clients WHERE email = 'joao@example.com';
SELECT * FROM cases WHERE client_id = 1;
SELECT * FROM interactions WHERE client_id = 1 ORDER BY created_at DESC;
```

### 9.4 Teste 4: Validar sincronização com Avisa

```bash
curl -H "Authorization: Bearer $AVISA_API_TOKEN" \
  https://api.avisa.com.br/v1/cases
```

---

## 10. Timeline e Próximos Passos

### Fase 1: Refatoração (2 dias)
- [ ] Criar `providers/base.py` (interface abstrata)
- [ ] Criar `providers/botpress_provider.py` (refatorar existente)
- [ ] Criar `services/message_service.py` (extrair lógica)
- [ ] Criar `routes/webhooks.py` (rota genérica)
- [ ] Atualizar `config.py` com variáveis Avisa
- [ ] Escrever testes unitários

### Fase 2: Implementação Avisa (1 dia)
- [ ] Criar `providers/avisa_provider.py`
- [ ] Testar webhook Avisa em staging
- [ ] Validar sincronização de clientes/casos
- [ ] Testar resposta via API Avisa

### Fase 3: Deploy e Validação (1 dia)
- [ ] Deploy em produção
- [ ] Teste end-to-end com usuários reais
- [ ] Monitorar logs e erros
- [ ] Documentar resolvidos e blockers

### Fase 4: Cleanup (opcional, 1 dia)
- [ ] Remover Botpress quando confiante com Avisa
- [ ] Deprecar botpress_service.py
- [ ] Limpar código legado

---

## 11. Critérios de Sucesso

- ✅ Webhook `/webhook/avisa` recebe e processa mensagens
- ✅ Clientes criados automaticamente com dados de Avisa
- ✅ Casos criados e sincronizados com Avisa
- ✅ Resposta gerada por Claude e enviada via API Avisa
- ✅ Interações logadas no banco
- ✅ Testes passando (unitários + integração)
- ✅ Sem erros em logs de produção

---

## 12. Riscos e Mitigação

| Risco | Impacto | Mitigação |
|-------|---------|-----------|
| API Avisa indisponível | Alto | Manter Botpress como fallback durante transição |
| Payload Avisa diferente do esperado | Alto | Testar em staging antes de produção |
| Token Avisa expirado | Médio | Implementar refresh token ou alert |
| Sincronização quebrada | Médio | Adicionar retry logic e logging |
| Claude API lentidão | Baixo | Cache respostas, usar timeout |

---

## Sumário

Esta especificação descreve uma refatoração arquitetural para suportar múltiplos provedores de mensagens (Avisa, Botpress, etc) usando um padrão Plugin bem definido. O design mantém a lógica de negócio neutra, permitindo testar Avisa em paralelo com Botpress antes de migração completa.

**Webhook do Avisa**: `https://fenice.ia.br/webhook/avisa`  
**Token Avisa**: Armazenado em `.env` como `AVISA_API_TOKEN`  
**Timeline estimado**: 4 dias (refatoração + implementação + validação)
