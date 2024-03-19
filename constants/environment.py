import os


class EnvironmentApp:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(EnvironmentApp, cls).__new__(cls)
            cls.mssql_host: str = os.environ.get('MSSQL_URI')
        return cls.__instance
