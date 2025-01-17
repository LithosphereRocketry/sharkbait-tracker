#!/usr/bin/python3
# Calculations for RF frontend based on STM32WL documentation
# (assuming embedded SX1262 IP is close in behavior to LLCC68):
# https://www.st.com/resource/en/application_note/an5457-rf-matching-network-design-guide-for-stm32wl-series-stmicroelectronics.pdf

from cmath import *

freq = 896e6 # Split the difference between 868 and 915 MHz so we should get
             # OK performance on both

# Conjugate of load-pull value from SX126x AN (very similar to STM32WL, so
# presumably also similar to LLCC68)
z_load_pull = 11.7 + 4.8j
Zout = z_load_pull.conjugate()

Rout = Zout.real
Cout = -1/(2*pi*freq*Zout.imag)

print("Output equivalent:", Rout, "ohms", Cout*1e12, "pF")

m = sqrt(50/Rout - 1)
L1 = abs(1/(2*pi*freq) * ((50*m)/(m**2 + 1) - Zout.imag))
C1 = abs(1/(2*pi*freq) * (sqrt(Rout/50 * (1 + m**2) - 1) + m) / (Rout*(1 + m**2)))

print("PA output matching:", L1*1e9, "nH", C1*1e12, "pF")

# Second harmonic notch filter

H2 = freq*2
# L2 = L1 * 3/4 # This is STM's "rule of thumb"
L2 = 3.9e-9 # This is very close to above, and is a JLC basic part
C2 = 1/((2*pi*H2)**2 * L2)

print("H2 notch filter:", L2*1e9, "nH", C2*1e12, "pF")

# I'm not considering the mismatch-correction steps in this, just the filter
# design, since I still don't 100% get if those are supposed to be possible to
# compute without testing

# Upper harmonics LPF
Llpf = 50 / (2*pi*freq)
Clpf = 0.95 / (50 * 2*pi*freq)
print("Upper harmonics low-pass:", Llpf*1e9, "nH", Clpf*1e12, "pF")