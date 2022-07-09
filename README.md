My process of completing this task were as follows:

1. I checked what data is required to be scraped
2. I checked the links provided and looked if the data is easily visible on the page
3. At this point I thought of multiple ways of scraping the data:
  - sending requests to the page and scraping the DOM (quite slow and hard to manipulate)
  - using the public API (takes a while to get API keys, can be restricting sometimes)
  - using the endpoints they use during page load (easy, data is readily available)
4. I chose to investigate the endpoints that are used during page load and opened up chrome dev tools (on https://www.airbnb.co.uk/rooms/20669368)
5. I filtered all requests using CTRL+F 'Little Country' and found a request where the property title is given as a response
6. Below is a call to the API that Airbnb makes

https://www.airbnb.co.uk/api/v3/StaysPdpSections?operationName=StaysPdpSections&locale=en-GB&currency=GBP&variables={"id":"U3RheUxpc3Rpbmc6MjA2NjkzNjg=","pdpSectionsRequest":{"adults":"1","bypassTargetings":false,"categoryTag":null,"causeId":null,"children":null,"disasterId":null,"discountedGuestFeeVersion":null,"displayExtensions":null,"federatedSearchId":null,"forceBoostPriorityMessageType":null,"infants":null,"interactionType":null,"layouts":["SIDEBAR","SINGLE_COLUMN"],"pets":0,"pdpTypeOverride":null,"preview":false,"previousStateCheckIn":null,"previousStateCheckOut":null,"priceDropSource":null,"privateBooking":false,"promotionUuid":null,"relaxedAmenityIds":null,"searchId":null,"selectedCancellationPolicyId":null,"selectedRatePlanId":null,"splitStays":null,"staysBookingMigrationEnabled":false,"translateUgc":null,"useNewSectionWrapperApi":false,"sectionIds":["BOOK_IT_FLOATING_FOOTER","EDUCATION_FOOTER_BANNER_MODAL","BOOK_IT_CALENDAR_SHEET","CANCELLATION_POLICY_PICKER_MODAL","POLICIES_DEFAULT","BOOK_IT_SIDEBAR","URGENCY_COMMITMENT_SIDEBAR","BOOK_IT_NAV","EDUCATION_FOOTER_BANNER","URGENCY_COMMITMENT"],"checkIn":null,"checkOut":null,"p3ImpressionId":"p3_1657279153_jHp1I46e4CiIu3c+"}}&extensions={"persistedQuery":{"version":1,"sha256Hash":"7ef281634f2824262c9f7e56bd5afa278cf341da77a26ad204c444109951eaef"}}

7. I compared this with another property and found that the call is identical apart from the ID
8. I noticed that the ID looks a lot like base64, so I entered it into a decoder and got the following:
  - Base64Encoded: U3RheUxpc3Rpbmc6MjA2NjkzNjg=
  - Base64Decoded: StayListing:20669368

9. From this we can begin trying to query the API using api/v3/StaysPdpSections and our own encrypted property IDs.
10. To start coding, I like to copy the request (see above) from dev tools as a cURL and use a cURL converter which converts the request into a language of my choice (Python). I like to use Python and its Requests module for scraping pages/APIs, which is what I'll be using for this task. This also allows me to test quickly if the request produces the same response when replicated. See below.

curl 'https://www.airbnb.co.uk/api/v3/StaysPdpSections?operationName=StaysPdpSections&locale=en-GB&currency=GBP&variables=%7B%22id%22%3A%22U3RheUxpc3Rpbmc6MjA2NjkzNjg%3D%22%2C%22pdpSectionsRequest%22%3A%7B%22adults%22%3A%221%22%2C%22bypassTargetings%22%3Afalse%2C%22categoryTag%22%3Anull%2C%22causeId%22%3Anull%2C%22children%22%3Anull%2C%22disasterId%22%3Anull%2C%22discountedGuestFeeVersion%22%3Anull%2C%22displayExtensions%22%3Anull%2C%22federatedSearchId%22%3Anull%2C%22forceBoostPriorityMessageType%22%3Anull%2C%22infants%22%3Anull%2C%22interactionType%22%3Anull%2C%22layouts%22%3A%5B%22SIDEBAR%22%2C%22SINGLE_COLUMN%22%5D%2C%22pets%22%3A0%2C%22pdpTypeOverride%22%3Anull%2C%22preview%22%3Afalse%2C%22previousStateCheckIn%22%3Anull%2C%22previousStateCheckOut%22%3Anull%2C%22priceDropSource%22%3Anull%2C%22privateBooking%22%3Afalse%2C%22promotionUuid%22%3Anull%2C%22relaxedAmenityIds%22%3Anull%2C%22searchId%22%3Anull%2C%22selectedCancellationPolicyId%22%3Anull%2C%22selectedRatePlanId%22%3Anull%2C%22splitStays%22%3Anull%2C%22staysBookingMigrationEnabled%22%3Afalse%2C%22translateUgc%22%3Anull%2C%22useNewSectionWrapperApi%22%3Afalse%2C%22sectionIds%22%3Anull%2C%22checkIn%22%3Anull%2C%22checkOut%22%3Anull%7D%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%227ef281634f2824262c9f7e56bd5afa278cf341da77a26ad204c444109951eaef%22%7D%7D' \
  -H 'authority: www.airbnb.co.uk' \
  -H 'accept: */*' \
  -H 'accept-language: en-GB,en-US;q=0.9,en;q=0.8,la;q=0.7' \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -H 'cookie: bev=1624308629_MTIxMjgzYmVlM2Fh; _aat=0%7CaywbzY9qcZ6eEFoRLLDTSMYacFqUu4Y7%2FeLqjtFp42%2FX7kt2b0nbgFenqfiEPaql; abb_fa2=%7B%22user_id%22%3A%2263%7C1%7C7rBvkO1VRGq4zZ%2BoWu8nataEnZawkds4X6cUbsacyDlw0D46HeWEkgM%3D%22%7D; _airbed_session_id=2ffe4501b2a13af9383fd4041f96db58; cdn_exp_b910f64ca3b409af4=treatment; cdn_exp_edca6a5ab9666c814=control; cdn_exp_7b27e8582f6ea5b25=control; cdn_exp_fea7ec9bd22598e31=treatment; cdn_exp_664025b35de9ca5f8=control; OptanonConsent=0_183345%3A1%2C0_179751%3A1%2C0_183219%3A1%2C0_200003%3A1%2C0_200005%3A1%2C0_179747%3A1%2C0_183241%3A1%2C0_200007%3A1%2C0_179754%3A1%2C0_179750%3A1%2C0_179737%3A1%2C0_179744%3A1%2C0_179739%3A1%2C0_179743%3A1%2C0_179749%3A1%2C0_200012%3A1%2C0_200011%3A1%2C0_183217%3A1%2C0_183096%3A1%2C0_179740%3A1%2C0_179752%3A1%2C0_183346%3A1%2C0_183095%3A1; OptanonAlertBoxClosed=2022-07-08T10%3A53%3A01.275Z; cookieConsentId=175089914; _csrf_token=V4%24.airbnb.co.uk%24Q7h5uyluow4%24NyVUC4FWkYEvr-5CTW_DeZ5vhmS-aU2nw3d95RwdIIA%3D; flags=8192; roles=0; fbs=connected; auth_jitney_session_id=ce2f731c-b908-4880-991d-222afa01d4d2; cdn_exp_7d88e310aadc73d9b=treatment; _abck=3213BF8C49309253DD1DD94838891718~0~YAAQWpp6XMLSj5aBAQAAaf1j4gjNmJPZLZHUewSuB2E14+GlEu4rGFTBRvToe2+NBI61C0jvPl5JpbiKWwbmjaDY+PxdKmuukkYcVY0lWTaJrnDJyOXvoFqN9OM3NG8+S+WB5p8RxvBVfqkI4UfhHwkk1UYqt/oMLBrkvutjDjAXjIbyAbZL2QI/oqvQeCX4acAIQ9KzC0tlvpnx36WXaPESWwxE+o8ak6VGaZU75Jl1kkRfnavKYKxcRBUmo7VqK+/IcD0aFsmab0AdGb0AZAdSC+lw8IxxEqEEAlDRYHwHcUybwydmVqxqz7pkZRmiKs8ueGHNdhczXGQV/zRRiurhwIXmUW9MKQm8/xWZn4v+ALfh/YZld86simXeY7IY8DmDO+hLeDWF2rP+283a7K47LSxekOwZ4ws=~-1~-1~-1; bm_sz=6C685D40A2E8AC89A77F1D9F4F2FA438~YAAQWpp6XMPSj5aBAQAAaf1j4hCGYvsAZHGJE/9t08BW3Jbcd8mVBKGT5jDaywZjr4HxlIAS9Ab3TccYYrdVZM6ACoHBTD77M2Zb/s1Z//4Q+Q99wQbPCuP0sWmYqeIwFvY7IUo/BcjS/rHFl+YTr+xIRMwTmWzhwe3QMsRSvtO1L+XPBs6QrHpb7KYdd60dnvPMYa0R6jmV5PrRGGIntRIWQAV9VCbGCf8DYfcwJo1W6Xjd/RX0yCzPqAdzX3TsR/O5xegdTDADKqV6P+W84H7DLYqjqOBsSRdekiw+MIMqM4Dk2w==~3159345~4604471; jitney_client_session_id=469637e3-d58a-40da-b6b2-be78d0dde073; jitney_client_session_created_at=1657360667; _user_attributes=%7B%22curr%22%3A%22GBP%22%2C%22guest_exchange%22%3A0.832605%2C%22device_profiling_session_id%22%3A%221624308646--037643bef31d32a6a5ae750d%22%2C%22giftcard_profiling_session_id%22%3A%221657360666-249816458-692a4b43c7b852e4943dd2c3%22%2C%22reservation_profiling_session_id%22%3A%221657360666-249816458-c27627d58c27977c0c8e03c3%22%2C%22id%22%3A249816458%2C%22hash_user_id%22%3A%2251f2ab23ae90f42cacfbb767febbeb088d8ddd2b%22%2C%22eid%22%3A%22L50nS-XRAjsifYlInpA1_A%3D%3D%22%2C%22num_h%22%3A0%2C%22num_trip_notif%22%3A0%2C%22name%22%3A%22Arnas%22%2C%22num_action%22%3A0%2C%22is_admin%22%3Afalse%2C%22can_access_photography%22%3Afalse%2C%22travel_credit_status%22%3Anull%2C%22referrals_info%22%3A%7B%22receiver_max_savings%22%3Anull%2C%22receiver_savings_percent%22%3Anull%2C%22receiver_signup%22%3Anull%2C%22referrer_guest%22%3A%22%C2%A315%22%2C%22terms_and_conditions_link%22%3A%22%2Fhelp%2Farticle%2F2269%22%2C%22wechat_link%22%3Anull%2C%22offer_discount_type%22%3Anull%7D%7D; _pt=1--WyI1MWYyYWIyM2FlOTBmNDJjYWNmYmI3NjdmZWJiZWIwODhkOGRkZDJiIl0%3D--a6dc124efcc956016f6c5310dcc9564827eee953; hli=1; previousTab=%7B%22id%22%3A%22492b3e8c-8e3b-4307-9fdb-22e8131fa01b%22%2C%22url%22%3A%22https%3A%2F%2Fwww.airbnb.co.uk%2Frooms%2F20669368%3Fsource_impression_id%3Dp3_1657306030_w%252B1rJfUxqjL8G%252Ftj%22%7D; frmfctr=wide; jitney_client_session_updated_at=1657361972; cfrmfctr=DESKTOP; cbkp=4; tzo=60' \
  -H 'device-memory: 8' \
  -H 'dpr: 2' \
  -H 'ect: 4g' \
  -H 'pragma: no-cache' \
  -H 'referer: https://www.airbnb.co.uk/rooms/20669368?source_impression_id=p3_1657306030_w%2B1rJfUxqjL8G%2Ftj' \
  -H 'sec-ch-ua: ".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"' \
  -H 'sec-ch-ua-mobile: ?1' \
  -H 'sec-ch-ua-platform: "Android"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-origin' \
  -H 'user-agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Mobile Safari/537.36' \
  -H 'viewport-width: 1680' \
  -H 'x-airbnb-api-key: d306zoyjsyarp7ifhu67rjxn52tv0t20' \
  -H 'x-airbnb-graphql-platform: web' \
  -H 'x-airbnb-graphql-platform-client: minimalist-niobe' \
  -H 'x-airbnb-supports-airlock-v2: true' \
  -H 'x-client-request-id: 02n47j2159kybo111e7tw0jytzdx' \
  -H 'x-csrf-token: V4$.airbnb.co.uk$Q7h5uyluow4$NyVUC4FWkYEvr-5CTW_DeZ5vhmS-aU2nw3d95RwdIIA=' \
  -H 'x-csrf-without-token: 1' \
  -H 'x-niobe-short-circuited: true' \
  --compressed

11. The replicated request in Python works the same, which is good news and means we can continue developing.
12. I searched the JSON response for the specific data required.
13. I extracted the JSON path of these so we could print them to the console. 
14. Modified request params so the property ID could be stored as a variable (so the code can be re-used).
15. Added code for converting property IDs to base64.
16. Bit of a refactor, tidied up some code and removed unnecessary headers.
17. After the program was made to extract all of the required data for a specific property ID, I tested this on different property IDs.
18. Added support for passing multiple properties as links (scrape info about multiple properties at once).
19. Added error handling for properties that have been removed/are unavailable.
20. Final refactor to tidy up code and test.