import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

class SystemeMasseRessortAmortisseur:
    def __init__(self, m, a, k, x0, v0):
        self.m = m
        self.a = a
        self.k = k
        self.x0 = x0
        self.v0 = v0

    def resolver(self, force_exterieure, t_start, t_end, dt):
        t = np.arange(t_start, t_end, dt)
        x_init = np.array([self.x0, self.v0])
        x_solution = odeint(self.systeme, x_init, t, args=(force_exterieure,))
        return t, x_solution

    def systeme(self, x, t, force_exterieure):
        x1, x2 = x[0], x[1]
        dx1dt = x2
        dx2dt = (force_exterieure(t) - self.a * x2 - self.k * x1) / self.m
        return [dx1dt, dx2dt]

def force_exterieure_a(t):
    return 0.0

def force_exterieure_b(t):
    F0 = 100.0
    w = 10.0
    return F0 * np.cos(w * t)

# Paramètres du système
m = 10.0  # Masse en kg
a = 20.0  # Coefficient de frottement de l'amortisseur en Ns/m
k = 4000.0  # Constante de raideur du ressort en N/m
x0 = 0.01  # Position initiale en m
v0 = 0.0  # Vitesse initiale en m/s
t_start = 0.0
t_end = 10.0  # Temps final
dt = 0.01  # Pas de temps

# Création des instances du système pour les deux cas
systeme_a = SystemeMasseRessortAmortisseur(m, a, k, x0, v0)
systeme_b = SystemeMasseRessortAmortisseur(m, a, k, x0, v0)

# Résolution de l'équation différentielle pour les deux cas
t_a, x_solution_a = systeme_a.resolver(force_exterieure_a, t_start, t_end, dt)
t_b, x_solution_b = systeme_b.resolver(force_exterieure_b, t_start, t_end, dt)

# Plot de la réponse du système pour les deux cas
plt.figure()
plt.subplot(2, 1, 1)
plt.plot(t_a, x_solution_a[:, 0], label='Position (m)')
plt.plot(t_a, x_solution_a[:, 1], label='Vitesse (m/s)')
plt.xlabel('Temps (s)')
plt.ylabel('Position, Vitesse')
plt.legend()
plt.title('Réponse du système masse-ressort-amortisseur (Cas a)')
plt.subplot(2, 1, 2)
plt.plot(t_b, x_solution_b[:, 0], label='Position (m)')
plt.plot(t_b, x_solution_b[:, 1], label='Vitesse (m/s)')
plt.xlabel('Temps (s)')
plt.ylabel('Position, Vitesse')
plt.legend()
plt.title('Réponse du système masse-ressort-amortisseur (Cas b)')
plt.show()

# Calcul des énergies cinétique, potentielle et mécanique pour le cas a)
Ec_a = 0.5 * m * x_solution_a[:, 1]**2
Ep_a = 0.5 * k * x_solution_a[:, 0]**2
Em_a = Ec_a + Ep_a

# Plot de l'Ep, l'Ec et l'Em
plt.figure()
plt.plot(t_a, Ec_a, label='Energie cinétique')
plt.plot(t_a, Ep_a, label='Energie potentielle')
plt.plot(t_a, Em_a, label='Energie mécanique')
plt.xlabel('Temps (s)')
plt.ylabel('Ec, Ep et Em (J)')
plt.legend()
plt.title('Ec, Ep et Em à tout instant')
plt.show()
