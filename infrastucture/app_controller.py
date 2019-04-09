class AppController:
    def start(self):
        import subprocess
        command = 'docker-compose -f ./app/docker-compose.yml up -d'
        process = subprocess.Popen(command, shell=True)
        while True:
            if process.poll() is not None and process.returncode != 0:
                break
            if self.__check_socket():
                return True
        raise SystemError('Unable to execute docker-compose')

    def stop(self):
        import subprocess
        command = 'docker-compose -f ./app/docker-compose.yml down'
        subprocess.Popen(command, shell=True)

    def get_base_uri(self):
        return "http://localhost/"

    def __check_socket(self):
        import requests
        try:
            requests.head(self.get_base_uri())
            return True
        except requests.ConnectionError:
            return False
