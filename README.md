# 🌧️ **Arc Weather Insurance** - AI Agent Oracle & Autonomous Payout Engine

[![ARC Network](https://img.shields.io/badge/Network-ARC_Testnet-6366F1?style=for-the-badge)](https://arc.network)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![Circle](https://img.shields.io/badge/Agent_Wallet-Circle_Developer_Controlled_Wallets-7B3FE4?style=for-the-badge&logo=circle)](https://circle.com)
[![WeatherAPI](https://img.shields.io/badge/Weather-WeatherAPI-0EA5E9?style=for-the-badge)](https://www.weatherapi.com)

**The first fully autonomous decentralized parametric weather insurance system on ARC Testnet, powered by Circle Agent Wallet.**

An AI Agent that runs 24/7: it scans on-chain policies, fetches high-precision weather data, and automatically triggers payouts using a **Circle Developer Controlled Wallet** — no human intervention required.

---

## ✨ Key Features

- **Circle Agent Wallet Powered** — Fully autonomous on-chain execution using Circle Developer Controlled Wallets
- **End-to-End Automation** — Real-time weather monitoring → condition evaluation → automatic `triggerPayout()`
- **High-Precision Weather Data** — Cumulative rainfall from WeatherAPI (global coverage)
- **Idempotent & Secure** — One-time payout per policy with retry logic and failure isolation
- **Production Ready** — Async tasks, structured logging, and robust error handling
- **Live Dashboard APIs** — Easy monitoring of policies, pool balance, and Agent status

---

## 🏗️ System Architecture

```mermaid
graph TD
    A[ARC Testnet Smart Contract] -->|Fetch unsettled policies| B[AI Agent Backend]
    B -->|Query WeatherAPI| C[High-Precision Rainfall Data]
    C -->|Rainfall ≥ Threshold?| D{Yes}
    D -->|Yes| E[Circle Agent Wallet]
    E -->|Execute triggerPayout()| A
    A -->|USDC Auto Transfer| F[User Wallet]
    style E fill:#7B3FE4,stroke:#fff,color:#fff
```

##  Quick Start
1. Clone the Repository
git clone https://github.com/fakenzi/weather-insurance-backend.git
cd weather-insurance-backend

2. Install Dependencies
pip install -r requirements.txt
3. Configure Environment Variables (.env)

CIRCLE_API_KEY=
ENTITY_SECRET=
AGENT_WALLET_ID=

CIRCLE_AGENT_ADDRESS=
CONTRACT_ADDRESS=
WEATHER_API_KEY=

# Development
uvicorn main:app --reload

# Production (recommended port)
uvicorn main:app --host 0.0.0.0 --port 8080
When started, you will see logs like:


⏰ Agent Scheduler started | Daily settlement at UTC 00:00
📅 Next run: 2026-06-03 00:00:00 UTC
⏳ 距离下次结算还有 23小时 15分钟
 ```

##Tech Stack


Autonomous Execution: Circle Developer Controlled Wallets
Scheduler: APScheduler (CronTrigger UTC 00:00)
Backend: FastAPI + AsyncIO
Blockchain: Web3.py + ARC Testnet
Weather Data: WeatherAPI





   
