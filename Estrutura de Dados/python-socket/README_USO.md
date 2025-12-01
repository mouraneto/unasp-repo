**README de Uso**
```
Professor, o README foi feito pelo chat. E pedimos ajuda em alguns arquivos. :)
```

 - **Propósito:** Guia rápido para rodar o sistema cliente/servidor do projeto `python-socket`. Contém instruções para: `server.py` (servidor), `client.py` (cliente em linha de comando) e `interface.py` (cliente com interface gráfica Tkinter). 

**Requisitos**:
- Python 3.8+ instalado.

**Arquivos principais**:
- `server.py` : servidor TCP que recebe listas de números, ordena (Bubble Sort) e retorna o resultado.
- `client.py` : cliente em linha de comando para enviar comandos e listas de números ao servidor.
- `interface.py` : cliente com interface gráfica (Tkinter). Facilita conectar, enviar números e visualizar respostas.

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
- Há tratamento de erros para desconexões inesperadas: a interface mostra mensagens e atualiza o status quando a conexão falha.

**Dicas de debug e testes locais**
- Teste localmente rodando `server.py` em uma janela de terminal e `client.py`/`interface.py` em outra na mesma máquina usando `localhost`.
- Para simular desconexão, feche o servidor enquanto o cliente está conectado — o cliente/GUI deve detectar a perda de conexão e exibir mensagem.
- Caso precise ver logs de erro no servidor, verifique a saída do terminal onde `server.py` está rodando.

**Porta e firewall**
- Certifique-se que a porta `5000` esteja liberada se for testar entre máquinas diferentes.

**Observações finais**
- O servidor usa Bubble Sort (implementação simples da disciplina). Se precisar de desempenho para grandes listas, considere trocar por `sorted()` ou outro algoritmo (QuickSort/MergeSort).

---
