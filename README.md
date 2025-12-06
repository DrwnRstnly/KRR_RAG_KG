# Sistem RAG dengan Knowledge Graph - Clash Royale

**Tugas Proyek II IF4070 - Representasi Pengetahuan dan Penalaran**

Sistem tanya-jawab berbahasa natural tentang Clash Royale menggunakan Knowledge Graph (Neo4j) dan Retrieval-Augmented Generation (RAG).

---

## 🎯 Ringkasan Eksekutif

Sistem ini memungkinkan pengguna bertanya dalam bahasa natural tentang kartu Clash Royale, dan mendapatkan jawaban yang di-grounded dengan data dari knowledge graph.

**Contoh:**
- **Input:** "Kartu apa yang counter P.E.K.K.A?"
- **Proses:** Pertanyaan → Cypher Query → Ambil dari Neo4j → Generate Jawaban
- **Output:** "Skeleton Army dan Mini P.E.K.K.A adalah counter kuat untuk P.E.K.K.A..."

---

## 📊 Arsitektur Sistem

```
┌─────────────────────────────────────────────────────────┐
│                    USER (Pertanyaan)                     │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│              CLI INTERFACE (Rich Terminal)               │
│  • Input pertanyaan natural language                     │
│  • Output dengan streaming & formatting                  │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                   RAG PIPELINE                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │ Translator  │→ │  Retriever  │→ │  Generator  │     │
│  │ NL→Cypher   │  │  Neo4j      │  │  Answer     │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
└─────────────────────────────────────────────────────────┘
         ↓                  ↓                  ↓
    ┌────────┐      ┌─────────────┐      ┌────────┐
    │  LLM   │      │   Neo4j KG  │      │  LLM   │
    │ Qwen   │      │  100+ Cards │      │ Qwen   │
    └────────┘      └─────────────┘      └────────┘
```

---

## 🔄 Alur Data

### 1. **Knowledge Graph (Neo4j)**
```
Data Mentah (JSON)
    ↓
[Ingestion Script]
    ↓
Neo4j Graph Database
├── Nodes: Card, Rarity, Arena, Target, Type, Archetype
└── Relationships: HAS_RARITY, COUNTERS, SYNERGIZES_WITH, dll.
```

### 2. **RAG Pipeline**
```
Pertanyaan User: "Berapa elixir cost Giant?"
    ↓
[Translator] → LLM mengubah ke Cypher
    ↓
Cypher: MATCH (c:Card {name: 'Giant'}) RETURN c.elixir
    ↓
[Retriever] → Eksekusi query ke Neo4j
    ↓
Data: [{elixir: 5}]
    ↓
[Generator] → LLM generate jawaban dari data
    ↓
Jawaban: "Giant memiliki cost 5 elixir."
```

### 3. **Flow Detail**
```
┌──────────────┐
│ User Input   │ "Which cards counter P.E.K.K.A?"
└──────────────┘
       ↓
┌──────────────────────────────────────────────────────┐
│ STEP 1: Query Translation                            │
│ Input:  Natural language question                    │
│ Process: LLM + Schema + Examples → Generate Cypher   │
│ Output: MATCH (c:Card)-[r:COUNTERS]->(p:Card         │
│         {name: 'P.E.K.K.A'})                         │
│         RETURN c.name, r.effectiveness               │
└──────────────────────────────────────────────────────┘
       ↓
┌──────────────────────────────────────────────────────┐
│ STEP 2: Data Retrieval                               │
│ Input:  Cypher query                                 │
│ Process: Execute on Neo4j, handle errors             │
│ Output: [{name: "Skeleton Army", eff: "strong"}, ... ]│
└──────────────────────────────────────────────────────┘
       ↓
┌──────────────────────────────────────────────────────┐
│ STEP 3: Answer Generation                            │
│ Input:  Retrieved data + original question           │
│ Process: LLM generates natural language answer       │
│ Output: "Skeleton Army provides a strong counter..." │
│ + Sources: ["Skeleton Army", "Mini P.E.K.K.A"]      │
│ + Confidence: 85%                                    │
└──────────────────────────────────────────────────────┘
       ↓
┌──────────────┐
│ User Output  │ Jawaban + Sources + Confidence
└──────────────┘
```

