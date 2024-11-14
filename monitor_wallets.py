import time
from datetime import datetime, timedelta, timezone
from solana.rpc.api import Client
from solana.exceptions import SolanaRpcException

# Imposta l'endpoint dell'API
API_ENDPOINT = "https://api.mainnet-beta.solana.com/"
client = Client(API_ENDPOINT)

# Elenco di wallet da analizzare
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

def get_wallet_tokens(wallet_address):
    """Recupera i token detenuti da un wallet."""
    try:
        response = client.get_token_accounts_by_owner(wallet_address, {"programId": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"})
        tokens = []
        for account in response['result']['value']:
            parsed_data = account['account']['data']['parsed']['info']
            token_address = parsed_data.get('mint')
            if token_address:
                tokens.append(token_address)
        return tokens
    except SolanaRpcException as e:
        print(f"Errore nel recuperare i token per il wallet {wallet_address}: {e}")
        return []

def get_recent_transactions(wallet_address, days=30):
    """Recupera le transazioni dell'ultimo mese."""
    try:
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(days=days)

        response = client.get_confirmed_signature_for_address2(wallet_address, limit=1000)
        transactions = response['result']
        recent_transactions = []

        for tx in transactions:
            block_time = datetime.fromtimestamp(tx['blockTime'], timezone.utc)
            if start_time <= block_time <= end_time:
                recent_transactions.append(tx)

        return recent_transactions
    except SolanaRpcException as e:
        print(f"Errore nel recuperare le transazioni per il wallet {wallet_address}: {e}")
        return []

def analyze_wallets():
    """Analizza i wallet specificati."""
    for wallet in wallets:
        print(f"Analizzando il wallet: {wallet}")
        
        # Recupera i token detenuti
        tokens = get_wallet_tokens(wallet)
        print(f"Token detenuti: {tokens}")
        
        # Recupera le transazioni recenti
        recent_transactions = get_recent_transactions(wallet)
        print(f"Transazioni recenti trovate: {len(recent_transactions)}")

        for tx in recent_transactions:
            try:
                tx_detail = client.get_confirmed_transaction(tx['signature'])
                if not tx_detail or 'meta' not in tx_detail:
                    continue
                print(f"Dettaglio transazione {tx['signature']}: {tx_detail}")
            except Exception as e:
                print(f"Errore nel recuperare i dettagli della transazione {tx['signature']}: {e}")
            
            # Pausa per evitare l'errore 429
            time.sleep(0.1)

if __name__ == "__main__":
    analyze_wallets()
