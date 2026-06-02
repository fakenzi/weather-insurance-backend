# 🌧️ Arc Weather Insurance - AI Agent Oracle & Autonomous Payout Engine

[![ARC Network](https://img.shields.io/badge/Network-ARC_Testnet-6366F1?style=for-the-badge)](https://arc.network)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![Circle](https://img.shields.io/badge/Agent_Wallet-Circle_Developer_Controlled_Wallets-7B3FE4?style=for-the-badge&logo=circle)](https://circle.com)
[![WeatherAPI](https://img.shields.io/badge/Weather-WeatherAPI-0EA5E9?style=for-the-badge)](https://www.weatherapi.com)

**The first fully autonomous decentralized parametric weather insurance system on ARC Testnet, powered by Circle Agent Wallet.**

An AI Agent that runs 24/7: scans on-chain policies, fetches high-precision weather data, and automatically triggers payouts **every day at UTC 00:00** using a Circle Developer Controlled Wallet.

---

## ✨ Key Features

- **Circle Agent Wallet Powered** — Secure programmable autonomous execution
- **Daily UTC 00:00 Settlement** — Fixed cron schedule every midnight UTC
- **End-to-End Automation** — Weather check → eligibility → on-chain payout
- **High-Precision Data** — Cumulative rainfall via WeatherAPI
- **Safe & Idempotent** — One payout per policy with retry logic

---

## 🏗️ System Architecture

```mermaid
graph TD
    A[ARC Testnet Contract] -->|Fetch unsettled policies| B[AI Agent Backend]
    B -->|Query WeatherAPI| C[Rainfall Data]
    C --> D{Rainfall ≥ Threshold?}
    D -->|Yes| E[Circle Agent Wallet]
    D -->|No| G[Close Policy / No Payout]
    E -->|triggerPayout()| A
    A -->|USDC Transfer| F[User Wallet]
    
    style E fill:#7B3FE4,stroke:#fff,color:#fff
