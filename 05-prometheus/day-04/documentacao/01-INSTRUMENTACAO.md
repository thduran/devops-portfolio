
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
- Uso de CPU sob demanda

**Histogram:**
- Tempo de resposta de requests HTTP (distribuição por buckets)

### Resultado Esperado
✅ Aplicação instrumentada com os 3 tipos principais de métricas  
✅ Endpoint `/metrics` respondendo  
✅ Métricas atualizando conforme interação com a aplicação  
✅ Instrumentação funcionando em ambiente distribuído  

---

## 🎉 Critérios de Sucesso

### ✅ **Instrumentação Completa**
- [x] **Counter**: Adições ao carrinho funcionando
- [x] **Counter**: Contagem de erros implementada
- [x] **Gauge**: Sessões ativas atualizando
- [x] **Gauge**: CPU sob demanda funcionando
- [x] **Histogram**: Tempo de resposta HTTP medindo

### ✅ **Funcionamento**
- [ ] Aplicação acessível
- [ ] Métricas expostas em /metrics
- [ ] Todas as métricas incrementando conforme uso
- [ ] Instrumentação funcionando em ambiente distribuído

### ✅ **Validação Funcional**
- [x] Navegar pelo site incrementa métricas
- [x] Adicionar produtos ao carrinho incrementa counter  
- [x] CPU gauge atualiza quando `/metrics` é acessado
- [x] Tempo de resposta aparece no histogram


## 💡 Dicas de Validação

### **🐛 Debug e Troubleshooting**
- Use `curl http://localhost:5000/metrics` para verificar métricas
- Monitore logs dos containers para errors

### **📊 Testando as Métricas**
1. **Counter**: Adicione vários produtos ao carrinho para ver incremento
2. **Gauge**: Acesse `/metrics` para ver CPU e sessões atuais
3. **Histogram**: Acesse páginas diferentes e observe tempo de resposta com buckets

### **✅ Métricas Implementadas**
- `ecommerce_cart_additions_total`: Counter de adições ao carrinho
- `ecommerce_errors_total`: Counter de erros no sistema  
- `ecommerce_active_sessions`: Gauge de sessões ativas
- `ecommerce_cpu_usage_percent`: Gauge de CPU sob demanda
