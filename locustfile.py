from locust import HttpUser, task, between

class BuscarProdutosTest(HttpUser):
    wait_time = between(1, 3)  # Tempo entre requisições

    @task
    def testar_busca(self):
        self.client.get("/buscar?produto=iphone")  # Simulando busca

if __name__ == "__main__":
    import os
    os.system("locust -f locustfile.py")