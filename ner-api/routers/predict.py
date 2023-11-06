from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel
import timeit


#Regex checker imports
# from text_handler.regex_search.rules import age, cpr, cvr, email, plate, vin, kontonr, kvhx, guid, tlf, date, gps, regnr, swift, iban, price, url, matrikel, law
from text_handler.regex_search.regex import age, cpr, cvr, email, plate, vin, kontonr, kvhx, guid, tlf, date, gps, regnr, swift, iban, price, url, matrikel, direktivnr
from text_handler.keyword_search import keyword_handler as kwhandler
from text_handler import functions as func

router = APIRouter()
data_titles = { "authority":"MYNDIGHED","commune":"KOMMUNE","complaint":"KLAGENÆVN","crime":"FORBRYDELSE","diagnose":"HELBRED","ethnicity":"ETNICITET","gender":"KØN","medicine":"MEDIKAMENT","nationality":"NATIONALITET","region":"REGION","religion":"IDEOLOGI","religiouscommunity":"TROSSAMFUND","sexuality":"SEKSUALITET","union":"FAGFORENING" }

class SourceText(BaseModel):
    text: str
    all_regex: Optional[bool] = False #All Regex
    all_keyword: Optional[bool] = False #All Keywords
    checks: Optional[list] = [] #Some Keywords and some Regex
    sensitive: Optional[bool] = False #Will not send the found word from the text, but only the positions
    filter_annotations: Optional[bool] = True #Will filter overlapping annotations
    # Entities which can be added to the list of cheks:
    # age, cpr, cvr, date, email, gps, guid, iban, kvhx, matrikel, plate, price, swift, tlf, url, vin, authority, commune, complaint, crime, diagnose, ethnicity, gender, medicine,nationality, region, religion, religiouscommunity, sexuality, uniion


@router.post("/age")
async def predict_age(srcText: SourceText):
    age_search = age.Age()
    return {
        "status_code": 200,
        "matches":age_search.match_regex(srcText.text, srcText.sensitive)
    }
    
@router.post("/cpr")
async def predict_cpr(srcText: SourceText):
    cpr_search = cpr.CPR()
    return {
        "status_code": 200,
        "matches":cpr_search.match_regex(srcText.text, srcText.sensitive)
    }
    
@router.post("/cvr")
async def predict_cvr(srcText: SourceText):
    cvr_search = cvr.CVR()
    return {
        "status_code": 200,
        "matches":cvr_search.match_regex(srcText.text, srcText.sensitive)
    }
    
@router.post("/date")
async def predict_date(srcText: SourceText):
    date_search = date.Date()
    return {
        "status_code": 200,
        "matches":date_search.match_regex(srcText.text, srcText.sensitive)
    }
    
@router.post("/email")
async def predict_email(srcText: SourceText):
    email_search = email.Email()
    return {
        "status_code": 200,
        "matches":email_search.match_regex(srcText.text, srcText.sensitive)
    }
    
@router.post("/gps")
async def predict_gps(srcText: SourceText):
    gps_search = gps.GPS()
    return {
        "status_code": 200,
        "matches":gps_search.match_regex(srcText.text, srcText.sensitive)
    }
    
@router.post("/guid")
async def predict_guid(srcText: SourceText):
    guid_search = guid.GUID()
    return {
        "status_code": 200,
        "matches":guid_search.match_regex(srcText.text, srcText.sensitive)
    }
    
@router.post("/iban")
async def predict_iban(srcText: SourceText):
    iban_search = iban.IBAN()
    return {
        "status_code": 200,
        "matches":iban_search.match_regex(srcText.text, srcText.sensitive)
    }
    
@router.post("/kontonr")
async def predict_kontonr(srcText: SourceText):
    kontonr_search = kontonr.Kontonr()
    return {
        "status_code": 200,
        "matches":kontonr_search.match_regex(srcText.text, srcText.sensitive)
    }    
    
@router.post("/kvhx")
async def predict_kvhx(srcText: SourceText):
    kvhx_search = kvhx.KVHX()
    return {
        "status_code": 200,
        "matches":kvhx_search.match_regex(srcText.text, srcText.sensitive)
    }
    
@router.post("/matrikel")
async def predict_matrikel(srcText: SourceText):
    matrikel_search = matrikel.Matrikel()
    return {
        "status_code": 200,
        "matches":matrikel_search.match_regex(srcText.text, srcText.sensitive)
    }

