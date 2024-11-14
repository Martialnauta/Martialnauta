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

    from solana.rpc.api import Client
import time
from datetime import datetime

# Impostare il client Solana (usiamo l'endpoint di Solana Explorer)
client = Client("https://api.mainnet-beta.solana.com")

# Elenco di indirizzi da monitorare
addresses = [
    "8zFZHuSRuDpuAR7J6FzwyF3vKNx4CVW3DFHJerQhc7Zd",
    "3STS7sBe5xzMycHBGx1HJNzPtry1MsgQV6wDxkMt6iV7",
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
    "ASmC3E5hwp4p7GDnQFuE5RUKcPaUsrwmnrFohcmnZaPh",
    "HbxY4qVrKftfsKiMQ5wPvRLKUMDTRBrVRhBLv6mDzcF8",
    "8v2tXQVEQcwhGYUX7728iKwb61TJ5mKDGjBdw9gmRcij",
    "3ZEA5o1eb9PWUmJg1CucyXPS1jud2o1b7558uQpAG2B1",
    "7UNP1m8bhjyTBSBWoFJQvsyRarWGziP6UhesstBCfA4Y",
    "3hB6a7V2YogLdVwwnQyLFH3u1wu8Gnj8bhG32D4YXUHb",
    "214567edYgNcFnEpnW11z39GZfUdo47mc61gDZpi7HNB",
    "4d9mokpWNLD5mTfutxAbKojedudfY5FCStCo1h8WR24c",
    "5UiPHopgEiS1EX5dUB8Aueh1T8aif7PAqCRm9QLmJC7x",
    "5UiPHopgEiS1EX5dUB8Aueh1T8aif7PAqCRm9QLmJC7x",
    # Aggiungi altri indirizzi qui
]

# Token da escludere (SOL, USDT, USDC)
excluded_tokens = [
    "So11111111111111111111111111111111111111112",  # SOL
    "Es9vMFrjJh9uQU6hdXw6dTmLJ2Vkcxyg2HgsF1ihy4rb",  # USDT (Tether)
    "EPjFWdd5Vq2X4lqGp8j3RysA6brrx3N1Wq2Q7jZPjp9f"   # USDC (USD Coin)
]

# Funzione per recuperare le transazioni di un indirizzo
def get_transactions(address):
    response = client.get_signatures_for_address(address, limit=10)  # Limita il numero di transazioni per chiamata
    return response['result']

# Funzione per verificare se una transazione coinvolge un token escludendo SOL, USDT, USDC
def is_non_excluded_token_transaction(transaction):
    token_mints = []
    
    # Verifica nel campo 'meta' o in altri campi che contengono i dettagli sui token
    if 'meta' in transaction and 'tokenTransfers' in transaction['meta']:
        for transfer in transaction['meta']['tokenTransfers']:
            if transfer['mint'] not in excluded_tokens:
                token_mints.append(transfer['mint'])
    
    return 

    # Aggiungi altri indirizzi qui
]

# Token da escludere (SOL, USDT, USDC)
excluded_tokens = [
    "So11111111111111111111111111111111111111112",  # SOL
    "Es9vMFrjJh9uQU6hdXw6dTmLJ2Vkcxyg2HgsF1ihy4rb",  # USDT (Tether)
    "EPjFWdd5Vq2X4lqGp8j3RysA6brrx3N1Wq2Q7jZPjp9f"   # USDC (USD Coin)
]

# Funzione per recuperare le transazioni di un indirizzo
def get_transactions(address):
    response = client.get_signatures_for_address(address, limit=10)  # Limita il numero di transazioni per chiamata
    return response['result']

# Funzione per verificare se una transazione coinvolge un token escludendo SOL, USDT, USDC
def is_non_excluded_token_transaction(transaction):
    token_mints = []
    
    # Verifica nel campo 'meta' o in altri campi che contengono i dettagli sui token
    if 'meta' in transaction and 'tokenTransfers' in transaction['meta']:
        for transfer in transaction['meta']['tokenTransfers']:
            if transfer['mint'] not in excluded_tokens:
                token_mints.append(transfer['mint'])
    
    return 

    # Aggiungi altri indirizzi qui
]

# Token da escludere (SOL, USDT, USDC)
excluded_tokens = [
    "So11111111111111111111111111111111111111112",  # SOL
    "Es9vMFrjJh9uQU6hdXw6dTmLJ2Vkcxyg2HgsF1ihy4rb",  # USDT (Tether)
    "EPjFWdd5Vq2X4lqGp8j3RysA6brrx3N1Wq2Q7jZPjp9f"   # USDC (USD Coin)
]

# Funzione per recuperare le transazioni di un indirizzo
def get_transactions(address):
    response = client.get_signatures_for_address(address, limit=10)  # Limita il numero di transazioni per chiamata
    return response['result']

# Funzione per verificare se una transazione coinvolge un token escludendo SOL, USDT, USDC
def is_non_excluded_token_transaction(transaction):
    token_mints = []
    
    # Verifica nel campo 'meta' o in altri campi che contengono i dettagli sui token
    if 'meta' in transaction and 'tokenTransfers' in transaction['meta']:
        for transfer in transaction['meta']['tokenTransfers']:
            if transfer['mint'] not in excluded_tokens:
                token_mints.append(transfer['mint'])
    
    return 

