from yql.search import SimpleYqlSearch

class FriendFeedFeedsYql(SimpleYqlSearch):
    table = 'friendfeed.feeds(0)'

    def set_table(self, table):
        pass

    def get_result(self, response):
        res = super(FriendFeedFeedsYql, self).get_result(response)
        if 'errors' in res:
            return res
        return {'friendfeed.feeds': res['yql']['entries']}