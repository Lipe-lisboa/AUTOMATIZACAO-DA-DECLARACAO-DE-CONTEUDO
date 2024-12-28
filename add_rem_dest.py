import streamlit as st
import sqlite3
import pandas as pd

# Cria ou abre um banco de dados chamado 'meu_banco.db'
conn = sqlite3.connect('logistica.db')

# Cria um cursor para executar comandos SQL
cursor = conn.cursor()

# Criação de uma tabela chamada 'clientes'
cursor.execute('''
CREATE TABLE IF NOT EXISTS remetente (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    endereco TEXT NOT NULL,
    cidade TEXT NOT NULL,
    uf TEXT NOT NULL,
    cep TEXT NOT NULL,
    cpf_cnpj TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS destinatario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    endereco TEXT NOT NULL,
    cidade TEXT NOT NULL,
    uf TEXT NOT NULL,
    cep TEXT NOT NULL,
    cpf_cnpj TEXT NOT NULL
)
''')

# Consultar os dados de nome e CNPJ da tabela 'remetentes'
cursor.execute("SELECT * FROM remetente")

# Recuperar todos os resultados da consulta
remetentes = cursor.fetchall()

# Consultar os dados de nome e CNPJ da tabela 'remetentes'
cursor.execute("SELECT * FROM destinatario")

# Recuperar todos os resultados da consulta
destinatarios = cursor.fetchall()

#VERIFICAÇÃO DO FORMULARIO DE DESTINATARIO
def verificacao_destinatario():
    sucesso = True
    if not nome or not endereco or not cidade or not uf or not cep:
        st.error("Todos os campos são obrigatórios❗")
        sucesso = False
    elif not cpf_cnpj and not sem_cpf_cnpj:
        st.warning('Destinatario sem CPF/CNPJ, caso o destinatario não tenha marque a opção "Destinatario sem CPF e CNPJ"⚠️')
        sucesso = False

    return sucesso

#VERIFICAÇÃO DO FORMULARIO DE REMETENTE
def verificacao_remetente():
    sucesso = False
    if nome and endereco and cidade and uf and cep and cpf_cnpj:
        sucesso = True
        st.success("Remetente cadastrado com sucesso✅")
    else:
        st.error("Todos os campos são obrigatórios❗")
    return sucesso

# ABAS
aba1, aba2, aba3, aba4 = st.tabs(['Remetente','Destinatario', 'View', 'Editar'])

# ABA DE CADASTRO DO REMETENTE
with aba1:
    st.title('📪 Adicionar Remetente')

    #FORMULARIO
    with st.form('forme_rem'):
        st.title('📋 Preenchimento')
        
        nome = st.text_input('Nome:')
        endereco = st.text_input('Endereço:')
        cidade = st.text_input('Cidade:')
        uf = st.text_input('UF:')
        cep = st.text_input('CEP:')
        cpf_cnpj = st.text_input('CPF/CNPJ:')
        
        btt_enviar = st.form_submit_button('Enviar')
        
        
        if btt_enviar:
            if verificacao_remetente():
                # Inserir os dados na tabela
                cursor.execute(f'''
                INSERT INTO remetente (nome, endereco, cidade, uf, cep, cpf_cnpj)
                VALUES (?, ?, ?, ?, ?, ?)
                ''', (nome, endereco, cidade, uf, cep, cpf_cnpj))        
 
# ABA DE CADATRO DO REMETENTE                      
with aba2:
    st.title('📬 Adicionar Destinatario')

    # FORMULARIO
    with st.form('forme_dest'):
        st.title('📋 Preenchimento')
        
        nome = st.text_input('Nome:')
        endereco = st.text_input('Endereço:')
        cidade = st.text_input('Cidade:')
        uf = st.text_input('UF:')
        cep = st.text_input('CEP:')
        cpf_cnpj = st.text_input('CPF/CNPJ:')
        sem_cpf_cnpj = st.checkbox('Destinatario sem CPF e CNPJ')
        
        btt_enviar = st.form_submit_button('Enviar')

        
        if btt_enviar:
            if verificacao_destinatario():
                if not cpf_cnpj and sem_cpf_cnpj:
                    cpf_cnpj = 'None'  
                    
                # Inserir os dados na tabela
                cursor.execute(f'''
                INSERT INTO destinatario (nome, endereco, cidade, uf, cep, cpf_cnpj)
                VALUES (?, ?, ?, ?, ?, ?)
                ''', (nome, endereco, cidade, uf, cep, cpf_cnpj))
                st.success("Destinatario cadastrado com sucesso✅")

