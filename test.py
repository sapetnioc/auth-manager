
from keycloak import KeycloakOpenID, KeycloakAdmin
from pydantic import BaseSettings

class Settings(BaseSettings):
    root_url : str = 'https://example.com/root'
    admin_user : str = 'admin'
    admin_password : str
    keycloak_realm : str
    studies_url : str = None


class PlatformManager:
    def __init__(self, server_url, username, password, realm,
                 studies_url):
        self.server_url = server_url
        self.username = username
        self.password = password
        self.realm = realm
        self.studies_url = studies_url

    def keycloak_admin(self):
        result = KeycloakAdmin(server_url=self.server_url,
                               username=self.username,
                               password=self.password)
        result.realm_name = self.realm
        return result

    def studies(self):
        keycloak_admin = self.keycloak_admin()
        return [s['clientId'] for s in keycloak_admin.get_clients() if s.get('rootUrl') == self.studies_url]
    
    def create_study(self, study):
        keycloak_admin = self.keycloak_admin()
        
        client = {
            'clientId': study,
            'redirectUris': [study],
            'rootUrl': self.studies_url,
        }
        keycloak_admin.create_client(client)
        client_id = m.keycloak_admin().get_client_id(study)

        keycloak_admin.create_client_role(client_id, 
                                          {'name': 'read', 
                                           'clientRole': True})
        read_role = keycloak_admin.get_client_role(client_id, 'read')
        keycloak_admin.create_client_role(client_id, 
                                          {'name': 'write', 
                                           'clientRole': True})
        write_role = keycloak_admin.get_client_role(client_id, 'write')
        keycloak_admin.create_client_role(client_id, 
                                          {'name': 'admin', 
                                           'clientRole': True})
        admin_role = keycloak_admin.get_client_role(client_id, 'admin')

        keycloak_admin.create_group({'name': study})
        study_group_id = keycloak_admin.get_group_by_path('/{}'.format(study))['id']

        keycloak_admin.create_group({'name': 'user'}, parent=study_group_id)
        group_id = keycloak_admin.get_group_by_path('/{}/user'.format(study), 
                                                    search_in_subgroups=True)['id']
        keycloak_admin.assign_group_client_roles(group_id,
                                                 client_id,
                                                 [read_role])

        keycloak_admin.create_group({'name': 'contributor'}, parent=study_group_id)
        group_id = keycloak_admin.get_group_by_path('/{}/contributor'.format(study), 
                                                    search_in_subgroups=True)['id']
        keycloak_admin.assign_group_client_roles(group_id,
                                                 client_id,
                                                 [read_role, write_role])

        keycloak_admin.create_group({'name': 'administrator'}, parent=study_group_id)
        group_id = keycloak_admin.get_group_by_path('/{}/administrator'.format(study), 
                                                    search_in_subgroups=True)['id']
        keycloak_admin.assign_group_client_roles(group_id,
                                                 client_id,
                                                 [read_role, write_role, admin_role])

    def delete_study(self, study):
        keycloak_admin = self.keycloak_admin()

        group_id = keycloak_admin.get_group_by_path('/{}'.format(study))['id']
        keycloak_admin.delete_group(group_id)

        client_id = m.keycloak_admin().get_client_id(study)
        keycloak_admin.delete_client(client_id)

settings = Settings(_env_file='.env')
m = PlatformManager(server_url='{}/keycloak/auth/'.format(settings.root_url),
                    username=settings.admin_user,
                    password=settings.admin_password,
                    realm=settings.keycloak_realm,
                    studies_url=settings.studies_url or '{}/studies'.format(settings.root_url))
