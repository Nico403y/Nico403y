from machine import Pin, PWM
from machine import Pin, ADC
from random import randint
from time import sleep
sens = ADC(Pin(36))
start_duty = 1023
frequency = 5000
r = PWM(Pin(18), frequency, start_duty)
g = PWM(Pin(5), frequency, start_duty)
b = PWM(Pin(19), frequency, start_duty)


while True:
    sens_val = sens.read()
    spaending = sens_val * (3.3/4096)
    Procent = sens_val / 40.96
    print("Analog sensor vaerdi:", sens_val)
    print("Spaending :", spaending)
    print("Procent :", Procent)
    sleep(1)
    if Procent < 20:
        print("nu er der under 20%!")
        r.duty(randint(0, 1023))
        g.duty(randint(0, 1023))
        b.duty(randint(0, 1023))
    else:
        print("nu er der over 20%!")
        r.duty(randint(1023, 1023,))
        g.duty(randint(1023, 1023,))
        b.duty(randint(1023, 1023,))
