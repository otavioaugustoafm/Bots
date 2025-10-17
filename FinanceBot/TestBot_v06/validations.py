from datetime import datetime
currentYear = datetime.now().year
currentMonth = datetime.now().month

def validateDate(date):
    try:
        print(f"Validando data: {date}")
        try:
            date = datetime.strptime(date, "%d/%m/%Y").date()
            dbDate = datetime.strftime(date, "%Y-%m-%d")
            print("Data válida.\n--------------------")
            return dbDate
        except:
            try:    
                date1 = f"{date}/{currentYear}"
                date1 = datetime.strptime(date1, "%d/%m/%Y").date()
                dbDate = datetime.strftime(date1, "%Y-%m-%d")
                print("Data válida.\n--------------------")
                return dbDate
            except:
                try:
                    date2 = f"{date}/{currentMonth}/{currentYear}"
                    date2 = datetime.strptime(date2, "%d/%m/%Y")
                    dbDate = datetime.strftime(date2, "%Y-%m-%d")
                    print("Data válida.\n--------------------")
                    return dbDate
                except:
                    print("Data inválida.\n--------------------")
                    return None
    except Exception as e:
        print(f"Erro ao validar data. Erro:\n {e}")

if __name__ == "__main__":
    x = validateDate("30/9")
    print(x)