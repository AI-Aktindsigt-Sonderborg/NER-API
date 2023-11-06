# NER-API Version 1.0
This is a REST API which can be used to search for certain different entities in a large amount of text.
The main language for this version is Danish.
Developed by Aktio.ai and published by Sønderborg Kommune.

## Running the API/Server
*Make sure you have a docker system up and running before running docker commands.*
0. (optional) change the docker-compose.yml file to your needs (port and host)
1. change directory to the root of this project
2. run: $ docker-compose up -d

# NER API Usage
Here is a complete list of NER endpoints, examples and relevant information.

## Input Attributes
| attribute | description |
| ------- | ------- |
| *(text: string), REQUIRED* | **The input text to search** |
| (all_regex: boolean), default = False  | **Searches the text for entities using RegEx** |
| (all_keyword: boolean), default = False  | **Searches the text for entities using a list of Keywords** |
| (checks: list[]), default = [] | **This can be used if only some entities are desired to use (NB: It is not usable for model entities yet). Add a list/array of strings - check Entities String List below.** |
| (sensitive: boolean), default = False  | **This will blur out the found words from the text, but keep the positions in the result** |
| (filter_annotations: boolean), default = True  | **This will filter overlapping annotations and remove them from the result** |

### Entities String List
["age", "cpr", "cvr", "date", "email", "gps", "guid", "iban", "kontonr", "kvhx", "law", "matrikel", "plate", "price", "regnr", "swift", "tlf", "url", "vin", "authority", "commune", "complaint", "crime", "diagnose", "ethnicity", "gender", "medicine", "nationality", "region", "religion", "religiouscommunity", "sexuality", "union"]

## Endpoints (Danish) 33 Total

### Brugerdefineret/custom (All Entitites)
- **Endpoint:** ”/predict/custom”
- **Beskrivelse:** Finder matches baseret på valgt søgning
- **Validering:** 
  - **Blacklist**
  - **Ordliste**
  - **Whitelist**
- **Parametre:** sensitivitet, alle regex, alle ordlister, modellen = true/false. Eller liste af ord [url, cpr, cvr].

### 1.	Alder (age)
- **Endpoint:** ”/predict/age”
- **Beskrivelse:** Hele tal forbundet med ord der omtaler alder.
- **Valideringer:** 
  - **Required Whitelist:** "age", "år", "år.", "gammel", "alder", "årige"
  - **Blacklist:** 
- **Eksempel:** "24 år", "I en alder af 24", "den er 24 gammel"
- **Tag:** ALDER
- **Parametre:** sensitivitet = true/false

### 2.	CPR-Nummer (cpr)
- **Endpoint:** ”/predict/cpr”
- **Beskrivelse:** Ticifret, personligt identifikationsnummer.
- **Valideringer:** 
  - **Whitelist:** ”cpr”
  - **Blacklist:** 
- **Eksempel:** "0000001111", "000000-1111"
- **Tag:** CPR
- **Parametre:** sensitivitet = true/false

### 3.	CVR-Nummer (cvr)
- **Endpoint:** ”/predict/cvr”
- **Beskrivelse:** Ottecifret, virksomheds identifikationsnummer.
- **Valideringer:** 
  - **Modulus11**
  - **Required Whitelist:** ”cvr”
  - **Blacklist:** "tlf", ”tlf.” "telefon", "tlfnr", ”tlfnr.”
- **Eksempel:** "12345678"
- **Tag:** CVR
- **Parametre:** sensitivitet = true/false

### 4.	Dato (date)
- **Endpoint:** ”/predict/date”
- **Beskrivelse:** En dato, med variernde format.
- **Valideringer:**
  - **Whitelist:** "date", "dato", "den", "d"
  - **Blacklist:** ”tlf”
- **Eksempel:** "04/20/2009", "04-20-09", "1/1/21", "Mar-20-2009", "20-Marts-09", "2009", "Mar 22", "Feb 2009", "6/2009", "20. Marts", "Marts 2021"
- **Tag:** DATO
- **Parametre:** sensitivitet = true/false

### 5.	Email (email)
- **Endpoint:** ”/predict/email”
- **Beskrivelse:** Emailadresse der skal indeholde '@' efterfulgt af et domæne.
- **Valideringer:**
  - **Whitelist:** "email", "mail"
  - **Blacklist:** 
