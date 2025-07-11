# Ollama Setup Guide

## What is Ollama?

Ollama is a tool that allows you to run large language models (LLMs) locally on your computer. It's completely free and doesn't require API keys.

## Ollama Advantages

✅ **Completely free** - No usage costs  
✅ **Total privacy** - Data never leaves your machine  
✅ **No limits** - No rate limits  
✅ **Works offline** - Once the model is downloaded  
✅ **Easy to use** - Automatic configuration  

## Available Models

### Recommended for this project:

1. **llama2** (default)
   - Size: ~4GB
   - Speed: Good
   - Accuracy: Excellent for expense analysis

2. **llama2:7b**
   - Size: ~4GB
   - Speed: Faster
   - Accuracy: Good

3. **llama2:13b**
   - Size: ~8GB
   - Speed: Slower
   - Accuracy: Excellent

4. **codellama**
   - Size: ~4GB
   - Speed: Good
   - Accuracy: Excellent for technical expenses

## Configuration

### 1. Automatic Configuration (Recommended)

The system configures automatically when you run:

```bash
# Windows
start.bat

# Linux/macOS
./start.sh
```

### 2. Manual Configuration

If you want to change the model:

1. Edit `bot-service/.env`:
```bash
OLLAMA_MODEL=llama2:7b  # Change the model here
```

2. Restart the services:
```bash
docker-compose down
docker-compose up -d
```

## Model Download

The first time you run the system:

1. **Automatic download**: The model downloads automatically
2. **Download time**: ~5-10 minutes (depending on your internet)
3. **Size**: ~4GB for llama2
4. **One time only**: Only downloads the first time

### Check progress:

```bash
# View Ollama logs
docker-compose logs ollama

# View bot service logs
docker-compose logs bot-service
```

## Troubleshooting

### Error: "Model not found"

```bash
# Check available models
curl http://localhost:11434/api/tags

# Download model manually
curl -X POST http://localhost:11434/api/pull -d '{"name": "llama2"}'
```

### Error: "Connection refused"

```bash
# Check if Ollama is running
docker-compose ps

# Restart Ollama
docker-compose restart ollama
```

### Error: "Out of memory"

If your computer has low RAM:

1. Use a smaller model:
```bash
OLLAMA_MODEL=llama2:7b
```

2. Or reduce available memory:
```bash
# In docker-compose.yml, add:
ollama:
  deploy:
    resources:
      limits:
        memory: 4G
```

## Comparison with OpenAI

| Aspect | OpenAI | Ollama |
|---------|--------|--------|
| Cost | $0.002 per 1K tokens | Free |
| Privacy | Data on OpenAI servers | Data on your machine |
| Speed | Very fast | Depends on your hardware |
| Configuration | API key required | No configuration |
| Limits | Rate limits | No limits |

## Additional Resources

- [Official Ollama documentation](https://ollama.ai/docs)
- [Available models](https://ollama.ai/library)
- [Ollama community](https://github.com/ollama/ollama) 