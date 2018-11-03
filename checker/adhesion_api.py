from json import JSONDecodeError
from oauthlib.oauth2 import BackendApplicationClient, TokenExpiredError
from requests_oauthlib import OAuth2Session
from rest_framework import status
from rest_framework.exceptions import APIException

from va_checker import settings
import logging
logger = logging.getLogger('adhesion_api')
class AdhesionAPI():
    url = settings.ADHESION_URL
    client_id = settings.ADHESION_CLIENT_ID
    client_secret = settings.ADHESION_CLIENT_SECRET
    token = None
    client = None
    oauth = None
    def __init__(self):
        self.refresh_token()
        super().__init__()

    @classmethod
    def refresh_token(self, needsRefresh=False):
        try:
            if (self.token is None and self.client is None) or needsRefresh:
                if needsRefresh: logger.info("Renouvellement du token car il est invalide")
                self.client = BackendApplicationClient(client_id=self.client_id)
                self.oauth = OAuth2Session(client=self.client)
                self.token = self.oauth.fetch_token(token_url=self.url + '/o/token/', client_id=self.client_id,
                                                    client_secret=self.client_secret)
                logger.info("Got token {} for external API".format(self.token['access_token']))
            else:
                logger.debug("Il y a dejà un Token : {} pour {}".format(self.token, self.client))
            #    r =self.client.refresh_token(self.url + '/o/token/') #ne faut-il pas le récupérer ??
            #    logger.debug(r.text)
        except:
            logger.exception("Impossible d'obtenir un token pour l'API externe Adhésion")

    def get(self, url, **kwargs):
        logger.info('api_va: GET {}'.format(url))
        import requests
        r = requests.get(url, headers={'Authorization': "Bearer "+self.token['access_token']}, **kwargs)
        logger.info("Réponse Adhésion ({}) : {}".format(str(r.status_code), r.text))
        if r.status_code == 401:
            logger.warning("Token expiré, on réessaie")
            self.refresh_token(needsRefresh=True) #visiblement y'a pas de refresh token avec une Application "client credentials"
            r = requests.get(url, headers={'Authorization': "Bearer " + self.token['access_token']}, **kwargs)
        if r.status_code not in [status.HTTP_200_OK, status.HTTP_201_CREATED, status.HTTP_202_ACCEPTED, status.HTTP_404_NOT_FOUND]:
            raise APIException("Une erreur est survenue lors de la connexion à un serveur externe")
        return r
        #try:
        #    r = self.oauth.get(url, **kwargs, timeout=10)
        #    if r.status_code ==401:
        #        raise TokenExpiredError
        #    return r
        #except TokenExpiredError:
        #    self.client.refresh_token(url+'/o/token/')
        #    logger.info("Credentials expirés ? le token a été refresh")
        #        #self.__init__() sinon on peut aussi en redemander
        #except Exception:
        #    logger.exception("Impossible de se connecter à {} pour l'API externe".format(url))

    def get_member(self, member_id):
        r = self.get(self.url+'/v1/members/{}/'.format(member_id))
        try:
            if r.status_code == 404: return None
            member = r.json()
            member['id']
            return member
        except KeyError: #keyerror si membre inexistant
            logger.exception(r.text)
            return None
        except AttributeError: #pas de réponse
            logger.exception(" ?")
            return None

    def get_infos_card(self, card_id):
        r = self.get(self.url+'/v1/cards/{}/'.format(card_id))
        try:
            if r.status_code == 404: return None
            card = r.json()
            if card['activated']:
                member = self.get_member(card['member'])
                card['first_name']=member['first_name']
                card['last_name'] = member['last_name']
                card['gender'] = member['gender']
            return card
        except KeyError: #keyerror si membre inexistant
            logger.exception(r.text)
            return None
        except AttributeError: #pas de réponse
            logger.exception(" ?")
            return None

    def try_member(self, member_id):
        if member_id is None: return False #pour éviter le flood
        r = self.get(self.url + '/v1/members/{}/'.format(member_id))
        try:
            if r.status_code == 404:
                return False
            elif r.status_code == 200:
                return True
            else:
                logger.debug("Erreur inconnue: "+str(r.status_code)+" "+r.text)
        except: #gaffe !
            logger.debug("Membre {} inexistant".format(member_id))
            return False

