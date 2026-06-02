# 🌧️ Arc Weather Insurance - AI Agent Oracle & Autonomous Payout Engine

[![ARC Network](https://img.shields.io/badge/Network-ARC_Testnet-6366F1?style=for-the-badge&logo=blockchain)](https://arc.network)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![Circle](https://img.shields.io/badge/Agent_Wallet-Circle_Developer_Wallets-7B3FE4?style=for-the-badge&logo=circle)](https://circle.com)
[![WeatherAPI](https://img.shields.io/badge/Weather_Data-Open--Meteo_%2F_WeatherAPI-0EA5E9?style=for-the-badge&logo=icloud)](https://open-meteo.com)

**The first fully autonomous decentralized parametric weather insurance system on ARC Testnet, powered by Circle Agent Wallet.**

This repository hosts the **AI Agent Oracle & Automated Settlement Engine** for the Decentralized Parametric Weather Insurance system. Operating as an unattended decentralized oracle, the AI Agent runs 24/7 to monitor on-chain policy logs, fetch real-time global meteorological data, and execute automated claim payouts securely via its built-in programmable wallet.

---

## ✨ Key Features (核心特性)

- **Circle Agent Wallet Powered** — Secure, programmable, and autonomous transaction execution without human intervention.
- **Daily UTC 00:00 Settlement** — Automated cron schedule every midnight UTC to process and settle past-day risk contracts.
- **End-to-End Automation** — Fully automated pipeline: On-chain check → Meteorological data query → Eligibility precision judging → Autonomous Web3 payout.
- **High-Precision Data Oracle** — Integrates multiple enterprise-grade weather APIs (Open-Meteo & WeatherAPI) for reliable cumulative rainfall validation.
- **Safe & Idempotent** — Robust transaction retry logic with strict on-chain safeguards ensuring one unique payout per policy.

---

## 🏗️ System Architecture & Business Workflow (系统架构与业务工作流)

The decentralized insurance ecosystem operates as an autonomous decentralized oracle, seamlessly bridging real-world meteorological data with the blockchain. The system consists of three core components:

1. **On-Chain Smart Contract**: Hosted on the **ARC Network Testnet** (`WeatherInsurance.sol`), managing premium collection (10% premium mechanism) and holding pool liquidity.
2. **Web3 Frontend Dashboard**: Built with **React + Wagmi** to visualize live on-chain metrics, including total active policies, pool balance, and cumulative payouts.
3. **AI Agent Backend (This Repo)**: A **Python-powered**, unattended execution engine that handles data ingestion, precision judging, and autonomous settlement.

---

### 🔄 Core Oracle Workflow (核心工作流)

The AI Agent triggers the automated settlement loop on a fixed cron schedule **every day at UTC 00:00**. The end-to-end business logic and transaction flow are structured as follows:

```text
========================================================================================
                                 ORACLE INTERACTION FLOW
========================================================================================

    [ ARC Testnet Contract ] 
       │                ▲
       │                │
(1. Fetch Policies) (4. triggerPayout via Circle Wallet)
       │                │
       ▼                │
    [    AI Agent Backend (Python Execution Engine)    ]
       │                ▲
       │                │
(2. Request Coordinates) (3. Return Cumulative Rainfall)
       │                │
       ▼                │
    [  Weather Data Oracle (Open-Meteo / WeatherAPI)  ]

========================================================================================
                             BACKEND ENGINE JUDGEMENT LOGIC
========================================================================================

               +-----------------------------------------+
               |       Extract Rainfall from Data        |
               +-----------------------------------------+
                                    │
                                    ▼
                      /---------------------------\
                     /                             \
                    <     Rainfall >= Threshold?    >
                     \                             /
                      \---------------------------/
                                    │
                   +----------------+----------------+
                   |                                 |
                [ Yes ]                           [ No ]
                   │                                 │
                   ▼                                 ▼
    +------------------------------+   +------------------------------+
    | Call Circle Agent Wallet     |   | Invoke On-Chain Closing Log  |
    | Sign & Broadcast Payout Tx   |   | Mark Policy as Expired       |
    +------------------------------+   +------------------------------+
                   │                                 │
                   ▼                                 ▼
    +------------------------------+   +------------------------------+
    | [Transfer USDC to User]      |   | [No Premium Transferred]     |
    +------------------------------+   +------------------------------+

## 🚀 Getting Started (快速开始)

Follow these steps to clone, configure, and run the AI Agent Oracle locally or on your server.

### 1. Clone the Repository (克隆项目)
```bash
git clone [https://github.com/fakenzi/weather-insurance-backend.git](https://github.com/fakenzi/weather-insurance-backend.git)
cd weather-insurance-backend

2. Install Dependencies (安装依赖)
Ensure you have Python 3.10+ installed. Then run:
pip install -r requirements.txt


3. Environment Configuration (环境变量配置)
Create a .env file in the root directory and configure your credentials:
# Circle Agent Wallet
CIRCLE_API_KEY=

ENTITY_SECRET=
AGENT_WALLET_ID=

CIRCLE_AGENT_ADDRESS=
CONTRACT_ADDRESS=
WEATHER_API_KEY=
4. Run the Application (运行服务)
# Development (开发模式)
uvicorn main:app --reload
# Production (生产模式)
uvicorn main:app --host 0.0.0.0 --port 8080
📺 Expected Output (运行预期输出)
⏰ Agent Scheduler started | Daily settlement at UTC 00:00
📅 Next run: 2026-06-03 00:00:00 UTC

