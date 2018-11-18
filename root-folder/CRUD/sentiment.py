from watson_developer_cloud import ToneAnalyzerV3

tone_analyzer = ToneAnalyzerV3(
    version='2018-11-17',
    iam_apikey='0BhiGpM_2XfxIs6vPS1J6Eg8FSdrHM2kyf8yiF1h35HT',
    url='https://gateway.watsonplatform.net/tone-analyzer/api'
)

def analyze(text):
    tone_analysis = tone_analyzer.tone({
        'text': text},
        'text/plain',
    ).get_result()
    return tone_analysis