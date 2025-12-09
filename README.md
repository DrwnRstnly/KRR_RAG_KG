# Sistem RAG Clash Royale dengan Knowledge Graph

Sistem tanya-jawab dalam bahasa natural tentang kartu Clash Royale menggunakan Neo4j Knowledge Graph dan Retrieval-Augmented Generation (RAG).

## Quickstart

### Opsi 1: Docker (Recommended)

#### 1. Jalankan Services

```bash
docker-compose up
```

#### 2. Seed Database (Pertama Kali Saja)

```bash
docker-compose --profile seed up seeder
```

#### 3. Akses Web Interface

```
Buka browser dan akses http://localhost:8000
```

#### CLI Interface (Opsional)

```bash
docker-compose --profile cli run --rm cli

docker-compose down
```

### Opsi 2: Setup Lokal (Tanpa Docker)

#### Persyaratan

- Python 3.11+
- Neo4j 5.15+ (berjalan lokal atau remote)
- RAM minimum 4GB

#### 1. Setup Python Environment

**Dengan UV (Direkomendasikan)**

```bash
pip install uv

uv sync
```

**Dengan Pip**

```bash
python -m venv .venv

.venv\Scripts\activate

source .venv/bin/activate

pip install .
```

#### 2. Konfigurasi Environment

```bash
cp .env.example .env
```

#### 3. Jalankan Neo4j Database

```bash
docker run --name neo4j \
  -e NEO4J_AUTH=neo4j/your-password \
  -p 7474:7474 -p 7687:7687 \
  neo4j:5.15-community
```

#### 4. Seed Database

```bash
python -m src.kg.ingestion
```

#### 5. Jalankan Aplikasi

**Web Interface**

```bash
python run_web.py
```

**CLI Interface**

```bash
python main.py
```

## Requirements

Lihat `pyproject.toml` untuk daftar lengkap dependency. Dependency utama:

- **langchain-core**: Orkestrasi RAG pipeline
- **langchain-huggingface**: Integrasi Hugging Face models
- **transformers**: LLM support
- **neo4j**: Driver Neo4j
- **rich**: Formatting terminal UI
- **fastapi**: Web interface
- **uvicorn**: ASGI server untuk FastAPI
- **jinja2**: HTML templating
- **torch**: PyTorch (CPU-optimized)

## Arsitektur Sistem

### Komponen Utama

#### 1. **Query Preprocessor** (`src/rag/query_preprocessor.py`)

Komponen pertama yang memproses query user sebelum masuk ke pipeline RAG:

- **Koreksi Otomatis Nama Kartu**: Mendeteksi typo atau variasi nama kartu menggunakan fuzzy matching
  - Contoh: "pekka" → "P.E.K.K.A.", "ewiz" → "Electro Wizard"
  - Menggunakan kombinasi capitalization detection dan similarity scoring
- **Deteksi Query Analisis Deck**: Mengidentifikasi pertanyaan tentang analisis deck
  - Keyword: "analyze", "check", "validate", "rate", "my deck"
- **Ekstraksi Deck dari Query**: Parsing 8 kartu dari berbagai format input
  - Format 1: Comma-separated: `Giant, Wizard, Musketeer, ...`
  - Format 2: Capitalized names: `Giant Wizard Musketeer ...`
  - Format 3: Dengan delimiter: `[Giant, Wizard, Musketeer, ...]`
- **Smart Response Enhancer**: Mencari data alternatif jika query tidak menemukan hasil
  - Counter alternatives: Menyarankan kartu murah untuk counter
  - Synergy alternatives: Mencari kartu dengan archetype yang sama
  - Contoh: Jika tidak ada data synergy untuk "Giant", cari kartu Beatdown lain

#### 2. **Deck Analyzer** (`src/rag/deck_analyzer.py`)

Sistem analisis deck **khusus** yang tidak menggunakan LLM, melainkan rule-based analysis:

**Fitur Analisis:**
- **Klasifikasi Archetype**: Mengidentifikasi deck sebagai Siege, Cycle, Beatdown, atau Bridge Spam
  - Siege: Deteksi X-Bow/Mortar
  - Cycle: Average elixir ≤ 3.0
  - Beatdown: Ada heavy tank (HP > 3000)
  - Bridge Spam: 3+ kartu bridge spam (Bandit, Prince, P.E.K.K.A, dll)

- **General Warnings** (berlaku untuk semua deck):
  - **Strong Warning**: No win condition, no air defense, no spell, avg elixir ≥ 4.8, no anti-tank, dll
  - **Weak Warning**: No small spell, only 1 air defense, no reset card, no splash damage, dll

- **Archetype-Specific Warnings**:
  - **Siege**: Butuh building killer spell, secondary defensive building, avg elixir ≤ 3.8
  - **Cycle**: Butuh defensive building, max 3 kartu ≥ 4 elixir, min 2 cycle cards
  - **Beatdown**: Min avg elixir 3.5, butuh reset cards, max 2 spells
  - **Bridge Spam**: Avg elixir ≤ 4.3, min 2 cycle cards, max 3 spells

- **Synergy & Counter Detection**: Query ke Knowledge Graph untuk relasi SYNERGIZES_WITH dan COUNTERS

