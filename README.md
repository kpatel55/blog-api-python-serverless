# Serverless Framework AWS Python

## Usage

### Deployment

In order to deploy the example, you need to run the following command:

```
$ sls deploy
```

After running deploy, you should see output similar to:

```bash
Deploying blog-api-python to stage dev (us-east-1)

✔ Service deployed to stack blog-api-python-dev (112s)
```

### Bundling dependencies

In case you would like to include third-party dependencies, you will need to use a plugin called `serverless-python-requirements`. You can set it up by running the following command:

```bash
serverless plugin install -n serverless-python-requirements
```
