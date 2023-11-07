import docker
from pymongo import MongoClient
import psutil
import os
import json
import paho.mqtt.client as mqtt


import paho.mqtt.publish as publish

msgs = [{'topic': "cpu_usg", 'payload':""},
        {'topic': "mem_usg", 'payload': ""}
        #{'topic': "storage", 'payload' : ""}
        ]

host = "localhost"

# Conecta-se ao Docker
client = docker.from_env()

# ID ou nome do container que você deseja monitorar
container_id_or_name = "690e2581971257a0d59675ff5a6221aadc521c8e7cb75d62319471f66598de36"

#Obtém informações do container
container = client.containers.get(container_id_or_name)

# Obtém estatísticas de uso de recursos
stats = container.stats(stream=False)

# Extrai informações de CPU, memória e disco
cpu_stats = stats['cpu_stats']
memory_stats = stats['memory_stats']
blkio_stats = stats['blkio_stats']
disk_stats = stats['storage_stats']
print ("blkio_stats: ", blkio_stats)

print ("disk_stats: ", disk_stats)

# Informações de CPU
cpu_usage = cpu_stats['cpu_usage']['total_usage']
system_cpu_usage = cpu_stats['system_cpu_usage']
cpu_percent = (cpu_usage / system_cpu_usage) * 100



# Informações de memória
memory_usage = memory_stats['usage']
memory_limit = memory_stats['limit']

msgs = [{'topic': "cpu_usg", 'payload':cpu_percent},
        {'topic': "mem_usg", 'payload': memory_usage}]

if __name__ == '__main__':
    # publish a single message
    publish.single(topic='cpu_usg', payload=cpu_percent, hostname=host)
    publish.single(topic='mem_usg', payload=memory_usage, hostname=host)

# Obtenha o ID do processo principal do container
pid = container.attrs['State']['Pid']

# Obtenha o diretório raiz do processo do container no host
#container_root_dir = os.path.join(os.environ['ProgramData'], 'docker', 'containers', container_id_or_name)

# Use o psutil para obter as estatísticas de uso de disco
#disk_usage = psutil.disk_usage(container_root_dir)

# Calcule a porcentagem de uso de disco
#disk_usage_percentage = (disk_usage.used / disk_usage.total) * 100

#print(f'Uso de disco: {disk_usage_percentage:.2f}%')

# Informações de disco
io_service_bytes_recursive = blkio_stats['io_service_bytes_recursive']
#used_bytes = disk_stats['bytes_used']
#total_bytes = disk_stats['bytes_total']

# Calcule a porcentagem de uso de disco
#disk_usage_percentage = (used_bytes / total_bytes) * 100

#print(f'Uso de disco : {disk_usage_percentage:.2f}%')

#except docker.errors.NotFound:
#    print(f'Container com ID {container_id} não encontrado.')

#except Exception as e:
#    print(f"Ocorreu um erro: {e}")


try:
    conn = MongoClient('localhost', 27017)
    print("Connected successfully!!!") 
except:   
    print("Could not connect to MongoDB") 

db = conn.tests

collection = db.sensors


#print(f"Uso de CPU: {cpu_percent}%")
# print(f"Uso de Memória: {memory_usage} bytes de {memory_limit} bytes")
# print(f"Uso de Disco: {io_service_bytes_recursive}")

read1 = {
   "Uso de CPU": cpu_percent,
   "Uso de Memória": memory_usage,
   #"Uso de Disco": disk_usage_percentage
}

insert1 = collection.insert_one(read1)


#recuperar todos os registros ja inseridos
cursor = collection.find() 
for record in cursor: 
    print(record)