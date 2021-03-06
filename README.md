# Autotietokanta (Tietokantasovellusten harjoitustyö)  

## Loppupalautus (vaihe 4)  

Autotietokanta, tuttavallisemmin AutoNetti, on internet-sovellus, jossa kirjautuneet käyttäjät voivat tehdä omista autoistaan myynti-ilmoituksia. Sovellus löytyy osoitteesta https://autonetti.herokuapp.com/  

### Sovelluksen käyttäminen  

#### Päänäkymä
Sovelluksen päänäkymä näyttää seuraavalta:  
![indexpage](photos/index_without_login.png)  
Aktiiviset ilmoitukset eli myytävät autot näkyvät allekkain heti etusivulla ja jokaisesta on linkki tarkempiin
tietoihin. Jos käyttäjä ei ole kirjautuneena, tarjotaan mahdollisuus kirjautumiseen sekä käyttäjän luontiin. Ilmoituksia on mahdollista lajitella valitsemalla lajitteluoptio valikosta ja painamalla painiketta *Lajittele*. Ilmoituksista voi myös hakea hakusanalla kirjoittamalla haluttu hakusana ja painamalla *Etsi*. Haku ei ole ns. *case sensitive* eli isot ja pienet kirjaimet ovat samanarvoisia.  
![querytest](photos/query_test.png)  
Ylemmässä on haettu aktiivista ilmoituksista hakusanan *jdm* sisältäviä ilmotuksia, joita on kaksi (2) kappaletta.  

#### Käyttäjän luominen  
Uuden käyttäjän luominen näyttää seuraavalta:  
![new_user](photos/new_user.png)  
Käyttäjä voi syöttää tiedot lomakkeelle jonka perusteella luodaan käyttäjä. Kaikki kentät on pakollista täyttää ja omia tietojaan poislukien salasanaa ja käyttäjätunnusta on mahdollista muuttaa jälkeenpäin. Puhelinnumero ja sähköposti eivät sisällä validoinnin suhteen mitään *Regex*-tarkistimia niiden monimutkaisuuden ja virhealttiuden takia. Syötteiden tarkistus tehdään niin käyttöliittymän puolella HTML-tiedostossa kuin myös palvelinpuolella ja tarvittaessa annetaan asianmukainen virheilmoitus. 
![new_user_success](photos/new_user_succesful.png) 

#### Kirjautuminen  
Kirjautumisnäkymä näyttää seuraavalta:  
![login](photos/login_with_user.png)  
Jos käyttäjätunnus tai salasana on väärä annetaan asianmukainen virheilmoitus.  

Kun käyttäjä on kirjautunut sisään, näyttää etusivu seuraavalta:  
![indexpage_with_login](photos/succesful_login.png)  
Kirjautuneena oleva käyttäjä voi siis:  
* Jättää uuden ilmoituksen  
* Muokata omia tietojaan  
* Katsella erikseen omia ilmoituksiaan
* Kirjautua ulos
* Ja tietenkin katsella muiden ilmoituksia  

![own_ads](photos/own_ads_Empty.png)  

Jos käyttäjä on admin-käyttäjä, näkyy etusivulla status-teksti.  
![admin](photos/admin_index.png)  
Sovelluksessa on siis kahdenlaisia käyttäjiä, tavallisia ja *Admin*-oikeuksin varustettuja käyttäjiä. *Admin*-käyttäjä on kuin tavallinen käyttäjä, mutta se voi poistaa jokaisen ilmoituksen. Sovelluksen tuotantoversiossa eli Herokussa olevassa sovelluksessa on tällä hetkellä yksi (1) *Admin*-käyttäjä, jolle on annettu oikeudet suoraan tietokannan kautta.  

