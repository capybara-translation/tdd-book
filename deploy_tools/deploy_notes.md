Deploying a new site
=======================

# Deployment command

```
# locally:
cd deploy_tools
fab staging|production SSH_CONFIG_FILE APP_CONFIG_FILE deploy

# on the server:
$ sudo systemctl daemon-reload
$ sudo systemctl restart gunicorn-stg.capybara-mt.com.service
```

