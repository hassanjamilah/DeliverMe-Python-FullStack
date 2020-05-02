import json
from flask import request, _request_ctx_stack , abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'andalussoft.au.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'deliver_me_api'

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code
        print ('🛑 🛑 🛑 🛑{},{}'.format(error , self.status_code))
        abort(self.status_code)

## Auth Header

'''
@TODO implement get_token_auth_header() method
    it should attempt to get the header from the request
        it should raise an AuthError if no header is present
    it should attempt to split bearer and the token
        it should raise an AuthError if the header is malformed
    return the token part of the header
'''

def get_token_auth_header():
    auth = request.headers.get('Authorization' , None)
    if not auth:
         raise AuthError({
             'code':'missing_headers' , 
             'description':'Authorization header is expected'
         } ,401)
        
    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code':'invalide_header' , 
            'description':'Autherization header should start with bearer'
        },401)
    
    elif len(parts[1]) == 1 :
        raise AuthError({
            'code':'invalide_header' , 
            'description':'Token not found'
        },401)
    elif len(parts) > 2:
        raise AuthError({
            'code':'invalide_header' , 
            'description':'Authorization header should only contain bearer and token'
        },401)
    token = parts[1]
    return token 
        
        
        
    raise Exception('Not Implemented')
 

'''
@TOTO implement check_permissions(permission, payload) method
    @INPUTS
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload

    it should raise an AuthError if permissions are not included in the payload
        !!NOTE check your RBAC settings in Auth0
    it should raise an AuthError if the requested permission string is not in the payload permissions array
    return true otherwise
'''

def check_permissions(permission, payload):
   # permission = 'get:drinks-detail'
   # token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImxBTVdfVmxZRmRMeXlVS0xubkdrZiJ9.eyJpc3MiOiJodHRwczovL2FuZGFsdXNzb2Z0LmF1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZTlhNDQ3MGM2MjMxMDBiZWRlMWI2NDciLCJhdWQiOiJjb2ZmZWVfc2hvcF9hcGkiLCJpYXQiOjE1ODcxNzkyMjIsImV4cCI6MTU4NzE4NjQyMiwiYXpwIjoiTG1sR29xZlI0SG5FbUYzMnZmbUFzOGVVdVF6ODZQbjIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpkcmlua3MiLCJnZXQ6ZHJpbmtzLWRldGFpbCIsInBhdGNoOmRyaW5rcyIsInBvc3Q6ZHJpbmtzIl19.QmxSKFsJKbNlakM_4SUsQf361cQM6gvIX7bUC-31eepkqh4bkd2vfQkAbGB8S_s5psqWP5We4ex2evkvdKiXdPCl_8O6IcOP7hR1GkZLP-dn6_f1pFBG8eDNJoyYM6yZm6LGiXkZuCKl8zZJBRusiiTlcw0k5wpbohh_PvjHB5jxG2C9hB9efWMFTMNbSB59AgpU1UI7_hcmiKNCRllUE-wpD_HipLWydS5_zFfgmmQU4gmWoQKzsyALt_ZxecuaGglypvpXXJUWbxH7TC4ZtjIQSHxw5wl4j8HTIi50uK8_0g_rYQfTGZKfy6CZKQFC10JEc6iqfkkojXvaT1LtDg'
   # payload = verify_decode_jwt(token)
    if 'permissions' not in payload:
        raise AuthError({
            'code':'no_premission' , 
            'description':'premissions not exist'
            } , 403)
        
    permissions  = payload['permissions']
    print ('🚵‍♀️ 🚵‍♀️ 🚵‍♀️ 🚵‍♀️ 🚵‍♀️ 🚵‍♀️ 🚵‍♀️ 🚵‍♀️ {}'.format(permissions))
    if permission not in permissions:
        raise AuthError({
            'code':'access_denied' , 
            'description':'you do not have permission'
        },403)
        
        
    return True
'''
@TOTO implement verify_decode_jwt(token) method
    @INPUTS
        token: a json web token (string)

    it should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    it should validate the claims
    return the decoded payload

    !!NOTE urlopen has a common certificate error described here: https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''
def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverifiedHeader = jwt.get_unverified_header(token)
    if 'kid' not in unverifiedHeader:
        raise AuthError({
           'code':'Invalid Header',
           'description':'Authorization malformed'
        },401)        
    
    rsa_key={}
    for key in jwks['keys']:
       if key['kid'] == unverifiedHeader['kid']:
            rsa_key={
               'alg':key['alg'],
               'kty':key['kty'],
               'use':key['use'],
               'kid':key['kid'],
               'n':key['n'],
               'e':key['e']    
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token ,
                rsa_key ,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://'+AUTH0_DOMAIN+'/'
            )
            print ('🍮 🍮 🍮 🍮 🍮 🍮 🍮 🍮 ')
            print (payload)
            return payload
        except jwt.ExpiredSignatureError :
            raise AuthError({
                'code':'token_expired',
                'description':'Token expired.'
            }, 401)
        except jwt.JWTClaimsError:
            raise AuthError({
                'code':'invalid_claims',
                'description':'Incorrect claims check the audiance and issuer'
            } , 401)
        except Exception:
            raise AuthError({
                'code':'Invalid header',
                'description':'Unable to parse autherication token'
            },400)   
    raise AuthError({
        'code':'Invalid Header',
        'description':'Unable to find the appropriate key'
    },400) 
        
      
           
    

           
          

    

  
    
    
            
        

'''
@TODO implement @requires_auth(permission) decorator method
    @INPUTS
        permission: string permission (i.e. 'post:drink')

    it should use the get_token_auth_header method to get the token
    it should use the verify_decode_jwt method to decode the jwt
    it should use the check_permissions method validate claims and check the requested permission
    return the decorator which passes the decoded payload to the decorated method
'''
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)

            check_permissions(permission, payload)
            return f( *args, **kwargs)

        return wrapper
    return requires_auth_decorator