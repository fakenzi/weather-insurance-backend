# 🌧️ **Arc Weather Insurance** - AI Agent Oracle & Autonomous Payout Engine

[![ARC Network](https://img.shields.io/badge/Network-ARC_Testnet-6366F1?style=for-the-badge)](https://arc.network)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![Circle](https://img.shields.io/badge/Agent_Wallet-Circle_Developer_Controlled_Wallets-7B3FE4?style=for-the-badge&logo=circle)](https://circle.com)
[![WeatherAPI](https://img.shields.io/badge/Weather-WeatherAPI-0EA5E9?style=for-the-badge)](https://www.weatherapi.com)

**The first fully autonomous decentralized parametric weather insurance system on ARC Testnet, powered by Circle Agent Wallet.**

An AI Agent that runs 24/7: scans on-chain policies, fetches high-precision weather data, and **automatically triggers payouts at UTC 00:00 every day** using a Circle Developer Controlled Wallet.

---

## ✨ Key Features

- **Circle Agent Wallet Powered** — Secure, programmable autonomous execution
- **Daily UTC 00:00 Settlement** — Fixed daily automatic settlement cycle
- **End-to-End Automation** — Weather data → condition check → on-chain payout
- **High-Precision Oracle** — Cumulative rainfall via WeatherAPI (global cities)
- **Idempotent & Safe** — One payout per policy, retry logic, failure isolation
- **Production Ready** — APScheduler + AsyncIO + Structured Logging

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
 Quick Start1. Clonebash

git clone https://github.com/fakenzi/weather-insurance-backend.git
cd weather-insurance-backend

2. Installbash

pip install -r requirements.txt

3. .envenv

# Circle Agent Wallet
CIRCLE_API_KEY=

ENTITY_SECRET=
AGENT_WALLET_ID=

CIRCLE_AGENT_ADDRESS=
CONTRACT_ADDRESS=
WEATHER_API_KEY=


4. Runbash

# Development
uvicorn main:app --reload

# Production
uvicorn main:app --host 0.0.0.0 --port 8080

You will see:

⏰ Agent Scheduler started | Daily settlement at UTC 00:00
📅 Next run: 2026-06-03 00:00:00 UTC
```
# Tech Stack
Autonomous Execution: Circle Developer Controlled Wallets
Scheduler: APScheduler (UTC 00:00)
Backend: FastAPI + AsyncIO
Blockchain: Web3.py + ARC Testnet
Weather: WeatherAPI