@router.post("/direktivnr")
async def predict_law(srcText: SourceText):
    law_search = direktivnr.Direktivnr()
    return {
        "status_code": 200,
        "matches":law_search.match_regex(srcText.text, srcText.sensitive)
    }
    
@router.post("/plate")
async def predict_plate(srcText: SourceText):
    plate_search = plate.Plate()
    return {
        "status_code": 200,
        "matches":plate_search.match_regex(srcText.text, srcText.sensitive)
    }
    
@router.post("/price")
async def predict_price(srcText: SourceText):
    price_search = price.Price()
    return {
        "status_code": 200,
        "matches":price_search.match_regex(srcText.text, srcText.sensitive)
    }
    
@router.post("/regnr")
async def predict_regnr(srcText: SourceText):
    regnr_search = regnr.Regnr()
    return {
        "status_code": 200,
        "matches":regnr_search.match_regex(srcText.text, srcText.sensitive)
    }
    
@router.post("/swift")
async def predict_swift(srcText: SourceText):
    swift_search = swift.Swift()
    return {
        "status_code": 200,
        "matches":swift_search.match_regex(srcText.text, srcText.sensitive)
    }
    
@router.post("/tlf")
async def predict_tlf(srcText: SourceText):
    tlf_search = tlf.Tlf()
    return {
        "status_code": 200,
        "matches":tlf_search.match_regex(srcText.text, srcText.sensitive)
    }
    
@router.post("/url")
async def predict_url(srcText: SourceText):
    url_search = url.URL()
    return {
        "status_code": 200,
        "matches":url_search.match_regex(srcText.text, srcText.sensitive)
    }
    
@router.post("/vin")
async def predict_vin(srcText: SourceText):
    vin_search = vin.VIN()
    return {
        "status_code": 200,
        "matches":vin_search.match_regex(srcText.text, srcText.sensitive)
    }

@router.post("/authority")
async def predict_authority(srcText: SourceText):
    extracted_keywords = kwhandler.get_keyword_processor(data_titles['authority']).extract_keywords(srcText.text, span_info=True)
    return {
        "status_code": 200,
        "matches": kwhandler.provide_match_info(extracted_keywords, srcText.text, srcText.sensitive, kwhandler.category_guid['authority']) 
    }

@router.post("/commune")
async def predict_commune(srcText: SourceText):
    extracted_keywords = kwhandler.get_keyword_processor(data_titles['commune']).extract_keywords(srcText.text, span_info=True)
    return {
        "status_code": 200,
        "matches": kwhandler.provide_match_info(extracted_keywords, srcText.text, srcText.sensitive, kwhandler.category_guid['commune'])
    }

@router.post("/complaint")
async def predict_complaint(srcText: SourceText):
    extracted_keywords = kwhandler.get_keyword_processor(data_titles['complaint']).extract_keywords(srcText.text, span_info=True)
    return {
        "status_code": 200,
        "matches": kwhandler.provide_match_info(extracted_keywords, srcText.text, srcText.sensitive, kwhandler.category_guid['complaint'])
    }

@router.post("/crime")
async def predict_crime(srcText: SourceText):
    extracted_keywords = kwhandler.get_keyword_processor(data_titles['crime']).extract_keywords(srcText.text, span_info=True)
    return {
        "status_code": 200,
        "matches": kwhandler.provide_match_info(extracted_keywords, srcText.text, srcText.sensitive, kwhandler.category_guid['crime'])
    }

@router.post("/diagnose")
async def predict_diagnose(srcText: SourceText):
    extracted_keywords = kwhandler.get_keyword_processor(data_titles['diagnose']).extract_keywords(srcText.text, span_info=True)
    return {
        "status_code": 200,
        "matches": kwhandler.provide_match_info(extracted_keywords, srcText.text, srcText.sensitive, kwhandler.category_guid['diagnose'])
    }

@router.post("/ethnicity")
async def predict_ethnicity(srcText: SourceText):
    extracted_keywords = kwhandler.get_keyword_processor(data_titles['ethnicity']).extract_keywords(srcText.text, span_info=True)
    return {
        "status_code": 200,
        "matches": kwhandler.provide_match_info(extracted_keywords, srcText.text, srcText.sensitive, kwhandler.category_guid['ethnicity'])
    }

