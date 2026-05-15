# 🖥️ Frontend: SteelVision SaaS Dashboard

A premium, enterprise-grade industrial monitoring interface built with **React 18**. This dashboard provides real-time defect telemetry, batch processing, and global standards compliance monitoring.

## 🎨 Design System

The UI utilizes a high-contrast **Zinc & Cobalt** theme, following modern "Ultron" design principles:
- **Glassmorphism**: Translucent panels for a futuristic industrial feel.
- **Micro-animations**: Lucide icons with CSS transitions for interactive feedback.
- **Typography**: Optimized with `Inter` for readability and `JetBrains Mono` for telemetry data.

## 📁 Directory Overview

| Component | Purpose |
|---|---|
| `src/App.js` | Core application logic, state management, and API orchestration. |
| `src/index.css` | The global design system, CSS variables, and layout utilities. |
| `public/` | Static assets, icons, and the HTML entry point. |

## 🚀 Development Setup

### 1. Installation
```bash
npm install
```

### 2. Configuration
Copy the environment template and set your backend API URL:
```bash
cp .env.example .env
```

### 3. Execution
```bash
npm start
```
*The dashboard will be available at `http://localhost:3000`.*

## ✨ Advanced Features

- **📦 Parallel Batch Engine**: Drag-and-drop hundreds of images; the engine queues and processes them with real-time progress updates.
- **📸 Live Optical Feed**: Integrated webcam support for on-the-spot quality inspections on the factory floor.
- **⚖️ Compliance Guard**: Automated flags for defects that fail **ISO 14488** or **ASTM E155** international standards.
- **📄 Reporting Engine**: Instant generation of PDF inspection reports and CSV telemetry exports.

---
> [!NOTE]
> All analysis data is persisted locally in the browser, allowing for historical review without the need for a centralized database in isolated industrial environments.
