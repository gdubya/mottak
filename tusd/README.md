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

Todo:
 - per idag så ligger disse binærene som binære filer som er ferdig kompilert. Det hadde vært fint om vi kan hente disse fra et sted evt. å kompilere disse opp fra github på egen hånd. Dockerfile.chained viser hvordan dette kan gjøres for tusd.




