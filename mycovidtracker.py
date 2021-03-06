# (c) Dominique Béréziat
# Licence LGPL
import pandas as pd
import matplotlib.pyplot as plt

#hopitaux = pd.read_csv('data/donnees-hospitalieres',sep=';')
hopitaux = pd.read_csv('https://www.data.gouv.fr/fr/datasets/r/63352e38-d353-4b54-bfd1-f1b3ee1cabd7',sep=';')
tests = pd.read_csv('https://www.data.gouv.fr/fr/datasets/r/406c6a23-e283-4300-9484-54e78c8ae675',sep=';')

# Ne garder que les enregistrements tels que sexe==0, réindexer et nettoyer
hopitaux = hopitaux[hopitaux.sexe==0].reset_index(drop=True).drop(columns='sexe')

# Grouper par date et sommer les autres champs, les dates deviennent les clés
hopitaux = hopitaux.groupby(['jour']).sum()

# tests pour toute classe d'âge
tests = tests[tests.cl_age90==0]

# groupement par date et fusion
tests = tests.groupby(['jour']).sum()

# calcul positivité
pos = tests['P']/tests['T']*100

# décumuler une somme (sans numpy)
def uncumsum(t):
    shifted = pd.concat([pd.Series([0]), t[:-1]])
    shifted.index=t.index
    return t - shifted

# Grapher ce qu'on veut
plt.suptitle('My Covidtracker')
plt.subplot(2,2,1)
plt.grid(True)
plt.grid(which='major')
plt.title('Hospitalisation')
hopitaux.hosp.rolling(7,center=True).mean().plot(label='fenêtre glissante')

plt.subplot(2,2,2)
plt.ylabel('%')
plt.grid(which='major')
plt.title('Tests (positivité)')
pos.rolling(7,center=True).mean().plot(label='')

plt.subplot(2,2,3)
plt.title('Réanimation')
plt.grid(which='major')
hopitaux.rea.rolling(7,center=True).mean().plot(label='smoothed rea')
plt.xlabel('')

plt.subplot(2,2,4)
plt.title('Décès')
plt.grid(which='major')
dc2 = uncumsum(hopitaux.dc)
dc2.rolling(7,center=True).mean().plot(label='décès, fenêtre glissante 7 jours')
plt.plot(dc2,'.',markersize=1)
plt.gcf().autofmt_xdate()
plt.xlabel('')
plt.legend()
plt.show()