#### Ilmoituksen luonti  
Kirjautunut käyttäjä voi luoda omia ilmoituksia painamalla *Jätä ilmoitus*-painiketta, jolloin avautuu seuraavanlainen näkymä:  
![new_ad](photos/new_ad1.png)  
![new_ad2](photos/new_ad2.png)  
Jälleen kaikki kentät on täytettävä, poislukien *Lisätiedot* ja *Kuva*. Lisäksi on mahdollista valita autoon varusteita. Varusteet ovat kovakoodattuja tietokantaan ja ne haetaan sieltä. On myös mahdollista liittää ilmoitukseen kuva, jonka maksimikoko on enintään 100 kilotavua ja tiedostomuotoa *jpeg*.   
Kun käyttäjä on painanut *Lähetä* ohjaa sovellus takaisin etusivulle listaukseen, jossa ilmoitus sitten näkyy. Syötteiden tarkistus tehdään tässäkin kahteen otteeseen eli käyttöliittymän puolella ja palvelinpuolella.  
![ad_succesful](photos/car_added_succesfully.png)  
![own_ads2](photos/own_ads.png)

#### Ilmoitusten katselu  
Sovellus tunnistaa käyttäjän perusteella, onko tarkasteltava ilmoitus käyttäjän itsensä jättämä vai jonkun muun. Jos käyttäjän tarkastelema ilmoitus on kirjautuneena olevan käyttäjän itsensä jättämä, tarjotaan mahdollisuus ilmoituksen poistamiseen, ilmoituksen muokkaamiseen ja etusivulle siirtymiseen.  
![own_ad](photos/viewing_own_ad.png)  
Jos taas ilmoitus on jonkun muun, tarjotaan vain mahdollisuus siirtyä etusivulle:  
![someones_ad](photos/visitor_ad1.png)  
![someones_ad2](photos/visitor_ad2.png)  
Jos taas ilmoituksen katselija on admin, tarjotaan mahdollisuus poistaa ilmoitus esimerkiksi jos siinä on aiheeton myyntiteksti tai kuva.  
![admin_ad](photos/viewing_as_Admin.png)  
Ilmoitukseen liitettyä kuvaa on mahdollista katsella painamalla linkkiä, jolloin se ohjaa uudelle sivulle. Jos ilmoituksessa ei ole kuvaa, ei ole myöskään tarjolla linkkiä.

#### Ilmoituksen muokkaus
Jos käyttäjä painaa omassa ilmoituksessaan *Muokkaa ilmoitusta*, avautuu samanlainen sivu kuin jättäisi kokonaan uuden ilmoituksen. Valitettavasti tällä hetkellä sovellus ei osaa asettaa radiobutton-komponentteja oikeaan tilaan vaan ne menevät oletusasetuksiin, jolloin vastuu on käyttäjällä muistaa muuttaa myös ne vastaamaan alkuperäistä.  
Myöskään varuste-checkboxit eivät ole itsestään valittuna kun muokataan auton tietoja jolla on varusteita, mutta käyttäjän avuksi on laitettu informatiivinen teksti ja listaus viimeeksi valituista varusteista.  
![editing](photos/editing_own_ad1.png)  
![editing2](photos/edit2.png)  
Valitettavasti tällä hetkellä ilmoitukseen ei ole mahdollista lisätä jälkeenpäin kuvaa ja jos ilmoitukseen on liitetty luomisvaiheessa kuva niin ei ole mahdollista poistaa tai muokata kuvaa poistamatta vanhaa ilmoitusta ja tekemällä uutta. Lisäksi asettaessa tietokannasta tuleva data *Lisätiedot*-tekstikenttään tulee mukana useita välilyöntejä. Tämä ei ole vaarallista, vaan on vain jokin mystinen bugi.

### Ilmoituksen poisto  
Ilmoitus poistetaan painamalla painiketta *Poista ilmoitus*, jonka jälkeen käyttäjä ohjataan etusivulle.  
![remove](photos/ad_removed_succesfully.png)  
![own_ads3](photos/own_ads2.png)  

#### Omien tietojen muokkaus  
Käyttäjän on mahdollista muokata omia käyttäjätietojaan, poislukien muuttaa salasanaa tai käyttäjätunnustaan.  
![updating_user_data](photos/change_user_info.png)  
Painamalla *Lähetä* tiedot tallettuvat tietokantaan ja käyttäjä ohjataan etusivulle.  
![updated_succesfully](photos/user_info_changed_succesfully.png)  