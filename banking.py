import random
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS card("
            "id INTEGER ,"
            "number TEXT,"
            "pin TEXT,"
            "balance INTEGER DEFAULT 0);")
conn.commit()

def menu():
    print("""
1. Create an account
2. Log into account
0. Exit
    """)
    option = int(input())
    return option


def log_menu():
    print("""
1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit
    """)
    option = int(input())
    return option


class Bank:

    card = None

    def __init__(self):
        pass

    # Se crea la tarjeta de credito
    def crear_tarjeta(self):
        total = 0
        counter = 0
        cur.execute("SELECT id FROM card") # Vamos a generar una ID para cada tarjeta.
        gen_id = len(cur.fetchall()) + 1 # Mediante len al fetch de ID + 1, aseguramos continuidad de IDs.
        random.seed(random.randint(0, 5000))
        a = random.randint(000000000, 999999999)
        card = str(400000000000000 + a)  # Se asigna un numero aleatorio a los 10 ultimos digitos

        for number in card:  # En este for llevaremos a cabo el algoritmo de Luhn
            x = int(number)
            if counter % 2 == 0:
                x *= 2
            if x > 9:
                x -= 9
            total += x
            counter += 1
        last_digit = 10 - total % 10
        if last_digit == 10:
            last_digit -= 10
        card += str(last_digit)

        pin = (random.randint(0, 9999))  # Nº aleatorio para el PIN
        pin = str(pin).zfill(4)

        cur.execute(f"INSERT INTO card (id, number, pin) VALUES ('{gen_id}', '{card}', '{pin}')")
        conn.commit()
        print(f"""
Your card has been created
Your card number:
{card}
Your card PIN:
{pin}
        """)

    def check_tarjeta(self, n_tarjeta, pin):
        aux = None
        cur.execute("SELECT number FROM card")
        rows = cur.fetchall()
        for row in rows:
            row = int(row[0])
            if row == n_tarjeta:
                cur.execute(f"SELECT pin FROM card WHERE number = {row}")
                number_pin = int(cur.fetchone()[0])
                if number_pin == pin:
                    return True
                else:
                    return False
            else:
                aux = False
        if not aux:
            return False

    def añadir_dineros(self, cuenta):
        dinero = int(input("Enter income: "))
        cur.execute(f"UPDATE card SET balance = balance + {dinero} WHERE number = {cuenta}")
        conn.commit()
        print("Income was added!")

    def transferencia(self, cuenta_actual):
        counter = 0
        total = 0
        print("Transfer")
        tarjeta_objetivo = input("Enter card number: ")

        if tarjeta_objetivo == cuenta_actual:
            print("You can't transfer money to the same account!")
            return None

        for number in str(tarjeta_objetivo):  # Comprobamos mediante Luhn que la tarjeta es correcta.
            x = int(number)
            if counter % 2 == 0:
                x *= 2
            if x > 9:
                x -= 9
            total += x
            counter += 1
        if total % 10 != 0:
            print("Probably you made a mistake in the card number. Please try again!")
            return None

        cur.execute("SELECT number FROM card")
        card_tup = [row[0] for row in cur.fetchall()]
        if tarjeta_objetivo in card_tup:
            money = int(input("Enter how much money you want to transfer: "))
            cur.execute(f"SELECT balance FROM card WHERE number = {cuenta_actual}")
            dinero_cuenta_actual = cur.fetchone()[0]
            if dinero_cuenta_actual >= money:
                cur.execute(f"UPDATE card SET balance = balance - {money} WHERE number = {cuenta_actual}")
                cur.execute(f"UPDATE card SET balance = balance + {money} WHERE number = {tarjeta_objetivo}")
                conn.commit()
                print("Success!")
            else:
                print("Not enough money!")
                return None
        else:
            print("Such a card does not exist.")
            return None


banco = Bank()

while True:

    # Menu de seleccion para dar las opciones al usuario
    option = menu()
    login = True

    if option == 1:
        banco.crear_tarjeta()
    if option == 2:
        n_tarjeta = int(input("Enter your card number: "))
        pin = int(input("Enter your PIN: "))
        if banco.check_tarjeta(n_tarjeta, pin):
            print("\nYou have successfully logged in!")
            while login:  # "Navegacion" al estar logueado.
                log_opts = log_menu()
                if log_opts == 1:
                    cur.execute(f"SELECT balance FROM card WHERE number = {n_tarjeta}")
                    print("Balance: " + str(cur.fetchone()[0]))
                if log_opts == 2:
                    banco.añadir_dineros(n_tarjeta)
                if log_opts == 3:
                    banco.transferencia(n_tarjeta)
                if log_opts == 4:
                    cur.execute(f"DELETE FROM card WHERE number = {n_tarjeta}")
                    conn.commit()
                    print("The account has been closed!")
                    login = False
                if log_opts == 5:
                    login = False
                    print("You have successfully logged out!")
                if log_opts == 0:
                    print("Bye!")
                    exit()
        else:
            print("Wrong card number or PIN!")
    if option == 0:
        print("Bye!")
        exit()




