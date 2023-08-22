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

    @arg_botcmd('env', type=str, help='env to deploy, to view envs list run: !errbotplugintest show environments' )
    def errbotplugintest_deploy(self, message, env=None):
        """
        Start deploy errbotplugintest service via gitlab trigger
        """

        try:
            username = str(message.frm).split("@")[1]
        except Exception as e:
            self.log.exception(e)
            yield "Request processing error. See errbot logs for details"
            return 'error fetching username'

        try:
            errbotplugintest.validate_params(self, env)
        except ValidationException as e:
            self.log.exception(e)
            yield e
            return 'error validation'

        #try:
            #return 'test: {0}'.format(message.frm)
        #usr = Profiles()
        yield f"message: { message }, env: { env }, usr: { username }"
        #yield f"{usr}"
        return
        #except Exception as e:
        #   self.log.exception(e)
        #    yield "Request processing error. See errbot logs for details"
        #    return


    @arg_botcmd('env', type=str, help='env to deploy, to view envs list run: !errbotplugintest show environments' )
    def errbotplugintest_deploy_dev(self, message, env=None):

        staging_pattern = 'stg|staging|pre-production'

        if re.match(staging_pattern, env):
            deploy = self.errbotplugintest_deploy(message, env)
            #self.errbotplugintest_deploy(message, env)
            return f"{deploy}"
        else:
            raise ValidationException(
                "You can deploy only on staging environments"
            )
