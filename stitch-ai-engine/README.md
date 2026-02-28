# Stitch AI Engine

AI-powered UI layout generation engine similar to Google Stitch. Generate React UI layouts from natural language prompts.

## Features

- **Prompt → Layout**: Generate UI layouts from text descriptions
- **RAG Pattern Retrieval**: Learns from UI pattern datasets via vector search
- **React Renderer**: Live preview of generated layouts
- **Extensible**: Designed for Figma export, screenshot-to-UI, drag-and-drop, code export

## Tech Stack

- Next.js 14, TypeScript, TailwindCSS
- OpenAI or Gemini API
- Zod schema validation

## Architecture

```
Prompt → UI Pattern Retrieval (RAG) → AI Layout Planner → Component Generator → React Renderer
```

## Setup

```bash
npm install
cp .env.example .env.local
# Add OPENAI_API_KEY or GEMINI_API_KEY to .env.local
npm run dev
```

## Usage

1. Open http://localhost:3000
2. Enter a prompt (e.g. "Landing page for roofing repair company")
3. Click Generate
4. View live preview

## Generate Pattern Dataset

To generate 1000 UI patterns (requires API key):

```bash
npm run generate-patterns
```

## Project Structure

```
src/
  ai/           - Planner, embeddings, pattern retrieval
  engine/       - Layout engine, pattern engine
  types/        - UI schema (Zod)
  data/         - uiPatterns.json
  renderer/     - RenderPage.tsx
  components/   - Hero, Features, Services, etc.
  app/          - Next.js app + API
```

## API

`POST /api/generate`

```json
{ "prompt": "Landing page for roofing repair company" }
```

Returns: `UIPage` JSON
