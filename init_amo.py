# import requests
# import json
#
# payload = {
#     'client_id': 'e9a129fe-7c84-4f9e-9bbc-5ce01612a78c',
#     'client_secret': 'ctijfYdwSf0KqIgEULFoyBKvLfdGQJl64d3unvu2WduHUCwU05gpLSqa3dSj2snc',
#     'grant_type': 'authorization_code',
#     'code': 'def502005cbb120a0dabae05041f01409fbd42a63b1aa032693732856629bd2fbea723304152c4410cd92e0154abd40c8f53cda65d4c91ea92aaef5b446058c70237a556a873eae9c044a7f8c3deb596913e365a26deb2c589305c7ebef99b8d16dc526bb85cd9c5765f4706254b0b2408799705a7bb6497429192eb3189660094dfc3f822086fc0da2bcd988b1352fe2b829de5bfe72051bec13f40482970d676eeafe37793c59494b6cf66e970b4ab6212dabdf3b1f43dbfde7bdf1fed8732ca480a0784b4ae01bbc1050c545828be33119f4e64a6c59e7f6bf3e92ad42ad0079cf8819282fadec73ba07d6887229af66a9b17548b3173efe4b96c31b2cfa4ce2a4ba95fcd9ed2d9e2c148be2adfe5a8d637d63b1fe8666f3cda6258d26fcafd57bdaccc0013f9a14633456eb427732ca5a5a50e8b2e6eaf7995311e079f48864abbb7f32e54a575c99565f4d2bddcdad9c8c42ee5820562c286c7568898f1b44a2e1c8395c1b0d5ba1cdddd92b7ca3f8fe5a6adc4c41021d8079b73ac8b0f439e127f6a766f7daef6895ac68eeaee7ee21be9d543aa6821e92845d04cde0fbff40a3efccdac26df1d0e80258ec23b6859d6b477f157c0c608fb61c2fcaed53323ebc8abeccdb7de1266b626c44d69f2102745ec6905756b99314c869b3f949bebdb57',
#     'redirect_uri': 'https://flexcamp.uz'
# }
#
# print("Отправляем:", json.dumps(payload, indent=2))
#
# response = requests.post(
#     'https://muslimpulatov0317.amocrm.com/oauth2/access_token',
#     headers={
#         'Content-Type': 'application/json',
#         'Accept': 'application/json'
#     },
#     data=json.dumps(payload)
# )
# print(response.status_code)
# print(response.text)