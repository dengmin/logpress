#!/usr/bin/env python
# *_* encoding=utf-8*_*

from weibopy import OAuthHandler, oauth, WeibopError

class WeiboOAuthHandler(OAuthHandler):
    
    def get_authorization_url_with_callback(self, callback, signin_with_twitter=False):
        try:
            self.request_token = self._get_request_token()
            if signin_with_twitter:
                 url = self._get_oauth_url('authenticate')
            else:
                url = self._get_oauth_url('authorize')
            request = oauth.OAuthRequest.from_token_and_callback(
                    token=self.request_token, callback=callback, http_url=url
                )
            return request.to_url()
        except Exception, e:
            raise WeibopError(e)
        
weibo_client = WeiboOAuthHandler('916563958','20b8bb503e2b76d360345c382b9b9901')