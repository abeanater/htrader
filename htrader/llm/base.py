
import os

prompts = {
'extract_targets': (lambda text  : f"Please consider the text from this news article. "+
                                  'If price target exist in the article return them as a json object like this: ' +
                                  '[{"ticker":"NAME", "price_target":10.00}, ...]' + ' if they are not in there return empty list [] ' +
                                  f"Here is news:\n### {text}"),
'extract_sentiment': (lambda text : f"""Please consider the text from this news article.'+
                                    'If sentiment exist in the article return them as a json object with range [-1,1] where
                                    positive sentiment is closer to 1 and negative sentiment is closer to -1 like this: ' +
                                    '[{"ticker":"NAME", "sentiment":"0.9"}, ...]' + ' if there is not really enough info return 0 as sentiment
                                    If not tickers in article or companies return empty list []'
                                    f'Here is news:\n### {text}"""),
}
