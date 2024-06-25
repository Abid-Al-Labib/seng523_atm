import sqlite3 
connection = sqlite3.connect("atm.db")
cursor = connection.cursor()
clear_query = """
        Drop Table IF Exists account;
        """
clear_atm_query ="""
        Drop Table IF Exists balance;
        """
create_account_query= """
        CREATE TABLE IF NOT EXISTS account(
          acc_num INT(255) NOT NULL,
          acc_pin INT(255),
          balance FLOAT,
          cardholder varchar(255),
          max_withdraw FLOAT,
          curr_withdraw FLOAT,
          last_withdraw STRING,
          PRIMARY KEY(acc_num)
);
"""
create_cashbank_query= """
        CREATE TABLE IF NOT EXISTS balance(
          atm_balance FLOAT,
          PRIMARY KEY(atm_balance)
);
"""
add_user_query = """
        INSERT INTO account(acc_num,acc_pin,balance,cardholder,max_withdraw,curr_withdraw)
        VALUES (1, 1234, 1200000, "Ethan", 1000,0),
        (2, 2121, 500000, "Ayush", 1000, 0),
        (3, 3333, 120000, "Max", 1000, 0);
        """ 
add_money_query = """
        INSERT INTO balance(atm_balance)
        VALUES (50);
        """ 
cursor.execute(clear_query)
cursor.execute(clear_atm_query)
cursor.execute(create_cashbank_query)
cursor.execute(create_account_query)
cursor.execute(add_user_query)
cursor.execute(add_money_query)
connection.commit()
