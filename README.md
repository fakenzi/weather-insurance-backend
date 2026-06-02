# 🌦️ Arc Weather Insurance - AI Agent Oracle & Backend

[![ARC Network](https://img.shields.io/badge/Network-ARC_Testnet-6366F1?style=for-the-badge&logo=blockchain)](https://arc.network)
[![Python](https://img.shields.io/badge/Backend-Python_3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![API-Provider](https://img.shields.io/badge/Weather_Data-Open--Meteo-0EA5E9?style=for-the-badge&logo=icloud)](https://open-meteo.com)

This repository hosts the **AI Agent Oracle & Automated Settlement Engine** for the Decentralized Parametric Weather Insurance system built on the **ARC Testnet**.

Operating as an autonomous decentralized oracle, the AI Agent periodically monitors on-chain policy logs, fetches real-time global meteorological data, and executes automated claim payouts via its built-in **Agent Wallet**.

---

## 💻 System Architecture & Business Workflow

The decentralized insurance ecosystem consists of three core components:
1. **On-Chain Smart Contract**: Hosted on the ARC Network (`WeatherInsurance.sol`), managing premium collection (10% premium mechanism) and automated payouts.
2. **Web3 Frontend Dashboard**: Built with React + Wagmi to visualize live on-chain metrics, including total policies, pool balance, and cumulative payouts (Total Paid).
3. **AI Agent Backend (This Repo)**: A Python-powered, unattended cron-job execution engine.

### 🔄 Agent Core Workflow Sequence
```text
[Smart Contract] ──(Sync Unsettled Policies)──> [AI Agent Backend]
                                                        │
                                         (Fetch Geo-Coordinates API)
                                                        ▼
[On-chain Settlement] <──(Agent Wallet Broadcast)── [Open-Meteo Precision Judging]
