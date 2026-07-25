temperatura_celsius = 40
conversor = lambda c: (c * 1.8) + 32
temperatura_fahrenheit = conversor(temperatura_celsius)

if temperatura_fahrenheit > 100:
    print("Alerta de calor")
else:
    print("Temperatura normal")