**Contoh Output:**
```
Deck: Giant, Wizard, Musketeer, Mini P.E.K.K.A, Zap, Fireball, Mega Minion, Ice Spirit
Archetype: Beatdown
Average Elixir: 3.5

General Warnings:
  [Weak Warning] No building - Harder to defend and control tempo
  [Weak Warning] No reset card - Vulnerable to Inferno Tower/Dragon

Beatdown Archetype Warnings:
  None
```

#### 3. **Query Translator** (`src/rag/translator.py`)

Mengkonversi pertanyaan bahasa natural ke Cypher query:

- **Schema-Aware Prompting**: Menyertakan full schema (nodes, relationships, properties)
- **Few-Shot Learning**: 8+ contoh pasangan (pertanyaan → Cypher)
- **LLM-based Translation**: Menggunakan Qwen 2.5 1.5B untuk generate Cypher
- **Output Cleaning**: Menghapus markdown, comments, dan formatting ekstra

**Contoh:**
- Input: "Berapa elixir cost Giant?"
- Output: `MATCH (c:Card {name: 'Giant'}) RETURN c.elixir`

#### 4. **Retriever** (`src/rag/retriever.py`)

Eksekusi Cypher query terhadap Neo4j:

- Koneksi ke Neo4j menggunakan driver resmi
- Error handling dan timeout management
- Mengembalikan QueryResult dengan data, error, dan execution time
- Connection pooling untuk performa optimal

#### 5. **Answer Generator** (`src/rag/generator.py`)

Generate jawaban bahasa natural dari data yang diambil:

- **Data-Grounded Generation**: Hanya menggunakan data dari Knowledge Graph
- **Complete Listing**: WAJIB menyebutkan SEMUA kartu dari hasil query
- **Smart Formatting**:
  - Jika ada `synergy_type`/`strength`: Jelaskan dengan detail
  - Jika TIDAK ada field tersebut: List nama kartu saja tanpa membuat-buat alasan
- **Champion Ability Detection**: Ekstrak ability dari field `level11_stats`
- **Plain Text Output**: Tidak menggunakan markdown untuk clean display
- **Source Tracking**: Mencatat semua entitas yang disebutkan
- **Confidence Scoring**: Berdasarkan kelengkapan data

#### 6. **RAG Pipeline** (`src/rag/pipeline.py`)

Orkestrasi seluruh komponen dengan 2 mode operasi:

**Mode 1: Standard RAG Flow**
```
User Question
      ↓
[Query Preprocessor] ← Koreksi nama kartu
      ↓
[Query Translator] ← Terjemahkan ke Cypher
      ↓
[Retriever] ← Eksekusi ke Neo4j
      ↓
[Smart Response Enhancer] ← Cari alternatif jika kosong
      ↓
[Answer Generator] ← Generate jawaban natural
      ↓
Final Answer (sources + confidence)
```

**Mode 2: Deck Analysis Flow** (Hybrid Approach)
```
User Question: "analyze my deck: Giant, Wizard, ..."
      ↓
[Query Preprocessor] ← Deteksi deck analysis query
      ↓
[Deck Analyzer - Rule-based]
  ├─ Klasifikasi archetype
  ├─ Hitung avg elixir
  ├─ Check general warnings
  └─ Check archetype warnings
      ↓
[Knowledge Graph Queries]
  ├─ Query synergies (SYNERGIZES_WITH)
  └─ Query counters (COUNTERS)
      ↓
[Format Analysis] ← Gabungkan rule-based + KG data
      ↓
Comprehensive Deck Analysis
```

**Keunggulan Hybrid Approach untuk Deck Analysis:**
- Rule-based cepat dan konsisten untuk validasi deck
- Knowledge Graph menyediakan relasi synergy/counter yang kompleks
- Tidak bergantung pada LLM untuk warnings (lebih reliable)
- LLM hanya digunakan untuk general queries (hemat resource)

### Alur Data Lengkap

```
┌─────────────────────────────────────────────────────────────┐
│                    User Input (Natural Language)             │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
         ┌────────────────────────────┐
         │   Query Preprocessor       │
         │  • Auto-correct card names │
         │  • Detect deck analysis    │
         │  • Extract deck (if any)   │
         └────────┬───────────────────┘
                  │
        ┌─────────┴─────────┐
        │                   │
        ▼                   ▼
┌───────────────┐   ┌──────────────────┐
│ Deck Analysis │   │  Standard Query  │
│    Branch     │   │     Branch       │
└───────┬───────┘   └────────┬─────────┘
        │                    │
        │                    ▼
        │          ┌──────────────────┐
        │          │ Query Translator │
        │          │  (NL → Cypher)   │
        │          └────────┬─────────┘
        │                   │
        │                   ▼
        │          ┌──────────────────┐
        │          │    Retriever     │
        │          │ (Execute Cypher) │
        │          └────────┬─────────┘
        │                   │
        │                   ▼
        │          ┌──────────────────┐
        │          │ Response Enhancer│
        │          │ (Find Alt Data)  │
        │          └────────┬─────────┘
        │                   │
        ▼                   ▼
┌───────────────┐   ┌──────────────────┐
│ Deck Analyzer │   │ Answer Generator │
│ (Rule-based + │   │  (LLM Generate)  │
│   KG Queries) │   │                  │
└───────┬───────┘   └────────┬─────────┘
        │                    │
        └────────┬───────────┘
                 │
                 ▼
      ┌──────────────────────┐
      │   Final Response     │
      │ • Answer text        │
      │ • Sources            │
      │ • Confidence score   │
      │ • Cypher query used  │
      └──────────────────────┘
```
