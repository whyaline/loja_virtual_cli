# 🛍️ Loja Virtual CLI – Projeto de POO

Sistema de linha de comando (CLI) com **menu interativo** para gerenciar uma loja virtual simplificada, desenvolvido como Trabalho de Projeto 1 de POO no curso de **Tecnologia em Banco de Dados – UFCA**.  

O sistema permite cadastrar produtos e clientes, gerenciar carrinhos e pedidos, aplicar cupons, calcular frete, registrar pagamentos, gerar relatórios e controlar o fluxo completo de pedidos (CRIADO → PAGO → ENVIADO → ENTREGUE → CANCELADO).  

---

## 📦 Principais Módulos e Classes

### Produto e Estoque
- **Classes:** `Produto`, `ProdutoFisico`, `ProdutoDigital`  
- **Funcionalidades:** CRUD de produtos, controle de estoque, preço e status ativo/inativo.  
- **Testes:** Adição, remoção e ajuste de estoque; validação de preço e quantidade.  

---

### 👤 Cliente e Endereço
- **Classes:** `Cliente`, `Endereco`  
- **Funcionalidades:** CRUD de clientes, validação de CPF/email, múltiplos endereços.  
- **Testes:** Impedir duplicidade de CPF/email, validação de campos obrigatórios.  

---

### 🛒 Carrinho e Pedido
- **Classes:** `Carrinho`, `ItemCarrinho`, `Pedido`, `ItemPedido`  
- **Funcionalidades:** Adicionar/remover itens, calcular subtotal, desconto e frete; criar pedidos a partir do carrinho; gerenciamento de estados do pedido.  
- **Testes:** Carrinho vazio, quantidade solicitada maior que estoque, transições de estado do pedido, resumo de pedido.  

---

### 💳 Pagamento, Frete e Cupom
- **Classes e Atributos:**
  - `Pagamento`  
    - Atributos: `pedido` (Pedido), `valor`, `forma` (PIX, Crédito, Débito, Boleto), `data`  
    - Métodos: `processar()`, `estornar()`, `cancelar()`
  - `Cupom`  
    - Atributos: `codigo`, `tipo` (VALOR ou PERCENTUAL), `valor`, `data_validade`, `uso_maximo`, `usos_feitos`, `categorias_elegiveis`  
    - Métodos: `validar_uso()`, `calcular_desconto()`, `registrar_uso()`
  - `Frete`  
    - Atributos: `uf`, `endereco` (cidade, uf, cep), `valor`, `prazo`  
    - Métodos: `buscar_regra()`, `calcular_preview()`  

---

### 🖥️ Interface CLI e Menu Interativo
- **Menu interativo:** Navegação completa via menus numerados para:
  - Selecionar cliente
  - Gerenciar produtos
  - Adicionar/remover itens do carrinho
  - Criar pedido
  - Pagar, enviar, entregar ou cancelar pedidos
  - Visualizar relatórios  
- **Persistência:** JSON via `dados.py` (produtos, clientes, pedidos, cupons)  
- **Relatórios:** Faturamento por período, top N produtos mais vendidos, vendas por categoria/UF, pedidos por status.  
- **Configurações:** Arquivo `settings.json` com regras de frete, validade de cupons e política de cancelamento.  

---

## ⚙️ Funcionalidades Principais
- Cadastro e gerenciamento de produtos e clientes  
- Carrinho de compras com cálculo de subtotal, desconto e frete  
- Aplicação de cupons de desconto (valor ou percentual)  
- Criação de pedidos a partir do carrinho  
- Registro e processamento de pagamentos  
- Controle de estados do pedido: CRIADO → PAGO → ENVIADO → ENTREGUE → CANCELADO  
- Relatórios de vendas, faturamento e produtos mais vendidos  
- Persistência de dados via JSON e seed inicial para teste  

---

## 🚀 Como Rodar o Projeto

1. **Clone o repositório:**
```bash
git clone <link-do-repo>
cd loja_virtual_cli

2. **Execute a loja virtual:**
```bash
python main.py

3. **Use os menus numerados para acessar clientes, produtos, carrinho e pedidos.**
