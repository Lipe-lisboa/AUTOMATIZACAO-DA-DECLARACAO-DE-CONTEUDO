import streamlit as st

pg1 = st.Page('dec.py', title='Declaração de conteudo')
pg2 = st.Page('add_rem_dest.py',title='Add Remetente e Destinatario')

pg = st.navigation({
    'Declaração de conteudo': [pg1, pg2]
})
pg.run()