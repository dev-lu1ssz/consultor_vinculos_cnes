import requests
import colors
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

cor = colors.Colors()

class CnesVinculos:
    def __init__(self):
        self.session = requests.Session()
        # O servidor do CNES apresenta um certificado expirado.
        self.session.verify = False
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'pt-BR,pt;q=0.9',
            'Referer': 'https://cnes.datasus.gov.br/pages/profissionais/consulta.jsp',
            'Origin': 'https://cnes.datasus.gov.br',
            'X-Requested-With': 'XMLHttpRequest'
        })

    def buscar_profissional(self, cpf):
        self.session.get("https://cnes.datasus.gov.br/pages/profissionais/consulta.jsp", timeout=15)
        params = {}

        if cpf:
            params['cpf'] = cpf

        response = self.session.get("https://cnes.datasus.gov.br/services/profissionais", params=params, timeout=15)
        
        if response.status_code == 200:
            try:
                data = response.json()
                if data:
                    return data[0].get('cns')
                else:
                    return None
            except ValueError:
                return None
        else:
            return None

    def vinculos_ativos(self, cpf):
        self.session.get("https://cnes.datasus.gov.br/pages/profissionais/consulta.jsp", timeout=15)
        params = {}

        if cpf:
            params['cpf'] = cpf

        response = self.session.get("https://cnes.datasus.gov.br/services/profissionais", params=params, timeout=15)
        if response.status_code == 200:
            try:
                data = response.json()
                if not data:
                    return None

                id_profissional = data[0].get('id')
                if id_profissional:
                    response_vinculos = self.session.get(f'https://cnes.datasus.gov.br/services/profissionais/{id_profissional}', timeout=15)
                    if response_vinculos.status_code == 200:
                        lista_vinculos = response_vinculos.json()
                        return lista_vinculos
                
            except ValueError:
                return None
    def validar_cpf(self, cpf: str) -> bool:
        import re

        cpf = re.sub(r'\D', '', cpf)
        if len(cpf) != 11 or len(set(cpf)) == 1:
            return False

        def calcular_digito(cpf_parcial, peso_inicial):
            soma = sum(int(digito) * peso for digito, peso in zip(cpf_parcial, range(peso_inicial, 1, -1)))
            resto = soma % 11
            return 0 if resto < 2 else 11 - resto

        primeiro_digito = calcular_digito(cpf[:9], 10)
        segundo_digito = calcular_digito(cpf[:10], 11)
        return int(cpf[9]) == primeiro_digito and int(cpf[10]) == segundo_digito