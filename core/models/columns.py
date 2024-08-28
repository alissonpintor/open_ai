class Columns:
    __referencia: str | None = None
    descricao: str | None = None
    quantidade: str | None = None
    vlr_unitario: str | None = None
    __pdf_columns_names: list = []

    @property
    def referencia(self):
        return self.__referencia
    
    @referencia.setter
    def referencia(self, value: str | None):
        self.__referencia = value
    
    def add_pdf_columns_names(self, columns_names: list):
        self.__pdf_columns_names.extend(columns_names)

    def get_pdf_columns_names(self) -> list:
        return self.__pdf_columns_names

    def has_columns_names(self) -> bool:
        return True if len(self.__pdf_columns_names) > 0 else False

    def get_columns_names(self) -> str:
        return f'Referencia se chama {self.referencia}, Descrição se chama {self.descricao}, Qtde se chama {self.quantidade} e Preço Líq se chama {self.vlr_unitario}'
    
    def has_all_names(self) -> bool:
        return all([
            self.__referencia,
            self.descricao,
            self.quantidade,
            self.vlr_unitario
        ])
    
    def clear_all(self) -> None:
        self.__pdf_columns_names.clear()
        self.__referencia = None
        self.descricao = None
        self.quantidade = None
        self.vlr_unitario = None
