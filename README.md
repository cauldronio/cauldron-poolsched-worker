## Pool scheduler worker for Cauldron

This Django project is exclusively used for running a poolsched instance.

Any instance of an [intention](https://gitlab.com/cauldronio/cauldron-pool-scheduler/) can be executed with this scheduler. 

You need to include the app in the project settings and the intention it in the list defined at `poolsched_worker/cauldron_worker/management/commands/schedworker.py` and it will be picked.

All the apps and intentions used for Cauldron are at https://gitlab.com/cauldronio/cauldron-common-apps/-/tree/master/cauldron_apps.

