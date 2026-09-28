APS 2 - 4° Perido Engenharia de Software - Back-End
https://github.com/MateusM312/aps-2-gerenciamento-de-eventos-acad-micos

Alunos: Mateus Mendes e Caio Santana


1. descrição do projeto;

Uma instituição de ensino deseja disponibilizar um sistema para gerenciamento de seus 
eventos acadêmicos, como palestras, workshops, minicursos, seminários e outras 
atividades. 
Para isso, você deverá desenvolver uma API RESTful utilizando Python e FastAPI, 
responsável por disponibilizar os recursos necessários para o gerenciamento dos eventos e 
de seus participantes. 
A API deverá seguir os princípios apresentados durante as aulas da disciplina, utilizando 
corretamente os métodos HTTP, códigos de status, JSON, validação de dados e separação 
de responsabilidades por meio da arquitetura MVC. 

2. instruções para instalação;
git clone https://github.com/MateusM312/aps-2-gerenciamento-de-eventos-acad-micos.git

cd aps-2-gerenciamento-de-eventos-acad-micos

python -m venv venv

Windows:

venv\Scripts\activate

Linux/macOS:

source venv/bin/activate

pip install -r requirements.txt

3. instruções para execução;

uvicorn main:app --reload

http://127.0.0.1:8000

http://127.0.0.1:8000/docs

Ou abrir index.html

4. descrição das principais rotas;

EVENTOS:
Listar Eventos -> lista todos os eventos criados
Cadastrar eventos -> cadastra seu proprio evento utilizando json em um "banco de dados"
Consultar evento -> Usado para achar um evento especifico utilizando o ID dele
Atualizar evento -> Atualizar dados do evento utilizando json e achando ele pelo ID
Excluir evento -> retira o evento do "banco de dados"
Inscrever participantes -> inscreve alguem para participar de um evento
Listar Inscritos -> lista as pessoas inscritas em um evento

PARTICIPANTES:
Listar participantes -> Lista todos os participantes no "banco de dados"
Cadastrar participantes -> Cadastra seu proprio participante utilizando json
Consultar participante -> encontra um participante apartir do ID dele
Atualizar participante -> atualiza dados de um participante utilizando um json
Excluir participante -> exclui um participante do "banco de dados"

5. exemplos de utilização;
Se você clicar em cadastrar eventos, inserir seus dados desejados e depois clicar em listar eventos você verá
que o evento foi cadastrado no sistema.