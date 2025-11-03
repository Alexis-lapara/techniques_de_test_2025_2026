Test Interne Triangulator :

### Cas de test détaillés
Test du lancement de serveur API (si il se lance avec la fonction de lancement dans le bonne état avec les bon port etc...)
Client -> Triangulator
- Test format UID :
    - UID manquant :test avec un uid manquante -> message erreur 400 renvoyer au client un message d'erreur
    - UID malformé : chaîne texte si un entier est attendu, ou UUID invalide -> message erreur 400 renvoyer au client un message d'erreur
    - UID valide : Triangulator tente la récupération. -> message  200 renvoyer au client un message validité


Triangulator -> PointSetManager
- Test si serveur est indisponible -> message erreur 503
- Test ressource absente : test avec une ressource qui n'est pas dans PointSetManager ->reception  de message 404 
- ***Test donnée corrompue : test si une ressource est corrompu *** -> reception  de message 404
- Test de fonctionalité avec une données valide dans PoinsetManager qui renvoie bien un PointSet ->reception  de message  200 

Triangulator-> Client:
    -Test fonction d'envoye de triangle
        test du format des triangles :
            Vide -> envoye un message d'erreur -> message erreur 500 au client
            triangles corrompus/mal Typé -> message erreur 500 au client
            triangles -> dans le format demander -> 200 OK au client
Tests internes Triangulator:

- Triangulation (algorithme) :
    Test des entrée sortie du programme:
        -test avec PointSet  ne correspondent pas au typage attendu -> message d'erreur 500 au client
        -test avec PointSet vide -> message d'erreur 500 au client
        test fonctionnel:
            n == nombre de point dans pointSet
            -test avec  n < 3 renvoye aucun triangle 
            -test avec n == 3 renvoye 1 triangle  
            -test avec n > 3 renvoye n-2 triangles 
test de la conversion binnaire des triangles -> sortie des triangles en format binaire

Qualité de code :
    utilisation de ruff avec les regle déjà près ecrite dans pyprojet

Test de performence :
    temps de la conversion en binnaire des triangles 
    temps de l'algo triangulation
    