---

## 🚀 Cara Menjalankan

### 1. **Setup Awal**

```bash
# Install dependencies
pip install -r requirements.txt

# Konfigurasi database (edit .env)
cp .env.example .env
nano .env  # Update NEO4J_PASSWORD

# Pastikan Neo4j running
# Buka Neo4j Desktop dan start database
```

### 2. **Ingest Data ke Neo4j**

```bash
python -m src.kg.ingestion
```

Output:
```
=== Phase 1: Ingesting Cards ===
  ✓ Arrows
  ✓ Giant
  ...
=== Phase 2: Creating Relationships ===
  ✓ Arrows COUNTERS Minion Horde
  ✓ Giant SYNERGIZES_WITH Musketeer
  ...
Total cards ingested: 100+
```

### 3. **Jalankan CLI**

```bash
python main_v2.py
```

### 4. **Gunakan Sistem**

```
You > What is the elixir cost of Giant?

Answer: The Giant costs 5 elixir.
Sources: Giant
Confidence: 90%

You > /help      # Lihat bantuan
You > /examples  # Lihat contoh pertanyaan
You > /stats     # Lihat statistik KG
You > /exit      # Keluar
```

---

## 📁 Struktur Kode

```
src/
├── domain/              # Model domain (Card, Deck, RAGResponse)
│   └── models.py
│
├── kg/                  # Knowledge Graph
│   ├── schema.py        # Definisi schema KG
│   ├── relationship_rules.py  # Ekstraksi counter/synergy
│   └── ingestion.py     # ⭐ Script ingestion utama
│
├── rag_v2/              # RAG Pipeline
│   ├── translator.py    # Natural Language → Cypher
│   ├── retriever.py     # Eksekusi query Neo4j
│   ├── generator.py     # Generate jawaban + grounding
│   └── pipeline.py      # Orkestrator RAG
│
├── services/            # Service layer (API-ready)
│   └── rag_service.py
│
├── cli/                 # Command-line interface
│   ├── display.py       # Rich formatting
│   └── main.py          # Aplikasi CLI
│
└── utils/               # Utilities
    └── config.py        # Konfigurasi

main_v2.py              # Entry point utama
test_system.py          # Testing script
```

---

## 🗃️ Schema Knowledge Graph

### **Nodes (6 tipe)**
- `Card`: Kartu dengan stats (HP, damage, DPS, elixir, dll.)
- `Rarity`: Common, Rare, Epic, Legendary, Champion
- `Arena`: Arena unlock
- `Target`: ground, air, buildings
- `Type`: Troop, Spell, Building
- `Archetype`: Beatdown, Cycle, Siege, Bait, dll.

### **Relationships (7 tipe)**
- `HAS_RARITY`: Card → Rarity
- `UNLOCKS_IN`: Card → Arena
- `CAN_HIT`: Card → Target
- `HAS_TYPE`: Card → Type
- `COUNTERS`: Card → Card (counter strategis)
- `SYNERGIZES_WITH`: Card ↔ Card (sinergi)
- `FITS_ARCHETYPE`: Card → Archetype (cocok untuk deck)

### **Contoh Query Cypher**
```cypher
// Kartu yang counter P.E.K.K.A
MATCH (c:Card)-[r:COUNTERS]->(p:Card {name: 'P.E.K.K.A'})
RETURN c.name, r.effectiveness, r.reason

// Kartu yang sinergi dengan Giant
MATCH (c:Card)-[s:SYNERGIZES_WITH]->(g:Card {name: 'Giant'})
RETURN c.name, s.synergy_type, s.strength

// Kartu untuk archetype Beatdown
MATCH (c:Card)-[f:FITS_ARCHETYPE]->(a:Archetype {name: 'Beatdown'})
RETURN c.name, f.role
```

---

## 🎨 Fitur Unggulan

### 1. **Query Translation Cerdas**
- Prompt engineering dengan schema awareness
- 8+ contoh query untuk guidance
- Handle query kompleks (agregasi, multi-hop)

