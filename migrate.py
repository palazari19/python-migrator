#busca os arquivos na pasta migrations
    #Arquivos são escritos com 2 funções python
    #Executa no MongoDB

from sys import exit, argv
import os.path
import importlib.util
import database_migration_repository
import bcolors

#Verifica se usuário passou a ação
try:
    action = argv[1] #migrate, rollback
    method = 'up' if action == 'migrate' else 'down'
except:
    print(f"{bcolors.FAIL}Defina uma action antes de mais nada! {bcolors.ENDC}")
    exit()

batch_id = database_migration_repository.get_batch_id();

#Lista arquivos no diretorio
files = os.listdir('migrations')

#Percorre cada arquivo do diretório
for file in files:
    if file in ['__pycache__', '.gitkeep']:
        continue

    module = importlib.util.spec_from_file_location("migrations", "migrations/"+file)
    module_from_spec = importlib.util.module_from_spec(module)
    module.loader.exec_module(module_from_spec)

    if action == 'migrate':
        try:
            module_from_spec.up()
            database_migration_repository.create_migration_register(file.replace(".py", ""), batch_id)
        except Exception as e:
            print(f"{bcolors.FAIL} Erro: %s! {bcolors.ENDC}" % (str(e)))
            exit()
    elif action == 'rollback':
        try:
            module_from_spec.down()
        except Exception as e:
            print(f"{bcolors.FAIL} Erro: %s! {bcolors.ENDC}" % (str(e)))
            exit()
    else:
        print(f"{bcolors.FAIL}Esta aplicação não suporta isso! {bcolors.ENDC}")
        exit()


