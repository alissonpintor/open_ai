class Columns:
    referencia: str = None
    descricao: str = None
    quantidade: str = None
    vlr_unitario: str = None

    def get_columns_names(self) -> str:
        return f'Referencia se chama {self.referencia}, Descrição se chama {self.descricao}, Qtde se chama {self.quantidade} e Preço Líq se chama {self.vlr_unitario}'
    
    def has_all_names(self) -> bool:
        return all([
            self.referencia,
            self.descricao,
            self.quantidade,
            self.vlr_unitario
        ])
    
    def clear_names(self) -> None:
        self.referencia = None
        self.descricao = None
        self.quantidade = None
        self.vlr_unitario = None
