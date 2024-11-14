from solana.rpc.api import Client
import time
from datetime import datetime

# Impostare il client Solana (usiamo l'endpoint di Solana Explorer)
client = Client("https://api.mainnet-beta.solana.com")

# Elenco di indirizzi da monitorare
addresses = [
    "8zFZHuSRuDpuAR7J6FzwyF3vKNx4CVW3DFHJerQhc7Zd",
    "3STS7sBe5xzMycHBGx1HJNzPtry1MsgQV6wDxkMt6iV7",
    "4K8zXYyPYVqTtnXe7bU3fThEUpwzgzP9ZB19MS4cWPvN",
    "HbxY4qVrKftfsKiMQ5wPvRLKUMDTRBrVRhBLv6mDzcF8",
    "ASmC3E5hwp4p7GDnQFuE5RUKcPaUsrwmnrFohcmnZaPh",
    "8v2tXQVEQcwhGYUX7728iKwb61TJ5mKDGjBdw9gmRcij",
    "3ZEA5o1eb9PWUmJg1CucyXPS1jud2o1b7558uQpAG2B1",
    "7UNP1m8bhjyTBSBWoFJQvsyRarWGziP6UhesstBCfA4Y",
    "3hB6a7V2YogLdVwwnQyLFH3u1wu8Gnj8bhG32D4YXUHb",
    "214567edYgNcFnEpnW11z39GZfUdo47mc61gDZpi7HNB",
    "4d9mokpWNLD5mTfutxAbKojedudfY5FCStCo1h8WR24c",
    "5UiPHopgEiS1EX5dUB8Aueh1T8aif7PAqCRm9QLmJC7x",
    "JDNooC8zhQcjNq8tsUcS9cdGiuAdR5gishqUVEVMARVz",
    "3drY9kTvdcRXHEDUkqncyXAVqEnFLDHckiDPM7ApegmT",
    "5B4bSL2bbd9y2Kp1SfjkxWUzdFTC2ysBaHpKuHpUESQH",
    "5UmdfKDoowTJ5DBYRUyq8HMH8KLuUb35Ko8rzrEuh5gy",
]

# Token da escludere (SOL, USDT, USDC)
excluded_tokens = [
    "So11111111111111111111111111111111111111112",  # SOL
    "Es9vMFrjJh9uQU6hdXw6dTmLJ2Vkcxyg2HgsF1ihy4rb",  # USDT (Tether)
    "EPjFWdd5Vq2X4lqGp8j3RysA6brrx3N1Wq2Q7jZPjp9f"   # USDC (USD Coin)
]

# Funzione per recuperare le transazioni di un indirizzo
def get_transactions(address):
    response = client.get_signatures_for_address(address)
    return response['result']

# Funzione per verificare se una transazione coinvolge un token escludendo SOL, USDT, USDC
def is_non_excluded_token_transaction(transaction):
    token_mints = []
    
    # Cerca tra i token della transazione (cerca nel 'meta' per postBalances)
    for item in transaction['meta']['postBalances']:
        if item['mint'] not in excluded_tokens:
            token_mints.append(item['mint'])
    
    return token_mints

# Funzione per analizzare le transazioni e distinguere acquisti e vendite
def analyze_transaction(tx, token_mints, address, token_count):
    # Separare le transazioni di acquisto (ricezione) e vendita (invio)
    for mint in token_mints:
        if mint not in token_count:
            token_count[mint] = {'acquisti': 0, 'vendite': 0}
        
        # Identifica se l'indirizzo è il mittente (vendita) o il destinatario (acquisto)
        if tx['transaction']['message']['accountKeys'][0] == address:
            # Se l'indirizzo è il mittente, è una vendita
            token_count[mint]['vendite'] += 1
        else:
            # Se l'indirizzo è il destinatario, è un acquisto
            token_count[mint]['acquisti'] += 1

# Funzione per monitorare i token ricorrenti e analizzare acquisti e vendite
def track_recurring_tokens():
    # Dizionario per memorizzare la frequenza di ciascun token
    token_count = {}
    
    # Monitoraggio continuo delle transazioni
    while True:
        for address in addresses:
            transactions = get_transactions(address)
            for tx in transactions:
                token_mints = is_non_excluded_token_transaction(tx)
                
                # Se sono stati trovati token (escludendo SOL, USDT, USDC)
                if token_mints:
                    for mint in token_mints:
                        if mint not in token_count:
                            token_count[mint] = {'acquisti': 0, 'vendite': 0}
                        
                        # Analizza la transazione per acquisti e vendite
                        analyze_transaction(tx, token_mints, address, token_count)
        
        # Ordinare i token per frequenza e stampare i più comuni
        print("Token Ricorrenti:")
        sorted_tokens = sorted(token_count.items(), key=lambda item: item[1]['acquisti'], reverse=True)
        
        # Crea il nome del file con la data corrente
        today = datetime.today().strftime('%Y-%m-%d')
        filename = f"analisi_{today}.txt"
        
        # Scrivere i risultati in un file di testo
        with open(filename, "w") as file:
            file.write(f"Analisi dei Wallet - {today}\n\n")
            for token, counts in sorted_tokens[:10]:  # Mostra i 10 token più ricorrenti
                file.write(f"Token: {token}, Acquisti: {counts['acquisti']}, Vendite: {counts['vendite']}\n")
                
                # Analisi speculativa (più acquisti che vendite)
                if counts['acquisti'] > counts['vendite']:
                    file.write(f"Possibile speculazione: Più acquisti di {token} rispetto alle vendite.\n")
        
        # Pausa prima di eseguire di nuovo il ciclo
        time.sleep(10)  # Controlla ogni 10 secondi

# Avvia il monitoraggio
track_recurring_tokens()


