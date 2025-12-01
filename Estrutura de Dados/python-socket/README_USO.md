**README de Uso**

- **Propósito:** Guia rápido para rodar o sistema cliente/servidor do projeto `python-socket`. Contém instruções para: `server.py` (servidor), `client.py` (cliente em linha de comando) e `interface.py` (cliente com interface gráfica Tkinter).

**Requisitos**:
- Python 3.8+ instalado.
- (Opcional) Se quiser notificações via Telegram: criar `telegram_config.py` com `BOT_TOKEN` e `ADMIN_ID`.

**Arquivos principais**:
- `server.py` : servidor TCP que recebe listas de números, ordena (Bubble Sort) e retorna o resultado. Também pode enviar notificações ao admin via Telegram (opcional).
- `client.py` : cliente em linha de comando para enviar comandos e listas de números ao servidor.
- `interface.py` : cliente com interface gráfica (Tkinter). Facilita conectar, enviar números e visualizar respostas.

**Como configurar (opcional - Telegram)**
1. Crie um arquivo `telegram_config.py` na mesma pasta com o conteúdo:

```
BOT_TOKEN = "<seu_bot_token_aqui>"
ADMIN_ID = <seu_id_numero_aqui>
```

Se `telegram_config.py` não existir, o sistema funcionará normalmente sem enviar notificações.

**Executando o servidor**
- Abra um PowerShell na pasta do projeto e execute:

```powershell
python server.py
```

O servidor por padrão escuta em `0.0.0.0:5000` (porta `5000`). Ele aceita conexões TCP e responde aos comandos descritos no menu.

Comportamento do servidor (resumo):
- Ao conectar, o cliente recebe um menu explicando os comandos.
- Envie números separados por espaço (ex: `45 12 78 34 5`) — o servidor tentará convertê-los em inteiros, ordená-los com Bubble Sort e retornar o resultado.
- Comando `info` retorna informações do servidor.
- Comando `sair` fecha a conexão do cliente.
- Comando `desligar` (se enviado) faz o servidor indicar desligamento para o cliente.
- Se Telegram estiver configurado, o servidor envia uma notificação ao `ADMIN_ID` contendo os números recebidos e o resultado ordenado.

**Usando o cliente em linha de comando (`client.py`)**
1. Execute no PowerShell:

```powershell
python client.py
```

2. Ao ser solicitado, digite o IP do host do servidor (ou pressione Enter para `localhost`).
3. Digite mensagens ou listas de números separadas por espaço e pressione Enter.
4. Exemplos:

```
> 45 12 78 34 5
Servidor: Ordenado com bubble sort: [5, 12, 34, 45, 78]
```

**Usando a interface gráfica (`interface.py`)**
1. Execute no PowerShell:

```powershell
python interface.py
```

2. Informe o `Host` e `Porta` ou clique no botão `SuperShirt` para conectar ao servidor `18.229.117.78:5000`.
3. Digite números separados por espaço no campo apropriado e clique em `Enviar Números` (ou aperte Enter).
4. As respostas do servidor aparecem na área de saída.

Observações da interface:
- A interface envia também (opcional) uma notificação ao admin via Telegram se `telegram_config.py` estiver presente.
- Há tratamento de erros para desconexões inesperadas: a interface mostra mensagens e atualiza o status quando a conexão falha.

**Dicas de debug e testes locais**
- Teste localmente rodando `server.py` em uma janela de terminal e `client.py`/`interface.py` em outra na mesma máquina usando `localhost`.
- Para simular desconexão, feche o servidor enquanto o cliente está conectado — o cliente/GUI deve detectar a perda de conexão e exibir mensagem.
- Caso precise ver logs de erro no servidor, verifique a saída do terminal onde `server.py` está rodando.

**Porta e firewall**
- Certifique-se que a porta `5000` esteja liberada se for testar entre máquinas diferentes.

**Contribuição e commits**
- Antes de fazer push, configure seu Git local (nome/email) com:

```powershell
git config --global user.name "SeuNome"
git config --global user.email "seu@email"
```

- Commit e push padrão:

```powershell
git add .
git commit -m "Mensagem do commit"
git push origin main
```

**Observações finais**
- O servidor usa Bubble Sort (implementação simples da disciplina). Se precisar de desempenho para grandes listas, considere trocar por `sorted()` ou outro algoritmo (QuickSort/MergeSort).
- O código foi escrito para ser funcional e didático; ajustes de segurança e robustez adicionais são recomendados para produção.

---
Arquivo criado: `README_USO.md` — contém instruções de uso para servidor, cliente e interface.