- **Eksempel:** "mysite@ourearth.com", "my.ownsite@ourearth.org", "mysite@you.me.net"
- **Tag:** EMAIL
- **Parametre:** sensitivitet = true/false

### 6.	Etnicitet (ethnicity)
- **Endpoint:** ”/predict/ethnicity”
- **Beskrivelse:** Hele eller dele af ord forbundet med en etnicitet.
- **Valideringer:** 
  - **Ordliste**
- **Eksempel:** "Albansk", "Indfødt Alaska"
- **Tag:** ETNICITET
- **Parametre:** sensitivitet = true/false

### 7.	Fagforening (union)
- **Endpoint:** ”/predict/union”
- **Beskrivelse:** Danske navne på kendte fagforeninger.
- **Valideringer:** 
  - **Ordliste**
- **Eksempel:** "Krifa", "Vagt- og Sikkerhedsfunktionærernes Fagforening"
- **Tag:** FAGFORENING
- **Parametre:** sensitivitet = true/false

### 8.	Forbrydelse (crime)
- **Endpoint:** ”/predict/crime”
- **Beskrivelse:** Hele eller dele af ord forbundet med domme eller straffe (ej hele sætninger!).
- **Valideringer:** 
  - **Ordliste**
- **Eksempel:** "Indbrud i lejlighed", "Bedrageri med øvrig afgifts- eller tilskudslovgivning - grov"
- **Tag:** FORBRYDELSER
- **Parametre:** sensitivitet = true/false

### 9.	GPS (gps)
- **Endpoint:** ”/predict/gps”
- **Beskrivelse:** Tal og tegn sammensat som GPS Koordinater
- **Valideringer:**
  - **Whitelist:** ”gps”, ”kordinater”
  - **Blacklist:** 
- **Eksempel:** "40° 41′ 21.4” N 74° 02′ 40.2” W", "45°23'36.123456"N 010°33'48"E", "-124.082778° 40.866389°"
- **Tag:** GPS
- **Parametre:** sensitivitet = true/false

### 10.	GUID (guid)
- **Endpoint:** ”/predict/guid”
- **Beskrivelse:** Tal og bogstaver sammensat til et globalt unik ID-identifikator
- **Valideringer:**
  - **Whitelist:** ”guid”, ”uuid”
  - **Blacklist:**
- **Eksempel:** "3F2504E0-4F89-41D3-9A0C-0305E82C3301"
- **Tag:** GUID
- **Parametre:** sensitivitet = true/false

### 11.	Helbred (diagnose)
- **Endpoint:** ”/predict/diagnose”
- **Beskrivelse:** Hele eller dele af navnet på eks. en diagnose, psykisk eller somatisk sygdom.
- **Valideringer:** 
  - **Ordliste**
- **Eksempel:** "Spiseforstyrrelser", "ADHD"
- **Tag:** HELBRED
- **Parametre:** sensitivitet = true/false

### 12.	Iban (iban)
- **Endpoint:** ”/predict/iban”
- **Beskrivelse:** Tal og bogstaver sammensat til Internationale bankkontonummer
- **Valideringer:**
  - **Whitelist:** ”iban”
  - **Blacklist:**  
- **Eksempel:** "FR123456789234888963D567401"
- **Tag:** IBAN
- **Parametre:** sensitivitet = true/false

### 13.	Ideologi (religion)
- **Endpoint:** ”/predict/religion”
- **Beskrivelse:** Hele eller dele af en ideologi eller religion.
- **Valideringer:**
  - **Ordliste**
- **Eksempel:** "Jødedommen", "Kristne"
- **Tag:** IDEOLOGI
- **Parametre:** sensitivitet = true/false

### 14.	Klagenævn (complaint organisation)
- **Endpoint:** ”/predict/complaint”
- **Beskrivelse:** "Danske navne på kendte klagenævn."
- **Valideringer:**
  - **Ordliste**
- **Eksempel:** "Huslejenævn", "Skat"
- **Tag:** KLAGENÆVN
- **Parametre:** sensitivitet = true/false

### 15.	Kommune (commune)
- **Endpoint:** ”/predict/commune”
- **Beskrivelse:** Navne på danske kommuner
- **Valideringer:**
  - **Ordliste**
- **Eksempel:** "Odense Kommune", "Holbæk Kommune"
- **Tag:** KOMMUNE
- **Parametre:** sensitivitet = true/false

