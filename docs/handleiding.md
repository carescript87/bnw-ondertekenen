# Handleiding digitaal ondertekenen

## In het kort

Met `bnw-ondertekenen.netlify.app` laat BNW een praktijk de ledenovereenkomst of de kennismakersovereenkomst digitaal ondertekenen. Administratie vult de praktijkgegevens in en stuurt een persoonlijke link; de praktijk leest, tekent en mailt de pdf terug.

| Wie | Doet | Hoe lang |
| --- | --- | --- |
| Administratie BNW | maakt de link en mailt hem naar de praktijk | 2 minuten |
| Praktijk | controleert gegevens, leest, tekent, mailt de pdf naar administratie@bnw.nl | 10 minuten |
| Administratie BNW | controleert de pdf en slaat hem op in het dossier | 2 minuten |

Een link is vijf werkdagen geldig en werkt één keer. De praktijk kan de gegevens niet wijzigen; klopt er iets niet, dan maakt administratie een nieuwe link.

Adressen:

- Link maken (alleen BNW, sleutel nodig): `https://bnw-ondertekenen.netlify.app/intern-1e2da84950/`
- Beheer en inzendingen: `https://app.netlify.com/projects/bnw-ondertekenen`
- Contactadres voor praktijken: administratie@bnw.nl

## Voor administratie: een praktijk laten ondertekenen

Zorg dat u de gegevens van de praktijk bij de hand heeft: naam, adres, KVK-nummer, AGB-code van de praktijk en de naam van de eigenaar die tekent.

1. Open `https://bnw-ondertekenen.netlify.app/intern-1e2da84950/`.
2. Vul onder Toegang de BNW-sleutel in. Dit hoeft één keer per computer; de pagina onthoudt hem. De sleutel krijgt u van de beheerder.
3. Kies de overeenkomst: Ledenovereenkomst of Kennismakersovereenkomst.
4. Vul de zeven gegevens in. Postcode als `1234 AB`; KVK-nummer en AGB-code zijn elk 8 cijfers. De pagina meldt het als iets niet klopt.
5. Kies Maak link. U ziet de link en tot en met welke dag hij geldig is.
6. Kies Kopieer link en plak hem in uw e-mail aan de praktijk. Een voorbeeldtekst staat hieronder.
7. Wilt u zien wat de praktijk ziet, kies dan Bekijk wat de praktijk ziet. Teken daar niet: de link werkt één keer.

Voorbeeld van de e-mail aan de praktijk:

> **Onderwerp: Uw ledenovereenkomst met BNW ondertekenen**
>
> Beste [naam],
>
> Via onderstaande link ondertekent u de ledenovereenkomst met BNW digitaal. Wij hebben de gegevens van uw praktijk al ingevuld; u controleert ze, leest de overeenkomst en zet uw handtekening. Na het ondertekenen krijgt u de overeenkomst als pdf. Stuur die pdf naar administratie@bnw.nl.
>
> [link]
>
> De link is geldig tot en met [datum] en werkt één keer. Klopt er iets niet in de gegevens? Onderteken dan niet en mail ons; u ontvangt een nieuwe link.
>
> Met vriendelijke groet,
> Administratie BNW

Let op:

- Stuur de link alleen naar het e-mailadres van de praktijk. Wie de link heeft, kan de gegevens zien en tekenen.
- Een fout in de gegevens? Maak een nieuwe link; de oude blijft tot zijn vervaldatum geldig met de oude gegevens. Vraag de praktijk de oude link niet te gebruiken.
- Is de link verlopen of al gebruikt, dan maakt u gewoon een nieuwe.

## Voor de praktijk: de overeenkomst ondertekenen

Deze stappen kunt u letterlijk doorgeven aan een praktijk die vragen heeft. Ondertekenen werkt op computer, tablet en telefoon, in elke moderne browser.

1. Open de link uit de e-mail van BNW. De pagina haalt uw gegevens op.
2. Controleer onder 1. Uw gegevens de praktijknaam, het adres, het KVK-nummer, de AGB-code en de naam van de ondertekenaar. Klopt er iets niet? Onderteken dan niet en mail naar administratie@bnw.nl.
3. Lees onder 2. De overeenkomst de volledige tekst.
4. Teken onder 3. Ondertekening in het vak met uw vinger, een pen of de muis. Niet tevreden? Kies Wis handtekening en teken opnieuw.
5. Vink aan dat u de overeenkomst heeft gelezen en bevoegd bent om te tekenen.
6. Kies Onderteken en verstuur. De pagina maakt de pdf en slaat hem op bij BNW; de pdf verschijnt ook bij uw downloads.
7. Mail de pdf naar administratie@bnw.nl. Bent u de pdf kwijt, kies dan Download uw kopie op dezelfde pagina.

