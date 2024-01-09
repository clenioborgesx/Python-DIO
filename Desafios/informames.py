def number(month):
  month_dict = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December",
  }
  return month_dict.get(month,"Invalid number")

month = int(input("Informa um número de 1 a 12 e te falarei o mês em inglês: "))
print(number(month))