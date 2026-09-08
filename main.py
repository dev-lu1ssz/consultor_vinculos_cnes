import cnes_consultor
from colors import Colors

cor = Colors()

cpf = input(f"{cor.NEGATIVE}Digite o CPF para obter o número CNS e os vínculos ativos:{cor.END} ")
estabelecimento = str(input(f"{cor.NEGATIVE}Digite o nome do estabelecimento para verificar o vínculo:{cor.END} "))

consultor = cnes_consultor.CnesVinculos()
validador = consultor.validar_cpf(cpf)

if validador == False:
    print('CPF inválido. Por favor, insira um CPF válido.')
    exit()

vinculos = consultor.vinculos_ativos(cpf)
vinculos_profissional = vinculos.get('vinculos', []) if vinculos else []
esta_vinculado = any(
    vinculo.get('noFant') == estabelecimento for vinculo in vinculos_profissional
)

if esta_vinculado:
    print(f'{cor.LIGHT_GREEN}O profissional está vinculado corretamente.{cor.END}')
else:
    print(f'{cor.LIGHT_RED}O profissional não está vinculado corretamente.{cor.END}')