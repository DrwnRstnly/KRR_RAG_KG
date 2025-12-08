# Sistem RAG Clash Royale dengan Knowledge Graph

Sistem tanya-jawab dalam bahasa natural tentang kartu Clash Royale menggunakan Neo4j Knowledge Graph dan Retrieval-Augmented Generation (RAG).

## Mulai Cepat

### Opsi 1: Docker (Direkomendasikan)

#### Web Interface (Recommended)

```bash
# Start Neo4j and Web Interface
docker-compose up web

# Access the web interface at http://localhost:8000
# Note: Database must be seeded first (see below)
```

#### Seed Database (First Time Only)

```bash
# Seed the Neo4j database with Clash Royale data
docker-compose --profile seed up seeder

# Wait for seeding to complete, then stop
docker-compose down
```

#### CLI Interface

```bash
# Run CLI interface
docker-compose --profile cli run --rm cli

# Stop services
docker-compose down
```

### Opsi 2: Setup Lokal

#### Requirements

- Python 3.11+
- Neo4j 5.15+
- RAM minimum 4GB

#### Instalasi dengan UV (Recommended)

```bash
# Install UV package manager
pip install uv

# Install dependencies from pyproject.toml
uv pip install --system .

# Or install in editable mode for development
uv pip install --system -e .

# Konfigurasi environment
cp .env.example .env
# Edit .env dengan kredensial Neo4j Anda
```

#### Instalasi dengan Pip

```bash
# Install dependencies from pyproject.toml
pip install .

# Or install in editable mode for development
pip install -e .

# Konfigurasi environment
cp .env.example .env
# Edit .env dengan kredensial Neo4j Anda
```

#### Setup Database

```bash
# Mulai Neo4j (gunakan Neo4j Desktop atau Docker)
docker run --name neo4j -e NEO4J_AUTH=neo4j/your-password \
  -p 7474:7474 -p 7687:7687 neo4j:5.15-community

# Seed database dengan data kartu
python -m src.kg.ingestion
```

#### Run Web Interface

```bash
# Start the web server
python run_web.py

# Access at http://localhost:8000
```

#### Run CLI Interface

```bash
# Run terminal-based interface
python main_v2.py
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

### Komponen

1. **Query Translator** (`src/rag_v2/translator.py`)

   - Mengkonversi pertanyaan bahasa natural ke query Cypher
   - Menggunakan LLM dengan schema-aware prompting
   - Menangani query kompleks (multi-hop)

2. **Retriever** (`src/rag_v2/retriever.py`)

   - Mengeksekusi query Cypher terhadap Neo4j
   - Error handling dan validasi query
   - Mengembalikan hasil terstruktur

3. **Answer Generator** (`src/rag_v2/generator.py`)

   - Generate jawaban dalam bahasa natural dari data yang diambil
   - Menyediakan source grounding (entitas mana yang digunakan)
   - Confidence scoring berdasarkan kualitas hasil

4. **RAG Pipeline** (`src/rag_v2/pipeline.py`)
   - Mengorkestrasi translator → retriever → generator
   - Mengelola context dan error handling
   - Support streaming output

### Alur Data

```
Pertanyaan User (Bahasa Natural)
          ↓
[Query Translator]
  - LLM menganalisis pertanyaan
  - Referensi schema + contoh
  - Generate query Cypher
          ↓
Query Cypher (contoh: MATCH (c:Card)-[r:COUNTERS]->...)
          ↓
[Query Retriever]
  - Eksekusi terhadap Neo4j
  - Parse hasil
  - Handle error
          ↓
Data Mentah dari Database
          ↓
[Answer Generator]
  - LLM konversi data ke bahasa natural
  - Tambahkan informasi sumber
  - Hitung confidence score
          ↓
Jawaban Final (dengan sumber & confidence)
```

## Schema Knowledge Graph

### Tipe Node

| Tipe          | Properties                                                        | Contoh                                  |
| ------------- | ----------------------------------------------------------------- | --------------------------------------- |
| **Card**      | name, elixir, hitpoints, damage, target_type, deploy_time, rarity | Giant, Arrows, P.E.K.K.A                |
| **Rarity**    | name, level                                                       | Common, Rare, Epic, Legendary, Champion |
| **Arena**     | name, level                                                       | Training Camp, Goblin Arena             |
| **Target**    | name                                                              | ground, air, buildings                  |
| **Type**      | name                                                              | Troop, Spell, Building                  |
| **Archetype** | name, description                                                 | Beatdown, Cycle, Siege, Bait            |

### Tipe Relationship

| Tipe                | Arah             | Properties             |
| ------------------- | ---------------- | ---------------------- |
| **HAS_RARITY**      | Card → Rarity    | -                      |
| **UNLOCKS_IN**      | Card → Arena     | level                  |
| **CAN_HIT**         | Card → Target    | -                      |
| **HAS_TYPE**        | Card → Type      | -                      |
| **COUNTERS**        | Card → Card      | effectiveness, reason  |
| **SYNERGIZES_WITH** | Card ↔ Card     | synergy_type, strength |
| **FITS_ARCHETYPE**  | Card → Archetype | role                   |

### Contoh Query

**Kartu yang counter P.E.K.K.A**

```cypher
MATCH (c:Card)-[r:COUNTERS]->(p:Card {name: 'P.E.K.K.A'})
RETURN c.name, r.effectiveness, r.reason
ORDER BY r.effectiveness DESC
```

**Sinergi untuk Giant**

```cypher
MATCH (c:Card)-[s:SYNERGIZES_WITH]->(g:Card {name: 'Giant'})
RETURN c.name, s.synergy_type, s.strength
```

**Kartu berdasarkan archetype**

```cypher
MATCH (c:Card)-[f:FITS_ARCHETYPE]->(a:Archetype {name: 'Beatdown'})
RETURN c.name, f.role, c.elixir
ORDER BY c.elixir
```

## Detail Implementasi

### Proses Query Translation

1. **Ekstraksi Schema**: Membangun deskripsi schema Cypher dari Neo4j
2. **Few-Shot Examples**: Menyertakan 8+ contoh pasangan (pertanyaan, Cypher)
3. **LLM Prompt**: Menggabungkan guidelines + schema + contoh
4. **Query Generation**: LLM menghasilkan query Cypher yang valid
5. **Validasi**: Memeriksa syntax sebelum eksekusi

Contoh prompt:

```
Anda adalah translator query Cypher untuk Knowledge Graph Clash Royale.

