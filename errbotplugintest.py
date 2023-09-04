# -*- coding: utf-8 -*-
"""
errbotplugintest errbot plugin
"""

from errbot import BotPlugin, botcmd, arg_botcmd, ValidationException, core_plugins
import re


class errbotplugintest(BotPlugin):
    """
    Manage errbotplugintest service via chatbot
    """

    def get_configuration_template(self):
        """
        Define default configuration for errbotplugintest service plugin
        """
        return { 'ENVIRONMENTS': ['production', 'stg', 'pre-production-1', 'staging1']}

    @staticmethod
    def validate_params(self, env):
        """
        Validate input params
        """
        if env not in self.config['ENVIRONMENTS']:
            raise ValidationException(
                "Wrong environment name: {0}".format(env)
            )

    @botcmd
    def errbotplugintest_show_environments(self):
        """
        Get list of errbotplugintest predefined environments
        """
        return ' | '.join(self.config['ENVIRONMENTS'])

    @arg_botcmd('branch', type=str, help='branch to deploy', default='master')
    @arg_botcmd('server', type=str, help='server to deploy')
    def errbotplugintest_deploy(self, message, server=None, branch=None):
        """
        Start deploy errbotplugintest service via gitlab trigger
        """
        print(message, "|", server, "|", branch)
        try:
            username = str(message.frm).split("@")[1]
        except Exception as e:
            self.log.exception(e)
            yield "Request processing error. See errbot logs for details"
            return 'error fetching username'
        #try:
            #errbotplugintest.validate_params(self, server)
        #except ValidationException as e:
        #    self.log.exception(e)
        #    yield e
        #    return 'error validation'

        #try:
            #return 'test: {0}'.format(message.frm)
        #usr = Profiles()
        #print(f"message: { message }, env: { env }, usr: { username }")
        #yield f"{usr}"
        yield next(errbotplugintest.deploy(self, server, branch))
        #except Exception as e:
        #   self.log.exception(e)
        #    yield "Request processing error. See errbot logs for details"
        #    return


    @arg_botcmd('branch', type=str, help='branch to deploy', default='master')
    @arg_botcmd('server', type=str, help='server to deploy')
    def errbotplugintest_deploy_dev(self, message, server=None, branch=None):

        staging_pattern = 'stg|staging|pre-production|_css'

        print(list(server))

        if all(re.findall(staging_pattern, word) for word in list(server)):
            print(message, "|", server, "|", branch)
            yield next(errbotplugintest.deploy(self, server, branch))
        else:
            raise ValidationException(
                "You can deploy only on staging environments"
            )

    @staticmethod
    def deploy(self, server, branch):
            yield f" server: { server }, branch {branch}"
            return