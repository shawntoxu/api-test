kubectl get pods --all-namespaces -o jsonpath="{..image}" |\
tr -s '[[:space:]]' '\n' |\
#sort
sort |\
uniq -c
#uniq 
