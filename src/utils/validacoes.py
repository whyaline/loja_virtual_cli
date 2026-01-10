#FUNÇÕES DE VALIDAÇÃO DE STRING E NÚMERO

def validar_string(valor, campo: str):
    if not isinstance(valor, str) or len(valor.strip()) <= 0:
        raise ValueError(f"{campo} deve ser uma string e não pode ser vazio!")

    if not valor.replace(" ", "").isalpha():
        raise ValueError(f"{campo} deve conter apenas letras!")


def validar_numero(valor, campo, *, tipo=int, tamanho=None, permitir_zero=False):
    if isinstance(valor, str) and tamanho is not None:
        if not valor.isdigit():
            raise ValueError(f'{campo} deve conter apenas dígitos numéricos!')
        if len(valor) != tamanho:
            raise ValueError(f"{campo} deve conter {tamanho} dígitos")

        try:
            numero = tipo(valor)
        except (ValueError, TypeError):
            raise ValueError(f'{campo} deve ser um número válido após conversão!')
    else:
        try:
            numero = tipo(valor)
        except (ValueError, TypeError):
            raise ValueError(f'{campo} deve ser um número válido!')

        if tamanho is not None:
            if len(str(int(abs(numero)))) != tamanho:
                raise ValueError(f"{campo} deve conter {tamanho} dígitos")

    if numero < 0:
        raise ValueError(f'{campo} não pode ser menor que zero!')

    if not permitir_zero and numero == 0:
        raise ValueError(f'{campo} não pode ser zero!')