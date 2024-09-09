---

# Chatbot para Agendamento de Relatórios

Este é um chatbot interativo desenvolvido em Python que permite aos usuários agendar relatórios de volumetria em CSV, de acordo com datas e frequências configuradas. Ele também pode notificar os usuários quando os relatórios estiverem prontos e permite o cancelamento de agendamentos.

## Funcionalidades

- **Agendamento de Relatórios**: O chatbot permite que o usuário agende relatórios periódicos fornecendo as datas de início, fim e a frequência desejada (diária, semanal ou mensal).
- **Validação de Datas e Horas**: O chatbot valida automaticamente as entradas de datas e horários para garantir que estejam no formato correto.
- **Suporte a Frequências**: Permite configurar relatórios com frequências diárias, semanais e mensais, com opções detalhadas para horários e dias específicos.
- **Notificações**: Oferece a opção de notificar o usuário quando o relatório estiver pronto.
- **Cancelamento de Agendamentos**: O chatbot pode cancelar um agendamento de relatório baseado no ID fornecido pelo usuário.
- **Mensagens de Ajuda**: Responde a perguntas sobre como usar o sistema e suas funcionalidades.

## Requisitos

- **Python 3.6+**
- Bibliotecas Python necessárias:
  - `nltk`
  - `requests`

### Instalando Dependências

Para instalar as dependências necessárias, use o seguinte comando:

```bash
pip install nltk requests
```

Além disso, você precisará baixar alguns recursos da NLTK (Natural Language Toolkit) para a funcionalidade de tokenização e sinônimos:

```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('rslp')
nltk.download('wordnet')
nltk.download('omw-1.4')
```

## Como Usar

1. **Inicialize o chatbot**: Execute o script principal `chatbot.py` no terminal.
   
   ```bash
   python chatbot.py
   ```

2. **Interaja com o chatbot**:
   - Pergunte sobre **relatórios** para agendar um novo.
   - Defina as **datas de início e término** do relatório.
   - Escolha a **frequência** (diária, semanal ou mensal).
   - Receba notificações quando o relatório estiver pronto.
   - Cancele um agendamento, se necessário.

3. **Saindo**: Digite `sair`, `exit` ou `quit` a qualquer momento para finalizar a conversa.

## Exemplo de Conversa

Usuário: *Gostaria de agendar um relatório*  
Chatbot: *Para agendar um relatório, forneça a data inicial, data final, data do primeiro relatório e a frequência desejada (diária, semanal ou mensal).*  
Usuário: *Data inicial: 01/01/2024*  
Usuário: *Data final: 31/12/2024*  
Usuário: *Primeira data: 01/01/2024*  
Chatbot: *Qual é a frequência desejada? (diária/semanal/mensal)*  
Usuário: *Diária*  
Chatbot: *Você deseja gerar o relatório a cada uma ou a cada duas horas?*  
Usuário: *Uma hora*  
Chatbot: *Agendamento definido: ...*

## Personalização

Este chatbot pode ser facilmente personalizado para outras funcionalidades além de agendamento de relatórios, como análise de dados ou integração com APIs adicionais. O fluxo de conversação também pode ser estendido para novas interações com base nas suas necessidades.

## Contribuindo

Sinta-se à vontade para contribuir com melhorias ou correções de bugs! Crie um **pull request** ou abra uma **issue** para discutirmos suas sugestões.

## Licença

Este projeto está sob a licença MIT. Sinta-se livre para usá-lo e modificá-lo conforme necessário.

---
