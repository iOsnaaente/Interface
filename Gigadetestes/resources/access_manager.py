import datetime
import sqlite3
import json 
import os 



PATH = os.path.dirname( __file__ )

class Database:
    ACCESS_OUT = 'OUT'
    ACCESS_IN  = 'IN' 
    def __init__( self, __debug : bool = False ) -> None:
        self.__debug = __debug 
        self.db_file = os.path.join( PATH, 'database', 'access_log.db' )
        self.con = sqlite3.connect(self.db_file)
        self.cursor = self.con.cursor()

        # Tabela de colaborador 
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS 
                colaborador (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    matricula TEXT NOT NULL
                );
        ''')
        # Tabela de acessos 
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS 
                acesso (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_colaborador INTEGER NOT NULL,
                    tipo TEXT,
                    data DATE,
                    hora TIME,
                    FOREIGN KEY(id_colaborador) REFERENCES colaborador(id)
                );
        ''')
        # Tabela de medições 
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS 
                medicao (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_colaborador INTEGER NOT NULL,
                    data DATE,
                    hora TIME,
                    resultado TEXT,
                    FOREIGN KEY(id_colaborador) REFERENCES colaborador(id)
                );
        ''')
        self.con.commit() 
    
    # Adiciona novos colaboradores (collaborator) à tabela 
    def new_collaborator( self, matricula : str ) -> int:
        # Procura a matricula do colaborador
        self.cursor.execute("SELECT id FROM colaborador WHERE matricula = ?", (matricula,))
        colaborador_id = self.cursor.fetchone()
        if colaborador_id is not None:
            if self.__debug:
                print("Colaborador já existe no banco de dados.")
            return colaborador_id 
        # Se não existir, cria um novo campo de colaborador 
        self.cursor.execute("INSERT INTO colaborador (matricula) VALUES (?)", (matricula,))
        colaborador_id = self.cursor.lastrowid
        self.con.commit()
        if self.__debug:
            print( f"Colaborador adicionado com sucesso. ID: {colaborador_id}")
        return colaborador_id 

    # Adiciona novos acessos (access) à tabela 
    def new_access( self, matricula : str, access_type : str ) -> None:
        self.cursor.execute("SELECT id FROM colaborador WHERE matricula = ?", (matricula,))
        colaborador_id = self.cursor.fetchone()
        if colaborador_id is None:
            if self.__debug:
                print("Matricula não encontrada no banco de dados.") 
            # Se não encontrar um colaborador, adiciona um novo colaborador 
            colaborador_id = self.new_collaborator( matricula )
        else: 
            colaborador_id = colaborador_id[0]
        # Registrar o acesso
        data = datetime.date.today()
        hora = datetime.datetime.now().strftime("%H:%M:%S")
        self.cursor.execute("INSERT INTO acesso (id_colaborador, tipo, data, hora) VALUES (?, ?, ?, ?)",
                            (colaborador_id, access_type, data, hora))
        self.con.commit()
        if self.__debug:
            print("Acesso registrado com sucesso.")
        return True 
        
    
    # Adiciona novas medições (measures) à tabela 
    def new_measure(self, matricula, resultado):
        self.cursor.execute("SELECT id FROM colaborador WHERE matricula = ?", (matricula,))
        colaborador_id = self.cursor.fetchone()[0]
        if colaborador_id is None:
            if self.__debug:
                print( "Colaborador não encontrado no banco de dados.")
            return False 
        
        data = datetime.date.today()
        hora = datetime.datetime.now().strftime("%H:%M:%S")
        self.cursor.execute("INSERT INTO medicao (id_colaborador, data, hora, resultado) VALUES (?, ?, ?, ?)",
                            (colaborador_id, data, hora, resultado))
        self.con.commit()
        if self.__debug:
            print( "Medição registrada com sucesso.")  
        return True 


    def generate_report(self, start_date, end_date ):
        report = {}
        self.cursor.execute("SELECT matricula FROM colaborador")
        colaboradores = self.cursor.fetchall()
        for colaborador in colaboradores:
            matricula = colaborador[0]
            report[matricula] = {
                'data considerada': {'data de inicio': start_date, 'data de fim': end_date},
                'Num acessos de entrada': 0,
                'Num acessos de saida': 0,
                'Num medicoes realizadas': 0,
                'Medicoes': []
            }
            self.cursor.execute("SELECT id FROM colaborador WHERE matricula = ? ", (matricula, ) )
            id_colaborador = self.cursor.fetchall()[0][0]

            # Contagem dos acessos de entrada
            self.cursor.execute("SELECT COUNT(*) FROM acesso WHERE id_colaborador = ? AND tipo = ? AND data BETWEEN ? AND ?", (id_colaborador, self.ACCESS_IN, start_date, end_date))
            num_acessos_entrada = self.cursor.fetchone()[0]
            report[matricula]['Num acessos de entrada'] = num_acessos_entrada
            # Contagem dos acessos de saída
            self.cursor.execute("SELECT COUNT(*) FROM acesso WHERE id_colaborador = ? AND tipo = ? AND data BETWEEN ? AND ?", (id_colaborador, self.ACCESS_OUT, start_date, end_date))
            num_acessos_saida = self.cursor.fetchone()[0]
            report[matricula]['Num acessos de saida'] = num_acessos_saida
            # Recuperação das medições
            self.cursor.execute("SELECT resultado FROM medicao WHERE id_colaborador = ? AND data BETWEEN ? AND ?", (id_colaborador, start_date, end_date))
            medições = self.cursor.fetchall()
            num_medições = len(medições)
            report[matricula]['Num medicoes realizadas'] = num_medições
            report[matricula]['Medicoes'] = [med[0] for med in medições]

        return json.dumps(report, indent=4)



if __name__ == '__main__':
    import random 
    
    msg = ''
    for c in [ chr( random.randint(0, 127)) for _ in range(25) ]:
        msg += c

    db = Database( True )
    db.new_collaborator( '202013054' )
    db.new_access( '202013054', db.ACCESS_IN )
    db.new_measure( '202013054', msg )
    db.new_access( '202013054', db.ACCESS_OUT )
    
    print( db.generate_report('2023-06-01', '2023-06-30'))
    