### 16.	Konto nummer (kontonr)
- **Endpoint:** ”/predict/kontonr”
- **Beskrivelse:** Dansk bank kontonummer på 10 cifre
- **Valideringer:**
  - **Required Whitelist:** "kontonr", "kontonr.", "konto", "konto.", "konto-nr", "konto-nr.", "konto nr", "konto nr.", "kontonummer"
  - **Blacklist:**
- **Eksempel:** ”3154079025”
- **Tag:** KONTONR
- **Parametre:** sensitivitet = true/false

### 17.	Kvhx (kvhx)
- **Endpoint:** ”/predict/kvhx”
- **Beskrivelse:** Tal og bogstaver der beskriver en unik identifikator for an enhedsadresse
- **Valideringer:**
  - **Whitelist:** ”kvhx”
  - **Blacklist:**
- **Eksempel:** ”01730722__2G__2__11", "01470688___4_st__tv"
- **Tag:** KVHX
- **Parametre:** sensitivitet = true/false

### 18.	Køn (gender)
- **Endpoint:** ”/predict/gender”
- **Beskrivelse:** Hele eller dele ord forbundet med person køn
- **Valideringer:**
  - **Ordliste**
- **Eksempel:** ”Ciskønnet", "Kønsneutral"
- **Tag:** KØN
- **Parametre:** sensitivitet = true/false

### 19.	Matrikelnummer (matrikel)
- **Endpoint:** ”/predict/matrikel”
- **Beskrivelse:** Sammensat bogstaver og tal der udgør et matrikelnummer
- **Valideringer:**
  - **Required Whitelist:** "matr", "matr.", "mat", "mat.", "matrikel", "matrikelnummer", "matrnr", "matnr", "matr.nr.", "mat.nr.", "mat.nr", "matr.nr", "mat-nr", "matr-nr"
  - **Blacklist:** "husnr", "husnr.", "hnr", "vejnr", "vejnr."
- **Eksempel:** "12", "402a", "5403", "14abc"
- **Tag:** MATRIKELNUMMER
- **Parametre:** sensitivitet = true/false

### 20.	Medikament (medicine)
- **Endpoint:** ”/predict/medicine”
- **Beskrivelse:** Hele eller dele af navnet på medicin eller medikament.
- **Valideringer:** 
  - **Ordliste**
- **Eksempel:** "Panodil", "Palonosetronhydrochlorid"
- **Tag:** MEDIKAMENT
- **Parametre:** sensitivitet = true/false

### 21.	Myndighed (authority)
- **Endpoint:** ”/predict/authority”
- **Beskrivelse:** Danske navne på kendte myndigheder.
- **Valideringer:**
  - **Ordliste**
- **Eksempel:** "Ankestyrelsen", "Beredskabsstyrelsen"
- **Tag:** MYNDIGHED
- **Parametre:** sensitivitet = true/false

### 22.	Nationalitet (nationality)
- **Endpoint:** ”/predict/nationality”
- **Beskrivelse:** Hele eller dele ord forbundet med nationalitet
- **Valideringer:**
  - **Ordliste**
- **Eksempel:** "canadier", "venezuelaner"
- **Tag:** NATIONALITET
- **Parametre:** sensitivitet = true/false

### 23.	Nummerplade (plate) 
- **Endpoint:** ”/predict/plate”
- **Beskrivelse:** Bogstaver efterfulgt af tal sammensat som en dansk nummerplade (ikke brugerdefinerede nummerplade)
- **Valideringer:** 
  - **Whitelist:** "plate", "platenumber", "nummerplade"
  - **Blacklist:**
- **Eksempel:** "HW24054"
- **Tag:** NUMMERPLADE
- **Parametre:** sensitivitet = true/false

### 24.	Pris (price)
NB: Careful when using Price. It is very difficult to create a good regex and validation to get the correct prices.
- **Endpoint:** ”/predict/price”
- **Beskrivelse:** Tal og valuta forbundet med priser (afhængig af valutanavn)
- **Valideringer:** 
  - **Required Whitelist:** "pris","dollar", "dollars", "euros", "euro", "kroner", "yen", "rubler", "bitcoin", "ethereum", "CNY", "EUR", "DKK", "USD", "BTC", "XBT", "ETC", "LTC", "XRP", "USDT", "XMR", "kr", "$", "£", "€", "¥", "₩"
  - **Blacklist:** "kl", "nr", "stk"
- **Eksempel:** "25 kroner", "€4500.45", "50 USD"
- **Tag:** PRIS
- **Parametre:** sensitivitet = true/false

