## Pool scheduler worker for Cauldron

This Django project is exclusively used for running a poolsched instance.

Any instance of an [intention](https://gitlab.com/cauldronio/cauldron-pool-scheduler/) can be executed with this scheduler. 

You need to include the app in the project settings, and the intention in the list defined at `poolsched_worker/cauldron_worker/management/commands/schedworker.py` and it will be picked.

All the apps and intentions used for Cauldron are at https://gitlab.com/cauldronio/cauldron-common-apps/-/tree/master/cauldron_apps.

### Docker

To build an image for this repository you need to run:

```
docker build -f docker/Dockerfile -t cauldronio/worker:test .
```

To run this container is highly recommended to use https://gitlab.com/cauldronio/cauldron-deployment where there is a specific Ansible role.