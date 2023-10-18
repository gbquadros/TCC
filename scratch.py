import docker

print(f"Versão da biblioteca Docker SDK: {docker.__version__}")
# Conecta-se ao Docker
client = docker.from_env()

# ID ou nome do container que você deseja monitorar
container_id_or_name = "welcome-to-docker"

# Obtém informações do container
container = client.containers.get(container_id_or_name)

# Obtém estatísticas de uso de recursos
stats = container.stats(stream=False)

# Extrai informações de CPU, memória e disco
cpu_stats = stats['cpu_stats']
memory_stats = stats['memory_stats']
blkio_stats = stats['blkio_stats']

# Informações de CPU
cpu_usage = cpu_stats['cpu_usage']['total_usage']
system_cpu_usage = cpu_stats['system_cpu_usage']
cpu_percent = (cpu_usage / system_cpu_usage) * 100

# Informações de memória
memory_usage = memory_stats['usage']
memory_limit = memory_stats['limit']

# Informações de disco
io_service_bytes_recursive = blkio_stats['io_service_bytes_recursive']

print(f"Uso de CPU: {cpu_percent}%")
print(f"Uso de Memória: {memory_usage} bytes de {memory_limit} bytes")
print(f"Uso de Disco: {io_service_bytes_recursive}")