@router.post("/gender")
async def predict_gender(srcText: SourceText):
    extracted_keywords = kwhandler.get_keyword_processor(data_titles['gender']).extract_keywords(srcText.text, span_info=True)
    return {
        "status_code": 200,
        "matches": kwhandler.provide_match_info(extracted_keywords, srcText.text, srcText.sensitive, kwhandler.category_guid['gender'])
        }

@router.post("/medicine")
async def predict_medicine(srcText: SourceText):
    extracted_keywords = kwhandler.get_keyword_processor(data_titles['medicine']).extract_keywords(srcText.text, span_info=True)
    return {
        "status_code": 200,
        "matches": kwhandler.provide_match_info(extracted_keywords, srcText.text, srcText.sensitive, kwhandler.category_guid['medicine'])
    }

@router.post("/nationality")
async def predict_nationality(srcText: SourceText):
    extracted_keywords = kwhandler.get_keyword_processor(data_titles['nationality']).extract_keywords(srcText.text, span_info=True)
    return {
        "status_code": 200,
        "matches": kwhandler.provide_match_info(extracted_keywords, srcText.text, srcText.sensitive, kwhandler.category_guid['nationality'])
    }

@router.post("/region")
async def predict_region(srcText: SourceText):
    extracted_keywords = kwhandler.get_keyword_processor(data_titles['region']).extract_keywords(srcText.text, span_info=True)
    return {
        "status_code": 200,
        "matches": kwhandler.provide_match_info(extracted_keywords, srcText.text, srcText.sensitive, kwhandler.category_guid['region'])
    }

@router.post("/religion")
async def predict_religion(srcText: SourceText):
    extracted_keywords = kwhandler.get_keyword_processor(data_titles['religion']).extract_keywords(srcText.text, span_info=True)
    return {
        "status_code": 200,
        "matches": kwhandler.provide_match_info(extracted_keywords, srcText.text, srcText.sensitive, kwhandler.category_guid['religion'])
    }

@router.post("/religiouscommunity")
async def predict_communities(srcText: SourceText):
    extracted_keywords = kwhandler.get_keyword_processor(data_titles['religiouscommunity']).extract_keywords(srcText.text, span_info=True)
    return {
        "status_code": 200,
        "matches": kwhandler.provide_match_info(extracted_keywords, srcText.text, srcText.sensitive, kwhandler.category_guid['religiouscommunity'])
    }

@router.post("/sexuality")
async def predict_sexuality(srcText: SourceText):
    extracted_keywords = kwhandler.get_keyword_processor(data_titles['sexuality']).extract_keywords(srcText.text, span_info=True)
    return {
        "status_code": 200,
        "matches": kwhandler.provide_match_info(extracted_keywords, srcText.text, srcText.sensitive, kwhandler.category_guid['sexuality'])
    }

@router.post("/union")
async def predict_union(srcText: SourceText):
    extracted_keywords = kwhandler.get_keyword_processor(data_titles['union']).extract_keywords(srcText.text, span_info=True)
    return {
        "status_code": 200,
        "matches": kwhandler.provide_match_info(extracted_keywords, srcText.text, srcText.sensitive, kwhandler.category_guid['union'])
    }

