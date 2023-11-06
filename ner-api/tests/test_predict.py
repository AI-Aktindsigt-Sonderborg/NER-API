from typing import Optional
from ..routers import predict
import asyncio
import pytest
from pydantic import BaseModel

class SourceText(BaseModel):
    text: str
    all_regex: Optional[bool] = False #All Regex
    all_keyword: Optional[bool] = False #All Keywords
    checks: Optional[list] = [] #Some Keywords and some Regex
    sensitive: Optional[bool] = False #Will not send the found word from the text, but only the positions
    filter_annotations: Optional[bool] = True #Will filter overlapping annotations

@pytest.mark.asyncio
class TestClassRegexCheck:
    async def test_predict_age(self):
        text = SourceText(text='Den 22. marts 2022 udfærdigede speciallæge i neurologi Karsten Bobby som er 40 år gammel en erklæring vedrørende 30-årige Frederik til Uddannelses- og Forskningsstyrelsen. Erklæringen skulle bruges i forbindelse med Frederikss ansøgning om handicaptillæg til hendes SU på grund af migræne.')
        result = await predict.predict_age(text)
        result = list(result['matches'])
        expected_match1 = "40"
        expected_match2 = "30"
        assert result[0]['match'] == expected_match1
        assert result[1]['match'] == expected_match2
        
    async def test_predict_cpr(self):
        text = SourceText(text='Den 22. marts 2022 skrev speciallæge Cindy (000090-0001) en mail til James, hvor han anførte, at han af personlige årsager var inderligt imod SU-handicaptillæg ved migræne, fordi han endnu ikke havde set et studium, der var lettere end det arbejde, som vedkommende efterfølgende skulle arbejde med. Hans cpr 0010100000 anførte videre, at han i henhold til de gældende regler var inhabil til at udtale sig om hendes skånebehov, og at han havde orienteret Uddannelses- og Forskningsstyrelsen om, at han var inhabil i spørgsmålet om skånebehov.')
        result = await predict.predict_cpr(text)
        result = list(result['matches'])
        expected_match1 = "000090-0001"
        expected_match2 = "0010100000"
        assert result[0]['match'] == expected_match1
        assert result[1]['match'] == expected_match2
    
    async def test_predict_cvr(self):
        text = SourceText(text='Disciplinærnævnet vurderer, at der er grundlag for at kritisere speciallæge i neurologi Freddy, cvr 28866984 for udfærdigelsen af erklæringen af den 22. marts 2022 CVR vedrørende 13612870 til Uddannelses- og Forskningsstyrelsen. Til sidst er der et tlf 28866984')
        result = await predict.predict_cvr(text)
        result = list(result['matches'])
        expected_match1 = "28866984"
        expected_match2 = "13612870"
        assert result[0]['match'] == expected_match1
        assert result[1]['match'] == expected_match2
    
    async def test_predict_date(self):
        text = SourceText(text='Disciplinærnævnet finder på den baggrund, at speciallæge i neurologi 25/10/09 ikke handlede med omhu og uhildethed ved udfærdigelsen af erklæringen af den 22. marts 2022 vedrørende  til Uddannelses- og Forskningsstyrelsen.')
        result = await predict.predict_date(text)
        result = list(result['matches'])
        expected_match1 = "25/10/09"
        expected_match2 = "22. marts 2022"
        assert result[0]['match'] == expected_match1
        assert result[1]['match'] == expected_match2
    
    async def test_predict_email(self):
        text = SourceText(text='Den 12. juli 2021 blev 29-årige mysite@ourearth.com kørt med ambulance til my.ownsite@ourearth.org, som traumepatient efter påkørsel af en løs trailer og fastklemning mellem en lygtepæl og traileren. Reservelæge A  tog imod hende og foretog en objektiv undersøgelse og ordinerede herefter en røntgenundersøgelse af brystkassen, bækkenet og venstre ben. Senere foretog reservelægen en supplerende objektiv undersøgelse af.')
        result = await predict.predict_email(text)
        result = list(result['matches'])
        expected_match1 = "mysite@ourearth.com"
        expected_match2 = "my.ownsite@ourearth.org"
        assert result[0]['match'] == expected_match1
        assert result[1]['match'] == expected_match2
        
    async def test_predict_gps(self):
        text = SourceText(text='Der blev foretaget en røntgenundersøgelse af brystkassen og bækkenet på traumestuen, 40° 41′ 21.4” N 74° 02′ 40.2” W og det blev vurderet, at røntgenbillederne ikke viste brud, blod i lungehulen (hæmothorax) og hul i lungehinderne (pneumothorax), hvorefter traumekaldet blev afblæst. Overlæge 45°23\'36.123456\"N 010°33\'48\"E fra  tolkede og beskrev røntgenbilleder af brystkassen.')
        result = await predict.predict_gps(text)
        result = list(result['matches'])
        expected_match1 = "40° 41′ 21.4” N 74° 02′ 40.2” W"
        expected_match2 = "45°23\'36.123456\"N 010°33\'48\"E"
        assert result[0]['match'] == expected_match1
        assert result[1]['match'] == expected_match2

    async def test_predict_guid(self):
        text = SourceText(text='Den 23. maj 2018 fik 44-årige guid 62d1fc56-9d57-4949-8d76-0cc9f96adae8 foretaget en kæbeoperation mod kæbeanomali (abnormiteter i kæbernes dimensioner) og blev efterfølgende udskrevet den 25. maj 2018 var efterfølgende til to kontroller den 29. maj og den 5. juni 2018, hvor det blev vurderet, at sammenbiddet ikke var optimalt. Der blev derfor truffet beslutning om at reoperere den 8. juni 2018, hvor man rettede på sammenbiddet.  kunne efterfølgende udskrives dagen efter. I perioden b3175c27-eaa3-43d2-9477-35f0c9ab0daa fra udskrivelsen og frem til den 18. juli 2018 blev  set til flere kontroller på afdelingen.')
        result = await predict.predict_guid(text)
        result = list(result['matches'])
        expected_match1 = "62d1fc56-9d57-4949-8d76-0cc9f96adae8"
        expected_match2 = "b3175c27-eaa3-43d2-9477-35f0c9ab0daa"
        assert result[0]['match'] == expected_match1
        assert result[1]['match'] == expected_match2
         
    async def test_predict_iban(self):
        text = SourceText(text='IBAN-nummeret er på 18 cifre og starter i Danmark altid med DK. Standarden for IBAN-nummeret blev oprindeligt udarbejdet af Den Europæiske Komité for Banktransaktionsstandarder DK9520000123456789 for at lette den automatiske behandling af internationale betalinger. IBAN-nummeret er opbygget af: 2 bogstaver, som karakteriserer landet, hvor kontoen er udstedt. 2 tal, som beregnes automatisk, og som sikrer, at IBAN-nummeret er korrekt Højst 30 tal og bogstaver, som i Danmark består af kontoens reg.nr. MU43BOMM0101123456789101000MUR og kontonummer Sammen med IBAN-nummeret skal du også bruge en BIC-kode (Bank Identifier Code). BIC-koden er bankens identifikationsnummer')
        result = await predict.predict_iban(text)
        result = list(result['matches'])
        expected_match1 = "DK9520000123456789"
        expected_match2 = "MU43BOMM0101123456789101000MUR"
        assert result[0]['match'] == expected_match1
        assert result[1]['match'] == expected_match2
    
    async def test_predict_kontonr(self):
        text = SourceText(text='Registreringsnummeret er på 4 cifre og kontonummeret er på op til 10 cifre. Du kan finde registreringsnummer og kontonummer 1234567890 på bagsiden af dit betalingskort (VISA/Dankort). Pas på ikke at forveksle kontonr 0987654321 med kort-nummeret, som er præget på kortets forside. Du kan også finde dit registrerings- og 1111222233 på dit kontoudtog fra banken.')
        result = await predict.predict_kontonr(text)
        result = list(result['matches'])
        expected_match1 = "1234567890"
        expected_match2 = "0987654321"
        assert result[0]['match'] == expected_match1
        assert result[1]['match'] == expected_match2
        
    async def test_predict_kvhx(self):
        text = SourceText(text='KVHX er en unik identifikator for an enhedsadresse, og er opbygget som følger: 01730722__2G__2__11, hvor K=kommunekode, V=vejkode, H=husnummer, E=etage, S=sidebetegnelse/dørnummer (numeriske værdier foranstilles med 0’er). Det er ikke konstant over tid, da den vil ændre sig hvis en adresse f. eks. skifter husnummer eller kommunekode. kvhx 01730722_10A__2__th BBR-ID og ZAP-ID er derfor bedre alternativer som nøgle for en enhedsadresse.')
        result = await predict.predict_kvhx(text)
        result = list(result['matches'])
        expected_match1 = "01730722__2G__2__11"
        expected_match2 = "01730722_10A__2__th"
        assert result[0]['match'] == expected_match1
        assert result[1]['match'] == expected_match2
            
    async def test_predict_matrikel(self):
        text = SourceText(text='Matrikelsystemet har til formål at danne overblik over samtlige faste ejendomme i landet. Systemet fokuserer ikke på selve ejendommen, Matrnr. 12a, men derimod kun på grunden hvor ejendommen ligger. Systemet har et register, som opbevarer alle relevante matrikeloplysninger. Registret indeholder følgende oplysninger om en matrikel: Matrikelbetegnelse, herunder matrikelnummer, landsbyområde og sogn, Arealstørrelse på matriklen, Lovbestemte noteringer f.eks. et matrikelnummer som 1453 i københavn. landbrugspligt eller fredskovspligt')
        result = await predict.predict_matrikel(text)
        print(result)
        result = list(result['matches'])
        expected_match1 = "12a"
        expected_match2 = "1453"
        assert result[0]['match'] == expected_match1
        assert result[1]['match'] == expected_match2
            
    async def test_predict_plate(self):
        text = SourceText(text='I Europa er nummerpladerne som regel aflange med alle tegn på én linje med dimensioner der ikke overstiger 52 x 12 cm. En typisk dansk plade er 50,2 x 12,0 cm. HJ24543 Der er dog i de fleste europæiske lande mulighed for nummerplader med tegnene fordelt på to linjer med dimensioner op til 34 x 24 cm. I de fleste lande i Nord- og Sydamerika anvendes nummerplader af størrelsen 30 x 15 cm med tegnene på én række og statsnavn, delstatsnavn, årstal eller andet med små tegn over og/eller under registreringsnummeret. AA55443 Motorcykler har de fleste steder nummerplader som er mindre end ovenstående mål. I Europa har motorcykler normalt ikke nummerplader større end 28 x 21 cm.')
        result = await predict.predict_plate(text)
        result = list(result['matches'])
        expected_match1 = "HJ24543"
        expected_match2 = "AA55443"
        assert result[0]['match'] == expected_match1
        assert result[1]['match'] == expected_match2
        
    async def test_predict_price(self):
        text = SourceText(text='Hvis du allerede har almindeligt kørekort til bil (Kategori B kørekort) så må du gerne køre med en trailer, hvis bilens tilladte totalvægt plus trailerens tilladte totalvægt ikke overstiger 3.500 kg. Har du erhvervet dit kørekort før 1/5-2009, så er reglerne lidt lempeligere, da det her gælder at bilens tilladte totalvægt plus trailerens faktiske vægt ikke må overstige 3.500 kg. Forvent at den ekstra pris for trailerkørekort vil ligge på ca. 4.000 kr. til op omkring 6.000 kr.')
        result = await predict.predict_price(text)
        result = list(result['matches'])
        expected_match1 = "4.000"
        expected_match2 = "6.000"
        assert result[0]['match'] == expected_match1
        assert result[1]['match'] == expected_match2
            
    async def test_predict_regnr(self):
        text = SourceText(text='Registreringsnummeret er på 4 cifre så regnr. 1234 er på op til 10 cifre. Du kan finde registreringsnummer og kontonummer på bagsiden af dit betalingskort (VISA/Dankort). Pas på ikke at forveksle kontonummeret med kort-nummeret, som er præget på kortets forside. Du kan også finde dit reg-nr 9876 på dit kontoudtog fra banken.')
        result = await predict.predict_regnr(text)
        result = list(result['matches'])
        expected_match1 = "1234"
        expected_match2 = "9876"
        assert result[0]['match'] == expected_match1
        assert result[1]['match'] == expected_match2
            
    async def test_predict_swift(self):
        text = SourceText(text='BIC-koden (Bank Identifier Code) bruges til entydigt at identificere banker i finansielle transaktioner på tværs af landegrænser. Swift DABADKKK Koden har en længde på 8 eller 11 karakterer. De første seks karakterer er altid bogstaver og resten er bogstaver og/eller tal. SWIFT: BKDNINBBDDR')
        result = await predict.predict_swift(text)
        result = list(result['matches'])
        expected_match1 = "DABADKKK"
        expected_match2 = "BKDNINBBDDR"
        assert result[0]['match'] == expected_match1
        assert result[1]['match'] == expected_match2
            
    async def test_predict_tlf(self):
        text = SourceText(text='Har du spørgsmål vedrørende en online ordre eller til et produkt du har købt i Matas, kan du få hurtigt svar ved at benytte vores kontaktformular eller skrive til kundeservice@matas.dk. Kontakt kundeservice på tlf. 4816 5544. Åbningstid på telefon: Mandag - fredag fra kl. 9.00 - 18.00 Lørdag kl. 10.00 - 15.00. Kundeservice åbningstider. Telefon +45 33 11 44 33 Vores kundeservice sidder til at hjælpe dig. Kontakt os som det passer dig, enten via telefon, e-mail eller chat')
        result = await predict.predict_tlf(text)
        result = list(result['matches'])
        expected_match1 = "4816 5544"
        expected_match2 = "+45 33 11 44 33"
        assert result[0]['match'] == expected_match1
        assert result[1]['match'] == expected_match2
            
    async def test_predict_url(self):
        text = SourceText(text='Den 12. juli 2021 blev 29-årige mysite@ourearth.com kørt med ambulance til my.ownsite@ourearth.org. Her er et link https://xn--hvidovrekreskole-txb.dk/personbil/?gclid=Cj0KCQjw1vSZBhDuARIsAKZlijTRQeoJIrUHFZ6SrGYM32IHFG9lYAyPBMTCSHmOVCq3g1gpw4OoUecaAvcMEALw_wcB, som traumepatient efter påkørsel af en løs trailer og fastklemning mellem en lygtepæl og traileren. support.magasin.dk/hc/da/requests/new. Reservelæge A  tog imod hende og foretog en objektiv undersøgelse og ordinerede herefter en røntgenundersøgelse af brystkassen, bækkenet og venstre ben. Senere foretog reservelægen en supplerende objektiv undersøgelse af.')
        result = await predict.predict_url(text)
        result = list(result['matches'])
        expected_match1 = "https://xn--hvidovrekreskole-txb.dk/personbil/?gclid=Cj0KCQjw1vSZBhDuARIsAKZlijTRQeoJIrUHFZ6SrGYM32IHFG9lYAyPBMTCSHmOVCq3g1gpw4OoUecaAvcMEALw_wcB"
        expected_match2 = "support.magasin.dk/hc/da/requests/new"
        assert result[0]['match'] == expected_match1
        assert result[1]['match'] == expected_match2
            
    async def test_predict_vin(self):
        text = SourceText(text='Alle biler efter 1981 har et unikt, 17-cifret stelnummer. Nummerets VF12RFL1H49621453 vigtigste funktioner er helt klart, at det kan bruges til at slå oplysninger om et køretøj op og herunder blandt andet blive klogere på, om der er gæld i bilen, hvornår den sidst har været til syn, hvis navn den er registreret i, og om den eventuelt skulle være meldt stjålet. Stelnr. VGA42000000005857 Men værksteder og automekanikere bruger også nummeret til at blive klogere på, hvilket indmad der er i bilen i form af motor og bremsesystemer, så de på den måde kan vælge den rigtige vedligeholdelses- og servicemetode.')
        result = await predict.predict_vin(text)
        result = list(result['matches'])
        expected_match1 = "VF12RFL1H49621453"
        expected_match2 = "VGA42000000005857"
        assert result[0]['match'] == expected_match1
        assert result[1]['match'] == expected_match2

