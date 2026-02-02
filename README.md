Agenda Auto — Notificador de Agendamentos por WhatsApp

Descrição
Projeto desenvolvido em 2024.
Script em Python que utiliza Selenium para ler agendamentos no sistema AppSalonSoft e enviar mensagens automáticas via WhatsApp Web antes do horário agendado.

Este projeto foi criado como estudo e protótipo. Devido a possíveis mudanças no AppSalonSoft, no WhatsApp Web ou no navegador, o funcionamento não é garantido atualmente.

Recursos
- Leitura automática de agendamentos na página do AppSalonSoft
- Extração de nome e telefone do cliente
- Envio de mensagens automáticas pelo WhatsApp Web
- Configurações ajustáveis, como modo headless e uso de variáveis de ambiente

Requisitos
- Python 3.10 ou superior
- Google Chrome instalado
- Chromedriver compatível com a versão do Chrome ou uso do webdriver-manager
- Bibliotecas Python: selenium

Exemplo mínimo de requirements.txt:
selenium>=4.0.0
webdriver-manager>=4.0.0

Configuração
**NUNCA** versionar credenciais no repositório. Use variáveis de ambiente ou um arquivo `.env` (adicione `.env` ao `.gitignore`). Crie também um arquivo `.env.example` sem valores sensíveis para referência.

Exemplo de arquivo `.env`:
AGENDA_USER=seu_login
AGENDA_PASS=sua_senha
HEADLESS=false
CHROMEDRIVER_PATH=path\to\chromedriver.exe

Como definir variáveis de ambiente (Windows):
- PowerShell (temporário na sessão): `$env:AGENDA_USER = "seu_login"`
- PowerShell (persistente): `setx AGENDA_USER "seu_login"`
- CMD (temporário): `set AGENDA_USER=seu_login`

Uso
1. Abra o WhatsApp Web. Na primeira execução, o script solicitará a leitura do QR Code.
2. Execute o script:

python agenda_auto.py
ou
python agenda_st.py

O bot verifica a agenda periodicamente e envia mensagens quando o horário configurado é atingido.
Para depuração, recomenda-se usar HEADLESS=false para visualizar o navegador.

Observações importantes
- Alterações no layout do AppSalonSoft podem quebrar os seletores CSS ou XPath utilizados.
- O uso de automação no WhatsApp pode violar termos de uso. Utilize por sua conta e risco.
- O script adiciona automaticamente o código 55 para números brasileiros. Ajustes podem ser necessários conforme o formato dos telefones.

Sugestões de melhorias
- Uso do webdriver-manager para reduzir problemas de compatibilidade
- Centralizar configurações em arquivo externo, como config.yaml
- Implementar sistema de logs
- Criar testes automatizados

Contribuições
Sugestões e correções são bem-vindas.
Abra uma issue descrevendo o problema ou envie um pull request com explicação clara das alterações.

Licença
MIT. Consulte o arquivo LICENSE para mais detalhes.

Contato
Autor: José Davi Silveira Gomes
Email: josedavisilveiragomes@gmail.com


