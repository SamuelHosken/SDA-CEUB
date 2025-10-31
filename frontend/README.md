# 🎨 SDA Frontend

Frontend do Sistema Digital de Alimentação usando React + Mantine.

## 🛠️ Tecnologias

- **React 18** - Framework UI
- **Vite** - Build tool ultra-rápido
- **Mantine 7** - Componentes UI modernos
- **React Hook Form** - Gerenciamento de formulários
- **Zod** - Validação de schemas
- **TanStack Table** - Tabelas poderosas
- **Recharts** - Gráficos e visualizações
- **Axios** - Cliente HTTP

## 📦 Instalação

```bash
# Instalar dependências
npm install

# ou
yarn install

# ou
pnpm install
```

## 🚀 Executar

```bash
# Desenvolvimento
npm run dev

# Build para produção
npm run build

# Preview da build
npm run preview
```

## 📁 Estrutura

```
src/
├── components/      # Componentes React
│   ├── Chat/        # Componente principal de chat
│   ├── StatusBar/   # Barra lateral de status
│   ├── AudioRecorder/ # Gravador de áudio
│   └── common/      # Componentes compartilhados
├── pages/           # Páginas da aplicação
├── hooks/           # Custom hooks
├── services/         # Chamadas à API
├── store/           # Gerenciamento de estado
├── styles/           # Estilos globais
└── utils/           # Utilitários
```

## 🎨 Design System

O projeto usa o tema dark com cores verde lime (#c7fc1c) conforme definido no DESIGN_SYSTEM.md.

## 🔌 API

O frontend se conecta ao backend via proxy configurado no `vite.config.js`. A API base é `/api`.

## 📝 Variáveis de Ambiente

Crie um arquivo `.env` se necessário:

```
VITE_API_URL=http://localhost:8000
```
