# =============================================================================
# Storage Configuration
# =============================================================================

BASE_PATH       = ""                                # replace with the directory path of the python script
SHEET_URL_ID    = ""                                # replace with the google spreadsheet ID for open data
CRAWLER_FILE    = BASE_PATH + "verto_website.json"

# =============================================================================
# Checking Scope Configuration
# =============================================================================

AREA_LIST       = ["Downtown East Toronto", "West Toronto", "Unity Health Toronto"]
CLINIC_NAME     = { "WCC": "Wellesley Community Centre", \
                    "RPV": "Regent Park", \
                    "RUV": "Ryerson University", \
                    "WPA": "West Park Healthcare Centre", \
                    "CPH": "Community Place Hub", \
                    "SMV": "St. Michael’s Hospital", \
                    "SJV": "St. Joseph’s Health Centre", \
                    "HLC": "Humber Lakeshore"}
AREA_KEY        = {"West Toronto": "e85169bf-1248-4899-8b6a-86258fe976c7", \
                   "Downtown East Toronto": "b6f65518-d5bc-4113-b7ed-ee33f7574929", \
                   "Unity Health Toronto": "543efe0f-0318-4e53-86d7-2e83ac59bf48"}
AREA_CLINIC     = {"West Toronto": ["WPA", "CPH", "HLC"], \
                   "Downtown East Toronto": ["WCC", "RPV", "RUV"], \
                   "Unity Health Toronto": ["SMV", "SJV"]}
ELIGIBILITY     = {"West Toronto": {            "1st dose, 18+, 'M' postal codes": "COMMUNITIES", \
                                                "1st dose, age 12-17, 'M' postal codes": "AGE12TO17", \
                                                "2nd dose, Pfizer, eligible group": "PUBLICPFIZER2NDDOSE", \
                                                "2nd dose, Moderna, eligible group": "PUBLICMODERNA2NDDOSE" \
                                    }, \
                   "Downtown East Toronto": {   "1st dose, 18+, 'M' postal codes": "COMMUNITIES", \
                                                "1st dose, age 12-17, 'M' postal codes": "AGE12TO17", \
                                                "2nd dose, Pfizer, eligible group": "PFIZERSECONDPUBLIC", \
                                                "2nd dose, Moderna, eligible group": "MODERNASECONDPUBLIC" \
                                            }, \
                   "Unity Health Toronto": {    "1st dose, 18+, 'M' postal codes": "Communities", \
                                                "1st dose, age 12-17, 'M' postal codes": "AGE12TO17AREA"}}

# =============================================================================
# URL Configuration
# =============================================================================

BASE_URL        = "https://uht-public.vertoengage.com/engage/api/api/cac-open-clinic/v1/slots/availability"
CLINIC_URL      = "https://uht-public.vertoengage.com/engage/generic-open-clinic"

# =============================================================================
# Browser Crawler Behavior Configuration
# =============================================================================

MAX_RETRY       = 3
INTERVAL_SEC    = 0.1
CLOUDFLARE_SEC  = 5
WAITROOM_SEC    = 600

# =============================================================================
# Credentials Configuration
# =============================================================================

CAPTCHA_KEY             = ""    # Replace with the CAPTCHA key on verto health website (never expires)
TWITTER_CONSUMER_KEY    = ""    # Replace with credentials for the twitter bot account
TWITTER_CONSUMER_SECRET = ""    # Replace with credentials for the twitter bot account
TWITTER_ACCESS_KEY      = ""    # Replace with credentials for the twitter bot account
TWITTER_ACCESS_SECRET   = ""    # Replace with credentials for the twitter bot account
SHEET_KEY_FILE          = BASE_PATH + "vaccinebotto.json"  # Replace with the google service account key to update spreadsheet

# =============================================================================
# Message Text Configuration
# =============================================================================

ACCOUNT_BIO     = "A bot that checks vaccine appointment slots in Toronto community clinics. Developed by @Dr_DayiLin."
TWEET_TEMPLATE  = '''[{slot_str} SLOTS] at {clinic_str} available for {eligibility}:
{date_breakdown}

- Checked at: {timestamp_now}
- Book at: https://uht-public.vertoengage.com/engage/generic-open-clinic?key={area_key_str}'''
