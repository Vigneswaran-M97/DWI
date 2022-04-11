from django.apps import AppConfig



class DwpAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'DWP_app'
    
    def on_starting(server):
        from DWP_app import watch
        watch.main.start_scheduler()     
        def ready(self):
            import DWP_app.watch
            DWP_app.watch.main()
     

    #     import os
    #     import sys
    #     if os.environ.get('RUN_MAIN') == True:
    #         DWP_app.watch.main()
    #         print("Shutting down")
    #     else:
    #         print('No main server')
    
    #     sys.exit(0)
        