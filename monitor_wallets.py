import time
from solana.rpc.api import Client
from solana.publickey import PublicKey
from datetime import datetime, timedelta

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
    "5UmdfKDoowTJ5DBYRUyq8HMH8KLuUb35Ko8rzrEuh5gy"
]

# Funzione per recuperare le transazioni degli ultimi 30 giorni con ritentativi
def get_recent_transactions(address, retries=3, delay=5, days=30):
    attempt = 0
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=days)
    while attempt < retries:
        try:
            response = client.get_signatures_for_address(
                PublicKey(address),
                until=None
            )
            if response.get('result') is None:
                print(f"Nessuna transazione trovata per l'indirizzo {address}")
                return []
            
            recent_transactions = []
            for tx in response['result']:
                block_time = datetime.utcfromtimestamp(tx['blockTime'])
                if start_time <= block_time <= end_time:
                    recent_transactions.append(tx)
            
            return recent_transactions
        except Exception as e:
            attempt += 1
            print(f"Errore nel recuperare le transazioni per {address}: {e}. Tentativo {attempt}/{retries}")
            time.sleep(delay)
    print(f"Errore persistente nel recuperare le transazioni per {address}")
    return []

# Funzione per verificare i token detenuti da un indirizzo
def get_tokens_in_wallet(address):
    try:
        response = client.get_token_accounts_by_owner(PublicKey(address), {"programId": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"})
        tokens = []
        for account in response['result']['value']:
            token_address = account['account']['data']['parsed']['info']['mint']
            tokens.append(token_address)
        return tokens
    except Exception as e:
        print(f"Errore nel recuperare i token per il wallet {address}: {e}")
        return []

# Funzione per analizzare i token e le transazioni recenti
def analyze_wallets():
    token_summary = {}
    for address in addresses:
        print(f"\nAnalizzando il wallet: {address}")
        
        # Recupera i token detenuti
        tokens = get_tokens_in_wallet(address)
        print(f"Token detenuti: {tokens}")
        
        # Recupera transazioni recenti
        recent_transactions = get_recent_transactions(address)
        print(f"Transazioni recenti trovate: {len(recent_transactions)}")
        
        for tx in recent_transactions:
            tx_detail = client.get_confirmed_transaction(tx['signature'])
            if not tx_detail or 'meta' not in tx_detail:
                continue
            
            # Analizza i bilanci post-transazione
            post_balances = tx_detail['meta']['postTokenBalances']
            for balance in post_balances:
                mint = balance['mint']
                owner = balance.get('owner', 'N/A')
                
                if mint not in token_summary:
                    token_summary[mint] = {'acquisti': 0, 'vendite': 0, 'holder': set()}
                
                token_summary[mint]['holder'].add(owner)
                
                if owner == address:  # Entrata
                    token_summary[mint]['acquisti'] += 1
                else:  # Uscita
                    token_summary[mint]['vendite'] += 1
        
    # Analizza i token comuni
    sorted_tokens = sorted(token_summary.items(), key=lambda x: x[1]['acquisti'], reverse=True)
    print("\nToken comuni negli ultimi 30 giorni:")
    for token, stats in sorted_tokens:
        print(f"Token: {token}, Acquisti: {stats['acquisti']}, Vendite: {stats['vendite']}, Holder unici: {len(stats['holder'])}")

# Avvia l'analisi
analyze_wallets()