@pytest.mark.asyncio
class TestClassKeywordCheck:   
    async def test_predict_authority(self):
        text = SourceText(text='I 2017 udkom den digitale publikation Det offentlige Danmark for første gang. Publikationen er en afløser for ”Hof & Stat”, som er blevet publiceret i varierende udgaver siden 1734. ”Hof & Stat” blev sidst udgivet i 2014. På grund af efterspørgsel fra særligt forskningsmiljøer blev det besluttet at udarbejde Det offentlige Danmark som en ny, digital udgave af ”Hof & Stat”. Udgangspunktet for Det offentlige Danmark er, at den omfatter alle myndigheder med selvstændig bevilling på finansloven, undtaget selvejende institutioner. Beredskabsstyrelsen I forhold til ”Hof & Stat” er der således tale om en slankere version af oversigten over de offentlige myndigheder, der primært fokuserer på indretningen af departementer og styrelser, domstolene samt organiseringen af Folketinget, Statsrådet, kommuner og regioner.')
        result = await predict.predict_authority(text)
        result = list(result['matches'])
        expected_match1 = "Beredskabsstyrelsen"
        expected_match2 = "Domstolene"
        assert result[0]['match'] == expected_match1
        assert result[1]['match'] == expected_match2
        
    async def test_predict_commune(self):
        text = SourceText(text='Ankenævnet finder efter en samlet vurdering, at Aarhus kommune var sindssyg, og at det ville være uforsvarligt ikke at tvangsbehandle ham, da udsigten til hans helbredelse eller en betydelig og afgørende bedring i tilstanden ellers ville blive væsentligt forringet. Aalborg kommune Nævnet har herved lagt vægt på, at han befandt sig i en psykotisk tilstand præget af manglende sygdomsindsigt, vrangforestillinger, hallucinationer samt svære tankeforstyrrelser.')
        result = await predict.predict_commune(text)
        result = list(result['matches'])
        expected_match1 = "Aarhus Kommune"
        expected_match2 = "Aalborg Kommune"
        assert result[0]['match'] == expected_match1
        assert result[1]['match'] == expected_match2
        
    async def test_predict_complaint(self):
        text = SourceText(text='Det fremgår videre af bekendtgørelse om anvendelse af anden tvang end frihedsberøvelse på psykiatriske afdelinger § 3, stk. 3, at overlægen i sin vurdering af betænkningstidens varighed blandt andet skal lægge vægt på sygdommens alvorlighed og varighed, Huslejenævn patientens ambivalens i forhold til behandlingstilbuddet, om den manglende medicinering vil kunne medføre anvendelse af andre former for tvang, samt patientens forpinthed m.v. Skat Det fremgår endeligt af § 3, stk. 2, at patienten skal have en passende betænkningstid, hvor patienten får lejlighed til at overveje sit eventuelle samtykke til behandlingen. Patienten har dog krav på højst tre dages betænkningstid.')
        result = await predict.predict_complaint(text)
        result = list(result['matches'])
        expected_match1 = "Huslejenævn"
        expected_match2 = "Skat"
        assert result[0]['match'] == expected_match1
        assert result[1]['match'] == expected_match2
        
    async def test_predict_crime(self):
        text = SourceText(text='Det fremgår af journalen, at Indbrud i lejlighed blev motiveret for hele den primære tvangsbehandling dagligt fra den 26. april 2021 kl. 14:10 til der den 29. april 2021 kl. 15:02 blev truffet beslutning om tvangsbehandling med smeltetablet Olanzapin 10 mg dagligt stigende afhængigt af effekt og bivirkninger til højest 20 mg dagligt, subsidiært injektion Zyprexa 5 mg stigende afhængigt af effekt og bivirkninger til højest to injektioner af 5 mg dagligt med pause på tredjedagen, og efter stabilisering på Bedrageri med øvrig afgifts- eller tilskudslovgivning - grov Olanzapin overgang til depotinjektion Zypadhera 210 mg hver anden uge stigende til højest 300 mg hver anden uge afhængigt af effekt og bivirkninger.')
        result = await predict.predict_crime(text)
        result = list(result['matches'])
        expected_match1 = "Indbrud"
        expected_match2 = "Bedrageri"
        assert result[0]['match'] == expected_match1
        assert result[1]['match'] == expected_match2
        
    async def test_predict_diagnose(self):
        text = SourceText(text='Det er på denne baggrund ankenævnets opfattelse, Spiseforstyrrelser at mindstemiddelsprincippet indebærer, at tvangsbehandling med injektion som udgangspunkt må betragtes som et mere indgribende middel end peroral behandling. adhd Det er nævnets praksis, at behandling med depotmedicin som udgangspunkt anses for den mest indgribende behandlingsform, hvorfor der skal være særlige grunde til stede for at vælge denne behandlingsform.')
        result = await predict.predict_diagnose(text)
        result = list(result['matches'])
        expected_match1 = "Spiseforstyrrelser"
        expected_match2 = "ADHD"
        assert result[0]['match'] == expected_match1
        assert result[1]['match'] == expected_match2
        
    async def test_predict_ethnicity(self):
        text = SourceText(text='Det er ankenævnets vurdering Albansk, at det som udgangspunkt ikke er i overensstemmelse med mindstemiddelprincippet, at der træffes beslutning om flere på hinanden følgende tvangsbehandlinger på samme tidspunkt. Indfødt Alaska Det skyldes, at patienten ved denne fremgangsmåde fratages muligheden for under indflydelse af den indledende behandling at forholde sig til spørgsmålet om den efterfølgende behandling.')
        result = await predict.predict_ethnicity(text)
        result = list(result['matches'])
        expected_match1 = "Albansk"
        expected_match2 = "Indfødt Alaska"
        assert result[0]['match'] == expected_match1
        assert result[1]['match'] == expected_match2
        
    async def test_predict_gender(self):
        text = SourceText(text='Ankenævnet kan videre oplyse, at det fremgår af medicinoversigten på pro.medicin.dk, at ved behandling af skizofreni med tablet Olanzapin, Ciskønnet anvendes initialt 5-10 mg en gang dagligt, fortrinsvis ved sengetid. Vedligeholdelsesdosis er sædvanligvis 5-20 mg dagligt. Det kan dog, i særlige tilfælde, være nødvendigt og forsvarligt at øge døgndosis op til højst 40 mg i døgnet.Endvidere kan ankenævnet oplyse, at det fremgår af medicinoversigten på pro.medicin.dk, at ved behandling med injektion Zyprexa (olanzapin) anvendes initialt 5-10 mg intramuskulært. Dosis kan gentages efter to timer og eventuelt igen efter fire timer efter anden injektion. Der bør højst gives tre injektioner og samlet op til 20 mg i døgnet. Kønsneutral Sikkerheden ved doser over 30 mg i døgnet er ikke undersøgt.')
        result = await predict.predict_gender(text)
        result = list(result['matches'])
        expected_match1 = "Ciskønnet"
        expected_match2 = "Kønsneutral"
        assert result[0]['match'] == expected_match1
        assert result[1]['match'] == expected_match2
        
    async def test_predict_medicine(self):
        text = SourceText(text='Ankenævnet kan oplyse, at det fremgår af psykiatrilovens § 31, stk. 1, Panodil at patienten skal underrettes om den påtænkte tvang, dens nærmere indhold, baggrund og formål. Det fremgår videre af bekendtgørelsens § 3, stk. 6, at tvangsmedicinering forudsætter, at patienten er fuldt informeret om behandlingens formål, virkninger og mulige bivirkninger. Det er ankenævnets opfattelse, at informationen skal indeholde oplysninger om både det primære, Palonosetronhydrochlorid det subsidiære og det tertiære præparat, idet der er en mulighed for, at tvangsbehandlingen iværksættes med det subsidiære og det tertiære præparat.')
        result = await predict.predict_medicine(text)
        result = list(result['matches'])
        expected_match1 = "Panodil"
        expected_match2 = "Palonosetronhydrochlorid"
        assert result[0]['match'] == expected_match1
        assert result[1]['match'] == expected_match2
        
    async def test_predict_nationality(self):
        text = SourceText(text='Ankenævnet finder imidlertid ikke, at sagen var tilstrækkeligt oplyst, canadier da Det Psykiatriske Patientklagenævn traf afgørelse om fortsat tvangsbehandling af  den 16. juli 2019, idet der ikke var indhentet journalmateriale fra før overflytningen, der kunne belyse s tilstand fra den 11. april 2019 og frem til overflytningen. venezuelaner Efter ankenævnets vurdering kan journalmaterialet fra den 20.- 29. juni 2019 ikke stå alene ved den aktuelle vurdering af sagen, herunder i forhold til vurderingen af om  fortsat var sindssyg og om den fortsatte tvangsbehandling opfyldte kravet om mindst indgribende foranstaltning for så vidt angår behandlingens udstrækning. Ankenævnet vurderer på den baggrund, at Nævnet derfor burde have indhentet journalmateriale fra før overflytningen den 20. juni 2019.')
        result = await predict.predict_nationality(text)
        result = list(result['matches'])
        expected_match1 = "canadier"
        expected_match2 = "venezuelaner"
        assert result[0]['match'] == expected_match1
        assert result[1]['match'] == expected_match2
        
    async def test_predict_region(self):
        text = SourceText(text='Det fremgår videre af psykiatrilovens § 4, stk. Region Midtjylland 4, at tvang ikke må anvendes i videre omfang, end hvad der er nødvendigt for at opnå det tilsigtede formål. Dette indebærer, at der skal ske en begrænsning i den tidsmæssige udstrækning af en tvangsforanstaltning til det absolut nødvendige. Ifølge lovens § 21 har overlægen til stadighed ansvaret for,Region Hovedstaden at frihedsberøvelse, tvangsbehandling, tvangsfiksering, fysisk magt og beskyttelsesfiksering ikke anvendes i videre omfang end nødvendigt.')
        result = await predict.predict_region(text)
        result = list(result['matches'])
        expected_match1 = "Region Midtjylland"
        expected_match2 = "Region Hovedstaden"
        assert result[0]['match'] == expected_match1
        assert result[1]['match'] == expected_match2
        
    async def test_predict_religion(self):
        text = SourceText(text='Det er ankenævnets opfattelse, at en patient i betænkningstiden skal tilbydes en konkret behandling. Jødedommen Tvangsbehandling skal som udgangspunkt iværksættes med det præparat og den dosis, som der er motiveret for, medmindre der foreligger særlige omstændigheder, der kan begrunde andet. Hvis patienten ikke er motiveret for den konkrete behandling Kristne kan motivationen ikke medregnes i betænkningstiden.')
        result = await predict.predict_religion(text)
        result = list(result['matches'])
        expected_match1 = "Jødedommen"
        expected_match2 = "Kristne"
        assert result[0]['match'] == expected_match1
        assert result[1]['match'] == expected_match2
        
    async def test_predict_religiouscommunity(self):
        text = SourceText(text='Det fremgår desuden af § 3, stk. 1, i Russisk ortodoks menighed bekendtgørelse om anvendelse af anden tvang end frihedsberøvelse på psykiatriske afdelinger, at tvangsmedicinering forudsætter at vedvarende forsøg er gjort på at forklare patienten behandlingens nødvendighed, bortset fra akutte situationer, hvor udsættelse af behandlingen er til fare for patientens liv eller helbred. Af § 3, stk. 5, fremgår at patienten i betænkningstiden dagligt skal tilbydes medicin til frivillig indtagelse, og at den forsøgte motivation skal journalføres. Af § 3, stk. 4, fremgår hertil, Worldwide Church of God at patienten så vidt muligt skal have haft mulighed for at drøfte spørgsmålet med sin patientrådgiver.')
        result = await predict.predict_communities(text)
        result = list(result['matches'])
        expected_match1 = "Russisk ortodoks menighed"
        expected_match2 = "Worldwide Church of God"
        assert result[0]['match'] == expected_match1
        assert result[1]['match'] == expected_match2
        
    async def test_predict_sexuality(self):
        text = SourceText(text='Ankenævnet har imidlertid fundet grundlag for at tilsidesætte overlægens skøn om, Ambiseksuel at en betænkningstid på 3 døgn og 23 timer var passende for , da det fremgår af journalen at han blev vurderet farlig for sine omgivelser samt i fare for at udvikle delirium. Han var således tvangsfikseret i hele motivationsperioden og fik desuden dagligt indgivet beroligende middel med magt, hvorfor ankenævnet vurderer, Multiseksuel at betænkningstiden var unødig lang.')
        result = await predict.predict_sexuality(text)
        result = list(result['matches'])
        expected_match1 = "Ambiseksuel"
        expected_match2 = "Multiseksuel"
        assert result[0]['match'] == expected_match1
        assert result[1]['match'] == expected_match2

    async def test_predict_union(self):
        text = SourceText(text='Det er ankenævnets opfattelse, at der skal motiveres konkret for det dosisinterval, Krifa der efterfølgende træffes beslutning om. Det skal fremgå af journalen, at der er motiveret for hele dosisintervallet. Det fremgår af journalen, at  blev motiveret for hele den primære tvangsbehandling dagligt fra den 4. marts 2016 kl. 10.10 til der den 8. marts 2016 kl. 8.50 blev truffet beslutning om tvangsbehandling med tablet Serenase 5 mg dagligt, stigende til maksimalt 20 mg dagligt fordelt på 2 doser. Vagt- og Sikkerhedsfunktionærernes Fagforening Alternativt injektion Serenase 5 mg dagligt stigende til maksimalt 10 mg dagligt.')
        result = await predict.predict_union(text)
        result = list(result['matches'])
        expected_match1 = "Krifa"
        expected_match2 = "Vagt- og Sikkerhedsfunktionærernes Fagforening"
        assert result[0]['match'] == expected_match1
        assert result[1]['match'] == expected_match2