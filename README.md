# RealTime Data Hub

## Visão Geral
Sistema backend para ingestão de dados, processamento assíncrono e comunicação em tempo real.

## Arquitetura
- Django + DRF
- Celery + Redis
- WebSocket (Django Channels)
- PostgreSQL
- Docker
- Google Cloud Platform

## Funcionalidades
- Autenticação JWT
- Upload de dados
- Processamento assíncrono
- Atualizações em tempo real
- APIs documentadas

## Executando Localmente
```bash
docker compose -f docker/docker-compose.yml up --build
