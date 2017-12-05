kubectl config set-context $(kubectl config current-context) --namespace=s

kubectl config view | grep namespace