@router.post("/custom")
async def predict_all_checks(srcText: SourceText):
    start = timeit.default_timer()
    print(f"--Custom Request Recieved--\n\
    options - defaults if nothing provided.\n\
    text length: {len(srcText.text)} characters\n\
    is searching Regex categories (all_regex): {srcText.all_regex}\n\
    is searching List of Words categories (all_keyword): {srcText.all_keyword}\n\
    custom entities to search (checks): {srcText.checks}\n\
    is sensitive (sensitive): {srcText.sensitive}\n\
    --Custom Request Recieved--")
    all_matches = []
    # REGEX & CHECKS - age, cpr, cvr, date, email, gps, guid, iban, kvhx, matrikel, plate, price, swift, tlf, url, vin
    if srcText.all_regex or "age" in srcText.checks:
        age_search = age.Age()
        all_matches.extend(age_search.match_regex(srcText.text, srcText.sensitive))
    if srcText.all_regex or "cpr" in srcText.checks:
        cpr_search = cpr.CPR()
        all_matches.extend(cpr_search.match_regex(srcText.text, srcText.sensitive))
    if srcText.all_regex or "cvr" in srcText.checks:
        cvr_search = cvr.CVR()
        all_matches.extend(cvr_search.match_regex(srcText.text, srcText.sensitive))
    if srcText.all_regex or "date" in srcText.checks:
        date_search = date.Date()
        all_matches.extend(date_search.match_regex(srcText.text, srcText.sensitive))
    if srcText.all_regex or "email" in srcText.checks:
        date_search = email.Email()
        all_matches.extend(date_search.match_regex(srcText.text, srcText.sensitive))
    if srcText.all_regex or "gps" in srcText.checks:
        gps_search = gps.GPS()
        all_matches.extend(gps_search.match_regex(srcText.text, srcText.sensitive))
    if srcText.all_regex or "guid" in srcText.checks:
        guid_search = guid.GUID()
        all_matches.extend(guid_search.match_regex(srcText.text, srcText.sensitive))
    if srcText.all_regex or "iban" in srcText.checks:
        iban_search = iban.IBAN()
        all_matches.extend(iban_search.match_regex(srcText.text, srcText.sensitive))
    if srcText.all_regex or "kontonr" in srcText.checks:
        kontonr_search = kontonr.Kontonr()
        all_matches.extend(kontonr_search.match_regex(srcText.text, srcText.sensitive))
    if srcText.all_regex or "kvhx" in srcText.checks:
        kvhx_search = kvhx.KVHX()
        all_matches.extend(kvhx_search.match_regex(srcText.text, srcText.sensitive))
    if srcText.all_regex or "matrikel" in srcText.checks:
        mat_search = matrikel.Matrikel()
        all_matches.extend(mat_search.match_regex(srcText.text, srcText.sensitive))
    if srcText.all_regex or "law" in srcText.checks:
        law_search = direktivnr.Direktivnr()
        all_matches.extend(law_search.match_regex(srcText.text, srcText.sensitive))
    if srcText.all_regex or "plate" in srcText.checks:
        plate_search = plate.Plate()
        all_matches.extend(plate_search.match_regex(srcText.text, srcText.sensitive))
    if srcText.all_regex or "price" in srcText.checks:
        price_search = price.Price()
        all_matches.extend(price_search.match_regex(srcText.text, srcText.sensitive))
    if srcText.all_regex or "regnr" in srcText.checks:
        regnr_search = regnr.Regnr()
        all_matches.extend(regnr_search.match_regex(srcText.text, srcText.sensitive))
    if srcText.all_regex or "swift" in srcText.checks:
        swift_search = swift.Swift()
        all_matches.extend(swift_search.match_regex(srcText.text, srcText.sensitive))
    if srcText.all_regex or "tlf" in srcText.checks:
        tlf_search = tlf.Tlf()
        all_matches.extend(tlf_search.match_regex(srcText.text, srcText.sensitive))
    if srcText.all_regex or "url" in srcText.checks:
        url_search = url.URL()
        all_matches.extend(url_search.match_regex(srcText.text, srcText.sensitive))
    if srcText.all_regex or "vin" in srcText.checks:
        vin_search = vin.VIN()
        all_matches.extend(vin_search.match_regex(srcText.text, srcText.sensitive))
    
    # KEYWORDS & CHECKS - authority, commune, complaint, crime, diagnose, ethnicity, gender, medicine,nationality, region, religion, religiouscommunity, sexuality, uniion
    if "authority" in srcText.checks or srcText.all_keyword:
        extracted_matches = kwhandler.get_keyword_processor(data_titles['authority']).extract_keywords(srcText.text, span_info=True)
        all_matches.extend(kwhandler.provide_match_info(extracted_matches, srcText.text, srcText.sensitive, kwhandler.category_guid['authority']))
    if "commune" in srcText.checks or srcText.all_keyword:
        extracted_matches = kwhandler.get_keyword_processor(data_titles['commune']).extract_keywords(srcText.text, span_info=True)
        all_matches.extend(kwhandler.provide_match_info(extracted_matches, srcText.text, srcText.sensitive, kwhandler.category_guid['commune']))
    if "complaint" in srcText.checks or srcText.all_keyword:
        extracted_matches = kwhandler.get_keyword_processor(data_titles['complaint']).extract_keywords(srcText.text, span_info=True)
        all_matches.extend(kwhandler.provide_match_info(extracted_matches, srcText.text, srcText.sensitive, kwhandler.category_guid['complaint']))
    if "crime" in srcText.checks or srcText.all_keyword:
        extracted_matches = kwhandler.get_keyword_processor(data_titles['crime']).extract_keywords(srcText.text, span_info=True)
        all_matches.extend(kwhandler.provide_match_info(extracted_matches, srcText.text, srcText.sensitive, kwhandler.category_guid['crime']))
    if "diagnose" in srcText.checks or srcText.all_keyword:
        extracted_matches = kwhandler.get_keyword_processor(data_titles['diagnose']).extract_keywords(srcText.text, span_info=True)
        all_matches.extend(kwhandler.provide_match_info(extracted_matches, srcText.text, srcText.sensitive, kwhandler.category_guid['diagnose']))
    if "ethnicity" in srcText.checks or srcText.all_keyword:
        extracted_matches = kwhandler.get_keyword_processor(data_titles['ethnicity']).extract_keywords(srcText.text, span_info=True)
        all_matches.extend(kwhandler.provide_match_info(extracted_matches, srcText.text, srcText.sensitive, kwhandler.category_guid['ethnicity']))
    if "gender" in srcText.checks or srcText.all_keyword:
        extracted_matches = kwhandler.get_keyword_processor(data_titles['gender']).extract_keywords(srcText.text, span_info=True)
        all_matches.extend(kwhandler.provide_match_info(extracted_matches, srcText.text, srcText.sensitive, kwhandler.category_guid['gender']))
    if "medicine" in srcText.checks or srcText.all_keyword:
        extracted_matches = kwhandler.get_keyword_processor(data_titles['medicine']).extract_keywords(srcText.text, span_info=True)
        all_matches.extend(kwhandler.provide_match_info(extracted_matches, srcText.text, srcText.sensitive, kwhandler.category_guid['medicine']))
    if "nationality" in srcText.checks or srcText.all_keyword:
        extracted_matches = kwhandler.get_keyword_processor(data_titles['nationality']).extract_keywords(srcText.text, span_info=True)
        all_matches.extend(kwhandler.provide_match_info(extracted_matches, srcText.text, srcText.sensitive, kwhandler.category_guid['nationality']))
    if "region" in srcText.checks or srcText.all_keyword:
        extracted_matches = kwhandler.get_keyword_processor(data_titles['region']).extract_keywords(srcText.text, span_info=True)
        all_matches.extend(kwhandler.provide_match_info(extracted_matches, srcText.text, srcText.sensitive, kwhandler.category_guid['region']))
    if "religion" in srcText.checks or srcText.all_keyword:
        extracted_matches = kwhandler.get_keyword_processor(data_titles['religion']).extract_keywords(srcText.text, span_info=True)
        all_matches.extend(kwhandler.provide_match_info(extracted_matches, srcText.text, srcText.sensitive, kwhandler.category_guid['religion']))
    if "religiouscommunity" in srcText.checks or srcText.all_keyword:
        extracted_matches = kwhandler.get_keyword_processor(data_titles['religiouscommunity']).extract_keywords(srcText.text, span_info=True)
        all_matches.extend(kwhandler.provide_match_info(extracted_matches, srcText.text, srcText.sensitive, kwhandler.category_guid['religiouscommunity']))
    if "sexuality" in srcText.checks or srcText.all_keyword:
        extracted_matches = kwhandler.get_keyword_processor(data_titles['sexuality']).extract_keywords(srcText.text, span_info=True)
        all_matches.extend(kwhandler.provide_match_info(extracted_matches, srcText.text, srcText.sensitive, kwhandler.category_guid['sexuality']))
    if "union" in srcText.checks or srcText.all_keyword:
        extracted_matches = kwhandler.get_keyword_processor(data_titles['union']).extract_keywords(srcText.text, span_info=True)
        all_matches.extend(kwhandler.provide_match_info(extracted_matches, srcText.text, srcText.sensitive, kwhandler.category_guid['union']))
    if srcText.filter_annotations:
        all_matches = func.remove_inner_annotations(all_matches)
    end = timeit.default_timer()
    print(f'Time Elapsed: {round(end - start, 5)} seconds')
    return {
        "status_code": 200,
        "matches": all_matches
    }