Schema:
- Node types: Card, Rarity, Arena, Target, Type, Archetype
- Relationships: HAS_RARITY, COUNTERS, SYNERGIZES_WITH, dll.

Guidelines:
1. Gunakan MATCH untuk query
2. Gunakan WHERE untuk filtering
3. Return dengan meaningful column names menggunakan AS

Contoh:
Q: "Berapa elixir cost Giant?"
A: MATCH (c:Card {name: 'Giant'}) RETURN c.elixir

Pertanyaan: [PERTANYAAN USER]
Output HANYA query Cypher, tanpa penjelasan.
```

### Proses Answer Generation

1. **Pemrosesan Data**: Ekstraksi field relevan dari hasil query
2. **Context Formatting**: Struktur data untuk konsumsi LLM
3. **Generation Prompt**: Sertakan pertanyaan, data, dan grounding instructions
4. **LLM Response**: Jawaban bahasa natural dari context
5. **Source Tracking**: Catat entitas mana saja yang digunakan
6. **Confidence Calculation**: Berdasarkan kelengkapan hasil

### Konfigurasi

Buat file `.env`:

```
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password

LLM_MODEL=Qwen/Qwen2.5-1.5B-Instruct
LLM_DEVICE=cpu
LLM_MAX_TOKENS=512
LLM_TEMPERATURE=0.1
```

## Struktur File

```
src/
├── domain/
│   └── models.py              # Data models (Card, Deck, RAGResponse)
├── kg/
│   ├── schema.py              # Definisi schema KG
│   ├── relationship_rules.py   # Ekstraksi counter/synergy
│   └── ingestion.py           # Script seeding database
├── rag_v2/
│   ├── translator.py          # Translasi NL ke Cypher
│   ├── retriever.py           # Eksekusi query
│   ├── generator.py           # Generate jawaban
│   ├── pipeline.py            # Orkestrasi RAG
│   └── query_preprocessor.py  # Preprocessing query
├── services/
│   └── rag_service.py         # Service layer
├── cli/
│   ├── main.py                # Aplikasi CLI
│   └── display.py             # Formatting terminal
└── utils/
    └── config.py              # Manajemen konfigurasi

main_v2.py                      # Entry point
```

## Penggunaan

```bash
python main_v2.py
```

Perintah:

- Masukkan pertanyaan bahasa natural tentang Clash Royale
- `/help` - Tampilkan perintah tersedia
- `/examples` - Tampilkan contoh pertanyaan
- `/stats` - Tampilkan statistik knowledge graph
- `/exit` - Keluar dari aplikasi

Contoh session:

```
You > Kartu apa yang counter P.E.K.K.A?

Answer: Skeleton Army dan Mini P.E.K.K.A adalah counter kuat untuk P.E.K.K.A.
Sources: [Skeleton Army, Mini P.E.K.K.A, P.E.K.K.A]
Confidence: 85%

You > Berapa elixir cost Giant?

Answer: Giant memiliki cost 5 elixir.
Sources: [Giant]
Confidence: 95%
```

## Teknologi

- **Graph Database**: Neo4j 5.15
- **LLM**: Qwen 2.5 1.5B (local inference)
- **RAG Framework**: LangChain
- **Package Manager**: UV
- **CLI Framework**: Rich
- **Container**: Docker & Docker Compose

## Troubleshooting

**Error koneksi ke Neo4j**

```bash
# Verifikasi Neo4j berjalan
docker ps | grep neo4j

# Cek kredensial di .env
cat .env
```

**Out of memory**

```bash
# Edit .env untuk gunakan CPU
LLM_DEVICE=cpu
```

**Tidak ada data yang diambil**

```bash
# Re-seed database
python -m src.kg.ingestion
```

## Statistik

- 100+ kartu Clash Royale
- 150+ relationships (counters, synergies, archetypes)
- 6 tipe node, 7 tipe relationship
- ~2500+ baris kode

## Deliverables

- Source code di direktori `src/`
- Setup Docker Compose yang berfungsi
- Database Neo4j dengan data seeded
- CLI interface untuk interaksi

## Informasi Kursus

- Kursus: IF4070 - Representasi Pengetahuan dan Penalaran
- Institusi: Institut Teknologi Bandung (ITB)
- Semester: Ganjil 2025/2026
- Milestone: 2 (Knowledge Graph + RAG)

## Referensi

- Neo4j: https://neo4j.com/docs/
- LangChain: https://python.langchain.com/
- Qwen: https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct

