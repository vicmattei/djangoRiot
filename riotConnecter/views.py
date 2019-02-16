from datetime import datetime

from django.views.generic import FormView
import funcy
import pytz
import requests

from . import forms
from . import constants


class SummonerSearchFormView(FormView):
    template_name = 'search/summoners.html'
    form_class = forms.SummonerSearchForm

    euw_root = 'https://euw1.api.riotgames.com'
    summoner_profile_url_template = (
        f'{euw_root}/lol/summoner/v4/summoners/by-name/{{}}')
    summoner_positions_url_template = (
        f'{euw_root}/lol/league/v4/positions/by-summoner/{{}}')
    summoner_match_history_url_template = (
        f'{euw_root}/lol/match/v4/matchlists/by-account/{{}}')
    champions_data_url = (
        'http://ddragon.leagueoflegends.com'
        '/cdn/9.2.1/data/en_US/champion.json')

    api_key = 'RGAPI-f3ffba36-69b8-499f-89c1-b8df72deb412'
    api_key_params = {'api_key': api_key}

    WRONG_CHAMPION_ID = 'WRONG_CHAMPION_ID'

    @funcy.cache(60)
    def _api_call(self, *args, **kwargs):
        res = requests.get(*args, params=self.api_key_params, **kwargs).json()

        if 'status' in res and res['status']['status_code'] == 403:
            raise ValueError('Api key has beed expired!')
        else:
            return res

    def _get_summoner_profile(self, username):
        summoner_profile_url = self.summoner_profile_url_template.format(
            username)
        return self._api_call(summoner_profile_url)

    def _get_summoner_id(self, username):
        return self._get_summoner_profile(username)['id']

    def _get_account_id(self, username):
        return self._get_summoner_profile(username)['accountId']

    def _get_summoner_position(self, username) -> dict:
        summoner_data_url = self.summoner_positions_url_template.format(
            self._get_summoner_id(username))
        summoner_positions = self._api_call(summoner_data_url)
        if summoner_positions == []:
            return {}
        else:
            return funcy.project(
                summoner_positions[0], ['tier', 'rank', 'leaguePoints'])

    def _post_process_match_history(self, matches):
        for match in matches:
            match['datetime'] = datetime.fromtimestamp(
                match['timestamp'] / 1000, pytz.utc)
            match['queue'] = constants.MATCHMAKING_QUEUES[match['queue']]
            match['champion_id'] = self._get_champion_id(match['champion'])
        return matches

    def _get_summoner_match_history(self, username, count=30):
        account_id = self._get_account_id(username)
        summoner_match_history_url = (
            self.summoner_match_history_url_template.format(account_id))
        matches = self._api_call(summoner_match_history_url)['matches'][:count]
        return self._post_process_match_history(matches)

    @funcy.cache(60)
    def _get_champion_id(self, key):
        res_json = self._api_call(self.champions_data_url)
        chapmions_data = res_json['data'].values()
        chapmion_data = funcy.lwhere(chapmions_data, key=str(key))
        if chapmion_data != []:
            return chapmion_data[0]['id']
        else:
            return self.WRONG_CHAMPION_ID

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        username = self.request.GET.get('username')
        if username is not None:
            context['summoner_profile'] = self._get_summoner_profile(username)
            context['summoner_position'] = self._get_summoner_position(
                username)
            context['summoner_match_history'] = (
                self._get_summoner_match_history(username))

        return context


# requests.get('http://google.com', params={'apikey': 123})
# google.com/?apikey=123

# context['riot_data'] = sgdfgdf
# context['key'] = summoner_data
# {{ key.a }}

# username = self.request.GET.get('username')
# if username is not None:
#     pass
#
# try:
#     username = self.request.GET['username']
#     pass
# except KeyError:
#     pass
