import time
import asyncio
from dataclasses import dataclass


@dataclass
class Funcionario:
    nome: str
    total_vendas: float


async def calcular_imposto(faturamento: float):
    print(faturamento * 0.1)
    return faturamento * 0.1

async def calcular_bonus_funcionario(funcionarios: list[Funcionario]):
    for funcionario in funcionarios:
        print(funcionario.nome, 'Bonus: ', funcionario.total_vendas * 0.05)
        # time.sleep(1)
        await asyncio.sleep(1)

async def fechamento():
    faturamento: float = 7000.0
    vendas: list[Funcionario] = [
        Funcionario('Lira', 1500),
        Funcionario('João', 500),
        Funcionario('Amanda', 5000),
    ]
    tarefa1 = asyncio.create_task(calcular_bonus_funcionario(vendas))
    tarefa2 = asyncio.create_task(calcular_imposto(faturamento))

    await tarefa1
    imposto: float = await tarefa2
    print('Imposto: ', imposto)


if __name__ == '__main__':
    asyncio.run(fechamento())

