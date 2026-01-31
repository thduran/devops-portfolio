# 🚀 Instrumentação Prometheus na TechCommerce

## 📋 O Mini Mundo: TechCommerce

### A Empresa
Você acabou de ser contratado como **Engenheiro DevOps** na **TechCommerce**, uma startup de e-commerce em rápido crescimento. A empresa desenvolveu uma plataforma de vendas online que está ganhando tração no mercado, mas enfrenta sérios problemas de observabilidade.

### A Situação Atual
Durante sua primeira semana, você descobriu alguns problemas críticos:

**📞 Segunda-feira, 09:30**
> **Sara (CTO)**: "Precisamos de sua ajuda urgente! Nosso e-commerce está tendo problemas de performance, mas não temos nenhuma métrica para entender o que está acontecendo. É como dirigir no escuro!"

**📞 Segunda-feira, 11:45**
> **João (Product Manager)**: "Quantos usuários temos online agora? Quais produtos são mais populares? Não faço ideia... Estamos tomando decisões no chute!"

**📞 Segunda-feira, 14:20**
> **Maria (Desenvolvedora)**: "O checkout trava às vezes, mas não sabemos se é problema de código, banco de dados ou infraestrutura. Precisamos de dados!"

### O Diagnóstico
Após análise, você identificou os problemas principais:

❌ **Zero Observabilidade**: A aplicação não possui nenhuma métrica  
❌ **Caixa Preta**: Impossível investigar problemas sem dados  
❌ **Performance Desconhecida**: Não sabem onde estão os gargalos  
❌ **Banco sem Monitoramento**: PostgreSQL sem visibilidade  
❌ **Decisões sem Base**: Product managers sem métricas de negócio  

## 🎯 Sua Missão

Implementar instrumentação Prometheus na aplicação Fake Shop da TechCommerce.

## 🎯 O Que Deve Ser Feito
> **Sara (CTO)**: "Precisamos instrumentar nossa aplicação com métricas Prometheus para finalmente termos visibilidade do que está acontecendo em produção."

### Implementar as Métricas

**Counter:**
- Adições ao carrinho por produto
- Quantidade de erros no sistema

**Gauge:**
- Sessões ativas com carrinho
- Uso de CPU em tempo real
- Conexões ativas do banco

**Histogram:**
- Latência de requests HTTP

**Summary:**
- Latência de operações de banco de dados

### Resultado Esperado
✅ Aplicação instrumentada com os 4 tipos de métricas  
✅ Endpoint `/metrics` respondendo  
✅ Métricas atualizando conforme interação com a aplicação  
✅ Instrumentação funcionando em ambiente distribuído  

---

## 🎉 Critérios de Sucesso

### ✅ **Instrumentação Completa**
- [ ] **Counter**: Adições ao carrinho funcionando
- [ ] **Counter**: Contagem de erros implementada
- [ ] **Gauge**: Sessões ativas atualizando
- [ ] **Gauge**: CPU em tempo real
- [ ] **Gauge**: Conexões do banco monitorando
- [ ] **Histogram**: Latência HTTP medindo
- [ ] **Summary**: Latência de operações internas

### ✅ **Funcionamento**
- [ ] Aplicação acessível
- [ ] Métricas expostas em /metrics
- [ ] Todas as métricas incrementando conforme uso
- [ ] Instrumentação funcionando em ambiente distribuído

### ✅ **Validação Funcional**
- [ ] Navegar pelo site incrementa métricas
- [ ] Adicionar produtos ao carrinho incrementa counter
- [ ] CPU gauge muda em tempo real
- [ ] Latência aparece no histogram
- [ ] Operações de banco aparecem no summary


## 💡 Dicas de Validação

### **🐛 Debug e Troubleshooting**
- Use `curl http://localhost:5000/metrics` para verificar métricas
- Monitore logs dos containers para errors

### **📊 Testando as Métricas**
1. **Counter**: Adicione vários produtos ao carrinho
2. **Gauge**: Monitore variação de CPU durante uso
3. **Histogram**: Acesse páginas diferentes e observe latências
4. **Summary**: Execute operações de banco e veja estatísticas
