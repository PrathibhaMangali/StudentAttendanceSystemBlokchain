# Student Attendance Management System using Blockchain — Comparative Analysis of Client-Server, P2P & Hybrid Models

A student attendance system that stores attendance and student records on a blockchain (Solidity smart contract) instead of a traditional centralized database. The project implements and compares three network architectures — Client-Server, Peer-to-Peer, and a Hybrid model — to evaluate which offers the best trade-off between availability, cost, and tamper-proof data integrity for attendance tracking.

## Architecture

- **Web layer**: Django app (`manage.py`) — handles UI, student/attendance entry, and admin views
- **Blockchain layer** (`blockchain/`): Solidity smart contract (`Attendance.sol`) deployed to a local/test chain, storing student records and attendance logs immutably. `Attendance.json` is the compiled contract ABI used by the app to interact with it.
- **Client-Server layer** (`network/ClientServer.py`): A traditional centralized socket server (port 2222) — all attendance writes go through one central node.
- **P2P layer** (`blockchain/P2P.py`): Two peer nodes (ports 3333, 4444) that receive and replicate attendance data directly across peers, with no single central authority.
- **Hybrid model**: Combines both — writes go to the blockchain for a tamper-proof, verifiable record, while the P2P layer replicates the write across peers so the system stays available even if one node goes down, instead of depending on the one central server.

## Models Compared

| Model | How it works | Strength | Weakness |
|---|---|---|---|
| **Client-Server** | Single central server (`ClientServer.py`) handles all reads/writes | Simple, easy to manage and audit | Single point of failure — server down means system down |
| **Peer-to-Peer** | Multiple peer nodes (`P2P.py`) replicate data directly to each other | No single point of failure, distributed | Harder to keep data consistent across peers |
| **Hybrid (this project's focus)** | Blockchain for tamper-proof storage + P2P replication for availability | Combines integrity of blockchain with fault tolerance of P2P | More complex to set up and maintain than either alone |

## Why hybrid P2P?

A pure centralized system is a single point of failure. Pure P2P has no central authority and can be harder to keep consistent. This project runs both alongside the blockchain layer, so attendance is written to the blockchain for an immutable audit trail, while the P2P layer keeps the system available even if one node fails — giving the reliability of distributed systems without giving up a verifiable record.

## Tech Stack

- Backend: Django, Python sockets (threaded Client-Server and P2P nodes)
- Blockchain: Solidity ^0.8.11
- ML/Data: NumPy, Pandas, Scikit-learn (for supporting cost/performance analysis)
- DB: MySQL (PyMySQL)

## Setup

```bash
pip install -r requirements.txt
```

1. Deploy `blockchain/Attendance.sol` to your local blockchain (e.g. Ganache) and update the contract address/ABI path used by the Django app.
2. Start the Client-Server node:
```bash
   python network/ClientServer.py
```
3. Start the P2P nodes:
```bash
   python blockchain/P2P.py
```
4. Start the web app:
```bash
   python manage.py runserver
```

(Windows users can just double-click `runweb.bat`, `runclient.bat`, and `runP2P.bat`.)

## Screenshots

![Screenshot 1](screenshots/image1.png)
![Screenshot 2](screenshots/image9.png)

*(more in the `screenshots/` folder)*

## Status

Academic project — comparative analysis of Client-Server, Peer-to-Peer, and Hybrid blockchain architectures for tamper-proof, cost-effective attendance tracking.
