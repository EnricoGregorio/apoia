class AnalisadorBase:
    def analisar(self, codigo, config):
        """
        Método base que deve ser implementado por todas as linguagens.
        Deve retornar 'SUCESSO' ou uma string com as violações encontradas.
        """
        raise NotImplementedError("O método 'analisar' deve ser implementado nas subclasses.")
