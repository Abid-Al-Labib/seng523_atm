import sqlite3


class DB_manager:

    def get_balance_by_id_query(account_id):
        if (account_id == ""): 
            return ""
        connection = sqlite3.connect("atm.db")
        cursor = connection.cursor()
        balance_by_id_query = "SELECT balance FROM account WHERE acc_num=?;" 

        cursor.execute(balance_by_id_query,(account_id,))

        rows = cursor.fetchall()
        connection.close()
        return rows[0][0]

    def get_maxWithdraw(account_id):
        connection = sqlite3.connect("atm.db")
        cursor = connection.cursor()
        withdraw_by_id_query = "SELECT max_withdraw FROM account WHERE acc_num=?;"
        cursor.execute(withdraw_by_id_query,(account_id,))
        rows = cursor.fetchall()
        connection.close()
        return rows[0][0]
    
    def get_currentWithdraw(account_id):
        connection = sqlite3.connect("atm.db")
        cursor = connection.cursor()
        query = "SELECT curr_withdraw FROM account WHERE acc_num=?;"
        cursor.execute(query,(account_id,))
        rows = cursor.fetchall()
        connection.close()
        return rows[0][0]
    
    def WithdrawMoney(amount,withdraw_time_str,account_id):
        connection = sqlite3.connect("atm.db")
        cursor = connection.cursor()
        withdraw_money = "UPDATE account SET balance = balance - ?, last_withdraw = ? WHERE acc_num = ?;"

        cursor.execute(withdraw_money,(amount,withdraw_time_str,account_id,))
        connection.commit()
        connection.close()

    def DepositMoney(amount,account_id):
        connection = sqlite3.connect("atm.db")
        cursor = connection.cursor()
        deposit_money = "UPDATE account SET balance = balance + ? WHERE acc_num = ?;"

        cursor.execute(deposit_money,(amount,account_id,))
        connection.commit()
        connection.close()
    
    def get_pin(account_id):
        connection = sqlite3.connect("atm.db")
        cursor = connection.cursor()
        pin_by_id_query = "SELECT acc_pin FROM account WHERE acc_num=?;" 

        cursor.execute(pin_by_id_query,(account_id,))

        rows = cursor.fetchall()
        connection.close()
        return rows[0][0]

    def get_last_withdraw_time_str_by_id(account_id):
        connection = sqlite3.connect("atm.db")
        cursor = connection.cursor()
        query = "SELECT last_withdraw FROM account WHERE acc_num=?;" 

        cursor.execute(query,(account_id,))

        rows = cursor.fetchall()
        connection.close()
        return rows[0][0]

    def setCurrentWithdraw(amount,account_id):
        connection = sqlite3.connect("atm.db")
        cursor = connection.cursor()
        withdraw_money = "UPDATE account SET curr_withdraw = curr_withdraw + ? WHERE acc_num = ?;"

        cursor.execute(withdraw_money,(amount,account_id,))
        connection.commit()
        connection.close()

    def resetCurrentWithdraw(account_id):
        connection = sqlite3.connect("atm.db")
        cursor = connection.cursor()
        reset_current_withdraw = "UPDATE account SET curr_withdraw = 0 WHERE acc_num = ?;"

        cursor.execute(reset_current_withdraw,(account_id,))
        connection.commit()
        connection.close()


    def get_AtmBalance():
        connection = sqlite3.connect("atm.db")
        cursor = connection.cursor()
        atm_query = "SELECT atm_balance FROM balance;" 

        cursor.execute(atm_query)

        rows = cursor.fetchall()
        connection.close()
        return rows[0][0]
    
    def WithdrawMoney_ATM(amount):
        connection = sqlite3.connect("atm.db")
        cursor = connection.cursor()
        withdraw_money = "UPDATE balance SET atm_balance = atm_balance - ? ;"

        cursor.execute(withdraw_money,(amount,))
        connection.commit()
        connection.close()

    def DepositMoneyATM(amount):
        connection = sqlite3.connect("atm.db")
        cursor = connection.cursor()
        deposit_money = "UPDATE balance SET atm_balance = atm_balance + ? ;"

        cursor.execute(deposit_money,(amount,))
        connection.commit()
        connection.close()