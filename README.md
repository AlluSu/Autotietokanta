# Autotietokanta (Tietokantasovellusten harjoitustyö)  

## Idea (Vaihe 1)  

Autotietokanta on internet-sovellus, jossa eri käyttäjät voivat myydä autoja.  

### Käyttäjät  
Käyttäjä voi luoda tunnuksen sovellukseen ja siten tehdä uuden ilmoituksen myytävästä autostaan. Yksi kirjautunut käyttäjä voi luoda useita myynti-ilmoituksia ja yhdessä ilmoituksessa myydään vain yhtä autoa.  
Tavallisten käyttäjien lisäksi järjestelmässä on ainakin yksi *Admin-käyttäjä*/*moderaattori*, joka voi tarvittaessa poistaa epäasiallisia ilmoituksia ja muuta mukavaa.  
Käyttäjistä tallennettaisiin ainakin:
  * id
  * käyttäjätunnus
  * nimi
  * osoite- ja yhteystiedot
  * onko admin
  * salasana
  * viite ilmoituksiinsa

### Autot  
Autot olisivat omassa taulussaan ja niiden tiedot täytettäisiin käyttäjän toimesta joko kirjoittamalla lomakkeelle tai raksimalla listasta tai valikosta tiedot.  
Autoista tallennettaisiin ainakin:  
  * id
  * korimalli
  * merkki 
  * malli
  * käyttövoima
  * vaihteisto
  * hinta
  * vuosimalli
  * väri
  * moottorin tilavuus
  * teho
  * vetotapa
  * tieliikennekelpoisuus
  * viite varusteet-tauluun varusteen id:hen
  * viite varusteet-tauluun varusteen id:hen
  * viite ...
  * (varusteet listattaisiin auton yhteyteen tähän tapaan)

### Varusteet  
Ilmoituksessa voisi olla optio täyttää varustelista auton yhteyteen jos auto ei oli aivan täysin karvalakkimalli.  
Varusteet-taulu voisi olla jotakuinkin seuraavanlainen:  
  * varuste_id
  * varusteen_nimi  
Tämä vaatii jatkokehittelyä jos haluaisi eritellä esimerkiksi, että jos autosta löytyy kattoluukku, onko se sähköinen vai manuaalinen tai jos autossa on sähköikkunat vain edessä mutta takapenkillä manuaaliset veivi-ikkunat niin miten tämä näkyy tietokannassa tai käyttäjälle.  

### Ilmoitukset  
Ilmoitus sisältäisi voisi sisältää seuraavat tiedot:  
  * id
  * milloin jätetty (pvm ja kellonaika)
  * myyntiteksti
  * viite myyjään eli ilmoituksen jättäjään eli käyttäjään
  * viite autoon  
 Ja jos aikaa niin tietenkin kuva autosta jolloin olisi viite kuvat-tauluun.

### Kuvat  
Jos on aikaa, tietokantaan voisi tehdä oman taulun kuville.  
  * id
  * nimi
  * data
  




