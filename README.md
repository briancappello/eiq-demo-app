# The App

The app is a small `Flask` app structured using the application factory pattern. It uses `Flask-WTF` and `Pandas` to handle the form and validation requirements. Due to time constraints, the templates use `Jinja2` and `Bootstrap4` for styling (I reused some open source code I had already written for the layout and utility macros).

[Live on GCP](http://104.198.14.34/) (I didn't set up any DNS records or HTTPS)

# GKE and Docker commands

This is where the bulk of my time went. I had toyed around with GCP and Kubernetes briefly maybe 2 years ago, but that being my only experience with them, I was essentially getting set up from scratch. I found the GCP console and related documentation to be a bit of a labyrinth, but after locating the relevant docs it wasn't bad to get "hello world" deployed. I faced a little bit of a hiccup debugging `gunicorn` with the transition from a single file to using the application factory pattern, which I found much easier to solve building and running docker images locally than by using Google's push build service.

```bash
# install google cloud SDK, kubectl, and docker

# set env vars
export PROJECT_ID="eiq-demo"
export GCP_REGION="us-west1"
export GCP_ZONE="us-west1-a"
export REPO_NAME="$PROJECT_ID-repo"  # for GCP Artifact Registry
export IMAGE_NAME="$PROJECT_ID-app"  # for docker image name stored in Artifact Registry
export CLUSTER_NAME="$PROJECT_ID-cluster"

# configure local gcloud env and authenticate
gcloud config configurations create $PROJECT_ID
gcloud config set project $PROJECT_ID
gcloud auth login
gcloud auth application-default login  # instead of setting up a service acct

# create an artifact repo to store containers
gcloud artifacts repositories create $REPO_NAME \
    --project=$PROJECT_ID \
    --repository-format=docker \
    --location=$GCP_REGION \
    --description="Docker repository"

# build & push the docker file
gcloud builds submit \
  --tag $GCP_REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$IMAGE_NAME .

# create a GKE cluster
gcloud container clusters create $CLUSTER_NAME --num-nodes 1 --zone $GCP_ZONE

# verify access to the cluster
kubectl get nodes

# create deployment.yaml and deploy it
kubectl apply -f deployment.yaml

# create service.yaml and deploy it
kubectl apply -f service.yaml

# list services to get EXTERNAL-IP
kubectl get services

# pushing new code
# ----------------

# rebuild container with a new tag
gcloud builds submit \
  --tag $GCP_REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$IMAGE_NAME:v2 .

# set the container the GKE deployment should use
kubectl set image deployment/app-deployment \
  app-container=$GCP_REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$IMAGE_NAME:v2

# building locally and pushing
# configure docker auth: https://cloud.google.com/artifact-registry/docs/docker/authentication#standalone-helper

docker build -t localtag:v1 .
docker tag localtag:v1 $GCP_REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$IMAGE_NAME:local
kubectl set image deployment/app-deployment \
  app-container=$GCP_REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$IMAGE_NAME:local
```

# Testing using `pytest`

Tests are run locally, using

```bash
pip install -r requirements-dev.txt
FLASK_ENV="test" pytest
```

(ideally these would be configured to run inside docker using tox, but I used up my allotted time)

# Approx time investment

Task | Time
--- | ---
Development environment setup | .5hrs (installing and configuring Cloud SDK and Docker)
Hello World to first live deploy on GCP | 2.5hrs
Writing the app | 1.5hrs
Writing tests | .5hrs
Debugging prod issues | .5hrs
Manual testing and documentation | .5hrs
Total | 6hrs