# ABA DE VISUALIZAÇÃO DOS REMETENTES/DESTINATARIOS
with aba3:
    
    st.title('👀 Visualização')
    
    # DICIONARIO DE DADOS PARA COLOCAR NA TABELA DE REMETENTES
    dict_remetentes = {
        'Nome': [],
        'Endereço': [],
        'Cidade':[],
        'UF': [],
        'CEP': [],
        'CPF/CNPJ': []
    }
    
    id = 1
    for remetente in remetentes:
        for i in dict_remetentes: 
            dict_remetentes[i].append(remetente[id])
            id += 1
        id = 1
    
    # DICIONARIO DE DADOS PARA COLOCAR NA TABELA DE DESTINATARIOS
    dict_destinatarios = {
        'Nome': [],
        'Endereço': [],
        'Cidade':[],
        'UF': [],
        'CEP': [],
        'CPF/CNPJ': []
    }
    
    id = 1
    for destinatario in destinatarios:
        for i in dict_destinatarios:  
            dict_destinatarios[i].append(destinatario[id])
            id += 1
        id = 1
            
            
    # TABELA DE REMETENTES
    st.subheader('📪 Remetentes')
    tabela_remetentes = pd.DataFrame(dict_remetentes)
    st.dataframe(tabela_remetentes, use_container_width=True)
    
    # REMOÇÃO DE REMETENTES
    if remetentes:
        st.subheader('Remover Remetente')
        indice = st.number_input('Indice do Remetente que deseja remover:', min_value=0)
        btt_remover_remetente_indice = st.button(f'Remover Remetente')
        if btt_remover_remetente_indice:
            try:
                id_remetente = remetentes[indice][0]
                cursor.execute("DELETE FROM remetente WHERE id = ?", (id_remetente,))
                conn.commit()
                st.rerun()
            except IndexError:
                st.error('Remetente não existe, por favor insira outro indice❗')
        
    
    #TABELA DE DESTINATARIOS
    st.subheader('📬 Destinatarios')
    tabela_destinatarios = pd.DataFrame(dict_destinatarios)
    st.dataframe(tabela_destinatarios, use_container_width=True)
    
    # REMOÇÃO DE REMETENTES
    if destinatarios:
        st.subheader('Remover Destinatario')
        indice = st.number_input('Indice do Destinatario que deseja remover:', min_value=0)
        btt_remover_destinatario_indice = st.button(f'Remover Destinatario')
        if btt_remover_destinatario_indice:
            try:
                id_destinatario = destinatarios[indice][0]
                cursor.execute("DELETE FROM destinatario WHERE id = ?", (id_destinatario,))
                conn.commit()
                st.rerun()
            except IndexError:
                st.error('Destinatario não existe, por favor insira outro indice❗')


if not 'editar' in st.session_state:
    st.session_state['editar'] = False
 
# EDIÇÃO DE REMETENTES/DESTINATARIOS 
with aba4:
    st.title('📝Editar Remetente/Destinatario')

    #FORMULARIO PARA ENCOUTRAR O REMETENTE/DESTINATARIO
    with st.form('forme_edit'):
        st.title('📋 Preenchimento')
        
        opition = st.selectbox('Oque deseja editar?', ['Remetente', 'Destinatario'])
    
        indice = st.number_input('Indice do Remetente/Destinatario que deseja editar:', min_value=0)
        btt_procurar = st.form_submit_button(f'Procurar')
        escolha = None
        
        if btt_procurar or st.session_state['editar']:
            st.session_state['editar'] = True
            if opition == 'Remetente':
                try:
                    escolha = remetentes[indice]
                except IndexError:
                    st.error('Remetente não existe, por favor insira outro indice❗')
            if opition == 'Destinatario':
                try:
                    escolha = destinatarios[indice]
                except IndexError:
                    st.error('Destinatario não existe, por favor insira outro indice❗')
            
            # SE EXISTIR O REMETENTE/DESTINATARIO MOSTRA O FORMULARIO DE EDIÇÃO
            if escolha:
                opition_escolhida = opition.lower()
                id_escolha = escolha[0]
                
                nome = st.text_input('Nome:', value=escolha[1])
                endereco = st.text_input('Endereço:', value=escolha[2])
                cidade = st.text_input('Cidade:', value=escolha[3])
                uf = st.text_input('UF:', value=escolha[4])
                cep = st.text_input('CEP:', value=escolha[5])
                cpf_cnpj = st.text_input('CPF/CNPJ:', value=escolha[6])
                if opition_escolhida == 'destinatario':
                    sem_cpf_cnpj = st.checkbox('Destinatario sem CPF e CNPJ')
            
                btt_editar = st.form_submit_button('Editar')
                
                if btt_editar:
                    sucesso = None
                    if opition_escolhida == 'destinatario':
                        sucesso = verificacao_destinatario()
                        
                    if opition_escolhida == 'remetente':
                        sucesso = verificacao_remetente()
                    
                    if sucesso: 
                        cursor.execute(f"""
                        UPDATE {opition_escolhida}
                        SET nome = ?, endereco = ?, cidade = ?, uf = ?, 
                        cep = ?, cpf_cnpj = ? 
                        WHERE id = ?
                        """, (
                            nome,
                            endereco,
                            cidade,
                            uf,
                            cep,
                            cpf_cnpj,
                            id_escolha
                        ))
                        # Salvar as alterações
                        conn.commit()
                        st.success("Edição feita com sucesso✅")
                        st.session_state['editar'] = False
                        st.rerun()
                    
# Salvar as alterações e fechar a conexão
conn.commit()
conn.close()