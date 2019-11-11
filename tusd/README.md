# tusd konteineren i mottak


Dette er den mest sentrale kontaineren i mottaksapplikasjonen. Den tar imot opplastede filer fra uploaderen. Den fyrer av to hooks som vi bruker.

 - Den første hooken validerer at opplastningen er slik den skal være. Altså at opplasteren har fått inn en gyldig lenke som vi selv har laget
 - Den andre hooken fyrer av når opplastingen er ferdig.
   - Denne lager så en input-yaml og fyrer opp "argo submit" og drar igang workflowen i Argo

Kontaineren inneholder tre binærer:
 - kubectl 
 - argo 
 - tusd

kubectl trengs mest til feilsøk. argo bruker naturlig nok til "argo submit".

Når kontainerne fyrer opp starter den tusd på port 1080. Den får også kopiert inn hooks når kontaineren bygges.

Tusd trenger tilgang til objektlageret. Det er noe krøll ved å bruke S3-APIene mot GCS og derfor bruker vi den innebyggede GCS-støtten til tusd frem til dette er løst.

## Kjøre opp tusd-kontainerne i kubernetes.
 - hent ned GCS-tilgangs JSON-object. Legg det inn som en secret i k8s. se create-k8s-secret.sh
 - kjør opp tusd sin deployment:
   - ```kubectl apply -f deployment.yaml```
 - kjør opp tusd sin service (kobler tusd-poden mot en load balancer slik at vi når den utenfra)
   - ```kubectl apply -f service.yaml```
 - for å finne IP-adressen til tusd-tjenestne gjør ```kubectl get services tusd-service```
  
## Feilsøk:

For å feilsøke tusd kan det være greit å få seg et shell på tusd-poden. Få ta i navnet på poden ```kubectl get pods``` og be om et shell på poden: ```kubectl exec -it tusd-57cd8cbfb7-kl86l bash```.

Det kan være hjelpsomt med en kontainer som inneholder en ubuntu-instans på innsiden i k8s-clusteret. For å kjøre opp dette kjør opp følgende: ```kubectl run my-shell --rm -i --tty --image ubuntu -- bash```. Husk å kjøpt ```apt update``` før du henter pakker med apt. Når du logges ut så slettes poden.

##Todo:
 - per idag så ligger disse binærene som binære filer som er ferdig kompilert. Det hadde vært fint om vi kan hente disse fra et sted evt. å kompilere disse opp fra github på egen hånd. Dockerfile.chained viser hvordan dette kan gjøres for tusd.
 - workflowene bør kopieres inn i denne kontaineren på et vis.
 - Ta ibruk TLS
 - Få en eller annen form for service discovery slik at tusd-tjensten gjør seg tilgjengelig på et kjent sted på internett så vi slipper å fjase med kubectl for å finne ut hvor tjenesten kjører.
 - Få opp helsesjekker slik at k8s kan starte om tusd-kontaineren om den går i frø.



