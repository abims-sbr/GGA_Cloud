import os
import argparse
import logging
# import yaml
# import ruamel.yaml
# import json

"""
docker-compose.yml generator
The method "generate" works for both docker-compose architecture (old), or docker stacks (new)
This method will write a formatted docker-compose.yml for the specified organism (only requires genus and species)

Made to work in the integration streamlined script "autoload.py" but can be used as a standalone (either with a CLI
or in another python file as a module)

TODO: write the whole yml dict from scratch (would allow the script to be more reusable into the future and make it
more customizable while being clearer (instead of the default yml string or input docker-compose template)

TODO: read json

API master key or galaxy: MASTER_API_KEY: XXXXXXX (alphanum, user prompt/git env variable)
"""


class DockerComposeGenerator:

    def __init__(self):
        self.mode = None
        self.genus = None
        self.species = None
        self.template = None
        self.outdir = None

    def generate(self):
        if self.template is None:
            self.template = str(os.getcwd() + "/templates/docker-compose.yml")
            # default docker-compose if no input template was specified --> doesnt work, yaml doesnt support direct string replacement, needs tags (maybe TODO) (https://stackoverflow.com/questions/5484016/how-can-i-do-string-concatenation-or-string-replacement-in-yaml)
            # self.template = "{'version': '3.7', 'services': {'proxy': {'image': 'quay.io/abretaud/nginx-ldap:latest', 'volumes': ['./src_data/:/project_data/', './nginx/conf:/etc/nginx/conf.d'], 'networks': ['traefik', 'genus_species'], 'deploy': {'labels': ['traefik.http.routers.genus_species-nginx.rule=(Host(`localhost`) && PathPrefix(`/sp/genus_species/download`))', 'traefik.http.routers.genus_species-nginx.tls=true', 'traefik.http.routers.genus_species-nginx.entryPoints=webs', 'traefik.http.routers.genus_species-nginx.middlewares=sp-auth,sp-app-trailslash,sp-prefix', 'traefik.http.services.genus_species-nginx.loadbalancer.server.port=80'], 'restart_policy': {'condition': 'on-failure', 'delay': '5s', 'max_attempts': 3, 'window': '120s'}}}, 'tripal': {'image': 'quay.io/galaxy-genome-annotation/tripal:v2.x', 'depends_on': ['tripal-db', 'elasticsearch'], 'volumes': ['./docker_data/galaxy/:/export/:ro', './src_data/:/project_data/:ro', './src_data:/data:ro'], 'environment': {'DB_HOST': 'tripal-db.genus_species', 'BASE_URL_PATH': '/sp/genus_species', 'UPLOAD_LIMIT': '20M', 'MEMORY_LIMIT': '512M', 'TRIPAL_GIT_CLONE_MODULES': 'https://github.com/abretaud/tripal_rest_api.git[@c6f9021ea5d4c6d7c67c5bd363a7dd9359228bbc] https://github.com/tripal/tripal_elasticsearch.git[@dc7f276046e394a80a7dfc9404cf1a149006eb2a] https://github.com/tripal/tripal_analysis_interpro.git https://github.com/tripal/tripal_analysis_go.git https://github.com/tripal/tripal_analysis_blast.git  https://github.com/tripal/tripal_analysis_expression.git[@7240039fdeb4579afd06bbcb989cb7795bd4c342]', 'TRIPAL_DOWNLOAD_MODULES': '', 'TRIPAL_ENABLE_MODULES': 'tripal_analysis_blast tripal_analysis_interpro tripal_analysis_go tripal_rest_api tripal_elasticsearch', 'SITE_NAME': 'Genus species', 'ELASTICSEARCH_HOST': 'elasticsearch.genus_species', 'ENABLE_JBROWSE': '/jbrowse/?data=data/gspecies', 'ENABLE_APOLLO': 'https://localhost/apollo/', 'ENABLE_BLAST': 1, 'ENABLE_DOWNLOAD': 1, 'ENABLE_WIKI': 1, 'ENABLE_GO': '/organism/Genus/species?pane=GO', 'ENABLE_ORTHOLOGY': 0, 'ENABLE_ORTHOLOGY_LINKS': 'http://localhost/sp/orthology/', 'ADMIN_PASSWORD': 'XXXXXX'}, 'networks': ['traefik', 'genus_species'], 'deploy': {'labels': ['traefik.http.routers.genus_species-tripal.rule=(Host(`localhost`) && PathPrefix(`/sp/genus_species`))', 'traefik.http.routers.genus_species-tripal.tls=true', 'traefik.http.routers.genus_species-tripal.entryPoints=webs', 'traefik.http.routers.genus_species-tripal.middlewares=sp-auth,sp-trailslash,sp-prefix,tripal-addprefix', 'traefik.http.services.genus_species-tripal.loadbalancer.server.port=80'], 'restart_policy': {'condition': 'on-failure', 'delay': '5s', 'max_attempts': 3, 'window': '120s'}}}, 'tripal-db': {'image': 'quay.io/galaxy-genome-annotation/chado:1.31-jenkins26-pg9.5', 'environment': ['POSTGRES_PASSWORD=postgres', 'INSTALL_CHADO_SCHEMA=0'], 'volumes': ['./docker_data/tripal_db/:/var/lib/postgresql/data/'], 'networks': ['genus_species']}, 'elasticsearch': {'image': 'docker.elastic.co/elasticsearch/elasticsearch:6.6.1', 'volumes': ['./docker_data/elastic_search_index/:/usr/share/elasticsearch/data/'], 'environment': {'bootstrap.memory_lock': 'true', 'xpack.security.enabled': 'false', 'xpack.monitoring.enabled': 'false', 'xpack.ml.enabled': 'false', 'xpack.graph.enabled': 'false', 'xpack.watcher.enabled': 'false', 'cluster.routing.allocation.disk.threshold_enabled': 'false', 'ES_JAVA_OPTS': '-Xms500m -Xmx500m', 'TAKE_FILE_OWNERSHIP': 'true'}, 'networks': ['genus_species']}, 'galaxy': {'image': 'quay.io/galaxy-genome-annotation/docker-galaxy-annotation:gmod', 'volumes': ['../galaxy_data_libs_SI.py:/opt/setup_data_libraries.py', './docker_data/galaxy/:/export/', './src_data/:/project_data/:ro', './docker_data/jbrowse/:/jbrowse/data/', './docker_data/apollo/:/apollo-data/', '../galaxy_nginx.conf:/etc/nginx/uwsgi_params'], 'environment': {'NONUSE': 'nodejs,proftp,reports,condor', 'GALAXY_LOGGING': 'full', 'GALAXY_CONFIG_BRAND': 'Genus species', 'GALAXY_CONFIG_ALLOW_LIBRARY_PATH_PASTE': 'True', 'GALAXY_CONFIG_USE_REMOTE_USER': 'True', 'GALAXY_CONFIG_REMOTE_USER_MAILDOMAIN': 'bipaa', 'GALAXY_CONFIG_ADMIN_USERS': 'admin@galaxy.org,gogepp@bipaa', 'ENABLE_FIX_PERMS': 0, 'PROXY_PREFIX': '/sp/genus_species/galaxy', 'GALAXY_TRIPAL_URL': 'http://tripal.genus_species/tripal/', 'GALAXY_TRIPAL_PASSWORD': 'XXXXXX', 'GALAXY_WEBAPOLLO_URL': 'http://one-of-the-swarm-node:8888/apollo/', 'GALAXY_WEBAPOLLO_USER': 'admin_apollo@bipaa', 'GALAXY_WEBAPOLLO_PASSWORD': 'XXXXXX', 'GALAXY_WEBAPOLLO_EXT_URL': '/apollo/', 'GALAXY_CHADO_DBHOST': 'tripal-db.genus_species', 'GALAXY_CHADO_DBSCHEMA': 'chado', 'GALAXY_AUTO_UPDATE_DB': 1, 'GALAXY_AUTO_UPDATE_CONDA': 1, 'GALAXY_AUTO_UPDATE_TOOLS': '/galaxy-central/tools_1.yaml', 'GALAXY_SHARED_DIR': '', 'BLAT_ENABLED': 1}, 'networks': ['traefik', 'genus_species'], 'deploy': {'labels': ['traefik.http.routers.genus_species-galaxy.rule=(Host(`localhost`) && PathPrefix(`/sp/genus_species/galaxy`))', 'traefik.http.routers.genus_species-galaxy.tls=true', 'traefik.http.routers.genus_species-galaxy.entryPoints=webs', 'traefik.http.routers.genus_species-galaxy.middlewares=sp-auth,sp-app-trailslash,sp-app-prefix', 'traefik.http.services.genus_species-galaxy.loadbalancer.server.port=80'], 'restart_policy': {'condition': 'on-failure', 'delay': '5s', 'max_attempts': 3, 'window': '120s'}}}, 'jbrowse': {'image': 'quay.io/galaxy-genome-annotation/jbrowse:v1.16.8', 'volumes': ['./docker_data/galaxy/:/export/:ro', './src_data/:/project_data/:ro', './docker_data/jbrowse/:/jbrowse/data/:ro'], 'networks': ['traefik', 'genus_species'], 'deploy': {'labels': ['traefik.http.routers.genus_species-jbrowse.rule=(Host(`localhost`) && PathPrefix(`/sp/genus_species/jbrowse`))', 'traefik.http.routers.genus_species-jbrowse.tls=true', 'traefik.http.routers.genus_species-jbrowse.entryPoints=webs', 'traefik.http.routers.genus_species-jbrowse.middlewares=sp-auth,sp-app-trailslash,sp-app-prefix', 'traefik.http.services.genus_species-jbrowse.loadbalancer.server.port=80'], 'restart_policy': {'condition': 'on-failure', 'delay': '5s', 'max_attempts': 3, 'window': '120s'}}}, 'blast': {'image': 'quay.io/abretaud/sf-blast:latest', 'depends_on': ['blast-db'], 'environment': {'DB_HOST': 'blast-db.genus_species', 'UPLOAD_LIMIT': '20M', 'MEMORY_LIMIT': '128M', 'DB_NAME': 'postgres', 'ADMIN_EMAIL': 'xxx@example.org', 'ADMIN_NAME': 'xxxxx', 'JOBS_METHOD': 'local', 'JOBS_WORK_DIR': '/xxxx/blast_jobs/', 'CDD_DELTA_PATH': '/db/cdd_delta/current/flat/cdd_delta', 'BLAST_TITLE': 'Genus species blast server', 'JOBS_SCHED_NAME': 'blast_gspecies', 'PRE_CMD': '. /local/env/envblast-2.6.0.sh; . /local/env/envpython-3.7.1.sh;', 'APACHE_RUN_USER': 'bipaaweb', 'APACHE_RUN_GROUP': 'bipaa', 'BASE_URL_PATH': '/sp/genus_species/blast/', 'UID': 55914, 'GID': 40259}, 'volumes': ['./blast/banks.yml:/var/www/blast/app/config/banks.yml:ro', './blast/links.yml:/etc/blast_links/links.yml:ro'], 'networks': ['traefik', 'genus_species'], 'deploy': {'labels': ['traefik.http.routers.genus_species-blast.rule=(Host(`localhost`) && PathPrefix(`/sp/genus_species/blast`))', 'traefik.http.routers.genus_species-blast.tls=true', 'traefik.http.routers.genus_species-blast.entryPoints=webs', 'traefik.http.routers.genus_species-blast.middlewares=sp-big-req,sp-auth,sp-app-trailslash,sp-app-prefix', 'traefik.http.services.genus_species-blast.loadbalancer.server.port=80'], 'restart_policy': {'condition': 'on-failure', 'delay': '5s', 'max_attempts': 3, 'window': '120s'}}}, 'blast-db': {'image': 'postgres:9.6-alpine', 'environment': ['POSTGRES_PASSWORD=postgres', 'PGDATA=/var/lib/postgresql/data/'], 'volumes': ['./docker_data/blast_db/:/var/lib/postgresql/data/'], 'networks': ['genus_species']}, 'wiki': {'image': 'quay.io/abretaud/mediawiki', 'environment': {'MEDIAWIKI_SERVER': 'http://localhost', 'MEDIAWIKI_PROXY_PREFIX': '/sp/genus_species/wiki', 'MEDIAWIKI_SITENAME': 'Genus species', 'MEDIAWIKI_SECRET_KEY': 'XXXXXXXXXX', 'MEDIAWIKI_DB_HOST': 'wiki-db.genus_species', 'MEDIAWIKI_DB_PASSWORD': 'password', 'MEDIAWIKI_ADMIN_USER': 'abretaud'}, 'depends_on': ['wiki-db'], 'volumes': ['./docker_data/wiki_uploads:/images'], 'networks': ['traefik', 'genus_species'], 'deploy': {'labels': ['traefik.http.routers.genus_species-blast.rule=(Host(`localhost`) && PathPrefix(`/sp/genus_species/blast`))', 'traefik.http.routers.genus_species-blast.tls=true', 'traefik.http.routers.genus_species-blast.entryPoints=webs', 'traefik.http.routers.genus_species-blast.middlewares=sp-big-req,sp-auth,sp-app-trailslash,sp-app-prefix', 'traefik.http.services.genus_species-blast.loadbalancer.server.port=80'], 'restart_policy': {'condition': 'on-failure', 'delay': '5s', 'max_attempts': 3, 'window': '120s'}}}, 'wiki-db': {'image': 'postgres:9.6-alpine', 'volumes': ['./docker_data/wiki_db/:/var/lib/postgresql/data/'], 'networks': ['genus_species']}}, 'networks': {'traefik': {'external': True}, 'genus_species': {'driver': 'overlay', 'name': 'genus_species'}}}"
            #
        else:
            with open(self.template, 'r') as infile:
                content = list()
                for line in infile:
                    content.append(line.replace("genus_species", str(self.genus.lower() + "_" + self.species)).replace("Genus species", str(self.genus + " " + self.species)).replace("Genus/species", str(self.genus + "/" + self.species)).replace("gspecies", str(self.genus.lower()[0] + self.species)))
                self.write_yml(content=content)

    def write_yml(self, content):
        with open(self.outdir + "/docker-compose.yml", 'w') as outfile:
            for line in content:
                outfile.write(line)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generator of docker-compose.yml for GGA automated integration "
                                                 "following the templates available @ "
                                                 "https://gitlab.inria.fr/abretaud/genodock_demo/")
    parser.add_argument("-g", "--genus", type=str, help="input genus")
    parser.add_argument("-s", "--species", type=str, help="input species")
    parser.add_argument("-t", "--template", type=str, help="input template docker-compose.yml (compose or stack), optional")
    parser.add_argument("-o", "--outdir", type=str, help="where to write the output docker-compose")
    args = parser.parse_args()

    dc_generator = DockerComposeGenerator()
    dc_generator.genus = args.genus
    dc_generator.species = args.species
    if args.template:
        dc_generator.template = args.template
    dc_generator.outdir = args.outdir
    dc_generator.generate()
    print("foo")