Na het versturen is de link verbruikt. Opent u hem opnieuw, dan ziet u alleen dat de overeenkomst al is ondertekend.

## Na ontvangst

1. U ontvangt de pdf per e-mail van de praktijk. Controleer of de gegevens op pagina 1 en de naam bij de handtekening overeenkomen met wat u heeft ingevuld.
2. Sla de pdf op in het dossier van de praktijk. BNW bewaart de pdf bij Netlify 30 dagen; daarna is hij daar weg.
3. Blijft de pdf uit? Kijk in Netlify onder Forms of de praktijk wel heeft getekend (zie hieronder). Zo ja, dan kunt u de pdf daar zelf ophalen via de pdf-link. Zo nee, herinner de praktijk.

**Inzendingen bekijken in Netlify**

1. Log in op Netlify en open het project `bnw-ondertekenen` (`https://app.netlify.com/projects/bnw-ondertekenen`).
2. Ga naar Forms en open het formulier `ondertekening`. Elke ondertekening staat erbij met praktijknaam, overeenkomst, tijdstip, IP-adres van de ondertekenaar en een pdf-link.
3. Open de pdf-link om de pdf te bekijken of te downloaden. De link werkt zonder inloggen; deel hem niet buiten BNW.
4. Ziet u een inzending niet, kijk dan onder Spam.

Oude inzendingen verwijderen is niet nodig: pdf's en gegevens worden na 30 dagen automatisch opgeruimd. Alleen de regel onder Forms blijft staan; die mag u handmatig verwijderen (kies de inzending, Delete).

## Veelgestelde vragen en problemen

| Vraag of melding | Oorzaak | Oplossing |
| --- | --- | --- |
| "De sleutel is onjuist" op de interne pagina | Verkeerde of verouderde BNW-sleutel | Vraag de actuele sleutel aan de beheerder en vul hem opnieuw in |
| De praktijk ziet "Deze link is niet compleet" | De link is niet volledig gekopieerd, of het deel achter `#` ontbreekt | Stuur de link opnieuw, als één geheel; of maak een nieuwe |
| De praktijk ziet "Deze link is verlopen" | Meer dan vijf werkdagen oud | Maak een nieuwe link |
| De praktijk ziet "Deze overeenkomst is al ondertekend" | De link is al gebruikt, bijvoorbeeld door een proefondertekening | Controleer onder Forms of de ondertekening er is; zo niet, maak een nieuwe link |
| "Versturen naar BNW is niet gelukt" bij de praktijk | Internetverbinding wegviel tijdens het versturen | De praktijk kiest opnieuw Onderteken en verstuur, of downloadt de kopie en mailt die |
| De gegevens in de overeenkomst kloppen niet | Typefout bij het aanmaken | Maak een nieuwe link met de juiste gegevens; vraag de praktijk de oude niet te gebruiken |
| De praktijk wil iets aan de tekst veranderen | De tekst is voor alle leden gelijk | Verwijs naar het bestuur; de tekst kan niet per praktijk worden aangepast |
| Tekenen lukt niet op de telefoon | Pagina is uitgezoomd of de browser is verouderd | Laat de praktijk de pagina vernieuwen of op een computer openen |
| De praktijk heeft twee overeenkomsten nodig | Elke link is voor één overeenkomst | Maak twee links, één per overeenkomst |

## Beheer

- **BNW-sleutel:** staat in Netlify bij het project onder Project configuration, Environment variables, als `INTERN_SLEUTEL`. Vervangen: nieuwe waarde invullen, het project opnieuw deployen (Deploys, Trigger deploy) en de nieuwe sleutel aan de medewerkers geven. Doe dit als een medewerker vertrekt of de sleutel is gelekt.
- **Bewaartermijn:** 30 dagen, instelbaar via `BEWAARTERMIJN_DAGEN` (daarna opnieuw deployen).
- **Toegang tot Netlify:** het project valt onder het team Vrone van Bastiaan Meijer. Vraag hem om een teamlidmaatschap als administratie zelf inzendingen wil bekijken.
- **Tekst van de overeenkomst wijzigen:** lever de nieuwe tekst aan bij de beheerder; de pagina's worden opnieuw gebouwd en uitgerold. Eerder gemaakte links blijven de oude tekst tonen tot ze verlopen.
- **E-mailmelding (nog in te stellen):** zodra in Netlify onder Forms, Form notifications een e-mailmelding naar administratie@bnw.nl is toegevoegd, hoeft de praktijk de pdf niet meer zelf te mailen. Meld dit bij de beheerder; de tekst op de ondertekenpagina wordt dan aangepast.
- **Technische documentatie:** zie *Technische opzet digitaal ondertekenen BNW* voor architectuur, beveiliging en de broncode op GitHub (`carescript87/bnw-ondertekenen`).
