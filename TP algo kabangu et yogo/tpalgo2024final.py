from typing import List, Dict, Any

class Client:
    def __init__(self, nom: str, dateNaissance: str, numerosTelephone: List[str]):
        self.nom = nom
        self.dateNaissance = dateNaissance
        self.numerosTelephone = numerosTelephone
        self.factureDollars = 0.0

class ImportCDR:
    def __init__(self):
        self.cdr_stack = []

    def fichier_cdr(self, path: str):
        with open(path, 'r') as file:
            for l in file:
                info = l.strip().split('|')
                if len(info) == 8:
                    cdr_info = {'type_call': int(info[1]), 'duree': int(info[5]) if info[5] else 0, 'taxe': int(info[6]), 'total_volume': int(info[7]) if info[7] else 0, 'appelant': info[3], 'appele': info[4], 'date_heure': info[2]}
                    self.cdr_stack.append(cdr_info)

class Facture:
    @staticmethod
    def _calculer_montant(cdr: Dict[str, Any], client: Client) -> float:
        base_price = (cdr['total_volume'] * 0.03) if cdr['type_call'] == 2 else (cdr['duree'] * (0.025 if cdr['type_call'] == 0 else 0.001 if cdr['type_call'] == 1 and cdr.get('appelant') in client.numerosTelephone and cdr.get('appele') and cdr['appele'].startswith(('24381', '24382', '24383')) else 0.002))
        tax_rate = 0.1 if cdr['taxe'] == 1 else 0.16 if cdr['taxe'] == 2 else 0
        return base_price + (base_price * tax_rate)

    @staticmethod
    def montantFacture(client: Client, cdr_stack: List[Dict[str, Any]]) -> float:
        return sum(Facture._calculer_montant(cdr, client) for cdr in cdr_stack)

class Statistiques:
    @staticmethod
    def calculer_statistiques_client(client: Client, cdr_stack: List[Dict[str, Any]], periode: str) -> Dict[str, Any]:
        return {'Nombre d\'appels': sum(1 for cdr in cdr_stack if cdr['type_call'] == 0 and cdr.get('appelant') in client.numerosTelephone and cdr.get('date_heure') and cdr['date_heure'].startswith(periode)),
                'Durée totale des appels (secondes)': sum(cdr['duree'] for cdr in cdr_stack if cdr['type_call'] == 0 and cdr.get('appelant') in client.numerosTelephone and cdr.get('date_heure') and cdr['date_heure'].startswith(periode)),
                'Nombre de SMS': sum(1 for cdr in cdr_stack if cdr['type_call'] == 1 and cdr.get('appelant') in client.numerosTelephone and cdr.get('date_heure') and cdr['date_heure'].startswith(periode)),
                'Volume internet utilisé (gigaoctets)': sum(cdr['total_volume'] / 1024 for cdr in cdr_stack if cdr['type_call'] == 2 and cdr.get('appelant') in client.numerosTelephone and cdr.get('date_heure') and cdr['date_heure'].startswith(periode))}

# Instanciation des classes et importation des données
CDR = ImportCDR()
CDR.fichier_cdr("cdr.txt")
CDR.fichier_cdr("tp_algo-1.txt")

# Affichage de la pile de dictionnaires des fichiers CDR
print("Pile de dictionnaires des fichiers CDR :")
for cdr_info in CDR.cdr_stack:
    print(cdr_info)

# Création de l'instance du client POLYTECHNIQUE
client_polytechnique = Client("POLYTECHNIQUE", "28-10-2001", ["243818140560", "243818140120"])

# Définir la période pour couvrir tout le mois de janvier 2023
periode = "2023"

# Génération de la facture pour le client POLYTECHNIQUE en dollars
facture_dollars = Facture.montantFacture(client_polytechnique, CDR.cdr_stack)

# Calcul des statistiques pour le client POLYTECHNIQUE sur une période spécifique
statistiques = Statistiques.calculer_statistiques_client(client_polytechnique, CDR.cdr_stack, periode)

print("\n" + "=" * 50)
print("FACTURE DETAILLEE POUR LE CLIENT POLYTECHNIQUE")
print("=" * 50)
print(f"{'Nom du client:':<35}{client_polytechnique.nom}")
print(f"{'Date de naissance:':<35}{client_polytechnique.dateNaissance}")
print(f"{'Numéros de téléphone:':<35}{', '.join(client_polytechnique.numerosTelephone)}")
print(f"{'Montant total en dollars:':<35}{facture_dollars} dollars")
print("-" * 50)
print(f"{'Statistiques pour la période spécifiée:':^50}")
print("-" * 50)
for key, value in statistiques.items():
    print(f"{key:<40}{value:>10}")
print("=" * 50)

