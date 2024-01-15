from django.core.management.commands.runserver import Command as RunserverCommand
from currency_app.management.commands.data_script import Command as RunFetchDataCommand


class Command(RunserverCommand):
    def inner_run(self, *args, **options):
        import threading
        fetch_data_thread = threading.Thread(target=RunFetchDataCommand().handle, args=args, kwargs=options)
        fetch_data_thread.start()

        super().inner_run(*args, **options)