### 25.	Produkt (None)
Not currently available
- **Endpoint:** None
- **Beskrivelse:** Hele eller dele af ord forbundet med produkter (ej hele sætninger!).
- **Valideringer:** None
- **Eksempel:** None
- **Tag:** PRODUKT
- **Parametre:** sensitivitet = true/false

### 26.	RegNr (regnr)
- **Endpoint:** ”/predict/regnr”
- **Beskrivelse:** Danske registreringsnummre på 4 cifre.
- **Valideringer:**
  - **Required Whitelist:** "regnr", "regnr.", "reg", "reg.", "reg-nr", "reg-nr.", "reg nr", "reg nr.", "reg nummer", "regnummer"
  - **Blacklist:** 
- **Eksempel:**  ”0040”, ”5020”
- **Tag:** REGNR
- **Parametre:** sensitivitet = true/false

### 27.	Region (region)
- **Endpoint:** ”/predict/region”
- **Beskrivelse:** Danske navne på regioner
- **Valideringer:** 
  - **Ordliste**
- **Eksempel:** "Region Midtjylland", "Region Hovedstaden"
- **Tag:** REGION
- **Parametre:** sensitivitet = true/false

### 28.	Seksualitet (sexuality)
- **Endpoint:** ”/predict/sexuality”
- **Beskrivelse:** Hele eller dele af ord forbundet med en seksualitet.
- **Valideringer:**
  - **Ordliste**
- **Eksempel:** "Ambiseksuel", "Multiseksuel"
- **Tag:** SEKSUALITET
- **Parametre:** sensitivitet = true/false

### 29.	Stelnummer (vin)
- **Endpoint:** ”/predict/vin”
- **Beskrivelse:** Tal og bogstaver sammensat til en blis stelnummer.
- **Valideringer:**
  - **Whitelist:** ” vin", "stelnr", "stelnummer" 
  - **Blacklist:**
- **Eksempel:** "VF12RFL1H49621453", "VGA42000000005857"
- **Tag:** STELNUMMER
- **Parametre:** sensitivitet = true/false

### 30.	SWIFT (swift)
- **Endpoint:** ”/predict/swift”
- **Beskrivelse:** 8-cifret/11-cifret af tal og bogstaver som bank identifikationskode
- **Valideringer:**
  - **Required Whitelist:** "swift", "bic", "iban", "society", "worldwide", "interbank", "financial", "telecommunication", "bank", "identifier", "code"
  - **Blacklist:**
- **Eksempel:** "UNCAITMMXXX"
- **Tag:** SWIFT
- **Parametre:** sensitivitet = true/false

### 31.	Telefon nummer (tlf)
- **Endpoint:** ”/predict/tlf”
- **Beskrivelse:** Tal sammensat som til et dansk telefonnummer
- **Valideringer:**
  - **Whitelist:** "tlf", "telefon", "nr", "nummer", "kontakt"
  - **Blacklist:** ”cvr”
- **Eksempel:** "+45 40 50 60 70", "40506070"
- **Tag:** TELEFONNUMMER
- **Parametre:** sensitivitet = true/false

### 32.	Trossamfund (religious community)
- **Endpoint:** ”/predict/religiouscommunity”
- **Beskrivelse:** Danske navne på trossamfund eller menigheder.
- **Valideringer:**
  - **Ordliste**
- **Eksempel:** "Russisk ortodoks menighed", "Worldwide Church of God"
- **Tag:** TROSSAMFUND
- **Parametre:** sensitivitet = true/false

### 33.	URL (url)
- **Endpoint:** ”/predict/url”
- **Beskrivelse:** Ord, tal og tegn sammensat til en URL weblink.
- **Valideringer:**
  - **Whitelist:** ”url”, ”web”, ”link”
  - **Blacklist:**
- **Eksempel:** "pro.medicin.dk", "www.google.com", "https://google.us.edi?34535/534534?dfg=g&fg", "google.com"
- **Tag:** URL
- **Parametre:** sensitivitet = true/false

### Orddefinition:
- **Whitelist:** Ord omkring match kan indeholde et whitelisted ord.
- **Required Whitelist:** Ord omkring match SKAL indholde et whitelisted ord.
- **Blacklist:** Ord omkring match må ikke indeholde et blacklisted ord.
- **Ordliste:** Søger entiteter i hele teksten baseret på en ordliste.