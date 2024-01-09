def verifica_texto(T):
  if len(T) <= 140:
    return "TWEET"
  else:
    return "MUTE"
T = input("Informa teu tweet: ")
print(verifica_texto(T))