# SpeakInsights - Prompt-Driven Data Analytics Platform

A scalable data analytics platform where users can query their datasets using natural language and get dynamic visualizations and insights.

## 🚀 Features

- **Natural Language Queries**: Ask questions in plain English
- **Dynamic Visualizations**: Automatically selects the best chart type
- **Intelligent Analysis**: AI-powered insights and recommendations
- **Multi-Dataset Support**: Manage multiple databases per user
- **Real-time Execution**: Instant query results and visualizations

## 🏗️ Architecture

- **Backend**: FastAPI (Python) with async support
- **Frontend**: React + TypeScript + Vite
- **Database**: SQLite (Phase 1) → PostgreSQL (Phase 2+)
- **LLM**: OpenAI GPT-4/3.5-turbo
- **Charts**: Recharts for dynamic visualizations

## 📋 Prerequisites

- Python 3.11+
- Node.js 18+
- OpenAI API key

## ⚡ Quick Start

See [SETUP.md](./SETUP.md) for detailed setup instructions.

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp env.example .env
# Add your OPENAI_API_KEY to .env
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Visit `http://localhost:5173` to use the application.

## 📁 Project Structure

```
speakinsights-prototype/
├── backend/
│   ├── app/
│   │   ├── api/          # API routes
│   │   ├── core/         # Core services (LLM, DB, Security)
│   │   ├── services/     # Business logic
│   │   └── utils/        # Utilities
│   ├── data/             # User databases (SQLite)
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── services/     # API client
│   │   ├── stores/       # State management
│   │   └── types/        # TypeScript types
│   └── package.json
└── README.md
```

## 🔄 How It Works

1. **User Query**: User types a natural language question
2. **Schema Context**: System retrieves database schema
3. **SQL Generation**: LLM converts natural language to SQL
4. **Query Execution**: SQL is executed against user's database
5. **Data Analysis**: Results are analyzed for structure and statistics
6. **Visualization**: Optimal chart type is selected automatically
7. **Insights**: LLM generates textual analysis and recommendations

## 📊 Example Queries

- "Show me total sales by region"
- "What are the top 5 products by revenue?"
- "Compare sales across different quarters"
- "Show me sales trends over time"
- "What is the average order value?"

## 🛠️ Development

### Backend API

- API docs: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

### Adding Sample Data

See `SETUP.md` for instructions on creating sample datasets.

## 🚧 Roadmap

### Phase 1 (Current) - MVP
- ✅ Natural language to SQL
- ✅ Dynamic visualizations
- ✅ Textual analysis
- ✅ SQLite support

### Phase 2 - Enhancement
- User authentication
- Query history
- More chart types
- CSV upload
- PostgreSQL support

### Phase 3 - Scale
- Query caching
- Background jobs
- Advanced analytics
- Export features
- Performance optimization

## 📝 License

MIT License