### 2. **Source Grounding**
- Setiap jawaban mencantumkan sumber data
- Memungkinkan fact-checking
- Meningkatkan kepercayaan

### 3. **Confidence Scoring**
- Skor kepercayaan 0-100%
- Berdasarkan jumlah data & kualitas jawaban
- Membantu user menilai reliabilitas

### 4. **Streaming Output**
- Response muncul word-by-word
- UX lebih baik meski latency sama
- Progress indicator di setiap tahap

### 5. **Rich CLI**
- Syntax highlighting untuk Cypher
- Tabel statistik
- Colored output
- Command system

---

## 🔬 Implementasi Teknis

### **LLM: Qwen 2.5 1.5B**
- Model instruction-tuned
- Local inference (tidak perlu API key)
- Cukup kecil untuk laptop

### **Knowledge Graph: Neo4j**
- Graph database
- Query dengan Cypher
- Relasi kompleks antar entitas

### **Framework: LangChain**
- Orkestrator RAG
- Runnable pipeline
- Modular components

### **CLI: Rich**
- Terminal formatting
- Progress bars
- Syntax highlighting

---

## 📈 Perbandingan dengan Milestone 1

| Aspek | M1 (Prolog) | M2 (Neo4j RAG) |
|-------|-------------|----------------|
| **Input** | 8 nama kartu | Natural language |
| **Teknologi** | Prolog rules | Neo4j + Python + LLM |
| **Output** | Warning, klasifikasi | Jawaban conversational |
| **Reasoning** | Logic-based | Retrieval + Generation |
| **Skalabilitas** | Terbatas | Sangat scalable |
| **Interface** | CLI struktural | Conversational |

**Kesinambungan:**
- Domain sama: Clash Royale
- Konsep sama: counter, synergy, archetype
- Evolusi dari rule-based ke data-driven

---

## 🧪 Testing

```bash
# Jalankan semua test
python test_system.py
```

Test mencakup:
1. ✅ Import modules
2. ✅ Koneksi Neo4j
3. ✅ Load LLM
4. ✅ Query translation
5. ✅ Data retrieval
6. ✅ Full RAG pipeline
7. ✅ Statistik KG

---

## 📊 Statistik Sistem

- **Lines of Code**: ~2500+
- **Python Files**: 19 files
- **KG Nodes**: 6 tipe
- **KG Relationships**: 7 tipe
- **Cards**: 100+ kartu Clash Royale
- **Relationships Created**: 150+ (counter, synergy, archetype)

---

## 🐛 Troubleshooting

### "Can't connect to Neo4j"
```bash
# Pastikan Neo4j running
# Di Neo4j Desktop, klik Start

# Cek kredensial di .env
cat .env | grep NEO4J
```

### "CUDA out of memory"
```bash
# Edit .env, gunakan CPU
LLM_DEVICE=cpu
```

### "No data retrieved"
```bash
# Run ingestion lagi
python -m src.kg.ingestion
```

---

## 📦 Deliverables (untuk submission)

1. ✅ **Source code**: Folder `src/` lengkap
2. ✅ **Neo4j dump**: Export dari Neo4j Desktop
3. ✅ **Dokumentasi**: README.md ini
4. ✅ **Working system**: `python main_v2.py`

**Cara export Neo4j dump:**
```bash
# Di Neo4j Desktop:
# 1. Klik database
# 2. Klik "..." → "Dump"
# 3. Save: neo4j_dump_2025-12-06.dump
```

---

## 👨‍💻 Informasi Proyek

- **Mata Kuliah**: IF4070 - Representasi Pengetahuan dan Penalaran
- **Semester**: Ganjil 2025/2026
- **Institusi**: Institut Teknologi Bandung
- **Milestone**: 2 (Knowledge Graph + RAG)
- **Teknologi**: Neo4j, Python, LangChain, Transformers, Rich

---

## 📚 Referensi

- Neo4j Documentation: https://neo4j.com/docs/
- LangChain: https://python.langchain.com/
- Qwen Model: https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct
- Clash Royale Data: Fandom Wiki

---

**Versi**: 2.0.0
**Tanggal**: Desember 2025
